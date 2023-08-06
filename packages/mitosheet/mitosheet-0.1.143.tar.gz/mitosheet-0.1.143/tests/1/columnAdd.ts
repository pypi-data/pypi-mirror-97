// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import {
    addColumnButton
} from '../utils/columnHelpers'

import { 
    checkSheet,
    tryTest
} from '../utils/helpers';

import { CURRENT_URL } from '../config';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';

fixture `Column Additions`
    .page(CURRENT_URL)

test('Can add a column when the new column would overlap with the column name', async t => {
    await tryTest(
        t,
        'import pandas as pd\nimport mitosheet\ndf = pd.DataFrame(data={\'B\': [1, 2, 3]})\nmitosheet.sheet(df)',
        async t => {
            await t.click(addColumnButton);

            await checkSheet(t, {
                'B': ['1', '2', '3'],
                'C': ['0', '0', '0']
            });

            const expectedDf = {
                'B': ['1', '2', '3'],
                'C': ['0', '0', '0']
            }

            await checkGeneratedCode(t, 'df', expectedDf)
        }
    )
});