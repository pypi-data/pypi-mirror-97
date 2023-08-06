// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

import '../../../../css/function-documentation.css'
import '../../../../css/margins.css';

import { functionDocumentationObjects } from '../../../data/function_documentation';

/*
    Returns content for the documentation taskpane that includes documentation
    for a specific function!
*/
const FunctionDocumentationContent = 
    (props: {
        function: string;
    }): JSX.Element => {

        const funcDocObject = functionDocumentationObjects.find((funcDocObject) => {
            return funcDocObject.function === props.function
        });

        return (        
            <React.Fragment>
                <h1 className='function-documentation-function-name'>
                    {funcDocObject?.function}
                </h1>
                <p>
                    {funcDocObject?.description}
                </p>
                <h2 className='mb-0'>
                Examples
                </h2>
                <ul className='function-documentation-example-list blue-text'>
                    {funcDocObject?.examples?.map((example) => {
                        return <li className='function-documentation-example' key={example}>{example}</li>
                    })}
                </ul>
                <h2 className='mb-0'>
                Syntax
                </h2>
                <p className='blue-text'>
                    {funcDocObject?.syntax}
                </p>
                <ul>
                    {funcDocObject?.syntax_elements?.map((syntax_element) => {
                        return (
                            <li key={syntax_element.element}>
                                <p className='blue-text'>{syntax_element.element}</p>
                                {syntax_element.description}
                            </li>
                        )
                    })}
                </ul>
            </React.Fragment>
        );    
    };

export default FunctionDocumentationContent;