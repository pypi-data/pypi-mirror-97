// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

import '../../css/column-header.css';
import '../../css/margins.css';
import { getHeaderWords } from '../utils/gridStyling';
import { FilterEmptyIcon, FilterNonEmptyIcon } from './icons/FilterIcons';
import { FilterType, FilterGroupType } from './taskpanes/ControlPanel/filter/filterTypes';
import { TaskpaneInfo, TaskpaneType } from './taskpanes/taskpanes';

/* 
  A custom component that AG-Grid displays for the column
  header, that we extend to open the column header popup when clicked.
*/
const ColumnHeader = (props: {
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) =>  void, 
    filters: (FilterType | FilterGroupType)[],
    displayName: string;
}): JSX.Element => {

    /*
      we split each word of the header (separated by _) into its own span element, adding the _ to 
      the latter half of the split. ie: first_name -> [first, _name]
      This lets us wrap the column headers without breaking words in half, which we would
      do if we just used a fix length cutoff for each row as the cutoff.

      Note: this behaves better when the header's words are <10 characters, but worse when
      the header's words are > 10 characters. The 10 number is decided by the default column width
    */
    const wordsSpans: JSX.Element[] = getHeaderWords(props.displayName).map(word => {
        // give the span a random key. we don't use the word because there may be duplicates
        return (<span key={Math.random()}>{word}</span>)
    });

    return (
        <div className='column-header-cell'>
            <div className='column-header-header-container'>
                <div 
                    onClick={() => {props.setCurrOpenTaskpane({
                        type: TaskpaneType.CONTROL_PANEL, 
                        columnHeader: props.displayName, 
                        openEditingColumnHeader: true}
                    )}} 
                    className="column-header-column-header mr-1"
                >
                    {wordsSpans}
                </div>
            </div>
            <div className='column-header-filter-container'>
                <div className='column-header-filter-button'
                    onClick={() => {props.setCurrOpenTaskpane({ 
                        type: TaskpaneType.CONTROL_PANEL, 
                        columnHeader: props.displayName, 
                        openEditingColumnHeader: false
                    })
                    }}>
                    {props.filters.length === 0 && 
                        <FilterEmptyIcon/>
                    }
                    {props.filters.length !== 0 && 
                        <FilterNonEmptyIcon/>
                    }
                </div>
            </div>
        </div>      
    )
} 

export default ColumnHeader