// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/


import {
    addColumnButton,
    getColumnHeaderContainerSelector,
} from '../utils/columnHelpers';

import { 
    createNotebookRunCell,
    fillCurrentNotebook,
    tryTest
} from '../utils/helpers';

import { saveAnalysis } from '../utils/saveAnalysisHelpers';
import { deleteSavedAnalysis, getSavedAnalysisNameDiv, renameSavedAnalysis, repeatAnalysis } from '../utils/repeatAnalysisHelpers';

import { CURRENT_URL } from '../config';

const code = 'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'A\': [1, 2, 3]})\nmitosheet.sheet(df1)';

fixture `Test Save and Repeat`
    .page(CURRENT_URL)


test('Save analysis saves, repeat analysis repeats', async t => {
    await tryTest(
        t,
        code,
        async t => {
            // Generate a random ID to save the test
            const randomId = '_' + Math.random().toString(36).substr(2, 9);

            await t.click(addColumnButton)

            await saveAnalysis(t, randomId)

            await fillCurrentNotebook(t, code);

            await repeatAnalysis(t, randomId)

            await t.expect(getColumnHeaderContainerSelector('B').exists).ok()
        }
    )
});
   

test('Rename and Delete Saved Analysis', async t => {
    await tryTest(
        t,
        code,
        async t => {
            // Generate a random ID to save the test
            const randomId = '_' + Math.random().toString(36).substr(2, 9);

            await t.click(addColumnButton)

            await saveAnalysis(t, randomId)

            const newRandomId = '_' + Math.random().toString(36).substr(2, 9);
            await renameSavedAnalysis(t, randomId, newRandomId)

            await t.expect(getSavedAnalysisNameDiv(newRandomId).exists).ok()
            await t.expect(getSavedAnalysisNameDiv(randomId).exists).notOk()

            // Delete saved analysis to clean up
            await deleteSavedAnalysis(t, newRandomId)

            // Make sure the saved analysis is gone
            await t.expect(getSavedAnalysisNameDiv(randomId).exists).notOk()
        }
    )
});