// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/


import {
    addColumnButton,
    setFormula
} from '../utils/columnHelpers';

import { 
    tryTest,
} from '../utils/helpers';

import { checkGeneratedCode } from '../utils/generatedCodeHelpers';

import { CURRENT_URL } from '../config';

const code = "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'String': ['123', '1', '2', '3', '4', '5'], 'Number': [123, 1, 2, 3, 4, 5],'Date': ['2001-01-01', '2002-01-01', '2003-01-01','2004-01-01', '2005-01-01', '2006-01-01'],'Mixed': [123, '1', '2', '3', 4, 5]})\nmitosheet.sheet(df1)";


fixture `Test Transpiled Code`
    .page(CURRENT_URL)

test('Test run generated code', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            
            // Create a new column and set it equal to the String column
            await t.click(addColumnButton)
            await setFormula(t, '=String', 'E', '0')

            const expectedDf = {
                'String': ['123', '1', '2', '3', '4', '5'],
                'Number': ['123', '1', '2', '3', '4', '5'],
                'Date': ['2001-01-01', '2002-01-01', '2003-01-01','2004-01-01', '2005-01-01', '2006-01-01'],
                'Mixed': ['123', '1', '2', '3', '4', '5'],
                'E': ['123', '1', '2', '3', '4', '5']
            }

            // Run the generated code
            await checkGeneratedCode(t, 'df1', expectedDf)
        }
    )
});
           