// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

import PivotTableColumnHeaderCard from './PivotTableColumnHeaderCard';
import { SelectionOperation, KeyType } from './PivotTaskpane';

// import css
import '../../../../css/pivot-table-key-selection.css'
import SmallSelect, { TitleColor } from '../../elements/SmallSelect';

/* 
  A custom component used in the pivot table which lets the
  user select column headers to add to the row or column keys
*/
const PivotTableKeySelection = (props: {
    sectionTitle: string;
    keyType: KeyType;
    selectableColumnHeaders: string[]
    selectedColumnHeaders: string[];
    editKeySelection: (keyType: KeyType, columnHeader: string, operation:  SelectionOperation) => void
}): JSX.Element => {

    const pivotTableColumnHeaderCards: JSX.Element[] = []
    for (const columnHeader of props.selectedColumnHeaders) {
        pivotTableColumnHeaderCards.push((
            <PivotTableColumnHeaderCard 
                key={columnHeader}
                columnHeader={columnHeader}
                editColumnKeySelection={props.editKeySelection}
                keyType={props.keyType}
            />
        ))
    }

    /* 
      Function passed to the SmallSelect so that when the user selects a 
      key to add, it can communicate the addition to the pivot table state

      Note: we use this wrapper around the editColumnKeySelection function so that 
      we can conform with the interface of the SmallSelect whose setValue function 
      only takes a string as a param
    */ 

    function selectColumnHeader (columnHeader: string): void {
        props.editKeySelection(props.keyType, columnHeader, SelectionOperation.ADD)
    }

    return (
        <div>
            <div className='pivot-taskpane-section-header-div'>
                <p className='default-taskpane-body-section-title-text'>
                    {props.sectionTitle}
                </p>
                <SmallSelect
                    startingValue={'add'}
                    optionsArray={props.selectableColumnHeaders}
                    setValue={selectColumnHeader}
                    titleColor={TitleColor.BLUE}
                />
            </div>
            {pivotTableColumnHeaderCards}
        </div>      
    )
} 

export default PivotTableKeySelection