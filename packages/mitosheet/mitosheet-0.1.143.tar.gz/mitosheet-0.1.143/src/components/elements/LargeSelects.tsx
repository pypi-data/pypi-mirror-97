// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';

import LargeSelect from './LargeSelect';
import '../../../css/large-select.css';

/* 
  An element that allows you to create mulitple large selects, all with the same options
  and the same starting value.
*/
const LargeSelects = (props: {
    numSelects: number,
    startingValue: string | undefined,
    optionsArray: string[],
    setValue: (index: number, value: string) => void,
    extraLarge?: boolean;
}): JSX.Element => {

    const largeSelects = [];
    for (let i = 0; i < props.numSelects; i++) {
        largeSelects.push((
            <LargeSelect
                key={i}
                startingValue={props.startingValue}
                optionsArray={props.optionsArray}
                setValue={(value) => {props.setValue(i, value)}}
                extraLarge={props.extraLarge}
            />
        ))
    }

    return (
        <Fragment>
            {largeSelects}
        </Fragment>
    )
}

export default LargeSelects
