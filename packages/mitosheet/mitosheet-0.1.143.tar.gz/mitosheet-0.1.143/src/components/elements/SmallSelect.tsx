// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';

import '../../../css/small-select.css';

/* 
  A custom select dropdown component created for use in the default taskpane
*/

export enum TitleColor {
    BLUE = '#0081DE',
    DARK = '#343434'
}

const SmallSelect = (props: {
    startingValue: string
    optionsArray: string[];
    setValue: (value: string) => void;
    titleColor: TitleColor
}): JSX.Element => {

    const optionsElements: JSX.Element[] = []
    props.optionsArray.forEach(option => {
        optionsElements.push((<option value={option} key={option}>{option}</option>))
    });
    
    /*  
        NOTE: because the starting value is not selectable, make sure if its an actual 
        option that you want to be selected by default that you elsewhere set the startingValue
        to be selected. 

        we use this because in the pivot table screen, we want to be able to have the select dropdown
        default to the title 'add' which is not an aggregation method so should not be able to be clicked.
    */ 
    return (
        <Fragment>
            <select className='small-select' value={props.startingValue} style={{color: props.titleColor}} onChange={(e) => props.setValue(e.target.value)}>
                <option selected hidden>{props.startingValue}</option>
                {optionsElements}
            </select>
        </Fragment>
    )
}

export default SmallSelect
