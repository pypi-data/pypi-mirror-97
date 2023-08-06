// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

import '../../../css/mutli-toggle-box.css'

/* 
  A box that contains a variety of options that can be toggled on and off indivigually.
  
  If optional toggleAllOptions are passed, then a Toggle All button is also displayed 
  that toggles all the buttons at once.
*/
const MultiToggleBox = (props: {
    itemsArray: string[];
    itemToggleState: boolean[];
    toggleItemAtIndex: (index: number) => void;
    toggleAllOptions?: {
        currentToggleAllState: boolean,
        toggleAll: () => void
    }; 
}): JSX.Element => {    

    return (
        <div className='multi-toggle-box'>
            {props.toggleAllOptions !== undefined &&
            <div key={'Toggle All'}>
                <input
                    key={'Toggle All'}
                    type="checkbox"
                    name={'Toggle All'}
                    checked={props.toggleAllOptions.currentToggleAllState}
                    onChange={props.toggleAllOptions.toggleAll}
                    className="form-check-input"
                />
              Toggle All
            </div>
            }
            {props.itemsArray.map((item, index) => {
                const currentToggle = props.itemToggleState[index];
                return (
                    <div key={item}>
                        <input
                            key={item}
                            type="checkbox"
                            name={item}
                            checked={currentToggle}
                            onChange={() => {props.toggleItemAtIndex(index)}}
                            className="form-check-input"
                        />
                        {item}
                    </div>
                );
            })}
        </div>
    )
}

export default MultiToggleBox;
