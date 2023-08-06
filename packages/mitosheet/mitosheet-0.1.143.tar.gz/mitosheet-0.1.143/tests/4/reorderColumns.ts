// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for reordering columns.
*/

import { 
    checkSheets,
    DELETE_PRESS_KEYS_STRING,
    tryTest,
} from '../utils/helpers';


import { CURRENT_URL } from '../config';
import { reorderColumn } from '../utils/columnHelpers';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';

const code = `import pandas as pd
import mitosheet
df = pd.DataFrame(data={'A': [123], 'B': [1234]})
mitosheet.sheet(df)`;

fixture `Column Dragging`
    .page(CURRENT_URL)

test('Can drag a column', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await reorderColumn(t, 'B', 'A');

            await checkSheets(t, {
                'df': {
                    'B': ['1234'],
                    'A': ['123']
                }
            })

            await checkGeneratedCode(t, 'df', {
                    'B': ['1234'],
                    'A': ['123']
                }
            )
        }
    )
});


test('Can flip column order twice', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await reorderColumn(t, 'B', 'A');
            await reorderColumn(t, 'A', 'B');

            await checkSheets(t, {
                'df': {
                    'A': ['123'],
                    'B': ['1234']
                }
            })

            await checkGeneratedCode(t, 'df', {
                    'A': ['123'],
                    'B': ['1234'],
                }
            )
        }
    )
});