// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { FunctionDocumentationObject } from '../../data/function_documentation';

import '../../../css/documentation-box.css'


/*
  The documentation box displays instructions on how to use
  a function beneath the cell editor.
*/
const DocumentationBox = (
    props: {
        funcDocObject: FunctionDocumentationObject
    }): JSX.Element => {
    const examples = props.funcDocObject.examples?.map((example) => {
        return (
            <div className='documentation-box-example' key={example}>
                {example}
            </div>
        )
    })

    return (
        <div className='documentation-box-container'>
            <div className='documentation-box-syntax'>
                {props.funcDocObject.syntax}
            </div>
            <div className='documentation-box-description'>
                {props.funcDocObject.description}
            </div>
            <div className='documentation-box-example-header'>
        Examples
            </div>
            {examples}      
        </div>
    )    
};

export default DocumentationBox;