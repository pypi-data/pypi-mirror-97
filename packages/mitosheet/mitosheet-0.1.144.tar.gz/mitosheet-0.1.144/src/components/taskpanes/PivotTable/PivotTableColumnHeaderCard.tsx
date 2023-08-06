// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { SelectionOperation, KeyType } from './PivotTaskpane';

// Import css
import '../../../../css/pivot-table-column-header-card.css'

/* 
  A custom component that displays the column headers chosen as the key for the pivot table. 
*/
const PivotTableColumnHeaderCard = (props: {
    columnHeader: string,
    editColumnKeySelection: (keyType: KeyType, columnHeader: string, operation:  SelectionOperation) => void,
    keyType: KeyType,
}): JSX.Element => {

    return (
        <div className='pivot-table-column-header-card-div'> 
            <p className='pivot-table-column-header-card-div-text'>
                {props.columnHeader}
            </p>  
            <div className='pivot-table-column-header-card-exit-div' onClick={() => props.editColumnKeySelection(props.keyType, props.columnHeader, SelectionOperation.REMOVE)}>
                <svg width="15" height="15" viewBox="0 0 7 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <line x1="0.353553" y1="0.646447" x2="5.66601" y2="5.9589" stroke="#343434"/>
                    <line x1="0.354943" y1="5.95895" x2="5.66739" y2="0.646497" stroke="#343434"/>
                </svg>
            </div>
        </div>    
    )
} 

export default PivotTableColumnHeaderCard