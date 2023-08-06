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
import { documentationButton, documentationTaskpaneBackButton, taskpaneCloseButton, documentationTaskpaneFunctionSelector } from '../utils/selectors';

const code = "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'A': [123]})\nmitosheet.sheet(df1)";

fixture `Test Documentation`
    .page(CURRENT_URL)

test('Test can open documentation', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            // open docuemntation taskpane
            await t.click(documentationButton);

            // click on the first documentation list item
            await t.click(documentationTaskpaneFunctionSelector);

            // use the back button
            await t.click(documentationTaskpaneBackButton);

            // close the documentation taskpane
            await t.click(taskpaneCloseButton);
        }
    )
});
           