// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment, MouseEvent } from 'react';

// Import intercom
import Intercom from 'react-intercom';

// Import types
import { CellFocusedEvent, ColumnMovedEvent } from 'ag-grid-community';
import { SheetJSON, ErrorJSON, SheetShape } from '../widget';
import { MITO_INDEX } from '../utils/gridData';
import { StepData } from '../types/StepTypes'

// Import helpers
import { getColumnWidthsArray } from '../utils/gridStyling';

// Import sheet and code components
import MitoSheet from './MitoSheet';
import SheetTabs from './tabs/SheetTabs';
import FormulaBar from './FormulaBar';
import MitoToolbar from './MitoToolbar';
import LoadingIndicator from './LoadingIndicator';

// Import modals
import ErrorModal from './ErrorModal';
import DownloadModal from './modals/DownloadModal';
import DeleteColumnModal from './modals/DeleteColumnModal';
import SaveAnalysisModal from './modals/SaveAnalysisModal';
import SaveAnalysisOverwriteModal from './modals/SaveAnalysisOverwriteModal';
import ImportModal from './modals/ImportModal';

// Import css
import "../../css/mito.css"
import { ImportSummaries, MitoAPI } from '../api';
import ReplayImportModal from './modals/ReplayImportModal';
import PivotTaskpane from './taskpanes/PivotTable/PivotTaskpane';
import IntroductionTour from './tours/IntroductionTour';
import { EDITING_TASKPANES, TaskpaneInfo, TaskpaneType } from './taskpanes/taskpanes';
import MergeTaskpane from './taskpanes/Merge/MergeTaskpane';
import DocumentationTaskpane from './taskpanes/Documentation/DocumentationTaskpane';
import ControlPanelTaskpane from './taskpanes/ControlPanel/ControlPanelTaskpane';
import SignUpModal from './modals/SignupModal';
import BookDemoModal from './modals/BookDemoModal';
import UpgradeModal from './modals/UpgradeModal';
import { FilterGroupType, FilterType } from './taskpanes/ControlPanel/filter/filterTypes';
import StepsTaskpane from './taskpanes/Steps/StepsTaskpane';
import TopLeftPopup from './elements/TopLeftPopup';
import ReplayAnalysisTaskpane from './taskpanes/ReplayAnalysis/ReplayAnalysisTaskpane';

export interface ColumnSpreadsheetCodeJSON {
    [Key: string]: string;
}

export type SheetColumnFiltersArray = SheetColumnFilterMap[]; 

export type ColumnType =
    | 'string'
    | 'number'
    | 'datetime'


export interface SheetColumnFilterMap {
    [column: string]: {
        operator: 'Or' | 'And',
        filters: (FilterType | FilterGroupType)[]
    }
}

export interface ColumnTypeJSON {
    [Key: string]: ColumnType;
}
export type ColumnTypeJSONArray = ColumnTypeJSON[]; 


export enum ModalEnum {
    None = 'None',
    Error = 'Error',
    RepeatAnalysis = 'RepeatAnalysis',
    Download = 'Download',
    DeleteColumn = 'DeleteColumn',
    SaveAnalysis = 'SaveAnalysis',
    SaveAnalysisOverwrite = 'SaveAnalysisOverwrite',
    Import = "Import",
    ReplayImport = "ReplayImport",
    SignUp = "SignUp",
    BookDemo = "BookDemo",
    Upgrade = 'Upgrade'
}

/* 
    Each modal comes with modal info, and we enforce (through types) that if you set
    the current modal, you must also pass it the data that it requires. 

    To see what information a modal requires, see it's <>ModalInfo type definition
    below!

    NOTE: Currently, the column header modal is the only modal that needs any data...
    but this is a good investment for the future :)
*/
interface NoneModalInfo {type: ModalEnum.None}
interface ErrorModalInfo {type: ModalEnum.Error}
interface DownloadModalInfo {type: ModalEnum.Download}

interface DeleteColumnModalInfo {
    type: ModalEnum.DeleteColumn;
    columnHeader: string;
}
interface SaveAnalysisModalInfo {
    type: ModalEnum.SaveAnalysis;
    saveAnalysisName?: string;
}
interface SaveAnalysisOverwriteModalInfo {
    type: ModalEnum.SaveAnalysisOverwrite;
    saveAnalysisName: string;
}
interface ImportModalInfo {
    type: ModalEnum.Import;
}

interface ReplayImportModalInfo {
    type: ModalEnum.ReplayImport;
    analysisName: string;
    importSummary: ImportSummaries;
}

interface SignUpModalInfo {
    type: ModalEnum.SignUp;
}

interface BookDemoModalInfo {
    type: ModalEnum.BookDemo;
    userEmail: string;
}

interface UpgradeModalInfo {
    type: ModalEnum.Upgrade;
}

export type ModalInfo = 
    | NoneModalInfo 
    | ErrorModalInfo
    | DownloadModalInfo
    | DeleteColumnModalInfo
    | SaveAnalysisModalInfo
    | SaveAnalysisOverwriteModalInfo
    | ImportModalInfo
    | ReplayImportModalInfo
    | SignUpModalInfo
    | BookDemoModalInfo
    | UpgradeModalInfo


type MitoProps = {
    mitoAPI: MitoAPI
    dfNames: string[];
    sheetShapeArray: SheetShape[];
    columnSpreadsheetCodeJSONArray: ColumnSpreadsheetCodeJSON[];
    sheetJSONArray: SheetJSON[];
    savedAnalysisNames: string[];
    columnFiltersArray: SheetColumnFiltersArray;
    columnTypeJSONArray: ColumnTypeJSONArray;
    model_id: string;
    isLocalDeployment: boolean;
    tutorialMode: boolean;
    userEmail: string;
    shouldUpgradeMitosheet: boolean;
    stepDataList: StepData[];
    currStepIdx: number;
};

type MitoState = {
    tutorialMode: boolean;
    runTour: boolean; // the variable passed to the JoyRide to start or stop the tour
    tourStepIndex: number;
    dfNames: string[];
    sheetShapeArray: SheetShape[];
    columnSpreadsheetCodeJSONArray: ColumnSpreadsheetCodeJSON[];
    sheetJSONArray: SheetJSON[];
    columnFiltersArray: SheetColumnFiltersArray;
    columnTypeJSONArray: ColumnTypeJSONArray;
    selectedSheetIndex: number;
    formulaBarValue: string;
    selectedColumn: string;
    selectedRowIndex: number;
    errorJSON: ErrorJSON;
    documentationOpen: boolean;
    editingModeState: EditingModeState;
    movingColumnParams: MovingColumnParams;
    savedAnalysisNames: string[];
    modalInfo: ModalInfo;
    loading: boolean;
    currOpenTaskpane: TaskpaneInfo;
    columnWidthsArray: Record<string, number>[];
    isLocalDeployment: boolean;
    currOpenSheetTabActions: number | undefined;
    /*
        This variable stores a reference to the div element that contains
        _all_ of Mito. It is useful in determining where to place things, 
        e.g. the SheetTabActions, so that they don't get cut off. 

        NOTE: when updating this, you _must_ check that it's not already defined
        as otherwise you will enter an infinite loop, and the app will crash
    */
    mitoContainerRef: HTMLDivElement | undefined | null;
    stepDataList: StepData[];
    currStepIdx: number;
};

type EditingModeState = {
    editingModeOn: boolean;
    editingSheetIndex: number;
    editingCellColumn: string;
    editingCellRowIndex: number;
    lastFormula: string; // This is the last formula there is, and it notably might be invalid
    formulaCursorIndex: number;
}

type MovingColumnParams = ColumnMovedState | undefined

type ColumnMovedState = {
    column: string;
    newIndex: number
}

class Mito extends React.Component<MitoProps, MitoState> {
    
    constructor(props: MitoProps) {
        super(props);
        
        let formulaBarValue = '';
        let selectedColumn = '';

        // Set the defaul values for the formula bar and selected column (if possible, aka the sheet has some data in it)
        if (this.props.sheetJSONArray.length > 0) {
            formulaBarValue = this.props.sheetJSONArray[0].data[0] === undefined
                ? '' : this.props.sheetJSONArray[0].data[0][0];
            selectedColumn = this.props.sheetJSONArray[0].columns[0] === undefined
                ? '' : this.props.sheetJSONArray[0].columns[0].toString();
        }

        // Build the default column widths
        const defaultColumnWidthsArray: Record<string, number>[] = getColumnWidthsArray(this.props.sheetJSONArray).columnWidthsArray;

        /*
            If the user has not input their email, then we default the modal info to the 
            email collection modal. Otherwise, if the user should update, we default to 
            the upgrade modal. 

            If neither of these conditons are true, then we don't default to any modal at 
            all.
        */
        const defaultModalInfo: ModalInfo = this.props.userEmail ==  '' ? {type: ModalEnum.SignUp} : (this.props.shouldUpgradeMitosheet ? {type: ModalEnum.Upgrade} : {type: ModalEnum.None});

        this.state = {
            tutorialMode: props.tutorialMode,
            runTour: false, 
            tourStepIndex: 0,
            dfNames: this.props.dfNames,
            sheetShapeArray: this.props.sheetShapeArray,
            columnSpreadsheetCodeJSONArray: this.props.columnSpreadsheetCodeJSONArray,
            sheetJSONArray: this.props.sheetJSONArray,
            columnFiltersArray: this.props.columnFiltersArray,
            columnTypeJSONArray: this.props.columnTypeJSONArray,
            selectedSheetIndex: 0,
            formulaBarValue: formulaBarValue,
            selectedColumn: selectedColumn,
            selectedRowIndex: 0,
            /*
                we tell if we're in cell editing mode through the editingModeOn state variable

                the editingCellColumn and editingCellRowIndex are used to update the formula of the correct
                cell editor. They get set to the new values when we turn cell editing mode back on, but are unchanged
                when we turn cell editing mode off so that we can handle formulas that error by letting the user 
                edit the formula that they submitted. 
            */
            editingModeState: {
                editingModeOn: false,
                editingSheetIndex: 0,
                editingCellColumn: "",
                editingCellRowIndex: -1,
                lastFormula: formulaBarValue,
                formulaCursorIndex: 2, // set to an arbitrary value -- it gets set correctly in gridData.tsx
            },
            movingColumnParams: undefined,
            documentationOpen: false,
            errorJSON: {
                event: '',
                type: '',
                header: '',
                to_fix: ''
            },
            modalInfo: defaultModalInfo,
            savedAnalysisNames: this.props.savedAnalysisNames,
            loading: false,
            columnWidthsArray: defaultColumnWidthsArray,
            isLocalDeployment: props.isLocalDeployment,
            currOpenTaskpane: {type: TaskpaneType.NONE},
            currOpenSheetTabActions: undefined,
            mitoContainerRef: undefined,
            stepDataList: this.props.stepDataList,
            currStepIdx: this.props.currStepIdx
        };
        
        this.cellFocused = this.cellFocused.bind(this);
        this.handleFormulaBarDoubleClick = this.handleFormulaBarDoubleClick.bind(this);
        this.sendCellValueUpdate = this.sendCellValueUpdate.bind(this);
        this.setEditingMode = this.setEditingMode.bind(this);
        this.setEditingFormula = this.setEditingFormula.bind(this);
        this.setModal = this.setModal.bind(this);
        this.getCurrentModalComponent = this.getCurrentModalComponent.bind(this);
        this.setSelectedSheetIndex = this.setSelectedSheetIndex.bind(this);
        this.turnOnCellEditor = this.turnOnCellEditor.bind(this);
        this.setCursorIndex = this.setCursorIndex.bind(this);
        this.columnMoved = this.columnMoved.bind(this);
        this.columnDragStopped = this.columnDragStopped.bind(this);
        this.setColumnWidth = this.setColumnWidth.bind(this);
        this.setCurrOpenTaskpane = this.setCurrOpenTaskpane.bind(this);
        this.getCurrOpenTaskpane = this.getCurrOpenTaskpane.bind(this);
        this.closeOpenEditingPopups = this.closeOpenEditingPopups.bind(this);
        this.setTourInfo = this.setTourInfo.bind(this);
        this.setCurrOpenSheetTabActions = this.setCurrOpenSheetTabActions.bind(this);
    }

    /*  
        if we're in tutorial mode, start the tour .5 seconds after page loading  
        so that the tour selector has items to select. This also looks nice :) 
    */  
    componentDidMount(): void {
        setTimeout(() => {
            if (this.state.tutorialMode == true) {
                this.setState({ runTour: true })
            }
        }, 500);
    }

    /* 
        Registers the step index with the Mito state so that when the
        tour is recreated because the key updates, we don't start back at the beginning
    */
    setTourInfo(runTour: boolean, newStepIndex: number): void {
        this.setState({
            tourStepIndex: newStepIndex,
            runTour: runTour, 
            tutorialMode: runTour
        }, () => {
            // Log the step advancement creation
            void this.props.mitoAPI.sendLogMessage(
                'Introduction Tour',
                {
                    tour_id: 'Introduction Tour',
                    stepIndex: newStepIndex,
                    runTour: runTour
                }
            )
        });
    }


    /*
        The componentDidUpdate hook is responsible for maintaining consistency in the state
        variables of this prop in the case of updates to the sheet data. NOTE: this consistency
        should enforce that any column you index into should be defined for all sheets + all columns
        (e.g. this.state.columnFilters should be defined everywhere). If this is not the case, then it MUST
        be enforced in the type system!

        For example, if a sheet is deleted, then selectedSheetIndex in that state should not 
        be set equal to the old index of that sheet.

        See more here: https://reactjs.org/docs/react-component.html#componentdidupdate

        NOTE: careful on calling this.setState in this function, as repeated calls cause
        the sheet to crash (as this recurses infinitely).

        NOTE: this function will fail if it is called on a dataframe with mulitple columns with
        the same name. This is an invariant we currently expect to be the case.
    */
    componentDidUpdate(prevProps: MitoProps, prevState: MitoState): void {
        const newSheetJSON = this.state.sheetJSONArray;
        let newSelectedSheetIndex = prevState.selectedSheetIndex;

        // If the selectedSheetIndex no longer exists, because of an undo, don't select that one!
        // Or, if there was an a new sheet creation, then default to the last sheet
        if (prevState.selectedSheetIndex >= newSheetJSON.length || prevState.sheetJSONArray.length < newSheetJSON.length) {
            newSelectedSheetIndex = newSheetJSON.length - 1;
        }

        if (newSelectedSheetIndex != prevState.selectedSheetIndex) {
            this.setState({
                selectedSheetIndex: newSelectedSheetIndex
            });
        }

        // Make sure the column widths are set correctly, which they may not be if the columns in sheet
        // have changed, or a sheet has been added or subtracted
        const columnWidthsArrayResult = getColumnWidthsArray(this.state.sheetJSONArray, this.state.columnWidthsArray);
        // Check if we need to actually update the column widths (sheet number change, any column change)
        if (columnWidthsArrayResult.changed) {
            this.setState({
                columnWidthsArray: columnWidthsArrayResult.columnWidthsArray
            })
        }
    }


    /* 
        Called by the cell editor so that the column the user clicks on can be appended
        to the correct location in the formula
    */
    setCursorIndex(index: number): void {
        this.setState(prevState => {
            return {
                editingModeState: {                   
                    ...prevState.editingModeState,    
                    formulaCursorIndex: index                          
                }
            };
        });
    }


    /* 
        This function is responsible for turning cell editing mode on and off
        by setting the state of editingCellColumn, and editingCellRowIndex.

        If you call this function with on===true, then the passed column and rowIndex
        should be the cell you want to start editing.

        If you call this function with on===false, then editing will be stopped, and the 
        passed column and rowIndex will be focused on.
    */
   
    setEditingMode(on: boolean, column: string, rowIndex: number): void {
        if (on && !this.state.editingModeState.editingModeOn) {
            // we close the taskpane if its open and its a editing taskpane
            this.closeOpenEditingPopups();

            /* 
                This runs (and turns on editing mode) when we're not in editing mode and:
                1. The user double clicks on a cell
                2. The user presses enter on a cell. 
                3. The user types any character on a cell. 
            */

            this.setState(prevState => {
                return {
                    editingModeState: {                   
                        ...prevState.editingModeState,  
                        editingSheetIndex: this.state.selectedSheetIndex,  
                        editingModeOn: true,
                        editingCellColumn: column,
                        editingCellRowIndex: rowIndex,
                    }
                };
            });
            
        } else if (!on) {
            /* 
                We turn off cell-editing mode and select the given cell.

                This handles some of the many ways cell editing can be stopped
                explicitly (e.g. ENTER), as we want only sometimes want ENTER to stop 
                editing (in other cases, we want it to select a suggestion!).

                To see a list of events that stop editing, see:
                https://www.ag-grid.com/javascript-grid-cell-editing/#stop-end-editing
            */

            this.setState(prevState => {
                return {
                    editingModeState: {                   
                        ...prevState.editingModeState,
                        editingModeOn: false,          
                    }
                };
            });
            

            // We actually stop the grid from editing in this case, and set cell focus
            // as stopping editing focuses on nothing by default.
            window.gridApiMap?.get(this.props.model_id)?.stopEditing();
            window.gridApiMap?.get(this.props.model_id)?.setFocusedCell(
                rowIndex, 
                column
            );
        }
    }

    /*
        This function is called by the cell editor to update the formula of the editing cell
        in the mito state, so that when cellFocused starts editing mode again, it can 
        pass in the starting formula.  

        We save the formula in the state because:
            1) when the user clicks on another cell, it closes the cell editor.
            We need to store the formula in state so when we put the editor 
            back in cell editing mode in the CellFocussedEvent, 
            we're able to start the cell editor with the correct formula. 
            
            Note: we don't want to send the intermediate formula to the parser

            2) we need to display the formula that is in the editor in the formula bar as well.  
    */
    setEditingFormula(formula: string): void {
        this.setState(prevState => {
            return {
                editingModeState: {                   
                    ...prevState.editingModeState, 
                    lastFormula: formula
                },
                formulaBarValue: formula,
            };
        });                 
    }

    turnOnCellEditor(): void {
        const editingModeParams = {
            rowIndex: this.state.editingModeState.editingCellRowIndex,
            colKey: this.state.editingModeState.editingCellColumn,
        }

        // Scroll to make sure this editor is visible (but only scroll just enough)
        window.gridApiMap?.get(this.props.model_id)?.ensureColumnVisible(editingModeParams.colKey)
        // TODO: we might want to ensureIndexVisible as well, but users always edit at the top
        // turn the editing cell's cell editor back on!
        window.gridApiMap?.get(this.props.model_id)?.startEditingCell(editingModeParams);
    }

    /* 
        Occurs when a cell is clicked. If we are currently editing a cell, we append the clicked
        column to the currently-edited cell. Otherwise, we select the clicked cell.
    */
    cellFocused(event: CellFocusedEvent): void {
        // We always close the sheet tab actions
        this.setCurrOpenSheetTabActions(undefined);

        /* 
            We avoid cell focused throwing an error when switching sheets by making sure the 
            event is defined, and just returning. Not sure why this occurs!

            Additionally, turn of cell editing mode & reset the formulaBarValue. when the user switches
            sheets we reset the editing cell to clear the formula bar
        */
        
        const column = event.column?.getColId();
        if (!column) {
            this.setEditingMode(false, "", -1);
            this.setState(prevState => {
                return {
                    editingModeState: {                   
                        ...prevState.editingModeState, 
                        editingCellColumn: '',
                        editingCellRowIndex: -1
                    },
                    formulaBarValue: '',
                };
            }); 
            return;
        } 


        // If the control panel is open, update the column header to the selected column
        if (this.state.currOpenTaskpane.type === TaskpaneType.CONTROL_PANEL && column !== MITO_INDEX) {
            this.setState({
                currOpenTaskpane: {
                    type: TaskpaneType.CONTROL_PANEL,
                    columnHeader: column, 
                    openEditingColumnHeader: false
                }
            });
        }

        // If we're in cell editing mode, turn cell editor back on
        if (this.state.editingModeState.editingModeOn) {

            /* 
                If the column we focussed on is the editing column or the index column, don't append to the formula
            */ 
            if (column === this.state.editingModeState.editingCellColumn || column === MITO_INDEX) {
                this.turnOnCellEditor();
                return;
            }

            /*
                If we're in editing mode & the cell focused on is not in the column we're editing
                or the index column, append the clicked column to the editing formula;
            */ 

            // Add the column reference to the formula where the user's cursor is in the input field
            const formulaCursorIndex = this.state.editingModeState.formulaCursorIndex
            
            const newFormula = this.state.formulaBarValue.slice(0, formulaCursorIndex) + column + this.state.formulaBarValue.slice(formulaCursorIndex);

            this.setState(prevState => {
                return {
                    editingModeState: {                   
                        ...prevState.editingModeState, 
                        lastFormula: newFormula,
                        formulaCursorIndex: formulaCursorIndex + column.length // update the formula cursor index to include appended characters
                    },
                    formulaBarValue: newFormula,
                    selectedColumn: column
                };
            }, () => {
                this.turnOnCellEditor()
            });
        } else {
            // If we're not in editing mode, then we update the formula bar only

            // If the column is the index column, then we reset the selected cell state
            if (column === MITO_INDEX) {
                this.setState({
                    selectedColumn: '',
                    selectedRowIndex: 0,
                    formulaBarValue: ''
                });
                return;
            }

            // Otherwise, get the cell's formula to display
            const columnIndex = this.state.sheetJSONArray[this.state.selectedSheetIndex].columns.indexOf(column);
            const rowIndex = event.rowIndex;

            const columnFormula = this.state.columnSpreadsheetCodeJSONArray[this.state.selectedSheetIndex][column];

            let formulaBarValue = this.state.formulaBarValue;

            if (columnFormula === '') {
                // If there no formula, we just display the value
                formulaBarValue = this.state.sheetJSONArray[this.state.selectedSheetIndex].data[rowIndex][columnIndex];
            } else {
                // Otherwise, we display the formula that is in the column
                formulaBarValue = columnFormula;
                if (this.state.selectedSheetIndex === this.state.editingModeState.editingSheetIndex && column === this.state.editingModeState.editingCellColumn) {
                    // The last formula is always equal to the _last_ edit made to a formula
                    // and so we take it so we keep an error formula
                    formulaBarValue = this.state.editingModeState.lastFormula;
                }
            }

            this.setState({
                selectedColumn: column,
                selectedRowIndex: rowIndex,
                formulaBarValue: formulaBarValue
            });
        }
    }

    handleFormulaBarDoubleClick(e: MouseEvent<HTMLButtonElement>): void {
        e.preventDefault();

        /*
            When the formula bar is double clicked, turns on cell editing mode and opens the 
            selected cell's cell editor 

            TODO: make sure it works with multiple sheets. fix: when we switch sheets, 
            reset this.state.selectedColumn & this.state.selectedRowIndex
        */

        // Do nothing if the selected cell is a data column
        if (this.state.columnSpreadsheetCodeJSONArray[this.state.selectedSheetIndex][this.state.selectedColumn] === '') {
            return
        }

        // Turn cell editing mode on
        this.setEditingMode(true, this.state.selectedColumn, this.state.selectedRowIndex)

        /* 
            Turns on the correct cell editor. If the selected cell is not in view, 
            the spreadsheet will be scrolled automatically until it is. 
        */
        const editingModeParams = {
            rowIndex: this.state.selectedRowIndex,
            colKey: this.state.selectedColumn,
        }
        window.gridApiMap?.get(this.props.model_id)?.startEditingCell(editingModeParams);
    }

    async sendCellValueUpdate(columnHeader: string, newFormula: string): Promise<void> {
        /*
            We don't send the formula to the evaluator while in cell editing mode
            because this function gets called after the CellValueChangedEvent fires 
            each time the cell editor is closed. 
            
            However, the cell editor closes each time the user uses their mouse 
            to reference another column - which isn't a finished update yet!
        */
        if (!this.state.editingModeState.editingModeOn) {
            await this.props.mitoAPI.sendSetColumnFormulaEditMessage(
                this.state.selectedSheetIndex,
                columnHeader,
                newFormula
            )
        }
    }

    /* 
        Sets the sheet tab at the given index to have an open sheet tab
        action block. 

        If undefined is passed, then the open sheet tab action is closed. 
    */
    setCurrOpenSheetTabActions(sheetIndex: number | undefined): void {
        // Log the click
        if (sheetIndex !== undefined) {
            // We just use a void, as we _don't care_ when this log gets sent,
            // and we don't want to everything async
            void this.props.mitoAPI.sendLogMessage(
                'clicked_sheet_tab_actions',
                {
                    sheet_index: sheetIndex
                }
            )
        }

        this.setState({
            currOpenSheetTabActions: sheetIndex
        })
    }

    getCurrentModalComponent(): JSX.Element {
        // Returns the JSX.element that is currently, open, and is used
        // in render to display this modal
        switch(this.state.modalInfo.type) {
            case ModalEnum.None: return <div></div>;
            case ModalEnum.Error: return (
                <ErrorModal
                    errorJSON={this.state.errorJSON}
                    setModal={this.setModal}
                />
            )
            case ModalEnum.Download: return (
                <DownloadModal
                    setModal={this.setModal}
                    mitoAPI={this.props.mitoAPI}
                    selectedSheetIndex={this.state.selectedSheetIndex}
                    dfName={this.state.dfNames[this.state.selectedSheetIndex]}
                />
            )
            case ModalEnum.DeleteColumn: return (
                <DeleteColumnModal
                    setModal={this.setModal}
                    columnHeader={this.state.modalInfo.columnHeader}
                    selectedSheetIndex={this.state.selectedSheetIndex}
                    mitoAPI={this.props.mitoAPI}
                />
            )
            case ModalEnum.SaveAnalysis: return (
                <SaveAnalysisModal
                    setModal={this.setModal}
                    savedAnalysisNames={this.state.savedAnalysisNames}
                    saveAnalysisName={this.state.modalInfo.saveAnalysisName} 
                    mitoAPI={this.props.mitoAPI}
                />
            )
            case ModalEnum.SaveAnalysisOverwrite: return (
                <SaveAnalysisOverwriteModal
                    setModal={this.setModal}
                    savedAnalysisNames={this.state.savedAnalysisNames}
                    saveAnalysisName={this.state.modalInfo.saveAnalysisName} 
                    mitoAPI={this.props.mitoAPI}
                />
            )
            case ModalEnum.Import: return (
                <ImportModal
                    setModal={this.setModal}
                    dfNames={this.state.dfNames}
                    mitoAPI={this.props.mitoAPI} />
            )
            case ModalEnum.ReplayImport: return (
                <ReplayImportModal
                    setModal={this.setModal}
                    dfNames={this.state.dfNames}
                    api={this.props.mitoAPI}
                    analysisName={this.state.modalInfo.analysisName}
                    importSummaries={this.state.modalInfo.importSummary} 
                    mitoAPI={this.props.mitoAPI}
                />
            )
            case ModalEnum.SignUp: return (
                <SignUpModal
                    setModal={this.setModal}
                    mitoAPI={this.props.mitoAPI}
                />
            )
            case ModalEnum.BookDemo: return (
                <BookDemoModal
                    setModal={this.setModal}
                    userEmail={this.state.modalInfo.userEmail}
                />
            )
            case ModalEnum.Upgrade: return (
                <UpgradeModal
                    setModal={this.setModal}
                    mitoAPI={this.props.mitoAPI}
                />
            )
        }
    }

    setModal(modalInfo: ModalInfo): void {
        // Sets the current modal. We _always_ turn off cell editing mode here, just
        // in case the user opens/closes a modal in cell editing mode.
        this.setEditingMode(false, "", -1);

        // unless opening an error modal or closing a modal, close open editing taskpanes
        if (modalInfo.type !== ModalEnum.Error && modalInfo.type !== ModalEnum.None) {
            this.closeOpenEditingPopups();
        }
        
        // And then we actually update the modalInfo
        this.setState({modalInfo: modalInfo});
    }

    /* 
        Returns the JSX.Element of the taskpane that should be currently
        displayed, stored in this.state.currOpenTaskpane.

        If this.state.currOpenTaskpane is undefined, then returns no taskpane
        at all.
    */
    getCurrOpenTaskpane(): JSX.Element {
        switch(this.state.currOpenTaskpane.type) {
            case TaskpaneType.NONE: return (
                <Fragment/>
            )
            case TaskpaneType.PIVOT: return (
                <PivotTaskpane
                    dfNames={this.state.dfNames}
                    sheetJSONArray={this.state.sheetJSONArray}
                    mitoAPI={this.props.mitoAPI}
                    selectedSheetIndex={this.state.selectedSheetIndex}
                    setCurrOpenTaskpane={this.setCurrOpenTaskpane}
                />
            )
            case TaskpaneType.MERGE: return (
                <MergeTaskpane
                    dfNames={this.state.dfNames}
                    sheetJSONArray={this.state.sheetJSONArray}
                    setCurrOpenTaskpane={this.setCurrOpenTaskpane}
                    mitoAPI={this.props.mitoAPI}
                />
            )
            case TaskpaneType.STEPS: return (
                <StepsTaskpane
                    stepDataList={this.state.stepDataList}
                    setCurrOpenTaskpane={this.setCurrOpenTaskpane}
                    mitoAPI={this.props.mitoAPI}
                    currStepIdx={this.state.currStepIdx}
                />
            )
            case TaskpaneType.DOCUMENTATION: return (
                <DocumentationTaskpane 
                    setCurrOpenTaskpane={this.setCurrOpenTaskpane} 
                    mitoAPI={this.props.mitoAPI}
                />
            )
            case TaskpaneType.CONTROL_PANEL: 

                /*
                    We define default values here so when we rename the column header through the control panel, 
                    we don't have to worry about a sheet-crashing race condition where the Mito state is not yet updated to reflect the 
                    updated backend state.
                */

                // eslint-disable-next-line no-case-declarations
                let filters: (FilterType | FilterGroupType)[] = [];
                // eslint-disable-next-line no-case-declarations
                let operator: 'And' | 'Or' = 'And'
                // eslint-disable-next-line no-case-declarations
                let columnType: ColumnType= 'string'

                if (this.state.columnFiltersArray[this.state.selectedSheetIndex][this.state.currOpenTaskpane.columnHeader] !== undefined) {
                    filters = this.state.columnFiltersArray[this.state.selectedSheetIndex][this.state.currOpenTaskpane.columnHeader].filters;
                    operator = this.state.columnFiltersArray[this.state.selectedSheetIndex][this.state.currOpenTaskpane.columnHeader].operator;
                    columnType = this.state.columnTypeJSONArray[this.state.selectedSheetIndex][this.state.currOpenTaskpane.columnHeader];
                } 
            
                return (
                    <ControlPanelTaskpane 
                        // set the columnHeader as the key so that the taskpane updates when it is switched
                        // TODO: figure out why we need this, if the other variables update?
                        key={this.state.currOpenTaskpane.columnHeader + this.state.currOpenTaskpane.openEditingColumnHeader} 
                        selectedSheetIndex={this.state.selectedSheetIndex}
                        columnHeader={this.state.currOpenTaskpane.columnHeader} 
                        openEditingColumnHeader={this.state.currOpenTaskpane.openEditingColumnHeader}
                        columnType={columnType}
                        operator={operator}
                        filters={filters}
                        setCurrOpenTaskpane={this.setCurrOpenTaskpane} 
                        mitoAPI={this.props.mitoAPI}
                    />
                )
            case TaskpaneType.REPLAY_ANALYSIS:
                return (
                    <ReplayAnalysisTaskpane
                        savedAnalysisNames={this.state.savedAnalysisNames}
                        mitoAPI={this.props.mitoAPI}
                        setCurrOpenTaskpane={this.setCurrOpenTaskpane} 
                        setModal={this.setModal}
                    />
                )
        }
    }

    /*
        Changes what taskpane is currently displayed. Set to undefined
        to close the open taskpane.
    */
    setCurrOpenTaskpane(newTaskpaneInfo: TaskpaneInfo): void {
        // Log this new change, including the column header if it 
        // is possible to do so
        const logParams: Record<string, unknown> = {
            new_taskpane: newTaskpaneInfo.type as string,
            sheet_index: this.state.selectedSheetIndex,
        };
        if (newTaskpaneInfo.type === TaskpaneType.CONTROL_PANEL) {
            logParams['column_header'] = newTaskpaneInfo.columnHeader;
        }
        void this.props.mitoAPI.sendLogMessage(
            'set_curr_open_taskpane', 
            logParams
        )

        this.setState({currOpenTaskpane: newTaskpaneInfo});
    }

    /* 
        Closes any open editing popups, which includes:
        1. Any open sheet tab actions
        2. The taskpane, if it is an EDITING_TASKPANE
    */ 
    closeOpenEditingPopups(): void {
        // We always close the sheet tab actions, no matter what
        this.setCurrOpenSheetTabActions(undefined);

        // Close the taskpane if it is an editing taskpane
        if (EDITING_TASKPANES.includes(this.state.currOpenTaskpane.type)) {
            this.setState({
                currOpenTaskpane: {type: TaskpaneType.NONE}
            });
        }
    }

    setSelectedSheetIndex(newIndex: number): void {
        // We turn off editing mode, if it is on, because we moved to a new sheet
        this.setEditingMode(false, "", -1);

        // We also make sure we don't switch to a sheet that doesn't exist
        const inBoundsNewIndex = Math.min(newIndex, this.state.sheetJSONArray.length - 1);

        // We use the backend to log that we switched sheets
        // NOTE: we don't await, because we don't care when this happens
        void this.props.mitoAPI.sendLogMessage(
            'switch_sheet_log_event',
            {
                'sheet_index': newIndex
            }
        );


        // And then we update the selected index
        this.setState({selectedSheetIndex: inBoundsNewIndex});
    }

    /*
        The ColumnMovedEvent gets fired when a user drags a column to change its location. 
        While dragging the column from one position to another, this event gets fired multiple times, 
        for both the column that is moved but also sometimes for undefined columns. 

        Thus, when the column is moving, and it is defined, we set the movingColumnParams 
        so we can send a reorder event to the backend when it stops moving. See columnDragStopped
    */ 
    columnMoved(event: ColumnMovedEvent): void {
        const colId = event.column?.getColId()
        const newIndex = event.toIndex;

        if (colId && newIndex) {
            this.setState({
                movingColumnParams: {
                    column: colId,
                    newIndex: newIndex
                }
            })
        }

        
    }

    // When the column stops moving, send the column reorder event to the backend 
    async columnDragStopped(): Promise<void> {

        /* 
            The DragStoppedEvent gets fired when the user changes the width of the column and when 
            the user reorders the column. We only want to send a column_reorder_event when the user is 
            reordering the column, so we check if the user is moving a column by checking this.state.columnMovedState.column
        */
        if (this.state.movingColumnParams != undefined) {

            // If the column did not change locations, don't send a column_reorder_event
            if (this.state.sheetJSONArray[this.state.selectedSheetIndex].columns[this.state.movingColumnParams.newIndex - 1] === this.state.movingColumnParams.column) {
                return;
            }

            void this.props.mitoAPI.sendReorderColumnMessage(
                this.state.selectedSheetIndex,
                this.state.movingColumnParams.column,
                this.state.movingColumnParams.newIndex - 1
            )
                    
            // Reset the columnMovedState so a column resizing doesn't cause the column_reorder_event to get sent
            this.setState({
                movingColumnParams : undefined
            });
        }
    }

    setColumnWidth(sheetIndex: number, columnHeader: string, columnWidth: number): void {
        this.setState(prevState => {
            const newColumnsWidthsArray = [...prevState.columnWidthsArray];
            newColumnsWidthsArray[sheetIndex][columnHeader] = columnWidth;

            return {
                ...prevState,
                columnWidthsArray: newColumnsWidthsArray
            }
        })
    }


    // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
    render() {

        // We get the class to open or close the taskpane, as we open the taskpane by changing
        // the widths of the divs in the css
        const mitoFormulaBarAndMitosheetClass = this.state.currOpenTaskpane.type !== TaskpaneType.NONE ? 
            'mito-formula-bar-and-mitosheet-div mito-formula-bar-and-mitosheet-div-taskpane-open' : 
            'mito-formula-bar-and-mitosheet-div' 

        const mitoDefaultTaskpaneClass = this.state.currOpenTaskpane.type !== TaskpaneType.NONE ? 
            'mito-default-taskpane mito-default-taskpane-open' : 
            'mito-default-taskpane'

        return (
            <div className="mito-container" ref={(ref) => {
                // NOTE: it is crucial we only set the ref it is not already defined, as we
                // will otherwise enter into an infinite loop
                if (!this.state.mitoContainerRef) {
                    this.setState({mitoContainerRef: ref})
                }}}>
                <MitoToolbar 
                    mitoContainerRef={this.state.mitoContainerRef}
                    sheetJSON={this.state.sheetJSONArray[this.state.selectedSheetIndex]} 
                    selectedSheetIndex={this.state.selectedSheetIndex}
                    setEditingMode={this.setEditingMode}
                    setModal={this.setModal}
                    model_id={this.props.model_id}
                    selectedColumn={this.state.selectedColumn}
                    setCurrOpenTaskpane={this.setCurrOpenTaskpane}
                    mitoAPI={this.props.mitoAPI}
                    closeOpenEditingPopups={this.closeOpenEditingPopups}
                    currStepIdx={this.state.currStepIdx}
                    numSteps={this.state.stepDataList.length}
                />
                <div className="mito-main-sheet-div"> 
                    <div className={mitoFormulaBarAndMitosheetClass}>
                        {
                            this.state.runTour && 
                            <IntroductionTour 
                                // Set key so IntroductionTour gets created with new state when tour is turned on/off or import modal is open/closed
                                // see comment in IntroductionTour constructor for more info
                                key={this.state.runTour + this.state.modalInfo.type.toString()} 
                                isImportModalOpen={this.state.modalInfo.type == ModalEnum.Import} 
                                run={this.state.runTour}
                                stepIndex={this.state.tourStepIndex}
                                setTourInfo={this.setTourInfo}
                            />  
                        }
                            
                        <FormulaBar
                            formulaBarValue={this.state.formulaBarValue}
                            handleFormulaBarDoubleClick={this.handleFormulaBarDoubleClick} 
                        />
                        <MitoSheet 
                            selectedSheetIndex={this.state.selectedSheetIndex}
                            formulaBarValue={this.state.formulaBarValue} 
                            editingColumn={this.state.editingModeState.editingCellColumn}
                            columnSpreadsheetCodeJSON={this.state.columnSpreadsheetCodeJSONArray[this.state.selectedSheetIndex]}
                            sheetJSON={this.state.sheetJSONArray[this.state.selectedSheetIndex]} 
                            columnFiltersJSON={this.state.columnFiltersArray[this.state.selectedSheetIndex]}
                            setEditingMode={this.setEditingMode}
                            setEditingFormula={this.setEditingFormula}
                            setCursorIndex={this.setCursorIndex}
                            cursorIndex={this.state.editingModeState.formulaCursorIndex}
                            cellFocused={this.cellFocused}
                            columnMoved={this.columnMoved}
                            columnDragStopped={this.columnDragStopped}
                            model_id={this.props.model_id}
                            sendCellValueUpdate={this.sendCellValueUpdate} 
                            columnWidths={this.state.columnWidthsArray[this.state.selectedSheetIndex]}
                            setColumnWidth={this.setColumnWidth}
                            setCurrOpenTaskpane={this.setCurrOpenTaskpane}
                        />
                    </div>
                    {
                        this.state.currOpenTaskpane.type !== TaskpaneType.NONE && 
                        <div className={mitoDefaultTaskpaneClass}>
                            {this.getCurrOpenTaskpane()}
                        </div>
                    }
                </div>
                {/* Displays the sheet tab bar beneath the sheet */}
                <SheetTabs
                    setCurrOpenSheetTabActions={this.setCurrOpenSheetTabActions}
                    currOpenSheetTabActions={this.state.currOpenSheetTabActions}
                    mitoContainerRef={this.state.mitoContainerRef}
                    dfNames={this.state.dfNames}
                    sheetShapeArray={this.state.sheetShapeArray}
                    selectedSheetIndex={this.state.selectedSheetIndex}
                    setSelectedSheetIndex={this.setSelectedSheetIndex}
                    mitoAPI={this.props.mitoAPI}
                    closeOpenEditingPopups={this.closeOpenEditingPopups}
                />
                {this.getCurrentModalComponent()}
                {this.state.loading && <LoadingIndicator/>}      
                {/* We display intercom for all the non-local users (aka those folks on the server) */}
                {!this.state.isLocalDeployment && <Intercom appID='mu6azgiv'/>}
                {this.state.currStepIdx !== this.state.stepDataList.length - 1 && 
                    <TopLeftPopup
                        message='You are viewing a previous step, and cannot make any edits. Fast forward to start editing.'
                    />
                }
            </div>
        );
    }
}


export default Mito;