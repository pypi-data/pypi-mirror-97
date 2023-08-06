// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all the selectors used across Mito frontend tests. 
*/

import { Selector} from 'testcafe';

// PURE JUPYTER SELECTORS

export const mainPanel = Selector('#jp-main-content-panel')

export const fileTab = Selector('#jp-MainMenu')
    .child('ul')
    .child('li')
    .child('div')
    .withText('File');

export const fileTabNew = Selector('div.lm-Menu-itemLabel')
    .withText('New');

export const fileTabCloseAllTabs = Selector('div.lm-Menu-itemLabel')
    .withText('New');

export const fileTabNewNotebook = Selector('div.lm-Menu-itemLabel')
    .withExactText('Notebook');

export const selectKernelButton = Selector('div.jp-Dialog-buttonLabel')
    .withExactText('Select');

// MITO SELECTORS

export const mito = Selector('div.mitosheet');

export const mitoToolbarContainerLeft = Selector('div.mito-toolbar-container-left')


// TODO: this does not need to be a function
export const getFormulaBarSelector = (): Selector => {
    return Selector('button.formula-bar-input');
}

// MITO TOOLBAR BUTTONS (NOTE: note all of these have been tested)

export const undoButton = Selector('div')
    .withExactText('Undo')
    .parent()

export const deleteColumnButton = Selector('div')
    .withExactText('Delete Column')
    .parent()

export const groupButton = Selector('div')
    .withExactText('Group')
    .parent()

export const downloadSheetButton = Selector('div')
    .withExactText('Download Sheet')
    .parent()

export const documentationButton = Selector('div')
    .withExactText('Documentation')
    .parent()

export const fullScreenButton = Selector('div')
    .withExactText('Full Screen')
    .parent()

export const closeFullScreenButton = Selector('div')
    .withExactText('Close Full Screen')
    .parent()

// DOCUMENTATION INTERACTION SELECTORS

export const documentationTaskpaneSelector = Selector('div.default-taskpane-div');

export const documentationTaskpaneFunctionSelector = Selector('li.documentation-taskpane-content-function-list-element');

export const documentationTaskpaneBackButton = Selector('div.documentation-taskpane-header-back');

export const taskpaneCloseButton = Selector('div.default-taskpane-header-exit-button-div');

// MODAL INTERACTION SELECTORS

/* 
    Helper function that returns a selector for the cell at columnHeader, row
*/
export const getCellSelector = (columnHeader: string, row: string): Selector => {    
    return Selector('div.ag-row')
        .withAttribute('row-index', row)
        .child('div')
        .withAttribute('col-id', columnHeader)
}

// CHANGE COLUMN HEADER MODAL
export const columnHeaderChangeErrorSelector = Selector('p.taskpane-error-message');

// ERROR MODAL
export const errorMessageSelector = Selector('div.modal-message')
    .child('div')
    .nth(0)


// SORT MODAL
export const ascendingSortSelector = Selector('button.sort-button').withText('Ascending')
export const descendingSortSelector = Selector('button.sort-button').withText('Descending')

// SIGNUP MODAL
export const signupInputSelector = Selector('input.modal-input')

// MISC SELECTORS
export const getActiveElement = Selector(() => {
    return document.activeElement
});
