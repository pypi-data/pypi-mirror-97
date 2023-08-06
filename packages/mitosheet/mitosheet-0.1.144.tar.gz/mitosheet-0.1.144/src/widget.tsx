// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import {
    DOMWidgetModel,
    DOMWidgetView,
    ISerializers,
    WidgetView,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// React
import React from 'react';
import ReactDOM from 'react-dom';

// Components
import Mito, { ColumnSpreadsheetCodeJSON, SheetColumnFiltersArray, ColumnTypeJSONArray } from './components/Mito';

// Logging
import { GridApi } from 'ag-grid-community';

export class ExampleModel extends DOMWidgetModel {

    // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
    defaults() {
        return {
            ...super.defaults(),
            _model_name: ExampleModel.model_name,
            _model_module: ExampleModel.model_module,
            _model_module_version: ExampleModel.model_module_version,
            _view_name: ExampleModel.view_name,
            _view_module: ExampleModel.view_module,
            _view_module_version: ExampleModel.view_module_version,
            df_json: '',
        };
    }

    static serializers: ISerializers = {
        ...DOMWidgetModel.serializers,
    // Add any extra serializers here
    };

    static model_name = 'ExampleModel';
    static model_module = MODULE_NAME;
    static model_module_version = MODULE_VERSION;
    static view_name = 'ExampleView'; // Set to null if no view
    static view_module = MODULE_NAME; // Set to null if no view
    static view_module_version = MODULE_VERSION;
}

// We save a Mito component in the global scope, so we
// can set the state from outside the react component
declare global {
    interface Window { 
        mitoMap:  Map<string, Mito> | undefined;
        mitoAPIMap:  Map<string, MitoAPI> | undefined;
        gridApiMap: Map<string, GridApi> | undefined;
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        commands: any;
        user_id: string;
    }
}

export interface SheetJSON {
    columns: string[];
    index: string[];
    data: string[][];
}

export type SheetShape = {'rows': number, 'cols': number};

export interface CodeJSON {
    imports: string;
    code: string[];
}

export interface ErrorJSON {
    event: string;
    type: string;
    header: string;
    to_fix: string;
}

import { ModalEnum } from "./components/Mito";
import { calculateAndSetHeaderHeight } from './utils/gridStyling';
import { MitoAPI } from './api';
import { StepData } from './types/StepTypes';

export class ExampleView extends DOMWidgetView {
    /*
    We override the DOMWidgetView constructor, so that we can
    create a logging instance for this view. 
  */
    initialize(parameters: WidgetView.InitializeParameters): void {
        super.initialize(parameters);
    }

    /* 
    We override the sending message utilities
  */
    send(msg: Record<string, unknown>): void{

        // If this is a message that makes a change (anything but a log_event or api_call or has_rendered_update),
        // then we make the system as loading, as we wait for a response
        if (msg['event'] !== 'log_event' && msg['event'] !== 'api_call' && msg['type'] !== 'has_rendered_update') {
            window.mitoMap?.get(this.model.model_id)?.setState({
                loading: true
            });
        }    

        super.send(msg);
    }

    render(): void {  
        // Capture the send, to pass to the component
        const send = (msg: Record<string, unknown>) => {
            this.send(msg);
        }

        // TODO: there is a memory leak, in the case where
        // we rerender the component (e.g. we run the mito.sheet)
        // cell again. We need to clean up the component somehow!
        const model_id = this.model.model_id;
        const mitoAPI = new MitoAPI(send);

        ReactDOM.render(
            <Mito 
                mitoAPI={mitoAPI}
                dfNames={this.getDfNames()}
                sheetShapeArray={this.getSheetShapeArray()}
                currStepIdx={this.getCurrStepIdx()}
                sheetJSONArray={this.getSheetJSONArray()}
                columnSpreadsheetCodeJSONArray={this.getColumnSpreadsheetCodeJSONArray()}
                savedAnalysisNames={this.getSavedAnalysisNames()}
                columnFiltersArray={this.getColumnFilters()}
                columnTypeJSONArray={this.getColumnTypeJSONArray()}
                tutorialMode={this.getTutorialMode()}
                model_id={model_id}
                isLocalDeployment={this.getIsLocalDeployment()}
                userEmail={this.getUserEmail()}
                shouldUpgradeMitosheet={this.getShouldUpgradeMitosheet()}
                ref={(Mito: Mito) => { 
                    // The first time we render the item, register the Mito instance
                    if (window.mitoMap === undefined) {
                        window.mitoMap = new Map();
                    }
                    window.mitoMap.set(model_id, Mito);

                    // We also register the API for this Mito instance
                    if (window.mitoAPIMap === undefined) {
                        window.mitoAPIMap = new Map();
                    }
                    window.mitoAPIMap.set(model_id, mitoAPI);
                }}
                stepDataList={this.getStepDataList()}
            />,
            this.el
        )
        
        this.model.on('msg:custom', this.handleMessage, this);

        /*
        The first render of a widget happens when the mitosheet.sheet call is
        run. It does not occur when the page that this widget on is refreshed.
        
        We only need to send update events for df_names and reading an existing analysis
        in the case that this is the first render, and not when the page is refreshed.

        NOTE: Rerunning a mitosheet.sheet call that has an analysis in the cell 
        below is _creating a new mitosheet_. Thus, this.getHasRendered() will
        return false in this case.
    */
        if (!this.getHasRendered()) {
            // Get df name from code block, and pass it to both the frontend and the backend
            window.commands?.execute('get-df-names').then((dfNames: string[]) => {
                // If there are dataframe names, send them to the backend
                if (dfNames.length > 0){
                    this.send({
                        'event': 'update_event',
                        'type': 'df_names_update',
                        'df_names': dfNames
                    })
                }
            });

            // Get any previous analysis and send it back to the model!
            window.commands?.execute('read-existing-analysis').then(async (analysisName: string | undefined) => {
                // If there is no previous analysis, we just ignore this step
                if (!analysisName) return;
                // We log that we read from below
                await mitoAPI.sendLogMessage(
                    'read_analysis_from_cell_below',
                    {
                        analysis_name: analysisName
                    }
                )

                // And send it to the backend (we don't care when it terminates)
                await mitoAPI.sendUseExistingAnalysisUpdateMessage(
                    analysisName,
                    undefined,
                    /* 
                        When we read in an analysis name from a cell, we replay this analysis
                        while also overwriting _everything_ that is already in the analysis. 

                        This is to avoid issues w/ passing in a saved analysis to the mitosheet.sheet
                        call, where then rerunning the cell with this call w/ doubly-apply things.
                    */
                    true
                )
            });        
        } 
        // Let the backend know we have now rendered the sheet, and all future
        // renders therefor must be page refreshes, and so we let the backend 
        // know that we have rendered
        this.send({
            'event': 'update_event',
            'type': 'has_rendered_update'
        })
    }

    getHasRendered(): boolean {
        return this.model.get('has_rendered');
    }

    getSheetJSONArray(): SheetJSON[] {
        const sheetJSONArray: SheetJSON[] = [];

        try {
            const modelSheetJSONArray = JSON.parse(this.model.get('sheet_json'));
            sheetJSONArray.push(...modelSheetJSONArray);
        } catch (e) {
            // Suppress error
            console.error(e);
        }

        return sheetJSONArray;
    }


    getIsLocalDeployment(): boolean {
        return this.model.get('is_local_deployment');
    }

    getSheetShapeArray(): SheetShape[] {
        const sheetShapeArray: SheetShape[] = [];

        try {
            const sheetShapeJSONArrayUnparsed = JSON.parse(this.model.get('df_shape_json'));
            sheetShapeArray.push(...sheetShapeJSONArrayUnparsed);
        } catch (e) {
            // Suppress error
            console.error(e);
        }

        return sheetShapeArray;
    }

    getColumnTypeJSONArray(): ColumnTypeJSONArray {
        const columnTypeJSONArray: ColumnTypeJSONArray = [];

        try {
            const modelColumnTypeJSONArray = JSON.parse(this.model.get('column_type_json'));
            columnTypeJSONArray.push(...modelColumnTypeJSONArray);
        } catch (e) {
            // Suppress error
            console.error(e);
        }

        return columnTypeJSONArray;
    }

    getSavedAnalysisNames(): string[] {
        const savedAnalysisNames: string[] = [];

        try {
            const savedAnalysisNamesJSON = JSON.parse(this.model.get('saved_analysis_names_json'));
            savedAnalysisNames.push(...savedAnalysisNamesJSON);
        } catch (e) {
            // Suppress error
            console.error(e);
        }

        return savedAnalysisNames;
    }

    getCurrStepIdx(): number {
        return this.model.get('curr_step_idx');
    }

    getStepDataList(): StepData[] {
        const stepDataList: StepData[] = [];

        try {
            const savedStepDataList = JSON.parse(this.model.get('step_data_list_json'));
            stepDataList.push(...savedStepDataList);
        } catch (e) {
            // Suppress error
            console.error(e);
        }

        return stepDataList;
    }

    getColumnSpreadsheetCodeJSONArray(): ColumnSpreadsheetCodeJSON[] {
        return JSON.parse(this.model.get('column_spreadsheet_code_json'));
    }

    getDfNames(): string[] {
        const dfNames: string[]= [];

        const unparsedDfNames = this.model.get('df_names_json');
        try {
            dfNames.push(...JSON.parse(unparsedDfNames)['df_names']);

            // And then we extend it to the length of the number of sheets,
            // as the dfNames sometimes aren't pulled correctly!
            const modelSheetJSONArray = this.getSheetJSONArray();
            for (let i = dfNames.length; i < modelSheetJSONArray.length; i++) {
                dfNames.push(`df${i + 1}`);
            }
        } catch (e) {
            // Suppress error
            console.error(e);
        }
        return dfNames;
    }

    getCodeJSON(): CodeJSON {
        const codeJSON: CodeJSON = {
            imports: '# No imports',
            code: ['# No code has been written yet!', 'pass']
        };

        const unparsedCodeJSON = this.model.get('code_json');
        try {
            codeJSON['imports'] = JSON.parse(unparsedCodeJSON)['imports'];
            codeJSON['code'] = JSON.parse(unparsedCodeJSON)['code'];
        } catch (e) {
            // Suppress error
            console.error(e);
        }
        return codeJSON;
    }

    getAnalysisName(): string {
        return this.model.get('analysis_name') as string;
    }

    getColumnFilters(): SheetColumnFiltersArray {
        return JSON.parse(this.model.get('column_filters_json'));
    }

    getTutorialMode(): boolean {
        return this.model.get('tutorial_mode');
    }

    getUserEmail(): string {
        return this.model.get('user_email')
    }

    getShouldUpgradeMitosheet(): boolean {
        return this.model.get('should_upgrade_mitosheet')
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/explicit-module-boundary-types
    handleMessage(message: any): void {
    /* 
      This route handles the messages sent from the Python widget
    */

        const model_id = this.model.model_id;
        const mito = window.mitoMap?.get(model_id);

        if (mito === undefined) {
            console.error("Error: a message was received for a mito instance that does not exist!")
            return;
        }

        console.log("Got a message, ", message);
        if (message.event === 'update_sheet') {
            console.log("Updating sheet.");
            mito.setState(() => {
                return {
                    sheetJSONArray: this.getSheetJSONArray(),
                    columnSpreadsheetCodeJSONArray: this.getColumnSpreadsheetCodeJSONArray(),
                    dfNames: this.getDfNames(),
                    sheetShapeArray: this.getSheetShapeArray(),
                    savedAnalysisNames: this.getSavedAnalysisNames(),
                    columnFiltersArray: this.getColumnFilters(),
                    columnTypeJSONArray: this.getColumnTypeJSONArray(),
                    loading: false,
                    tutorialMode: this.getTutorialMode(),
                    stepDataList: this.getStepDataList(),
                    currStepIdx: this.getCurrStepIdx()
                }
            }, () => {
                // then recalculate the header height to make sure all headers are visible
                calculateAndSetHeaderHeight(model_id);
            });
      
        } else if (message.event === 'update_code') {
            console.log('Updating code.');
            window.commands?.execute('write-code-to-cell', {
                analysisName: this.getAnalysisName(),
                codeJSON: this.getCodeJSON()
            });
            mito.setState({
                loading: false
            });
        } else if (message.event === 'edit_error') {
            console.log("Updating edit error.");
            mito.setState({
                modalInfo: {type: ModalEnum.Error},
                errorJSON: message,
                loading: false
            });
        } else if (message.event === 'api_response') {
            // We get the MitoAPI associated with this Mito instance, and add to it's unconsumed queue
            const mitoAPI = window.mitoAPIMap?.get(model_id);
            mitoAPI?.receiveResponse(message);
        }
    }
}
