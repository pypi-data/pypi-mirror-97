// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all useful selectors and helpers for interacting with the pivot taskpane
*/

import { Selector } from 'testcafe';
import { getTabSelector } from './tabHelpers';

export const pivotButton = Selector('div')
    .withExactText('Pivot Table')
    .parent()

// Data Source Selectors
const dataSourceSelector = Selector('p').withExactText('Data Source').parent().child('select')
const dataSourceOptionsSelector = dataSourceSelector.find('option')

// Rows Selectors
const rowsSelector = Selector('p').withExactText('Rows').parent().child('select')
const rowsOptionsSelector = rowsSelector.find('option')

// Columns Selectors
const columnsSelector = Selector('p').withExactText('Columns').parent().child('select')
const columnsOptionsSelector = columnsSelector.find('option')

// Values Columns Selectors
const valuesSelector = Selector('p').withExactText('Values').parent().child('select')
const valuesOptionsSelector = valuesSelector.find('option')

// Agg Function Selector
export const aggFuncSelector = Selector('div.pivot-table-value-aggregation-card-aggregation-info-div').find('select')
const aggFuncOptionSelector = aggFuncSelector.find('option')

// Delete Selectors
const deleteSelector = Selector('div.pivot-table-column-header-card-exit-div');

/*
    Helper function for adding specific state to a pivot table. NOTE: this just adds, 
    it does not delete any values that may already be there. See updatePivot!

    TODO: handle errors here.
*/
async function addStateToPivot(t: TestController, sourceSheet: string, rows: string[], columns: string[], values: Record<string, string>) {
    await t
        .click(dataSourceSelector)
        .click(dataSourceOptionsSelector.withText(sourceSheet))
    
    // Set rows
    for (let i = 0 ; i < rows.length; i++) {
        const columnHeader = rows[i];
        await t
            .click(rowsSelector)
            .click(rowsOptionsSelector.withExactText(columnHeader))
    }

    // Set columns
    for (let i = 0 ; i < columns.length; i++) {
        const columnHeader = columns[i]
        await t
            .click(columnsSelector)
            .click(columnsOptionsSelector.withExactText(columnHeader))
    }

    // Set Values
    const valueKeys = Object.keys(values);
    for (let i = 0 ; i < valueKeys.length; i++) {
        const columnHeader = valueKeys[i]
        const aggFunc = values[columnHeader];
        await t
            .click(valuesSelector)
            .click(valuesOptionsSelector.withExactText(columnHeader))

        await t
            .click(aggFuncSelector.nth(i))
            .click(aggFuncOptionSelector.withExactText(aggFunc).nth(i))
    }    
}


/*
    Creates a pivot table with the passed params. NOTE: this will close the pivot table if 
    it is open, and will not update an existing pivot table. To do that, use the updatePivot
    function below.
*/
export async function doNewPivot(t: TestController, sourceSheet: string, rows: string[], columns: string[], values: Record<string, string>): Promise<void> {
    
    // Open table
    await t
        .click(getTabSelector(sourceSheet))
        .click(pivotButton)

    // Add state
    await addStateToPivot(t, sourceSheet, rows, columns, values);
}

/*
    Updates a pivot table that is already open with new parameters. Does so by completly
    clearing the pivot table and then setting it to the new params (and clearing any errors
    along the way if it must).
*/
export async function updatePivot(t: TestController, sourceSheet: string, rows: string[], columns: string[], values: Record<string, string>): Promise<void> {

    // Update the source sheet
    await t
        .click(dataSourceSelector)
        .click(dataSourceOptionsSelector.withText(sourceSheet))

    // Delete all the things
    const count = await deleteSelector.count;
    // NOTE: go backwards to not change the indexes
    for (let i = count - 1; i >= 0; i--) {
        // TODO: possibly handle errors here? Not sure if they can occur
        await t.click(deleteSelector.nth(i))
    } 

    // Then, we can just do the pivot (NOTE: it doesn't actually create a new one, which is nice!)
    await addStateToPivot(t, sourceSheet, rows, columns, values);

}