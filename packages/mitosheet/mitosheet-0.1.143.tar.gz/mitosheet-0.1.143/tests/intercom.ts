// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { 
    checkColumn,
    createNotebookRunCell,
    deleteAllNotebooks,
} from './utils/helpers';

import {
    setFormula
} from './utils/columnHelpers'

import { CURRENT_URL, LOCAL_TEST } from './config';
import { Selector } from 'testcafe';

fixture `Test Intercom on Server`
    .page(CURRENT_URL)
    .beforeEach( async t => {
        await createNotebookRunCell(t, true, "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'A': [1, 2, 3]})\nmitosheet.sheet(df1)");
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

const intercomSelector = Selector('div.intercom-launcher');

test('Test displays Intercom on the server', async t => {
    if (!LOCAL_TEST) {
        // Should exist when on the server!
        await t.expect(intercomSelector.exists).ok()
    } else {
        // Should not exist when local
        await t.expect(intercomSelector.exists).notOk()
    }
});