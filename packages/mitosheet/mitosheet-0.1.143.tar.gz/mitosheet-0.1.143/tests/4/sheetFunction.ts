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

import {
    applyFiltersToColumn
} from '../utils/filterHelpers'


import { CURRENT_URL } from '../config';
import { deleteSheet, duplicateSheet, getTabActionSelector, renameSheet } from '../utils/tabHelpers';
import { setFormula } from '../utils/columnHelpers';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';
import { getActiveElement } from '../utils/selectors';

const code = `import mitosheet
mitosheet.sheet(saved_analysis_name='mito_simple_raw_import')`;

fixture `Sheet Function`
    .page(CURRENT_URL)

test('Can pass a saved analysis to sheet function, correct df names', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await checkSheets(t, {
                'df': {
                    'A': ['123']
                },
            })

            await setFormula(t, '=A', 'B', '0', true);
            await applyFiltersToColumn(t, 'A', [{filterCondition: '=', filterValue: '123'}])

            await checkSheets(t, {
                'df': {
                    'A': ['123'],
                    'B': ['123']
                },
            })

            await checkGeneratedCode(t, 'df', {
                'A': ['123'],
                'B': ['123']
            })
            
        }
    )
});