// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

import { AggregationType, SelectionOperation } from './PivotTaskpane';
import SmallSelect, { TitleColor } from '../../elements/SmallSelect';
import PivotTableValueAggregationCard from './PivotTableValueAggregationCard';

// import css
import '../../../../css/pivot-table-key-selection.css'

/* 
  A custom component used in the pivot table which lets the
  user select column headers to add to the row or column keys
*/
const PivotTableValueSelection = (props: {
    columnHeaders: string[]
    aggregatedValuesInSection: Record<string, AggregationType>; // Column header, aggregation type pairs to determine which have already been selected
    editValueAggregationSelection: (columnHeader: string, selectionOperation: SelectionOperation, aggregationType?: AggregationType) => void 
}): JSX.Element => {
    
    // TODO: Put these in order of selection so that the new one is at the top so that the user can easily change its aggregation method
    const PivotTableValueAggregationCards: JSX.Element[] = []
    for (const columnHeader of Object.keys(props.aggregatedValuesInSection)) {
        PivotTableValueAggregationCards.push((
            <PivotTableValueAggregationCard 
                key={columnHeader}
                columnHeader={columnHeader}
                aggregationType={props.aggregatedValuesInSection[columnHeader]}
                editValueAggregationSelection={props.editValueAggregationSelection}
            />
        ))
    }

    // get column headers that are not yet aggregated
    const selectableColumnHeaders = props.columnHeaders.filter(x => !Object.keys(props.aggregatedValuesInSection).includes(x));

    /* 
      Function passed to the SmallSelect so that when the user selects a 
      key to add, it can communicate the addition to the pivot table state

      Note: we use this wrapper around the editColumnKeySelection function so that 
      we can conform with the interface of the SmallSelect whose setValue function 
      only takes a string as a param
    */ 
    function addAggregatedValue (columnHeader: string): void {
        props.editValueAggregationSelection(columnHeader, SelectionOperation.ADD, AggregationType.COUNT)
    }

    return (
        <div>
            <div className='pivot-taskpane-section-header-div'>
                <p className='default-taskpane-body-section-title-text'>
            Values
                </p>
                <SmallSelect
                    startingValue={'add'}
                    optionsArray={selectableColumnHeaders}
                    setValue={addAggregatedValue}
                    titleColor={TitleColor.BLUE}
                />
            </div>
            {PivotTableValueAggregationCards}
        </div>      
    )
} 

export default PivotTableValueSelection