// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all useful selectors and helpers for interacting with the merge modal.
*/

import { Selector } from 'testcafe';

export const mergeButton = Selector('div')
    .withExactText('Merge')
    .parent()


export const mergeModalSheetOneSelector = Selector('select.large-select').nth(0)
export const mergeModalSheetOneOptionSelector = mergeModalSheetOneSelector.find('option')
export const mergeModalKeyOneSelector = Selector('select.large-select').nth(1)
export const mergeModalKeyOneOptionSelector = mergeModalKeyOneSelector.find('option')

export const mergeModalSheetTwoSelector = Selector('select.large-select').nth(2)
export const mergeModalSheetTwoOptionSelector = mergeModalSheetTwoSelector.find('option')
export const mergeModalKeyTwoSelector = Selector('select.large-select').nth(3)
export const mergeModalKeyTwoOptionSelector = mergeModalKeyTwoSelector.find('option')


/* Helper that gets the column selector toggle box */
export const getMergeModalColumnBoxSelector = (sheet: 1 | 2): Selector => {
    return Selector('div.multi-toggle-box')
        .nth(sheet - 1)
}

export const getMergeModalColumnSelector = (sheet: 1 | 2, columnHeader: string): Selector => {
    return getMergeModalColumnBoxSelector(sheet)
        .child('div')
        .withExactText(columnHeader)
        .child('input');
}


/*
    Helper function for setting an open merge modal to the given state.

    NOTE: updateNumber is the number of times this specific modal as been updated
    and is used to make implementing this function easier, as we use the toggle all
    button to set the columns that we want. 
*/
async function setMergeToState(
        t: TestController, 
        updateNumber: number,
        sheetOneName: string,
        sheetOneKey: string, 
        sheetTwoName: string, 
        sheetTwoKey: string, 
        columns?: {
            sheetOneColumns: string[], 
            sheetTwoColumns: string[],
        }
    ): Promise<void>  {
    await t
        .click(mergeModalSheetOneSelector)
        .click(mergeModalSheetOneOptionSelector.withExactText(sheetOneName))
        .click(mergeModalKeyOneSelector)
        .click(mergeModalKeyOneOptionSelector.withExactText(sheetOneKey))
        .click(mergeModalSheetTwoSelector)
        .click(mergeModalSheetTwoOptionSelector.withExactText(sheetTwoName))
        .click(mergeModalKeyTwoSelector)
        .click(mergeModalKeyTwoOptionSelector.withExactText(sheetTwoKey))

    if (columns !== undefined) {
        /* 
            We handle the updateNumber here. If updateNumber is even, then Toggle All is set to True,
            and so we just have to toggle it once. Otherwise, if updateNumber is odd, the Toggle All
            is set to False, and so we toggle it twice.

            In both cases, we want to get to the state of "all columns unselected", that way we can
            go through and add only the columns we want.
        */

        await t.click(getMergeModalColumnSelector(1, 'Toggle All'))
        await t.click(getMergeModalColumnSelector(2, 'Toggle All'))

        if (updateNumber % 2 == 1) {
            await t.click(getMergeModalColumnSelector(1, 'Toggle All'))
            await t.click(getMergeModalColumnSelector(2, 'Toggle All'))
        }

        for (let i = 0; i < columns.sheetOneColumns.length; i++) {
            const columnHeader = columns.sheetOneColumns[i];
            await t.click(getMergeModalColumnSelector(1, columnHeader))
        }

        for (let i = 0; i < columns.sheetTwoColumns.length; i++) {
            const columnHeader = columns.sheetTwoColumns[i];
            await t.click(getMergeModalColumnSelector(2, columnHeader))
        }
    }
}


/*
    If repeating an analysis with imports, this changes the files
    that are imported, as well as the pythonCode 
*/
export async function doNewMerge(
        t: TestController, 
        sheetOneName: string,
        sheetOneKey: string, 
        sheetTwoName: string, 
        sheetTwoKey: string, 
        columns?: {
            sheetOneColumns: string[], 
            sheetTwoColumns: string[],
        }
    ): Promise<void> {
    
    await t.click(mergeButton)

    await setMergeToState(t, 0, sheetOneName, sheetOneKey, sheetTwoName, sheetTwoKey, columns)
}


/*
    Helper function for updating a merge modal to the given state.

   The updateNumber param should be equal to the number of times that you have updated
   the columns to keep selection previously.
   
   For example, if you just called doNewMerge(t, 'df1', 'id', 'df2', 'id'), then update
   number would be 0. But if you called await doNewMerge(t, 'df1', 'id', 'df2', 'id', {... columns}),
   then update number would be 1.
*/
export async function updateMerge(
        t: TestController, 
        updateNumber: number, 
        sheetOneName: string, 
        sheetOneKey: string, 
        sheetTwoName: string, 
        sheetTwoKey: string, 
        columns?: {
            sheetOneColumns: string[], 
            sheetTwoColumns: string[],
        }
    ): Promise<void> {
    await setMergeToState(t, updateNumber, sheetOneName, sheetOneKey, sheetTwoName, sheetTwoKey, columns);
}
