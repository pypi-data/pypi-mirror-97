// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for combinations of sorting and rolling window calculations
*/

import { 
    addColumnButton,
    setFormula
} from '../utils/columnHelpers';

import { 
    checkColumn,
    sortColumn,
    tryTest
} from '../utils/helpers';

import { CURRENT_URL } from '../config';

const code = "import pandas as pd\nimport mitosheet\ndf = pd.DataFrame(data={'day': [1, 5, 3, 9, 33, 2, -4, 8], 'score': [-100, -50, 0, 10, 61, 100, 151, 1000]})\nmitosheet.sheet(df)";


fixture `Test Sort and Rolling Window Workflow`
    .page(CURRENT_URL)

test('Can sort and then rolling window backwards', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await sortColumn(t, 'day', 'ascending');
            await t.click(addColumnButton)
            await setFormula(t, '=score - OFFSET(score, -1)', 'C', '0');
            await checkColumn(t, 'C', ['NaN', '-251', '200', '-100', '-50', '1050', '-990', '51'])
        }
    )
});

test('Can sort and then rolling window backwards', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await sortColumn(t, 'day', 'ascending');
            await t.click(addColumnButton)
            await setFormula(t, '=score - OFFSET(score, 1)', 'C', '0');
            await checkColumn(t, 'C', ['251', '-200', '100', '50', '-1050', '990', '-51', 'NaN'])
        }
    )
});
