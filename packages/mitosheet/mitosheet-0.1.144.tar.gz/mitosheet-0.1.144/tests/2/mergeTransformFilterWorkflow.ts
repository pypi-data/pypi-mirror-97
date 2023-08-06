// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains a merging, transforming, and then filtering workflow
*/

import {
    doNewMerge,
} from '../utils/mergeHelpers'

import { 
    checkColumn,
    tryTest,
} from '../utils/helpers';

import {
    applyFiltersToColumn
} from '../utils/filterHelpers';

import {
    addColumnButton,
    renameColumn,
    setFormula
} from '../utils/columnHelpers';

import { checkGeneratedCode } from '../utils/generatedCodeHelpers';

import { CURRENT_URL } from '../config';

const code = 'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'id\': [1, 2, 3], \'first_name\': [\'Nate\', \'Aaron\', \'Jake\']})\ndf2 = pd.DataFrame(data={\'id\': [1, 2, 3], \'last_name\': [\'rush\', \'Diamond-Reivich\', \'diamond-reivich\']})\nmitosheet.sheet(df1, df2)';

fixture `Test Merge Transform Filter Workflow`
    .page(CURRENT_URL)

test('Merge Transform Filter', async t => {
    await tryTest(
        t, 
        code, 
        async t => {
            // Do the merge
            await doNewMerge(t, 'df1', 'id', 'df2', 'id');
            
            // Create a new column
            await t.click(addColumnButton)

            await renameColumn(t, 'D', 'full_name')

            // Set column formula to concat first name and last name
            await setFormula(t, '=CONCAT(first_name, " ", last_name)', 'full_name', '0');

            // then update the last_name column to upper case 
            await setFormula(t, '=UPPER(CONCAT(first_name, " ", last_name))', 'full_name', '0');

            // only keep rows whose full name column contains 'VICH'
            await applyFiltersToColumn(
                t, 
                'full_name', 
                [
                    {filterCondition: 'contains', filterValue: 'VICH'},
                ]
            )
            await checkColumn(t, 'full_name', ['AARON DIAMOND-REIVICH', 'JAKE DIAMOND-REIVICH']);

            const expectedDf = {
                'id': ['2', '3'],
                'first_name': ['Aaron', 'Jake'],
                'last_name': ['Diamond-Reivich', 'diamond-reivich'],
                'full_name': ['AARON DIAMOND-REIVICH', 'JAKE DIAMOND-REIVICH']
            }

            await checkGeneratedCode(t, 'df3', expectedDf)
        }
    )
});

