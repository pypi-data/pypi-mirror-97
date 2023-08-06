// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import { SheetJSON } from "../widget";

export const SHEET_HEIGHT_PIXELS = 400;

export const DEFAULT_COLUMN_WIDTH = 125;
export const LAST_COLUMN_DEFAULT_WIDTH = 300; /* Make sure that this is the width as suggestion-box-container in suggestion-box.css */ 

export const headerHeightParams = {
    defaultHeaderHeight: 40,
    charactersPerRow: 9, // our estimate of the number of characters that fit in each row 
    pixelsPerRow: 35 // number of pixels per row
}


/*
    A helper function for getting the width of columns, for all columns in all sheets. If given the prevColumnWidths, then
    will take columnWidths from there - and if not, will default to the DEFAULT_COLUMN_WIDTH.
*/
export function getColumnWidthsArray(
    sheetJSONArray: SheetJSON[], 
    prevColumnWidthsArray?: Record<string, number>[]
): {columnWidthsArray: Record<string, number>[]; changed: boolean} {
    
    let changed = prevColumnWidthsArray === undefined || sheetJSONArray.length !== prevColumnWidthsArray.length;

    const newColumnWidthsArray = []
    for (let i = 0; i < sheetJSONArray.length; i++) {
        const columnHeaders = sheetJSONArray[i].columns;
        const prevColumnWidths = prevColumnWidthsArray ? prevColumnWidthsArray[i] : undefined;
        const newColumnsWidthsResult = getColumnWidths(columnHeaders, prevColumnWidths)
        newColumnWidthsArray.push(newColumnsWidthsResult.columnWidths)
        changed = changed || newColumnsWidthsResult.changed;
    }

    return {
        columnWidthsArray: newColumnWidthsArray,
        changed: changed
    };
}

/*
    A helper function for getting the width of a list of columns. If given the prevColumnWidths, then
    will take columnWidths from there - and if not, will default to the DEFAULT_COLUMN_WIDTH.

    Includes a helper variable, changed, which tells if you if anything is different between these objects.
*/
export function getColumnWidths(
    columnHeaders: string[], 
    prevColumnWidths?: Record<string, number>
): {columnWidths: Record<string, number>; changed: boolean} {
    const newColumnWidths: Record<string, number> = {};

    // We mark these widths as changed if there were no previous widths, or if there are a different number of columns
    let changed = prevColumnWidths === undefined || columnHeaders.length !== Object.keys(prevColumnWidths)?.length;

    for (let i = 0; i < columnHeaders.length; i ++) {
        const columnHeader = columnHeaders[i];

        if (prevColumnWidths && i === columnHeaders.length - 1 && prevColumnWidths[columnHeader] < LAST_COLUMN_DEFAULT_WIDTH) {
            // If its the last column, make sure the column is at least LAST_COLUMN_DEFAULT_WIDTH so the cell editor is not cutoff
            newColumnWidths[columnHeader] = LAST_COLUMN_DEFAULT_WIDTH;
            changed = true
        } else if (prevColumnWidths && i !== columnHeaders.length - 1 && prevColumnWidths[columnHeader] === LAST_COLUMN_DEFAULT_WIDTH) {
            // If it was previously the last column and the user didn't change it from the default with, 
            // set the column width to DEFAULT_COLUMN_WIDTH.
            newColumnWidths[columnHeader] = DEFAULT_COLUMN_WIDTH;
            changed = true
        } else if (prevColumnWidths && prevColumnWidths[columnHeader]) {
            // if the column has a width, then maintain it
            newColumnWidths[columnHeader] = prevColumnWidths[columnHeader]
        } else {
            newColumnWidths[columnHeader] = DEFAULT_COLUMN_WIDTH;
            // If there is a new column, then things have changed!
            changed = true;
        }
    }

    return {
        columnWidths: newColumnWidths,
        changed: changed
    }
}


export function calculateAndSetHeaderHeight(model_id: string): void {

    // we now do some work to find the best height to give the header row
    // first find the largest header
    let maxHeaderLength = 0
    const gridApi = window.gridApiMap?.get(model_id);

    // if the gridApi does not exist, stop
    if (gridApi === undefined) {
        return
    }

    const rowNodeData = gridApi.getRowNode('0')?.data;
    if (rowNodeData === undefined) {
        // This is undefined when the sheet is empty, and thus there aren't
        // any column headers to resize. Thus, we don't need to do anything.
        return;
    }

    Object.keys(rowNodeData).forEach(key => {
        /* 
            because each row can only hold 9 characters on average, 
            if any words are greater than 9 characters, it will be split into two rows. 

            To make sure that we accommodate these special situations, we assume the worst case
            scenario, and add an extra entire line. 
        */

        let paddingCharacters = 0
        getHeaderWords(key).forEach(word => {
            if (word.length > headerHeightParams.charactersPerRow) {
                paddingCharacters += headerHeightParams.charactersPerRow
            }
        });

        maxHeaderLength = key.length + paddingCharacters > maxHeaderLength ? key.length + paddingCharacters : maxHeaderLength
    });

    /* 
        then set the correct header height... 
        we fit on average 10 letters per row with a starting width of 40 pixels
        and we give each row 30 px of space
    */ 

    gridApi.setHeaderHeight(
        Math.min(
            Math.max(
                (maxHeaderLength / headerHeightParams.charactersPerRow - 1) * headerHeightParams.pixelsPerRow, 
                headerHeightParams.defaultHeaderHeight
            ), SHEET_HEIGHT_PIXELS / 3)
    );

    gridApi.refreshHeader();
}


       

export function getHeaderWords(header: string): string[] {
    /*
        We split the headers at _, and add _ to the latter half (e.g. first_name -> [first, _name]).

        If consecutive words can be combined and be less than the characters per row, then 
        we combine them greedly.

    */

    const headerWords = [];

    const headerWordSplit = header.split(/(?=_)/g);
    let i;
    for (i = 0; i < headerWordSplit.length - 1; i++) {
        const firstWord = headerWordSplit[i];
        const secondWord = headerWordSplit[i + 1];

        if ((firstWord.length + secondWord.length) <= headerHeightParams.charactersPerRow) {
            headerWords.push(firstWord + secondWord)
            i++;
        } else {
            headerWords.push(firstWord)
        }
    }
    if (i === headerWordSplit.length - 1) {
        headerWords.push(headerWordSplit[headerWordSplit.length - 1])
    }

    return headerWords;
} 
