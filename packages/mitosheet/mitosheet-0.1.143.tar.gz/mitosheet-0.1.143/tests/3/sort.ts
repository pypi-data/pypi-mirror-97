// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for sorting.
*/

import { 
    checkColumn,
    sortColumn,
    tryTest,
} from '../utils/helpers';

import {
    applyFiltersToColumn
} from '../utils/filterHelpers'

import { CURRENT_URL } from '../config';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';
import { renameColumn } from '../utils/columnHelpers';

const code = "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'String': ['123', '1', '2', '3', '4', '5'], 'Number': [123, 1, 2, 3, 4, 5],'Date': ['2001-01-01', '2002-01-01', '2003-01-01','2004-01-01', '2005-01-01', '2006-01-01'],'Mixed': [123, '1', '2', '3', 4, 5]})\nmitosheet.sheet(df1)";

fixture `Test Sorts`
    .page(CURRENT_URL)

test('Sort strings, numbers, dates ', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await sortColumn(t, 'String', 'ascending');
            await checkColumn(t, 'String', ['1', '123', '2', '3', '4', '5'])
            await sortColumn(t, 'String', 'descending');
            await checkColumn(t, 'String', ['5', '4', '3', '2', '123', '1'])

            await sortColumn(t, 'Number', 'ascending');
            await checkColumn(t, 'String', ['1', '2', '3', '4', '5', '123'])
            await sortColumn(t, 'Number', 'descending');
            await checkColumn(t, 'String', ['123', '5', '4', '3', '2', '1'])

            await sortColumn(t, 'Date', 'ascending');
            await checkColumn(t, 'Date', ['2001-01-01', '2002-01-01', '2003-01-01', '2004-01-01', '2005-01-01', '2006-01-01'])
            await sortColumn(t, 'Date', 'descending');
            await checkColumn(t, 'Date', ['2006-01-01', '2005-01-01', '2004-01-01', '2003-01-01', '2002-01-01', '2001-01-01'])

            const  expectedDf = {
                'String': ['5', '4', '3', '2', '1', '123'],
                'Number': ['5', '4', '3', '2', '1', '123'],
                'Date': ['2006-01-01', '2005-01-01', '2004-01-01', '2003-01-01', '2002-01-01', '2001-01-01'],
                'Mixed': ['5', '4', '3', '2', '1', '123']
            }

            await checkGeneratedCode(t, 'df1', expectedDf)
        }
    )
});


test('Sort, filter, and rename interactions', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await applyFiltersToColumn(t, 'String', [{filterCondition: 'contains', filterValue: '1'}])
            await sortColumn(t, 'Number', 'ascending');
            await renameColumn(t, 'String', 'Strings')

            const  expectedDf = {
                'Strings': ['1', '123'],
                'Number': ['1', '123'],
                'Date': ['2002-01-01', '2001-01-01'],
                'Mixed': ['1', '123']
            }

            await checkGeneratedCode(t, 'df1', expectedDf)
        }
    )
});
