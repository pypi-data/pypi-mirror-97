// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for IntroductionTour
*/

import {
    checkSheets,
    createNotebookRunCell,
    deleteAllNotebooks,
} from './utils/helpers';

import {
    doSimpleImport
} from './utils/importHelpers';

const code = `
import pandas as pd
import mitosheet

df1 = pd.DataFrame(data={'A': [1, 2, 3], 'B': [4, 5, 6]})
df1.to_csv("df1.csv", index=False)

mitosheet.sheet(tutorial_mode=True)
`
import { CURRENT_URL } from './config';
import { JoyRideNextButton, JoyRideCloseButton, JoyRideLastButton } from './utils/joyRideTourHelpers';

fixture `Test Introduction Tour`
    .page(CURRENT_URL)
    .beforeEach( async t => {
        await createNotebookRunCell(t, true, code);
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Can go through the tutorial', async t => {
    await t.wait(1000) // wait 1 second

    await t.click(JoyRideNextButton)

    // do import
    await doSimpleImport(t, ['df1.csv'])

    await t.click(JoyRideLastButton)

    // Expect the tour to be closed
    await t.expect(JoyRideNextButton.exists).notOk()

    await checkSheets(t, {
        'df1_csv': {
            'A': ['1', '2', '3'],
            'B': ['4', '5', '6']
        }
    })
});

test('Can use the close button in the tutorial', async t => {
    await t.wait(1000) // wait 1 second

    await t.click(JoyRideCloseButton)

    // Expect the tour to be closed
    await t.expect(JoyRideCloseButton.exists).notOk()
});


