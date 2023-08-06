// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { 
    tryTest,
} from '../utils/helpers';


import { CURRENT_URL } from '../config';
import { fullScreenButton, closeFullScreenButton } from '../utils/selectors';
import { addColumnButton } from '../utils/columnHelpers';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';


const code = "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'A': [123]})\nmitosheet.sheet(df1)";

fixture `Test Full Screen`
    .page(CURRENT_URL)

/* 
    We skip this test as test cafe cannot test fullscreen currently, see here:
    https://github.com/DevExpress/testcafe/issues/2863
*/
test.skip('Test open full screen, writes code, close full screen', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            await t.click(fullScreenButton);
            await t.click(addColumnButton);
            await t.click(closeFullScreenButton);
            await checkGeneratedCode(t, 'df', {
                'A': ['123'],
                'B': ['0']
            })
        }
    )
});
           