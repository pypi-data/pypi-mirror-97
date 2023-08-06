// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { 
    checkColumn,
    tryTest
} from '../utils/helpers';

import {
    setFormula
} from '../utils/columnHelpers'

import { CURRENT_URL } from '../config';

fixture `Test Handles Dates`
    .page(CURRENT_URL)

test('Test displays dates, works with date functions', async t => {
    await tryTest(
        t, 
        "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'name': ['alice','bob','charlie'], 'dob': ['2005-10-23','2002-10-2','2001-11-14']})\ndf1['dob'] = pd.to_datetime(df1['dob'])\nmitosheet.sheet(df1)",
        async t => {
            await checkColumn(t, 'dob', ['2005-10-23 00:00:00', '2002-10-02 00:00:00', '2001-11-14 00:00:00'])

            await setFormula(t, '=DAY(dob)', 'C', '0', true);
            await setFormula(t, '=MONTH(dob)', 'D', '0', true);
            await setFormula(t, '=YEAR(dob)', 'E', '0', true);
            await setFormula(t, '=DATEVALUE(CONCAT(E, \'-\', D, \'-\', C))', 'F', '0', true);

            await checkColumn(t, 'F', ['2005-10-23 00:00:00', '2002-10-02 00:00:00', '2001-11-14 00:00:00'])
        }
    )
});