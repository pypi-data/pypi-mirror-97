// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/


import {
    addColumnButton,
    setFormula
} from '../utils/columnHelpers';

import { 
    checkSheet,
    tryTest,
} from '../utils/helpers';

import { CURRENT_URL } from '../config';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';

const code = "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'Name': ['Nate', 'Aaron', None], 'Height': ['4', None, 7], 'Weight': [None, 300, 400]})\nmitosheet.sheet(df1)";

fixture `Test Handles Undefined Values`
    .page(CURRENT_URL)

test('Test displays NaNs', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await checkSheet(t, {
                'Name': ['Nate', 'Aaron', 'NaN'],
                'Height': ['4', 'NaN', '7'],
                'Weight': ['NaN', '300', '400']
            })
        }
    )
});

// See here: https://devexpress.github.io/testcafe/documentation/recipes/basics/test-select-elements.html
test('Test allows you to divide NaNs, only carries through in rows', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await t.click(addColumnButton);
            await setFormula(t, '=Height/Weight', 'D', '0');
            await checkSheet(t, {
                'Name': ['Nate', 'Aaron', 'NaN'],
                'Height': ['4', 'NaN', '7'],
                'Weight': ['NaN', '300', '400'],
                'D': ['NaN', 'NaN', '0.0175']
            })
        }
    )
});
