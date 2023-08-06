// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.
import React from 'react';

import CallMitoSheetExampleContent from './CallMitoSheetExampleContent';
import FirstFormulaExampleContent from './FirstFormulaExampleContent';

export const basicExamples = [
    {
        basicExampleName: 'Basic Mitosheet Python Example',
        content: CallMitoSheetExampleContent
    },
    {
        basicExampleName: 'Writing your first formula',
        content: FirstFormulaExampleContent
    }
]

/*
    This container displays a single basic example, depending on
    what it is told to display!
*/
const BasicExampleContainer = (props: {basicExampleName: string}): JSX.Element => {

    const basicExample = basicExamples.find((basicExample) => {
        return basicExample.basicExampleName == props.basicExampleName;
    })

    return (        
        <React.Fragment>
            {basicExample?.content()}
        </React.Fragment>
    );    
};

export default BasicExampleContainer;




