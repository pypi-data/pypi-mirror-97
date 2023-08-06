// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { 
    checkSheets,
    tryTest,
} from '../utils/helpers';


import { CURRENT_URL } from '../config';
import { addColumnButton, setFormula } from '../utils/columnHelpers';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';
import { fastForwardButton, rewindToStep, topLeftPopup } from '../utils/stepHelpers';
import { doNewMerge } from '../utils/mergeHelpers';

const code = "import pandas as pd\nimport mitosheet\ndf = pd.DataFrame(data={'A': [123]})\nmitosheet.sheet(df)";

fixture `Test Steps`
    .page(CURRENT_URL)

test('Can rewind to a step by clicking on it, and then cannot edit', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await setFormula(t, '=A', 'B', '0', true);
            await rewindToStep(t, 0);

            await t
                .expect(fastForwardButton.exists).ok()
                .expect(topLeftPopup.exists).ok()

            await checkSheets(t, {
                'df': {
                    'A': ['123']
                }
            })

            await checkGeneratedCode(t, 'df', {
                'A': ['123']
            })

            // Should not add a column
            await t.click(addColumnButton);
            await checkSheets(t, {
                'df': {
                    'A': ['123']
                }
            })
        }
    )
});


test('Can fast forward to catch to the start of the steps, and then edit more', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await setFormula(t, '=A', 'B', '0', true);
            await rewindToStep(t, 0);
            await t.click(fastForwardButton);

            await t
                .expect(fastForwardButton.exists).notOk()
                .expect(topLeftPopup.exists).notOk()

            await checkSheets(t, {
                'df': {
                    'A': ['123'],
                    'B': ['123']
                }
            })

            await checkGeneratedCode(t, 'df', {
                'A': ['123'],
                'B': ['123']
            })

            await t.click(addColumnButton);
            await checkSheets(t, {
                'df': {
                    'A': ['123'],
                    'B': ['123'],
                    'C': ['0']
                }
            })
        }
    )
});


test('Can roll back to before a sheet-creating step', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await doNewMerge(t, 'df', 'A', 'df', 'A')
            await rewindToStep(t, 0);

            await t
                .expect(fastForwardButton.exists).ok()
                .expect(topLeftPopup.exists).ok()

            await checkSheets(t, {
                'df': {
                    'A': ['123'],
                }
            })

            await t.click(fastForwardButton);

            // Should not add a column
            await checkSheets(t, {
                'df': {
                    'A': ['123'],
                },
                'df2': {
                    'A': ['123'],
                }
            })
        }
    )
});