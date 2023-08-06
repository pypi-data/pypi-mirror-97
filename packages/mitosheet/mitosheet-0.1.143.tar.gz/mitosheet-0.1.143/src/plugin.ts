// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import { Application, IPlugin } from '@phosphor/application';

import { Widget } from '@phosphor/widgets';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import {
    INotebookTracker, NotebookActions
} from '@jupyterlab/notebook';

import {
    ICellModel
} from "@jupyterlab/cells";

import * as widgetExports from './widget';

import { MODULE_NAME, MODULE_VERSION } from './version';

import {
    IObservableString,
    IObservableUndoableList
} from '@jupyterlab/observables';

const EXTENSION_ID = 'mitosheet:plugin';

/**
 * The example plugin.
 */
const examplePlugin: IPlugin<Application<Widget>, void> = ({
    id: EXTENSION_ID,
    requires: [IJupyterWidgetRegistry, INotebookTracker],
    activate: activateWidgetExtension,
    autoStart: true,
} as unknown) as IPlugin<Application<Widget>, void>;
// the "as unknown as ..." typecast above is solely to support JupyterLab 1
// and 2 in the same codebase and should be removed when we migrate to Lumino.

export default examplePlugin;


function getCellAtIndex(cells: IObservableUndoableList<ICellModel> | undefined, index: number): ICellModel | undefined {
    if (cells == undefined) {
        return undefined;
    }

    const cellsIterator = cells.iter();
    let cell = cellsIterator.next();
    let i = 0;
    while (cell) {
        if (i == index) {
            return cell;
        }

        i++;
        cell = cellsIterator.next();
    }

  
    return undefined;
}

function codeContainer(
    analysisName: string,
    code: string[]
): string {

    if (code.length == 0) {
        return '';
    }

    return `# MITO CODE START (DO NOT EDIT)
# SAVED-ANALYSIS-START${analysisName}SAVED-ANALYSIS-END

from mitosheet import *

${code.join('\n\n')}
  
# MITO CODE END (DO NOT EDIT)`
}


function getAnalysisName(codeblock: string): string | undefined {
    /*
    Given the code container format, returns the name of the analysis.
  */

    if (!codeblock.includes('SAVED-ANALYSIS-START')) {
        return undefined;
    }

    // We get just the string part of the container that is the column spreadsheet code
    return codeblock.substring(
        codeblock.indexOf('SAVED-ANALYSIS-START') + 'SAVED-ANALYSIS-START'.length,
        codeblock.indexOf('SAVED-ANALYSIS-END')
    );
}

function getCellText(cell: ICellModel| undefined): string {
    if (cell == undefined) return ''; 
    const value = cell.modelDB.get('value') as IObservableString;
    return value.text;
}

function isMitosheetSheetCell(cell: ICellModel | undefined): boolean {
    // Returns true iff a the given cell ends with a mitosheet.sheet call
    // and so displays a mito sheet when run!

    const currentCode = getCellText(cell);

    // Take all the non-empty lines from the cell
    const lines = currentCode.split('\n').filter(line => {return line.length > 0});
    if (lines.length == 0) {
        return false;
    }

    const lastLine = lines[lines.length - 1];
    return lastLine.startsWith('mitosheet.sheet(');
}

function isMitoAnalysisCell(cell: ICellModel | undefined): boolean {
    // Returns true iff a the given cell is a cell containing the generated
    // mito analysis code
    const currentCode = getCellText(cell);
    return currentCode.startsWith('# MITO CODE START');
}

/* Returns True if the passed cell is empty */
function isEmptyCell(cell: ICellModel | undefined): boolean {
    const currentCode = getCellText(cell);
    return currentCode.trim() === '';
}

function writeToCell(cell: ICellModel | undefined, code: string): void {
    if (cell == undefined) {
        return;
    }
    const value = cell.modelDB.get('value') as IObservableString;
    value.text = code;
}


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(
    app: Application<Widget>,
    registry: IJupyterWidgetRegistry,
    tracker: INotebookTracker
): void {

    /*
    We define a command here, so that we can call it elsewhere in the
    app - and here is the only place we have access to the app (which we
    need to be able to add commands) and tracker (which we need to get
    the current notebook).
  */
    app.commands.addCommand('write-code-to-cell', {
        label: 'Write Mito Code to a Cell',
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        execute: (args: any) => {
            /*
        Given an analysisName and code, this writes the code to the cell.
        
        We assume this function is called either:
        1. When the current cell is the cell that calls mitosheet.sheet
        2. When the current cell is _right below_ the cell that calls mitosheet.sheet

        If we're in case (1):
        - If the cell below already has a mito analysis written to it, we overwrite it
        - If the cell below has no existing mito analysis, we insert a new cell and write to that. 

        If we're in case (2):
        - If this has the analysis written to it, we overwrite it.
        - Otherwise, we insert a new cell above and write to that. 
      */

            const analysisName = args.analysisName as string;
            const codeJSON = args.codeJSON as widgetExports.CodeJSON;

            // This is the code that was passed to write to the cell.
            const code = codeContainer(analysisName, codeJSON.code);

            // We get the current notebook (currentWidget)
            const notebook = tracker.currentWidget?.content;
            const cells = notebook?.model?.cells;

            if (notebook == undefined || cells == undefined) {
                return 
            }

            const activeCell = notebook.activeCell;
            const activeCellIndex = notebook.activeCellIndex;

            if (isMitosheetSheetCell(activeCell?.model)) {
                const nextCell = getCellAtIndex(cells, activeCellIndex + 1)
                if (isMitoAnalysisCell(nextCell)) {
                    // If the next cell contains a mito analysis, we overwrite it
                    writeToCell(nextCell, code);
                } else {
                    // Otherwise, we insert a cell above and write to that. 
                    NotebookActions.insertBelow(notebook);
                    const newNextCell = getCellAtIndex(cells, activeCellIndex + 1);
                    writeToCell(newNextCell, code);
                }
            } else {
                // We assume we're in case 2, and thus the current cell is where the analysis should be
                if (isMitoAnalysisCell(activeCell?.model)) {
                    // If this is already analysis, we overwrite it
                    writeToCell(activeCell?.model, code);
                } else {
                    // Otherwise, we insert a cell above, and write to that, if the current cell is not empty
                    if (!isEmptyCell(activeCell?.model)) {
                        NotebookActions.insertAbove(notebook);
                    }
                    // New cell is the previous cell, now
                    const prevCell = notebook.activeCell;
                    writeToCell(prevCell?.model, code);
                }
            }
        }
    });


    app.commands.addCommand('repeat-analysis', {
        label: 'Replicates the current analysis on a given new file, in a new cell.',
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        execute: (args: any) => {

            const fileName = args.fileName as string;

            // We get the current notebook (currentWidget)
            const notebook = tracker.currentWidget?.content;
            const context = tracker.currentWidget?.context;
            if (!notebook || !context) return;

            // We run the current cell and insert a cell below
            // TODO: see if handling this promise is good enough!
            void NotebookActions.runAndInsert(notebook, context.sessionContext);

            // And then we write to this inserted cell (which is now the active cell)
            const activeCell = notebook.activeCell;
            if (activeCell) {
                const value = activeCell.model.modelDB.get('value') as IObservableString;
                const df_name = fileName.replace(' ', '_').split('.')[0]; // We replace common file names with a dataframe name
                const code = `# Repeated analysis on ${fileName}\n\n${df_name} = pd.read_csv('${fileName}')\n\nmito_analysis(${df_name})\n\nmitosheet.sheet(${df_name})`
                value.text = code;
            }
        }
    });

    app.commands.addCommand('get-df-names', {
        label: 'Read df name from mitosheet.sheet call',
        execute: (): string[] => {
            /*
        This function has to deal with the fact that there are 2 cases
        in which we want to get the dataframe names:
        1. The first time we are rendering a mitosheet (e.g. after you run a sheet
          with a mitosheet.sheet call).
          
          In this case, the active cell is the cell _after_ the mitosheet.sheet call.

        2. When you have a Mito sheet already displayed and saved in your notebook, 
          and your refresh the page. 

          In this case, the active cell is the first cell in the notebook, which
          may or may not be the cell the mitosheet.sheet call is actually made. 

        We handle these cases by detecting which case we're in based on the index
        of the currently selected cell. 

        However, in a sheet with _multiple_ mitosheet.sheet calls, if we're in
        case (2), we can't know which cell to pull from. I haven't been able to
        think of away around this. 
        
        However, since this is rare for now, we don't worry about it and just do whatever
        here for now, and hope the user will refresh the sheet if it's not working!
      */

            // We get the current notebook (currentWidget)
            const notebook = tracker.currentWidget?.content;

            if (!notebook) return [];

            const activeCellIndex = notebook.activeCellIndex;
            const cells = notebook.model?.cells;

            const getDfNamesFromCellContent = (content: string): string[] => {
                let nameString = content.split('mitosheet.sheet(')[1].split(')')[0];
        
                // If there is a tutorial mode parameter passed, we ignore it
                if (nameString.includes('tutorial_mode')) {
                    nameString = nameString.split('tutorial_mode')[0].trim();
                }

                // If there is a analysis name parameter passed, we ignore it
                if (nameString.includes('saved_analysis_name')) {
                    nameString = nameString.split('saved_analysis_name')[0].trim();
                }
        
                const dfNames = nameString.split(',').map(dfName => dfName.trim()).filter(dfName => dfName.length > 0);
                return dfNames;
            }

            // See comment above. We are in case (2). 
            if (activeCellIndex === 0 && cells !== undefined) {
                // We just get the first mitosheet.sheet call we can find

                const cellsIterator = cells.iter();
                let cell = cellsIterator.next();
                while (cell) {
                    const cellContent = (cell.modelDB.get('value') as IObservableString).text;
                    if (cellContent.includes('mitosheet.sheet')) {
                        return getDfNamesFromCellContent(cellContent);
                    }
                    cell = cellsIterator.next();
                }
                return [];
            } else {
                // Otherwise, were in case (1)
                const previousCell = getCellAtIndex(cells, activeCellIndex - 1); // TODO: change this to next cell model or something
                if (previousCell) {
                    // remove the df argument to mitosheet.sheet() from the cell's text
                    const previousCellContent = (previousCell.modelDB.get('value') as IObservableString).text;
                    return getDfNamesFromCellContent(previousCellContent);
                }
                return [];
            }      
        }
    });

    app.commands.addCommand('read-existing-analysis', {
        label: 'Reads any existing mito analysis from the previous cell, and returns the saved ColumnSpreadsheetCodeJSON, if it exists.',
        execute: (): string | undefined => {
            /*
        This should _only_ run right after the mitosheet.sheet call is run, 
        and so the currently selected cell is the cell that actually contains the mito
        analysis.
      */

            // We get the current notebook (currentWidget)
            const notebook = tracker.currentWidget?.content;

            if (!notebook) return undefined;

            // We get the previous cell to the current active cell
            const activeCell = notebook.activeCell;

            if (activeCell) {
                // remove the df argument to mitosheet.sheet() from the cell's text
                const previousValue = activeCell.model.modelDB.get('value') as IObservableString;
                return getAnalysisName(previousValue.text);
            } 
            return undefined;
        }
    });

    window.commands = app.commands; // so we can write to it elsewhere
    registry.registerWidget({
        name: MODULE_NAME,
        version: MODULE_VERSION,
        exports: widgetExports,
    });
}