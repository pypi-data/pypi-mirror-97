// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/
import { 
    checkColumn,
    checkSheet,
    DELETE_PRESS_KEYS_STRING,
    tryTest
} from '../utils/helpers';

import {    
    addFilterSelectSelector, addFilterSelector, filterConditionOptionSelector, filterConditionSelector, filterValueInputSelector,
    applyFiltersToColumn,
    deleteFirstFilter,
    filterGroupSelector,
} from '../utils/filterHelpers';

import { CURRENT_URL } from '../config';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';
import { getColumnHeaderFilterSelector } from '../utils/columnHelpers';
import { modalSelector } from '../utils/allModals';
import { taskpaneCloseButton } from '../utils/selectors';

fixture `Test Filter`
    .page(CURRENT_URL)

const code = `import pandas as pd
import mitosheet
df1 = pd.DataFrame(data={'A': ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9'], 'B': [123, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9], 'C': [123, '1', '2', '3', 4, 5, 5, 6, 7, 8, 9], 'Date': ['2001-01-01', '2002-01-01', '2003-01-01','2004-01-01', '2005-01-01', '2006-01-01', '2007-01-01', '2008-01-01', '2009-01-01', '2010-01-01', '2011-01-01']})
df1['Date'] = pd.to_datetime(df1['Date'])
mitosheet.sheet(df1)`

const codeWithNegativeNumbers = `import pandas as pd
import mitosheet
df1 = pd.DataFrame(data={'A': ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9'], 'B': [-123, -1, -2, 3, 4, 5, 5, 6, 7, -8, 9], 'C': [123, '1', '2', '3', 4, 5, 5, 6, 7, 8, 9], 'Date': ['2001-01-01', '2002-01-01', '2003-01-01','2004-01-01', '2005-01-01', '2006-01-01', '2007-01-01', '2008-01-01', '2009-01-01', '2010-01-01', '2011-01-01']})
df1['Date'] = pd.to_datetime(df1['Date'])
mitosheet.sheet(df1)`

// See here: https://devexpress.github.io/testcafe/documentation/recipes/basics/test-select-elements.html
test('Test single filter conditions, string column', async t => {
    await tryTest(
        t,
        code,
        async t => {
            const filterTests = [
                {
                    filterCondition: 'contains',
                    filterValue: '1',
                    columnValues: ['123', '1']
                },
                {
                    filterCondition: 'does not contain',
                    filterValue: '1',
                    columnValues: ['2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
                {
                    filterCondition: 'is exactly',
                    filterValue: '1',
                    columnValues: ['1']
                },
                {
                    filterCondition: 'is empty',
                    filterValue: undefined,
                    columnValues: []
                },
                {
                    filterCondition: 'is not empty',
                    filterValue: undefined,
                    columnValues: ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
            ]

            for (let i = 0; i < filterTests.length; i++) {
                await applyFiltersToColumn(
                    t, 
                    'A', 
                    [{filterCondition: filterTests[i].filterCondition, filterValue: filterTests[i].filterValue}]
                )

                await checkColumn(t, 'A', filterTests[i].columnValues)
            }
        }
    )
});

// See here: https://devexpress.github.io/testcafe/documentation/recipes/basics/test-select-elements.html
test('Test single filter conditions, mixed column', async t => {
    await tryTest(
        t,
        code,
        async t => {
            const filterTests = [
                {
                    filterCondition: 'contains',
                    filterValue: '1',
                    columnValues: ['1']
                },
                {
                    filterCondition: 'does not contain',
                    filterValue: '1',
                    columnValues: ['123', '2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
                {
                    filterCondition: 'is exactly',
                    filterValue: '1',
                    columnValues: ['1']
                },
                {
                    filterCondition: 'is empty',
                    filterValue: undefined,
                    columnValues: []
                },
                {
                    filterCondition: 'is not empty',
                    filterValue: undefined,
                    columnValues: ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
            ]

            for (let i = 0; i < filterTests.length; i++) {
                await applyFiltersToColumn(
                    t, 
                    'C', 
                    [{filterCondition: filterTests[i].filterCondition, filterValue: filterTests[i].filterValue}]
                )

                await checkColumn(t, 'C', filterTests[i].columnValues)
            }
        }
    )
});


test('Test single filter conditions, number column', async t => {
    await tryTest(
        t,
        code,
        async t => {
            
            // See: https://devexpress.github.io/testcafe/documentation/guides/basic-guides/select-page-elements.html#select-elements-that-contain-special-characters
            const filterTests = [
                {
                    filterCondition: '=',
                    filterValue: '1',
                    columnValues: ['1']
                },
                {
                    filterCondition: '\u003E', // https://www.toptal.com/designers/htmlarrows/math/greater-than-sign/
                    filterValue: '1',
                    columnValues: ['123', '2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
                {
                    filterCondition: '\u2265', //https://www.toptal.com/designers/htmlarrows/math/greater-than-or-equal-to/
                    filterValue: '3',
                    columnValues: ['123', '3', '4', '5', '5', '6', '7', '8', '9']
                },
                {
                    filterCondition: '\u003C', //https://www.toptal.com/designers/htmlarrows/math/less-than-sign/
                    filterValue: '3',
                    columnValues: ['1', '2']
                },
                {
                    filterCondition: '\u2264', //https://www.toptal.com/designers/htmlarrows/math/less-than-or-equal-to/
                    filterValue: '5',
                    columnValues: ['1', '2', '3', '4', '5', '5']
                },
                {
                    filterCondition: 'is empty',
                    filterValue: undefined,
                    columnValues: []
                },
                {
                    filterCondition: 'is not empty',
                    filterValue: undefined,
                    columnValues: ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9']
                },
            ]

            for (let i = 0; i < filterTests.length; i++) {
                await applyFiltersToColumn(
                    t, 
                    'B', 
                    [{filterCondition: filterTests[i].filterCondition, filterValue: filterTests[i].filterValue}]
                )

                await checkColumn(t, 'B', filterTests[i].columnValues)
            }
        }
    )
});


test('Test single filter conditions, date column', async t => {
    await tryTest(
        t,
        code,
        async t => {
            
            // See: https://devexpress.github.io/testcafe/documentation/guides/basic-guides/select-page-elements.html#select-elements-that-contain-special-characters
            const filterTests = [
                // NOTE: for date tests, we have to input them in format yyyy-mm-dd, for test cafe. 
                // see more here: https://devexpress.github.io/testcafe/documentation/reference/test-api/testcontroller/typetext.html#typing-into-datetime-color-and-range-inputs
                {
                    filterCondition: '=',
                    filterValue: '2001-01-01',
                    columnValues: ['2001-01-01 00:00:00']
                },
                {
                    filterCondition: '\u003E', // https://www.toptal.com/designers/htmlarrows/math/greater-than-sign/
                    filterValue: '2010-01-01',
                    columnValues: ['2011-01-01 00:00:00']
                },
                {
                    filterCondition: '\u2265', //https://www.toptal.com/designers/htmlarrows/math/greater-than-or-equal-to/
                    filterValue: '2010-01-01',
                    columnValues: ['2010-01-01 00:00:00', '2011-01-01 00:00:00']
                },
                {
                    filterCondition: '\u003C', //https://www.toptal.com/designers/htmlarrows/math/less-than-sign/
                    filterValue: '2002-01-01',
                    columnValues: ['2001-01-01 00:00:00']
                },
                {
                    filterCondition: '\u2264', //https://www.toptal.com/designers/htmlarrows/math/less-than-or-equal-to/
                    filterValue: '2002-01-01',
                    columnValues: ['2001-01-01 00:00:00', '2002-01-01 00:00:00']
                },
                {
                    filterCondition: 'is empty',
                    filterValue: undefined,
                    columnValues: []
                },
                {
                    filterCondition: 'is not empty',
                    filterValue: undefined,
                    columnValues: ['2001-01-01 00:00:00', '2002-01-01 00:00:00', '2003-01-01 00:00:00', '2004-01-01 00:00:00', '2005-01-01 00:00:00', '2006-01-01 00:00:00', '2007-01-01 00:00:00', '2008-01-01 00:00:00', '2009-01-01 00:00:00', '2010-01-01 00:00:00', '2011-01-01 00:00:00']
                },
            ]

            for (let i = 0; i < filterTests.length; i++) {
                await applyFiltersToColumn(
                    t, 
                    'Date', 
                    [{filterCondition: filterTests[i].filterCondition, filterValue: filterTests[i].filterValue}]
                )

                await checkColumn(t, 'Date', filterTests[i].columnValues)
            }
        }
    )
});


test('Test switch between filter conditions doesnt error', async t => {
    await tryTest(
        t,
        code,
        async t => {
            // Open the filter modal
            await t.click(getColumnHeaderFilterSelector('A'))

            await t
                .click(addFilterSelectSelector)
                .click(addFilterSelector)
            
            await t
                .click(filterConditionSelector)
                .click(filterConditionOptionSelector.withExactText('is exactly'))                    
                .click(filterValueInputSelector)
                .pressKey(DELETE_PRESS_KEYS_STRING)
                .typeText(filterValueInputSelector, 'string')
                .click(filterConditionSelector)
                .click(filterConditionOptionSelector.withExactText('is empty'))
                .click(filterConditionSelector)
                .click(filterConditionOptionSelector.withExactText('is exactly'))   
                // Make sure the error modal doesn't pop up
                .expect(modalSelector.exists).notOk()
        }
    )
});


test('Test range filter conditions, number column', async t => {
    await tryTest(
        t,
        "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'A': ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9'], 'B': [123, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9],'C': [123, '1', '2', '3', 4, 5, 5, 6, 7, 8, 9]})\nmitosheet.sheet(df1)",
        async t => {
            await applyFiltersToColumn(
                t, 
                'B', 
                [
                    // Greater than 1, less than 3
                    {filterCondition: '\u003E', filterValue: '1'},
                    {filterCondition: '\u003C', filterValue: '3'},

                ]
            )
            await checkColumn(t, 'B', ['2'])
        }
    )
});

   
test('Test mulitple string contains with OR, string column', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await applyFiltersToColumn(
                t, 
                'A', 
                [
                    {filterCondition: 'contains', filterValue: '1'},
                    {filterCondition: 'contains', filterValue: '3'},
        
                ],
                'Or'
            )
            await checkColumn(t, 'B', ['123', '1', '3'])
        }
    )
});

test('Test saves changed operators', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await applyFiltersToColumn(
                t, 
                'A', 
                [
                    {filterCondition: 'contains', filterValue: '1'},
                    {filterCondition: 'contains', filterValue: '3'},
        
                ],
                'Or'
            )
            await checkColumn(t, 'B', ['123', '1', '3'])
        
            await applyFiltersToColumn(
                t, 
                'A', 
                [
                    {filterCondition: 'contains', filterValue: '1'},
                    {filterCondition: 'contains', filterValue: '4'},
        
                ]
            )
            await checkColumn(t, 'B', ['123', '1', '4']);
        }
    )
});

test('Test allows you to filter out NaNs', async t => {
    await tryTest(
        t,
        "import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={'Name': ['Nate', 'Aaron', None]})\nmitosheet.sheet(df1)",
        async t => {

            await applyFiltersToColumn(
                t, 
                'Name', 
                [
                    {filterCondition: 'is not empty', filterValue: undefined},
                ],
            )
            await checkSheet(t, {
                'Name': ['Nate', 'Aaron']
            })

            const expectedDf = {
                'Name': ['Nate', 'Aaron']
            }

            await checkGeneratedCode(t, 'df1', expectedDf)
        }
    )
});

   
test('allows you to make groups of filters with non-grouped filters', async t => {
    await tryTest(
        t,
        code,
        async t => {

            await applyFiltersToColumn(
                t, 
                'A',
                [
                    {filters: [{filterCondition: 'contains', filterValue: '1'}, {filterCondition: 'contains', filterValue: '3'}], operator: 'And'},
                    {filterCondition: 'contains', filterValue: '4'},
                    {filters: [{filterCondition: 'contains', filterValue: '5'}, {filterCondition: 'contains', filterValue: '5'}], operator: 'And'},
                ],
                'Or'
            )

            await checkColumn(t, 'A', ['123', '4', '5', '5']);
        }
    )
});


test('allows the user to delete filter groups by deleting all filters in a group', async t => {
    await tryTest(
        t,
        code,
        async t => {

            await applyFiltersToColumn(
                t, 
                'A',
                [
                    {filters: [{filterCondition: 'contains', filterValue: '1'}, {filterCondition: 'contains', filterValue: '3'}], operator: 'And'},
                ],
            )

            await checkColumn(t, 'A', ['123']);

            // Delete both filters in filter group
            await deleteFirstFilter(t)
            await deleteFirstFilter(t)

            // Make sure the column is unfiltered
            await checkColumn(t, 'A', ['123', '1', '2', '3', '4', '5', '5', '6', '7', '8', '9']);

            // Make sure the filter group is no longer displayed
            await t.expect(filterGroupSelector.exists).notOk()

        }
    )
});


test('Allows the user to just have a single filter group', async t => {
    await tryTest(
        t,
        code,
        async t => {

            await applyFiltersToColumn(
                t, 
                'A',
                [
                    {filters: [{filterCondition: 'contains', filterValue: '1'}, {filterCondition: 'contains', filterValue: '3'}], operator: 'And'},
                ],
            )

            await checkColumn(t, 'A', ['123']);
        }
    )
});

   
test('saves filter groups properly when the filter modal is closed', async t => {
    await tryTest(
        t,
        code,
        async t => {
            
            await applyFiltersToColumn(
                t, 
                'A',
                [
                    {filters: [{filterCondition: 'contains', filterValue: '1'}, {filterCondition: 'contains', filterValue: '3'}], operator: 'And'},
                ],
            )

            await checkColumn(t, 'A', ['123']);

            await t.click(taskpaneCloseButton);

            // Open the filter modal
            await t.click(getColumnHeaderFilterSelector('A'))
            
            // Expect the filter group to be there
            await t.expect(filterGroupSelector.exists).ok()
        }
    )
});
   

test('simple filter allows negative number', async t => {
    await tryTest(
        t,
        codeWithNegativeNumbers,
        async t => {

            await applyFiltersToColumn(
                t, 
                'B',
                [
                    // less than -2.5
                    {filters: [{filterCondition: '\u003C', filterValue: '-2.5'}], operator: 'And'},
                ],
            )

            await checkColumn(t, 'B', ['-123', '-8']);
        }
    )
});

   
test('simple filter allows decimal', async t => {
    await tryTest(
        t,
        codeWithNegativeNumbers,
        async t => {
            await applyFiltersToColumn(
                t, 
                'B',
                [
                    // Less than 1.05, or greater than 9.05
                    {filterCondition: '\u003C', filterValue: '1.05'},
                    {filters: [{filterCondition: '\u003E', filterValue: '9.05'}], operator: 'And'},
                ],
                'Or'
            )

            await checkColumn(t, 'B', ['-123', '-1', '-2', '-8']);

        }
    )
});
   