// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
Contains useful selectors and helpers for adding a new column (and setting it's formula).
*/

import { Selector } from "testcafe";
import { DELETE_PRESS_KEYS_STRING } from "./helpers";
import { getActiveElement, getCellSelector } from "./selectors";

export const stepHistoryButton = Selector('div')
    .withExactText('Step History')
    .parent()


export const fastForwardButton = Selector('div')
    .withExactText('Fast forward to apply all steps')
    .parent()

export const topLeftPopup = Selector('div.top-left-popup-container')


export const rewindToStep = async (t: TestController, index: number): Promise<void> => {
    await t
        .click(stepHistoryButton)
        .click(Selector('div.step-taskpane-step-container-left').nth(index))
}