// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';


import '../../../../css/documentation-basic-example.css';


/*
    Returns a documentation entry telling a user how to 
    write their first formula!
*/
const FirstFormulaExampleContent = (): JSX.Element => {
    return (        
        <React.Fragment>
            <div className='documentation-basic-example-title'>
                Writing your first formula
            </div>
            <p>
                Mito allows you to write Excel-like formulas to transform your data. 
            </p>
            <div className='documentation-basic-example-section-title'>
                Instructions
            </div>
            <ol className='documentation-basic-example-instructions-list'>
                <li className='documentation-basic-example-instructions-list-element'>
                    <div>
                        1.
                    </div>
                    <div className='documentation-basic-example-instructions-list-element-content'>
                        Click the Add Column button in the Mito toolbar to create an empty column on the right of the sheet.
                        <svg className='documentation-basic-example-instructions-list-element-content-centered' width="22" height="30" viewBox="0 0 8 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M6.45459 1V2.81818" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                            <path d="M7.36365 1.90909L5.54547 1.90909" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                            <path d="M6.45455 4.18182V6.90909V10.5455C6.45455 10.7965 6.25104 11 6 11H1.45455C1.20351 11 1 10.7965 1 10.5455V1.45455C1 1.20351 1.20351 1 1.45455 1H4.8961" stroke="#343434" strokeWidth="0.7"/>
                            <rect x="1" y="4.63635" width="5.45455" height="3.63636" fill="#343434" fillOpacity="0.19"/>
                        </svg>
                    </div>
                </li>
                <li className='documentation-basic-example-instructions-list-element'>
                    <div>
                        2.
                    </div>
                    <div className='documentation-basic-example-instructions-list-element-content'>
                        Double click on a cell in the new column and write a basic formula:
                        <div className='documentation-basic-example-instructions-list-element-content-centered'>
                            =4 + 5
                        </div>
                    </div>
                </li>
                <li className='documentation-basic-example-instructions-list-element'>
                    <div>
                        3.
                    </div>
                    <div className='documentation-basic-example-instructions-list-element-content'>
                        Double click the cell again. Enter the formula:
                        <div className='documentation-basic-example-instructions-list-element-content-centered mb-1'>
                            =LEFT(FirstColumn)
                        </div>
                        Replace FirstColumn with the name of the first column in your data. The column will update with the first characters from the first column!
                    </div>
                </li>
                <li className='documentation-basic-example-instructions-list-element'>
                    <div>
                        4.
                    </div>
                    <div className='documentation-basic-example-instructions-list-element-content'>
                        To see a full list of the functions available, click the back arrow at the top of this taskpane and scroll down!
                    </div>
                </li>
            </ol>
        </React.Fragment>
    );    
};

export default FirstFormulaExampleContent;