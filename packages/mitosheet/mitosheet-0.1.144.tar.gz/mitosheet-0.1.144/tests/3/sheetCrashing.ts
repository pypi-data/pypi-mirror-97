// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for importing data.
*/


import {
    checkSheets,
    tryTest,
} from '../utils/helpers';

import {
    doSimpleImport,
} from '../utils/importHelpers';
import { repeatAnalysisButton } from '../utils/repeatAnalysisHelpers';
import { saveButton } from '../utils/saveAnalysisHelpers';

const code = `
import pandas as pd
import mitosheet

df1 = pd.DataFrame(data={'A': [1, 2, 3], 'B': [4, 5, 6]})
df1.to_csv("df1.csv", index=False)

df2 = pd.DataFrame(data={'A': [7, 8, 9], 'B': [10, 11, 12]})
df2.to_csv("df2.csv", index=False)

mitosheet.sheet()
`
import { CURRENT_URL } from '../config';
import { deleteColumnButton, downloadSheetButton, undoButton } from '../utils/selectors';
import { pivotButton } from '../utils/pivotHelpers';
import { mergeButton } from '../utils/mergeHelpers';
import { deleteSheet, getTabSelector } from '../utils/tabHelpers';
import { getColumnHeaderFilterSelector } from '../utils/columnHelpers';

fixture `Test Sheet Crashing Prevention`
    .page(CURRENT_URL)

test('Can click modal buttons with an empty sheet then do a simple import', async t => {
    await tryTest(
        t,
        code,
        async t => {
            // click the edit button 
            await t.click(undoButton);

            // click the delete button 
            await t.click(deleteColumnButton);

            // click the download button
            await t.click(downloadSheetButton)

            // click the pivot button 
            await t.click(pivotButton);

            // click the pivot button 
            await t.click(mergeButton);

            // click the save analysis button
            await t.click(saveButton);

            // click repeat analysis button
            await t.click(repeatAnalysisButton);

            // click the documentation button 
            //await t.click(documentationButton);

            // then do an import 
            await doSimpleImport(t, ['df1.csv', 'df2.csv'])
            await checkSheets(t, {
                'df1_csv': {
                    'A': ['1', '2', '3'],
                    'B': ['4', '5', '6']
                },
                'df2_csv': {
                    'A': ['7', '8', '9'],
                    'B': ['10', '11', '12']
                }
            })
        }
    )
});


test('Can delete the last sheet while the column control panel is open', async t => {
    await tryTest(
        t,
        'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'A\': [1, 2, 3]})\ndf2 = pd.DataFrame(data={\'ABC\': [4, 5, 6]})\nmitosheet.sheet(df1, df2)',
        async t => {
            // go to the second sheet
            await t.click(getTabSelector('df2'))

            // Open the filter modal
            await t.click(getColumnHeaderFilterSelector('ABC'))

            // Delete teh Second Sheet
            await deleteSheet(t, 'df2');

            // make sure that the sheet is still there
            await t.expect(deleteColumnButton.exists).ok();
        }
    )
});