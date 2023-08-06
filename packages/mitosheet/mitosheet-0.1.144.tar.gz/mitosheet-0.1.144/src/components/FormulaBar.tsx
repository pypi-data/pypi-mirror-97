// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { MouseEvent } from 'react';

// Import css
import "../../css/formula-bar.css";
import "../../css/widths.css"

const FormulaBar = (props: {
    formulaBarValue: string, 
    handleFormulaBarDoubleClick: (e: MouseEvent<HTMLButtonElement>) => void
}): JSX.Element => {

    return(
        <div className="vertical-align-content formula-bar-container">
            <div className="formula-bar">
                <p className="fx-text">Fx</p>
                <div className="vertical-line"></div>
                <button className="formula-bar-input w-100p" onDoubleClick={props.handleFormulaBarDoubleClick}>
                    {props.formulaBarValue} 
                </button>
            </div>
        </div>
    )
}

export default FormulaBar
