// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all useful selectors and helpers for saving an analysis.
*/

import { Selector } from 'testcafe';
import { modalAdvanceButtonSelector, modalInput } from './allModals';

export const saveButton = Selector('div')
    .withExactText('Save')
    .parent()

/*
    Saves an analysis with the given name. Fails if there is an analysis with this name already.
*/
export async function saveAnalysis(t: TestController, analysisName?: string): Promise<string> {
    if (analysisName === undefined) {
        analysisName = '_' + Math.random().toString(36).substr(2, 9);
    }

    await t
        .click(saveButton)
        .typeText(modalInput, analysisName)
        .click(modalAdvanceButtonSelector)

    return analysisName
}
