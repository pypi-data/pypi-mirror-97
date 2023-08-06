// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { 
    checkSheets,
    tryTest
} from '../utils/helpers';

import { 
    doNewMerge, updateMerge,
} from '../utils/mergeHelpers';

import { CURRENT_URL } from '../config';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';

const mergeCode = `import pandas as pd
import mitosheet
df1 = pd.DataFrame(data={'id': [1, 2, 3], 'values': [101, 102, 103]})
df2 = pd.DataFrame(data={'id': [1, 2, 3], 'values': [201, 202, 203]})
mitosheet.sheet(df1, df2)`

fixture `Test Merge Functionality`
    .page(CURRENT_URL)


test('Merge opens modal, can create an edit sheet', async t => {
    await tryTest(
        t,
        mergeCode,
        async t => {
            await doNewMerge(t, 'df1', 'id', 'df2', 'id');
            await checkSheets(t, {
                'df3': {
                    'id': ['1', '2', '3'],
                    'values_df1': ['101', '102', '103'],
                    'values_df2': ['201', '202', '203']
                }
            })

            await updateMerge(t, 0, 'df1', 'id', 'df2', 'id', {sheetOneColumns: ['values'], sheetTwoColumns: []});
            await checkSheets(t, {
                'df3': {
                    'id': ['1', '2', '3'],
                    'values': ['101', '102', '103']
                }
            })

            await updateMerge(t, 1, 'df1', 'id', 'df2', 'id', {sheetOneColumns: [], sheetTwoColumns: ['values']});
            await checkSheets(t, {
                'df3': {
                    'id': ['1', '2', '3'],
                    'values': ['201', '202', '203']
                }
            })
        }
    )
});


test('Test merge a single sheet into itself doesnt crash sheet', async t => {
    await tryTest(
        t,
        mergeCode,
        async t => {
            await doNewMerge(t, 'df1', 'id', 'df1', 'id');
            await checkSheets(t, {
                'df3': {
                    'id': ['1', '2', '3'],
                    'values_df1': ['101', '102', '103'],
                    'values_df1_2': ['101', '102', '103']
                }
            })

            const expectedDf = {
                'id': ['1', '2', '3'],
                'values_df1': ['101', '102', '103'],
                'values_df1_2': ['101', '102', '103']
            }

            await checkGeneratedCode(t, 'df3', expectedDf)
        }
    )
});