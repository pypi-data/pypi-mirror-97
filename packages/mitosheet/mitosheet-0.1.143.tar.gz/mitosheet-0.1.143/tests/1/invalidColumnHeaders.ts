// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/


import {
    checkSheet,
    tryTest
} from '../utils/helpers';


import { CURRENT_URL } from '../config';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';

const code = "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'What is your first name?': ['Nate'], 'What is your height?!': [4], 'Weight-Of-You': [100]})\nmitosheet.sheet(df1)";

fixture `Test Invalid Column Headers`
    .page(CURRENT_URL)

test('Displays sheet', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await checkSheet(t, {
                'What_is_your_first_name_': ['Nate'],
                'What_is_your_height__': ['4'],
                'Weight_Of_You': ['100']
            }, 'df1')

            const expectedDf = {
                'What_is_your_first_name_': ['Nate'],
                'What_is_your_height__': ['4'],
                'Weight_Of_You': ['100']
            }
    
            await checkGeneratedCode(t, 'df1', expectedDf)
        }
    )
});