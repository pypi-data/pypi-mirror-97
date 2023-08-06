// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
Contains useful selectors and helpers for interacting with the generated code
*/

import { Selector } from "testcafe";

export const selectGeneratedCode = Selector('span.cm-comment')
    .withExactText('# MITO CODE START (DO NOT EDIT)');

export const selectLastLineOfGeneratedCode = Selector('span.cm-comment')
    .withExactText('# MITO CODE END (DO NOT EDIT)');

export const dataframeSelector = Selector('table.dataframe')
export const dataframeHeadersSelector = dataframeSelector
    .child('thead')
export const dataframeBodySelector = dataframeSelector
    .child('tbody')

export const getDataframeHeaderSelector = (headerIndex: number): Selector => {
    return dataframeHeadersSelector
        .find('th')
        .nth(headerIndex + 1) // we skip the index column
}

export const getDataframeContentSelector = (headerIndex: number, dataIndex: number): Selector => {
    return dataframeBodySelector
        .find('tr')
        .nth(dataIndex)
        .find('td')
        .nth(headerIndex) // we don't have to skip index column as it is a th, not a td
}


export async function checkGeneratedCode(t: TestController, dfName: string, expectedDf: Record<string, string[]>): Promise<void> {
    
    // Select the Generated Code
    await t.click(selectGeneratedCode);

    // print out the edited df by:
    // 1. selecting the last line of the generated code
    await t.click(selectLastLineOfGeneratedCode);
    // 2. going to the end of the line
    let i = 0;
    for (i = 0; i < 16; i++) {
        await t.pressKey('right')
    } 

    // 3. create a new line
    await t.pressKey('enter')

    // press the keys to type the dataframe name
    for (let i = 0; i < dfName.length; i++) {
        await t.pressKey(dfName.charAt(i))        
    }

    // run the cell
    await t.pressKey('shift+enter');

    /* converts string representation of df into js df 

        note: we convert from actual output to js df and not the other way
        because there seems to be a variable number of spaces between column headers, 
        which makes it hard to always properly format the string correctly. 
    
        -- IMPORTANT NOTE: this requires that no elements contain a space! --
    */


    const columnHeaders = Object.keys(expectedDf);
    for (let i = 0; i < columnHeaders.length; i++) {
        const columnHeader = columnHeaders[i];
        const columnData = expectedDf[columnHeader];

        // Check the column headers are correct
        await t.expect(getDataframeHeaderSelector(i).innerText).eql(columnHeader)
        for (let j = 0; j < columnData.length; j++) {
            const data = columnData[j];
            // Then, check all the data is correct
            await t.expect(getDataframeContentSelector(i, j).innerText).eql(data)
        }
    }
}