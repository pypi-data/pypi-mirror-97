// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { 
    checkSheets,
    DELETE_PRESS_KEYS_STRING,
    tryTest,
} from '../utils/helpers';


import { CURRENT_URL } from '../config';
import { deleteSheet, duplicateSheet, getTabActionSelector, renameSheet } from '../utils/tabHelpers';
import { setFormula } from '../utils/columnHelpers';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';
import { getActiveElement } from '../utils/selectors';

const code = "import pandas as pd\nimport mitosheet\ndf = pd.DataFrame(data={'A': [123]})\nmitosheet.sheet(df)";

fixture `Dataframe Operations`
    .page(CURRENT_URL)

test('Can duplicate a tab', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await duplicateSheet(t, 'df');

            await checkSheets(t, {
                'df': {
                    'A': ['123']
                },
                'df_copy': {
                    'A': ['123']
                },
            })

            await checkGeneratedCode(t, 'df_copy', {
                'A': ['123'],
            })
        }
    )
});
           
test('Can duplicate a tab mulitple times', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await duplicateSheet(t, 'df');
            await duplicateSheet(t, 'df');

            await checkSheets(t, {
                'df': {
                    'A': ['123']
                },
                'df_copy': {
                    'A': ['123']
                },
                'df_copy_1': {
                    'A': ['123']
                },
            })

            await checkGeneratedCode(t, 'df_copy_1', {
                'A': ['123'],
            })
        }
    )
});


test('Can duplicate then delete a tab', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await duplicateSheet(t, 'df');
            await deleteSheet(t, 'df');

            await checkSheets(t, {
                'df_copy': {
                    'A': ['123']
                }
            })

            await checkGeneratedCode(t, 'df_copy', {
                'A': ['123'],
            })
        }
    )
});
           

test('Can rename a tab and then add formulas to it', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await renameSheet(t, 'df', 'haha');
            await setFormula(t, '=A', 'B', '0', true);

            await checkSheets(t, {
                'haha': {
                    'A': ['123'],
                    'B': ['123']
                }
            })

            await checkGeneratedCode(t, 'haha', {
                'A': ['123'],
                'B': ['123']
            })
        }
    )
});


test('Can duplicate, rename, and then set a formula', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await duplicateSheet(t, 'df');
            await renameSheet(t, 'df_copy', 'haha');
            await setFormula(t, '=A', 'B', '0', true);

            await checkSheets(t, {
                'df': {
                    'A': ['123'],
                },
                'haha': {
                    'A': ['123'],
                    'B': ['123']
                }
            })

            await checkGeneratedCode(t, 'haha', {
                'A': ['123'],
                'B': ['123']
            })
        }
    )
});
           

test('Can double click to rename a sheet', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await t
                .doubleClick(getTabActionSelector('df'))
                .pressKey(DELETE_PRESS_KEYS_STRING)
                .typeText(getActiveElement(), 'new_name')
                .pressKey('enter')

            await checkSheets(t, {
                'new_name': {
                    'A': ['123']
                }
            })

            await checkGeneratedCode(t, 'new_name', {
                'A': ['123'],
            })
        }
    )
});