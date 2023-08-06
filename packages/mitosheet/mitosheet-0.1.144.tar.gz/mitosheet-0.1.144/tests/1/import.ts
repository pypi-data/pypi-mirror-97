// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for importing data.
*/


import {
    checkSheets,
    tryTest,
    fillCurrentNotebook,
    deleteAllNotebooks,
    createNotebookRunCell
} from '../utils/helpers';

import {
    doRawPythonImport,
    doSimpleImport
} from '../utils/importHelpers';
import { repeatAnalysis, repeatAnalysisChangeImports } from '../utils/repeatAnalysisHelpers';
import { saveAnalysis } from '../utils/saveAnalysisHelpers';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';


const code = `
import pandas as pd
import mitosheet

df1 = pd.DataFrame(data={'A': [1, 2, 3], 'B': [4, 5, 6]})
df1.to_csv("df1.csv", index=False)

df2 = pd.DataFrame(data={'A': [7, 8, 9], 'B': [10, 11, 12]})
df2.to_csv("df2.csv", index=False)

mitosheet.sheet()
`
import { CURRENT_URL } from '../config';

fixture `Test Import`
    .page(CURRENT_URL)

test('Can do a simple import', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await doSimpleImport(t, ['df1.csv', 'df2.csv'])
            await checkSheets(t, {
                'df1_csv': {
                    'A': ['1', '2', '3'],
                    'B': ['4', '5', '6']
                },
                'df2_csv': {
                    'A': ['7', '8', '9'],
                    'B': ['10', '11', '12']
                }
            })
        }
    )
});

test('Can save a simple import, prompted to change dataframes', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await doSimpleImport(t, ['df1.csv', 'df2.csv'])
            const analysisName = await saveAnalysis(t);

            // Reset the notebook
            await deleteAllNotebooks(t);
            await createNotebookRunCell(t, false, code);

            await repeatAnalysis(t, analysisName);
            await repeatAnalysisChangeImports(t, {file_names: ['df1.csv', 'df1.csv']});
            await checkSheets(t, {
                'df1_csv': {
                    'A': ['1', '2', '3'],
                    'B': ['4', '5', '6']
                },
                'df1_csv_0': {
                    'A': ['1', '2', '3'],
                    'B': ['4', '5', '6']
                }
            })
        }
    )
});

test('Can do a raw Python import', async t => {
    await tryTest(
        t,
        code,
        async t => {
            const pythonCode = `import pandas as pd\ndf = pd.DataFrame({'A': [1, 2, 3]})\ndf1 = pd.DataFrame({'A': [4, 5, 6]})`
            await doRawPythonImport(t, pythonCode, 'df, df1')
            await checkSheets(t, {
                'df': {
                    'A': ['1', '2', '3'],
                },
                'df1': {
                    'A': ['4', '5', '6'],
                }
            })
        }
    )
});

test('Can save a raw Python import, prompted to change code', async t => {
    await tryTest(
        t,
        code,
        async t => {
            const pythonCode = `import pandas as pd\ndf = pd.DataFrame({'A': [1, 2, 3]})\ndf1 = pd.DataFrame({'A': [4, 5, 6]})`;
            await doRawPythonImport(t, pythonCode, 'df, df1');
            const analysisName = await saveAnalysis(t);

            // Reset the notebook
            await fillCurrentNotebook(t, code);

            await repeatAnalysis(t, analysisName);
            const newPythonCode = `import pandas as pd\ndf2 = pd.DataFrame({'A': [1, 2, 3]})\ndf3 = pd.DataFrame({'A': [4, 5, 6]})`;
            await repeatAnalysisChangeImports(t, {rawPythonImports: [{pythonCode: newPythonCode, dfNamesString: 'df2, df3'}]});
            await checkSheets(t, {
                'df2': {
                    'A': ['1', '2', '3'],
                },
                'df3': {
                    'A': ['4', '5', '6'],
                }
            })

            const expectedDf2 = {
                'A': ['1', '2', '3'],
            }

            await checkGeneratedCode(t, 'df2', expectedDf2)
        }
    )
});