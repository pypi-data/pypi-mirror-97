

import { Selector } from 'testcafe';
import { DELETE_PRESS_KEYS_STRING } from './helpers';
import { getActiveElement } from './selectors';

/* 
    Helper function that returns a selector for a tab with the passed
    tab name.
*/
export const getTabSelector = (tabName: string): Selector => {    
    return Selector('p.tab-sheet-name')
        .withExactText(tabName)
        .parent()
        .parent()
}

/* 
    Opens the tab actions
*/
export const getTabActionSelector = (tabName: string): Selector => {   
    return getTabSelector(tabName).find('svg');
}

const deleteSelector = Selector('div.sheet-tab-action').withExactText('Delete');
const duplicateSelector = Selector('div.sheet-tab-action').withExactText('Duplicate');
const renameSelector = Selector('div.sheet-tab-action').withExactText('Rename');

export async function deleteSheet(t: TestController, dfName: string): Promise<void> {
    await t
        .click(getTabActionSelector(dfName))
        .click(deleteSelector)
}

export async function duplicateSheet(t: TestController, dfName: string): Promise<void> {
    await t
        .click(getTabActionSelector(dfName))
        .click(duplicateSelector)
}

export async function renameSheet(t: TestController, oldDfName: string, newDfName: string): Promise<void> {
    await t
        .click(getTabActionSelector(oldDfName))
        .click(renameSelector)
        .pressKey(DELETE_PRESS_KEYS_STRING)
        .typeText(getActiveElement(), newDfName)
        .pressKey('enter')
}
