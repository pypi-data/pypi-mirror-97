// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import { 
    CellValueChangedEvent, 
    CellFocusedEvent, 
    GridReadyEvent, 
    SuppressKeyboardEventParams,
    GridColumnsChangedEvent,
    ColumnMovedEvent,
    ColumnResizedEvent
} from 'ag-grid-community';
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';
import '../../css/mitosheet.css';
import MitoCellEditor from './MitoCellEditor';

import { TAKE_SUGGESTION_KEYS, ARROW_UP_KEYS, ARROW_DOWN_KEYS } from './MitoCellEditor';

// And functions for building components
import { buildGridData, buildGridColumns } from '../utils/gridData';

// Import types
import { SheetJSON } from '../widget';
import { ColumnSpreadsheetCodeJSON, SheetColumnFilterMap } from './Mito';
import { calculateAndSetHeaderHeight, headerHeightParams } from '../utils/gridStyling';
import { TaskpaneInfo } from './taskpanes/taskpanes';
    
const MitoSheet = (props: {
    selectedSheetIndex: number,
    sheetJSON: SheetJSON | undefined; 
    formulaBarValue: string;
    editingColumn: string;
    columnSpreadsheetCodeJSON: ColumnSpreadsheetCodeJSON;
    columnFiltersJSON: SheetColumnFilterMap;
    sendCellValueUpdate: (column: string, newValue: string) => void; 
    setEditingMode: (on: boolean, column: string, rowIndex: number) => void;
    setEditingFormula: (formula: string) => void;
    setCursorIndex: (index: number) => void;
    cursorIndex: number;
    cellFocused: (event: CellFocusedEvent) => void;
    columnMoved: (event: ColumnMovedEvent) => void;
    columnDragStopped: () => void;
    model_id: string;
    columnWidths: Record<string, number>;
    setColumnWidth: (sheetIndex: number, columnHeader: string, columnWidth: number) => void;
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) =>  void; 
}): JSX.Element => {
    
    function onGridReady(params: GridReadyEvent) {
        if (window.gridApiMap === undefined) {
            window.gridApiMap = new Map();
        }
        window.gridApiMap.set(props.model_id, params.api);

        calculateAndSetHeaderHeight(props.model_id);
    }

    /* 
        Ag-grid does some sort of caching that means if we rename a column
        it will treat this as a new column that got added to the _end_.

        This function runs whenever the columns change. 
        
        It makes sure that the columns are in the correct order. If they aren't,
        it then places them in the correct order.
    */
    function onGridColumnsChanged(params: GridColumnsChangedEvent) {
        
        if (props.sheetJSON === undefined) {
            return;
        }

        const columnState = params.columnApi.getColumnState();
        const correctColumnOrder = props.sheetJSON.columns;

        for (let i = 0; i < correctColumnOrder.length; i++) {
            const columnName = correctColumnOrder[i].toString();

            // If, ignoring the index column, this column is not in the right place, then
            // we have some reordering to do!
            const correctIndex = i + 1;
            const currentDisplayIndex = columnState.findIndex((columnState) => {
                return columnState.colId === columnName;
            })

            if (correctIndex !== currentDisplayIndex) {
                params.columnApi.moveColumn(columnName, correctIndex);
            }
        }
    }

    /*
        Listener that is run when a cell value changes, which in our case
        means a formula was updated. In this case, we send a message
        to the backend of this update.
    */
    const cellValueChanged = (e: CellValueChangedEvent) => {
        const column = e.colDef.field ? e.colDef.field : "";
        const newValue = e.newValue;
        
        props.sendCellValueUpdate(column, newValue);
    };

    /*
        Listener that is run anytime a column resizes. If this resize is caused
        by a user dragging the column, then we save the final width the user
        has dragged it to.
    */
    const onColumnResized = (e: ColumnResizedEvent) => {
        // We save the resize when it occurs because the user finishes dragging a column!
        if (e.finished && e.source == 'uiColumnDragged') {
            const columns = e.columns;
            if (columns) {
                const resizedColumn = columns[0].getColId();
                const newWidth = columns[0].getActualWidth();
                props.setColumnWidth(props.selectedSheetIndex, resizedColumn, newWidth);
            }
        }
    }

    const columns = buildGridColumns(
        props.sheetJSON?.columns, 
        props.columnSpreadsheetCodeJSON, 
        props.columnFiltersJSON,
        props.formulaBarValue,
        props.editingColumn,
        props.cursorIndex,
        props.setEditingMode, 
        props.setEditingFormula,
        props.setCursorIndex,
        props.setCurrOpenTaskpane,
        props.columnWidths
    );
    const rowData = buildGridData(props.sheetJSON);

    const frameworkComponents = {
        simpleEditor: MitoCellEditor,
    }

    return (
        <div style={{height: '100%'}}>
            <div className="ag-theme-alpine mitosheet-ag-grid"> 
                <AgGridReact
                    onGridReady={onGridReady}
                    onGridColumnsChanged={onGridColumnsChanged}
                    onCellFocused={(e: CellFocusedEvent) => props.cellFocused(e)}
                    onColumnMoved={(e: ColumnMovedEvent) => props.columnMoved(e)}
                    onDragStopped={() => props.columnDragStopped()}
                    rowData={rowData}
                    rowHeight={25}
                    rowSelection={'multiple'} // allows multiple rows to be selected.
                    headerHeight={headerHeightParams.defaultHeaderHeight}
                    frameworkComponents={frameworkComponents}
                    suppressKeyboardEvent={(params: SuppressKeyboardEventParams) => {
                        /* 
                            While we're editing a cell, we suppress events that we use
                            to do things within the editor.

                            NOTE: this function should suppress the events matched in onKeyDown
                            in MitoCellEditor!
                        */

                        if (!params.editing) {
                            return false;
                        }
                        return TAKE_SUGGESTION_KEYS.includes(params.event.key) ||
                               ARROW_UP_KEYS.includes(params.event.key) ||
                              ARROW_DOWN_KEYS.includes(params.event.key);
                    }}
                    onCellValueChanged={cellValueChanged}
                    suppressDragLeaveHidesColumns={true}
                    suppressColumnMoveAnimation={true} 
                    onColumnResized={onColumnResized}>
                    {columns}
                </AgGridReact>
            </div>
        </div>
    );
};

export default MitoSheet;