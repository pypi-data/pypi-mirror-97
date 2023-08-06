// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { SuggestionItem, SuggestionType } from '../MitoCellEditor';

import '../../../css/suggestion-box.css'


/*
  The suggestion box suggests functions that you could be trying to
  type, beneath the cell editor. 
*/
const SuggestionBox = (
    props: {
        suggestions: SuggestionItem[],
        index: number,
        onMouseEnterSuggestion: (suggestionIndex: number) => void,
        onSelectSuggestion: (startOfFunction: string, restOfFunction: string, type: SuggestionType) => void
    }): JSX.Element => {

    const selectedIndex = props.index % props.suggestions.length;
    
    const functionMatchesDivs = props.suggestions.map((suggestionObject, idx) => {
        const restOfSuggestion = suggestionObject.suggestion.substr(suggestionObject.match.length);
        if (idx === selectedIndex) {
            return (
                <div 
                    key={suggestionObject.suggestion} 
                    onMouseEnter={() => props.onMouseEnterSuggestion(idx)} 
                    onClick={() => {props.onSelectSuggestion(suggestionObject.match, restOfSuggestion, suggestionObject.type)}}
                >
                    <div className='suggestion-box-selected-function'>
                        {suggestionObject.suggestion}
                    </div>
                    <div className='suggestion-box-selected-description'>
                        {suggestionObject.subtitle}
                    </div>
                </div>
            );
        } else {
            return (
                <div 
                    className='suggestion-box-function'
                    key={suggestionObject.suggestion} 
                    onMouseEnter={() => props.onMouseEnterSuggestion(idx)} 
                    onClick={() => {props.onSelectSuggestion(suggestionObject.match, restOfSuggestion, suggestionObject.type)}}
                >
                    {suggestionObject.suggestion}
                </div>
            )
        }
    })

    return (
        <div className='suggestion-box-container'>
            {functionMatchesDivs}  
        </div>
    )    
};

export default SuggestionBox;