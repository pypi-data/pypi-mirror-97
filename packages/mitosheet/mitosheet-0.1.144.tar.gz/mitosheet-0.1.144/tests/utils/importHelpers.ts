// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all useful selectors and helpers for interacting with the import modals. 
*/

import { Selector } from 'testcafe';

import { modalAddSelector, modalAdvanceButtonSelector } from './allModals';

// Toolbar Button
export const importButton = Selector('div')
    .withExactText('Import Data')
    .parent()

// Which sort of import do you want to do?
export const importMethodSelect = Selector('select.select')
    .nth(0)
export const importMethodSelectOption = importMethodSelect
    .find('option')

// Simple Import Selectors
export const simpleImportSelect = Selector('select.select')
export const simpleImportSelectOption = Selector('select.select')
    .find('option')

// Raw Python Import Selectors
export const rawPythonCodeblockSelector = Selector('textarea.raw-python-textarea')
export const dfNamesStringSelector = Selector('input.modal-input')

/*
    Does a simple import, importing the passed file_names
*/
export async function doSimpleImport(t: TestController, file_names: string[]): Promise<void> {
    
    await t
        .click(importButton)
        // We wait here, because data has to be gotten from the API, and sometimes
        // when we move to quick this causes issues. I found it impossible to move
        // this quick in practice. 
        .wait(500)

    // Add space for all of these files
    for (let i = 0; i < file_names.length; i++) {
        await t.click(modalAddSelector);
    }

    // And then go and actually set the files
    for (let i = 0; i < file_names.length; i++) {
        await t
            .click(simpleImportSelect.nth(i + 1)) // increment by 1, as the import type also is a selector
            .click(simpleImportSelectOption.withExactText(file_names[i]).nth(i))
    }

    await t.click(modalAdvanceButtonSelector);
}

/*
    Does a raw python, with the given pythonCode and dfNamesString
*/
export async function doRawPythonImport(t: TestController, pythonCode: string, dfNamesString: string): Promise<void> {
    
    await t
        .click(importButton)
        .click(importMethodSelect)
        .click(importMethodSelectOption.withExactText('Raw Python Import'))
        .typeText(rawPythonCodeblockSelector, pythonCode)
        .typeText(dfNamesStringSelector, dfNamesString)

    await t.click(modalAdvanceButtonSelector);
}