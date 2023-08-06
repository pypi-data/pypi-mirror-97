// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { CSSProperties } from 'react';
import { CONDITIONS_WITH_NO_INPUT, DATETIME_DROPDOWN_OPTIONS, NUMBER_DROPDOWN_OPTIONS, STRING_DROPDOWN_OPTIONS } from './filterConditions';
import { 
    FilterType,
    Operator
} from './filterTypes';

// import css
import '../../../../../css/filter-card.css'

/* 
    
*/
export function Filter(
    props: {
        first: boolean;
        filter: FilterType;
        operator: Operator;
        displayOperator: boolean;
        setFilter: (newFilter: FilterType) => void;
        setOperator: (operator: Operator) => void;
        deleteFilter: () => void;
    }): JSX.Element {

    // We hide the input if it is not necessary
    const inputStyle: CSSProperties = CONDITIONS_WITH_NO_INPUT.includes(props.filter.condition) ? {'visibility': 'hidden'} : {'visibility': 'visible'};

    return (
        <div className='filter-object'>
            {props.first && 
                <div className='filter-where-label mr-10px'>
                    Where
                </div>
            }
            {!props.first && 
                <select
                    className='filter-select filter-operator mr-10px'
                    value={props.operator}
                    onChange={(e) => {props.setOperator(e.target.value as Operator)}}
                >
                    <option value='And'>And</option>
                    <option value='Or'>Or</option>
                </select>
            }
            <select 
                className='filter-select filter-condition filter-object-item'
                value={props.filter.condition}
                onChange={(e) => {
                    // We perform some unplesant type casting to keep the code
                    // short here
                    props.setFilter({
                        type: props.filter.type as any,
                        condition: e.target.value as any,
                        value: props.filter.value
                    })
                }}>
                {props.filter.type === 'string' && STRING_DROPDOWN_OPTIONS}
                {props.filter.type === 'number' && NUMBER_DROPDOWN_OPTIONS}
                {props.filter.type === 'datetime' && DATETIME_DROPDOWN_OPTIONS}
            </select>
            <input 
                className='filter-select filter-value filter-object-item'
                style={inputStyle}
                type={props.filter.type === 'datetime' ? 'date' : 'text'}
                value={props.filter.value}
                onChange={e => {
                    props.setFilter({
                        type: props.filter.type as any,
                        condition: props.filter.condition as any,
                        value: e.target.value
                    })
                }}
            />
            <div 
                className='filter-object-item filter-close-button' 
                onClick={() => props.deleteFilter()}
            >
                <svg width="15" height="15" viewBox="0 0 13 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <line x1="0.707107" y1="1.29289" x2="11.3136" y2="11.8994" stroke="#343434" strokeWidth="2"/>
                    <line x1="0.7072" y1="11.8995" x2="11.3137" y2="1.29297" stroke="#343434" strokeWidth="2"/>
                </svg>  
            </div>
        </div>
    )
}