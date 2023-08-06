// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import {
    getColumnHeaderNameSelector,
    getColumnHeaderContainerSelector,
    columnControlPanelColumnHeaderSelector
} from '../utils/columnHelpers'


import {
    columnHeaderChangeErrorSelector,
    getActiveElement,
    getCellSelector,
} from '../utils/selectors';

import { 
    tryTest,
    DELETE_PRESS_KEYS_STRING
} from '../utils/helpers';

import { CURRENT_URL } from '../config';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';

const code = 'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'id\': [1, 2, 3], \'values\': [101, 102, 103]})\nmitosheet.sheet(df1)';

fixture `Test Rename Column Headers`
    .page(CURRENT_URL)

test('Allows you to rename to valid headers only', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await t
                .click(getColumnHeaderNameSelector('id'))

            // Enter some invalid headers, and get error messages
            await t
                .pressKey(DELETE_PRESS_KEYS_STRING)
                .typeText(getActiveElement(), "123")
                .expect(columnHeaderChangeErrorSelector.exists).ok()
                .pressKey(DELETE_PRESS_KEYS_STRING)
                .typeText(getActiveElement(), "h a")
                .expect(columnHeaderChangeErrorSelector.exists).ok()
                .pressKey(DELETE_PRESS_KEYS_STRING)
                .typeText(getActiveElement(), "h-a")
                .expect(columnHeaderChangeErrorSelector.exists).ok()
                .pressKey(DELETE_PRESS_KEYS_STRING)
            
            // Finially, change to a valid header, and make sure the change goes through
            await t
                .typeText(getActiveElement(), "h_a")
                .expect(columnHeaderChangeErrorSelector.exists).notOk()
                .pressKey('enter')
                .expect(getColumnHeaderContainerSelector('h_a').exists).ok()

            const expectedDf = {
                'h_a': ['1', '2', '3'],
                'values': ['101', '102', '103']
            }

            await checkGeneratedCode(t, 'df1', expectedDf)
        }
    )
});


test('Allows you to rename column headers by clicking on them', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await t
                .click(getColumnHeaderNameSelector('id'))
                .pressKey('enter')
                .click(columnControlPanelColumnHeaderSelector)
                .pressKey(DELETE_PRESS_KEYS_STRING)
                .typeText(getActiveElement(), "h_a")
                .pressKey('enter')

            const expectedDf = {
                'h_a': ['1', '2', '3'],
                'values': ['101', '102', '103']
            }

            await checkGeneratedCode(t, 'df1', expectedDf)
        }
    )
});


test('Clicking a different cell changes the column header that is open', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await t
                .click(getColumnHeaderNameSelector('id'))
                .pressKey('enter')
                .click(getCellSelector('values', '1'))
                .expect(columnControlPanelColumnHeaderSelector.innerText).eql('values')
                .click(getCellSelector('id', '1'))
                .expect(columnControlPanelColumnHeaderSelector.innerText).eql('id')
        }
    )
});
   