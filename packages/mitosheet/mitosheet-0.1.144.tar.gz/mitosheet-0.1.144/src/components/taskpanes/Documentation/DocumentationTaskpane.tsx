// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState } from 'react';
import { TaskpaneInfo, TaskpaneType } from '../taskpanes';

// Import the content this displays
import FunctionDocumentationContent from './FunctionDocumentationContent';
import DocumentationListContent from './DocumentationListContent';
import BasicExampleContainer from './BasicExampleContainer';

// Import css
import "../../../../css/margins.css"
import { MitoAPI } from '../../../api';

type BasicDocumentation = {
    kind: 'basic';
    basicExampleName: string;
}

type FunctionDocumentation = {
    kind: 'function';
    function: string;
}

export type SelectedDocumentation = BasicDocumentation | FunctionDocumentation | undefined;

/*
    This object holds the documentation taskpane, as well as the
    state currently displayed by the documentation. 

    This can either be:
    1. A list of all content (when selectedDocumentation is undefined)
    2. Documentation for a specific function (when typeof selectedDocumentation is FunctionDocumentation)
    3. Documentation for some basic example (when typeof selectedDocumentation is BasicDocumentation)
*/
const DocumentationTaskpane = (
    props: {
        setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void,
        mitoAPI: MitoAPI
    }): JSX.Element => {
    const [selectedDocumentation, setSelectedDocumentation] = useState<SelectedDocumentation>(undefined);

    const getSelectedDocumentationContent = () => {
        // Returns the selected documentation, which is either nothing (the list of all documentation), 
        // a basic example, or a specific function.

        if (selectedDocumentation === undefined) {
            return (
                <DocumentationListContent 
                    setSelectedDocumentation={setSelectedDocumentation}
                    mitoAPI={props.mitoAPI}
                />
            )
        } else if (selectedDocumentation.kind === 'basic') {
            return <BasicExampleContainer basicExampleName={selectedDocumentation.basicExampleName}/>
        } else if (selectedDocumentation.kind === 'function') {
            return (<FunctionDocumentationContent function={selectedDocumentation.function}/>)
        }
    }

    return (
        <div className='default-taskpane-div'>
            <div className='default-taskpane-header-div'>
                {
                    selectedDocumentation === undefined &&
                    <div className='default-taskpane-header-text'>
                        Documentation
                    </div>
                }
                {
                    selectedDocumentation !== undefined &&
                    <div className='documentation-taskpane-header-back-and-title'>
                        <div className='documentation-taskpane-header-back' onClick={() => {setSelectedDocumentation(undefined)}}>
                            <svg width="12" height="16" viewBox="0 0 12 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M0.292893 7.29289C-0.0976311 7.68342 -0.0976311 8.31658 0.292893 8.70711L6.65685 15.0711C7.04738 15.4616 7.68054 15.4616 8.07107 15.0711C8.46159 14.6805 8.46159 14.0474 8.07107 13.6569L2.41421 8L8.07107 2.34315C8.46159 1.95262 8.46159 1.31946 8.07107 0.928932C7.68054 0.538408 7.04738 0.538408 6.65685 0.928932L0.292893 7.29289ZM12 7L1 7V9L12 9V7Z" fill="#343434"/>
                            </svg>
                        </div>
                        <div className='default-taskpane-header-text'>
                            Documentation
                        </div>
                    </div>
                }
                <div className='default-taskpane-header-exit-button-div' onClick={() => props.setCurrOpenTaskpane({type: TaskpaneType.NONE})}>
                    <svg width="18" height="18" viewBox="0 0 13 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <line x1="0.707107" y1="1.29289" x2="11.3136" y2="11.8994" stroke="#343434" strokeWidth="2"/>
                        <line x1="0.7072" y1="11.8995" x2="11.3137" y2="1.29297" stroke="#343434" strokeWidth="2"/>
                    </svg>
                </div>
            </div>
            <div className='default-taskpane-body-div'>
                {getSelectedDocumentationContent()}
            </div>
        </div>
    )
};

export default DocumentationTaskpane;