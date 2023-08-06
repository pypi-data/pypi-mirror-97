// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/


import {
    errorMessageSelector,
} from '../utils/selectors';

import { 
    modalCloseButtonSelector 
} from '../utils/allModals';

import {
    addColumnButton,
    setFormula
} from '../utils/columnHelpers';

import { 
    tryTest,
} from '../utils/helpers';

import { CURRENT_URL } from '../config';

fixture `Test Errors`
    .page(CURRENT_URL)

test('Reports errors to user', async t => {
    await tryTest(
        t,
        'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'A\': [1, 2, 3]})\nmitosheet.sheet(df1)',
        async t => {
            /*
                Tests the following errors:
                1. Write LEFT(A), and get an error telling you to use an equals sign
                2. Reference cell A1 instead of A, get an error correcting this
                3. Reference column B, get a circular reference error
                4. Write =FUNC(A), get a function does not exist error
                5. Write =SUM(C), get a column does not exist error
                6. Write =VLOOKUP(A) and get a invalid formula error, pointing you to merge
            */

            const formulaErrorPairs = [
                {
                    formula: '=B',
                    error: "Sorry, circular references are not supported currently."
                },
                {
                    formula: '=FUNC(A)',
                    error: "Sorry, mito does not currently support the function FUNC."
                },
                {
                    formula: '=SUM(C)',
                    error: "Sorry, there is no column with the name C."
                },
                {
                    formula: '=VLOOKUP(A)',
                    error: "Instead of VLOOKUP, try using the merge button"
                },
            ]

            await t.click(addColumnButton)

            for (let i = 0; i < formulaErrorPairs.length; i++) {
                const formula = formulaErrorPairs[i].formula;
                const error = formulaErrorPairs[i].error;
                await setFormula(t, formula, 'B', '0');
                await t
                    .expect(errorMessageSelector.innerText).contains(error)
                    .click(modalCloseButtonSelector)
            }
            

        }
    )
});
   