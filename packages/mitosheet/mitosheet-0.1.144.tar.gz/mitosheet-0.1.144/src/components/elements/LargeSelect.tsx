// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';

import '../../../css/large-select.css';

/* 
  A custom select dropdown component created for use in the default taskpane
  The Large Select element is wider than the Small Select element
*/
const LargeSelect = (props: {
    startingValue: string | undefined;
    // For options, you can either pass a set of strings, or you can pass a list of JSX options
    optionsArray: string[] | JSX.Element[];
    setValue: (value: string) => void;
    extraLarge?: boolean;
}): JSX.Element => {

    const optionsElements: JSX.Element[] = []
    props.optionsArray.forEach((option: string | JSX.Element) => {
        if (typeof option === 'string') {
            optionsElements.push((<option value={option} key={option}>{option}</option>));
        } else {
            optionsElements.push(option);
        }
    })

    const className = !props.extraLarge ? 'select large-select' : 'select extra-large-select';

    return (
        <Fragment>
            <select className={className} value={props.startingValue} onChange={(e) => props.setValue(e.target.value)}>
                {optionsElements}
            </select>
        </Fragment>
    )
}

export default LargeSelect
