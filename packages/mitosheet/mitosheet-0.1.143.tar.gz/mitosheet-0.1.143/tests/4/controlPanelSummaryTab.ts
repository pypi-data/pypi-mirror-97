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
import { columnSummaryGraphSelector, columnSummaryTableSelector, openColumnStatistics } from '../utils/columnHelpers';
import { errorMessageSelector } from '../utils/selectors';

fixture `Control Panel Summary Tab`
    .page(CURRENT_URL)

test('Works (no errors) on a number column', async t => {
    await tryTest(
        t,
        `import mitosheet\nimport pandas as pd\ndf = pd.DataFrame({\'A\': [123]})\nmitosheet.sheet(df)`, 
        async t => {
            await openColumnStatistics(t, 'A');
            await t
                .expect(errorMessageSelector.exists).notOk()
                .expect(columnSummaryGraphSelector.exists).ok()
                .expect(columnSummaryTableSelector.exists).ok()
                .expect(columnSummaryTableSelector.find('tr').count).gt(0)
        }
    )
});

test('Works (no errors) on a string column', async t => {
    await tryTest(
        t,
        `import mitosheet\nimport pandas as pd\ndf = pd.DataFrame({\'A\': [\'A\']})\nmitosheet.sheet(df)`, 
        async t => {
            await openColumnStatistics(t, 'A');
            await t
                .expect(errorMessageSelector.exists).notOk()
                .expect(columnSummaryGraphSelector.exists).ok()
                .expect(columnSummaryTableSelector.exists).ok()
                .expect(columnSummaryTableSelector.find('tr').count).gt(0)
        }
    )
});

test('Works (no errors) on a boolean column', async t => {
    await tryTest(
        t,
        `import mitosheet\nimport pandas as pd\ndf = pd.DataFrame({\'A\': [True, False]})\nmitosheet.sheet(df)`, 
        async t => {
            await openColumnStatistics(t, 'A');
            await t
                .expect(errorMessageSelector.exists).notOk()
                .expect(columnSummaryGraphSelector.exists).ok()
                .expect(columnSummaryTableSelector.exists).ok()
                .expect(columnSummaryTableSelector.find('tr').count).gt(0)
        }
    )
});

test('Works (no errors) on a datetime column', async t => {
    await tryTest(
        t,
        `import mitosheet\nimport pandas as pd\ndf = pd.DataFrame({\'A\': pd.to_datetime(['12-20-2020', '12-20-2020'])})\nmitosheet.sheet(df)`, 
        async t => {
            await openColumnStatistics(t, 'A');
            await t
                .expect(errorMessageSelector.exists).notOk()
                .expect(columnSummaryGraphSelector.exists).ok()
                .expect(columnSummaryTableSelector.exists).ok()
                .expect(columnSummaryTableSelector.find('tr').count).gt(0)
        }
    )
});


test('Works (no errors) on a mixed column', async t => {
    await tryTest(
        t,
        `import mitosheet\nimport pandas as pd\ndf = pd.DataFrame({\'A\': ['12-20-2020', True, 10]})\nmitosheet.sheet(df)`, 
        async t => {
            await openColumnStatistics(t, 'A');
            await t
                .expect(errorMessageSelector.exists).notOk()
                .expect(columnSummaryGraphSelector.exists).ok()
                .expect(columnSummaryTableSelector.exists).ok()
                .expect(columnSummaryTableSelector.find('tr').count).gt(0)
        }
    )
});