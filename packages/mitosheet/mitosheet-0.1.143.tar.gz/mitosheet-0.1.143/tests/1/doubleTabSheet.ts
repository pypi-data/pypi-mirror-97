// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/


import { 
    getCellSelector,
    getFormulaBarSelector
} from '../utils/selectors';

import { getTabSelector } from '../utils/tabHelpers';

import { 
    tryTest,
} from '../utils/helpers';

import {
    addColumnButton,
    setFormula
} from '../utils/columnHelpers';


import { CURRENT_URL } from '../config';


fixture `Create a Double Tab Mitosheet`
    .page(CURRENT_URL)

test('Switching between tabs switches formula bar', async t => {
    await tryTest(
        t,
        'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'A\': [1, 2, 3]})\ndf2 = pd.DataFrame(data={\'A\': [4, 5, 6]})\nmitosheet.sheet(df1, df2)',
        async t => {
            // Set formula on the first sheet
            await t.click(addColumnButton)
            await setFormula(t, '=10', 'B', '0')
            await t.expect(getFormulaBarSelector().innerText).eql('=10')

            // Switch to the second sheet, and set the formula there
            await t.click(getTabSelector('df2'))
            await t.click(addColumnButton)
            await setFormula(t, '=11', 'B', '0')
            await t.expect(getFormulaBarSelector().innerText).eql('=11')

            // Switch back to the first sheet, click on the B column, and make sure the formula updates
            await t.click(getTabSelector('df1'))
            await t.click(getCellSelector('B', '0'))
            await t.expect(getFormulaBarSelector().innerText).eql('=10')
        }
    )
});