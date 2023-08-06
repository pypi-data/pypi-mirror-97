// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains helper functions for filter tests
*/

import { Selector } from "testcafe";
import { getColumnHeaderFilterSelector } from "./columnHelpers";
import { DELETE_PRESS_KEYS_STRING } from "./helpers";


export const addFilterSelectSelector = Selector('select.filter-add-filter-button')
export const addFilterSelector = addFilterSelectSelector
    .find('option')
    .withExactText('+ Add a Filter')
export const addFilterGroupSelector = addFilterSelectSelector
    .find('option')
    .withExactText('+ Add a group of filters')

export const filterGroupSelector = Selector('div.filter-group')
export const filterGroupAddFilterSelector = filterGroupSelector
    .find('div.filter-add-filter-button')

export const filterConditionSelector = Selector('select.filter-condition')
export const filterConditionOptionSelector = filterConditionSelector
    .find('option')
export const filterValueInputSelector = Selector('input.filter-value')
export const operatorSelector = Selector('select.filter-operator')
export const operatorOptionSelector = operatorSelector.find('option')

export const firstDeleteFilterSelector = Selector('div.filter-close-button')

export type FilterType = {
    filterCondition: string,
    filterValue?: string 
}

export type FilterGroupType = {
    'filters': FilterType[]; 
    operator: 'And' | 'Or'
}

/* A list of either filters or filter groups*/
export type FilterListType = (FilterType | FilterGroupType)[]

/*
    Applies the given filters to a column. Notably, deletes all other filters that may be on 
    the column at that time to apply these filters!
*/
export async function applyFiltersToColumn(
        t: TestController, 
        columnHeader: string, 
        filters: FilterListType,
        operator?: 'Or' | 'And'
    ): Promise<void> {

    // Open the filter modal
    await t.click(getColumnHeaderFilterSelector(columnHeader))

    const numFilters = await Selector('div.filter-close-button').count;

    // Delete all existing filters
    for (let i = 0; i < numFilters; i++) {
        await t.click(Selector('div.filter-close-button'))
    }

    let filterNumber = 0;
    let filterGroupNumber = 0;

    for (let i = 0; i < filters.length; i++) {
        // Do something different, depending if it is a normal filter or a group
        let filterOrGroup = filters[i];
        if ((filterOrGroup as FilterGroupType).filters !== undefined) {
            const filterGroup = <FilterGroupType>filterOrGroup;

            await t
                .click(addFilterSelectSelector)
                .click(addFilterGroupSelector)

            const specificFilterGroupSelector = filterGroupSelector
                .nth(filterGroupNumber)

            const groupOperatorSelector = specificFilterGroupSelector
                .find('select.filter-operator')
            const groupOperatorOptionSelector = groupOperatorSelector
                .find('option')
            const groupOperator = filterGroup.operator;
            
            for (let j = 0; j < filterGroup.filters.length; j++) {
                const groupFilterConditionSelector = specificFilterGroupSelector
                    .find('select.filter-condition')
                    .nth(j)
                const groupFilterConditionOptionSelector = specificFilterGroupSelector
                    .find('option')
                const groupFilterInputSelector = specificFilterGroupSelector
                    .find('input.filter-value')
                    .nth(j)

                if (j > 0) {
                    // If we're not on the the first filter, we add more filters
                    const addFilterInGroupSelector = specificFilterGroupSelector
                        .find('div.filter-add-filter-button')

                    await t.click(addFilterInGroupSelector)
                }

                const filterCondition = filterGroup.filters[j].filterCondition;
                const filterValue = filterGroup.filters[j].filterValue;
    
                await t
                    .click(groupFilterConditionSelector)
                    .click(groupFilterConditionOptionSelector.withExactText(filterCondition).nth(j))
                    
                if (filterValue !== undefined) {
                    await t
                        .click(groupFilterInputSelector)
                        .pressKey(DELETE_PRESS_KEYS_STRING)
                        .typeText(groupFilterInputSelector, filterValue)
                }

                filterNumber++;
            }

            // If there is an operator, and it makes sense to apply it, we apply it
            if (groupOperator !== undefined && filterGroup.filters.length > 1) {
                await t
                    .click(groupOperatorSelector)
                    .click(groupOperatorOptionSelector.withExactText(groupOperator));
            }

            filterGroupNumber++;
        } else {
            const filter = <FilterType>filterOrGroup;

            await t
                .click(addFilterSelectSelector)
                .click(addFilterSelector)

            const filterCondition = filter.filterCondition;
            const filterValue = filter.filterValue;

            await t
                .click(filterConditionSelector.nth(filterNumber))
                .click(filterConditionOptionSelector.withExactText(filterCondition).nth(filterNumber))
                
            if (filterValue !== undefined) {
                await t
                    .click(filterValueInputSelector.nth(filterNumber))
                    .pressKey(DELETE_PRESS_KEYS_STRING)
                    .typeText(filterValueInputSelector.nth(filterNumber), filterValue)
            }

            filterNumber++;
        }
    }

    // If there is an operator, and it makes sense to apply it, we apply it
    if (operator !== undefined) {
        let outterOperator = Selector('div.filter-modal-centering-container')
            .child('div.filter-object')
            .child('select.filter-operator')
        if (filterGroupNumber > 0) {
            outterOperator = Selector('div.filter-modal-centering-container')
                .child('div.filter-group-and-operator-div')
                .child('div.filter-operator')
                .child('select.filter-operator')
        }
        
        await t
            .click(outterOperator)
            .click(outterOperator.find('option').withExactText(operator));
    }
}

export async function deleteFirstFilter(t: TestController) {
    await t.click(firstDeleteFilterSelector)
}