// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

import '../../../../css/documentation-taskpane.css';

const listIcon = (
    <svg width="16" height="18" viewBox="0 0 16 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <mask id="path-1-inside-1" fill="white">
            <rect width="16" height="18" rx="1"/>
        </mask>
        <rect width="16" height="18" rx="1" stroke="#0081DE" strokeWidth="2.4" mask="url(#path-1-inside-1)"/>
        <line x1="2" y1="3.2" x2="14" y2="3.2" stroke="#0081DE" strokeWidth="1.2"/>
        <line x1="2" y1="7" x2="14" y2="7" stroke="#0081DE" strokeWidth="1.2"/>
        <line x1="2" y1="10.8" x2="14" y2="10.8" stroke="#0081DE" strokeWidth="1.2"/>
        <line x1="2" y1="14.6" x2="14" y2="14.6" stroke="#0081DE" strokeWidth="1.2"/>
    </svg>
)

import { SelectedDocumentation } from './DocumentationTaskpane';
import { functionDocumentationObjects } from '../../../data/function_documentation';
import { basicExamples } from './BasicExampleContainer';
import { MitoAPI } from '../../../api';


/*
    This documentation taskpane content displays a list of all 
    documentation entries users can select. 

    These are either:
    1. Basic examples (e.g. how to write a formula)
    2. Function documentations
*/
const DocumentationListContent = (
    props: {
        setSelectedDocumentation: React.Dispatch<React.SetStateAction<SelectedDocumentation>>,
        mitoAPI: MitoAPI
    }): JSX.Element => {

    const basicExamplesList = basicExamples.map((basicExample) => {
        return (
            <li 
                className='documentation-taskpane-content-function-list-element'
                key={basicExample.basicExampleName} 
                onClick={() => {
                    // Log the selection of the basic documentation
                    // NOTE: we don't need to wait on this promise, as we don't care when
                    // it finishes
                    void props.mitoAPI.sendLogMessage(
                        'documentation_log_event',
                        {
                            kind: 'basic',
                            function: basicExample.basicExampleName
                        }
                    );
                    
                    // Set the documentation element
                    props.setSelectedDocumentation({
                        kind: 'basic',
                        basicExampleName: basicExample.basicExampleName
                    })
                }}>
                <div className='documentation-taskpane-content-function-list-icon'>
                    {listIcon}
                </div>
                {basicExample.basicExampleName}
            </li>
        )
    })

    const functionNameList = functionDocumentationObjects.map((funcDocObject) => {
        return (
            <li 
                className='documentation-taskpane-content-function-list-element'
                key={funcDocObject.function} 
                onClick={() => {
                    // Log they selected this function
                    // NOTE: we don't need to wait on this promise, as we don't care
                    // when it finishes
                    void props.mitoAPI.sendLogMessage(
                        'documentation_log_event',
                        {
                            kind: 'function',
                            function: funcDocObject.function
                        }
                    );
                
                    // Set the documentation
                    props.setSelectedDocumentation({
                        kind: 'function',
                        function: funcDocObject.function
                    });
                }}>
                <div className='documentation-taskpane-content-function-list-icon'>
                    {listIcon}
                </div>
                {funcDocObject.function}
            </li>
        )
    })

    return (
        <React.Fragment>
            <div className='documentation-taskpane-content-function-list-title'>
                Basic Examples
            </div>
            <ul className='documentation-taskpane-content-function-list'>
                {basicExamplesList}
            </ul>
            <div className='documentation-taskpane-content-function-list-section-title'>
                Functions
            </div>
            <ul className='documentation-taskpane-content-function-list'>
                {functionNameList}
            </ul>
        </React.Fragment>
    ) 
};

export default DocumentationListContent;