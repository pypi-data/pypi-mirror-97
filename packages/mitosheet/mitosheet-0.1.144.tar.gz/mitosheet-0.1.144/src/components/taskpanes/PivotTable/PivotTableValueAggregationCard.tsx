// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { AggregationType, SelectionOperation } from './PivotTaskpane';

// import css
import '../../../../css/pivot-table-column-header-card.css'
import '../../../../css/pivot-table-value-aggregation-card.css'
import '../../../../css/margins.css'
import SmallSelect, { TitleColor } from '../../elements/SmallSelect';

/* 
  A custom component that displays the column headers chosen as the key for the pivot table. 
*/
const PivotTableValueAggregationCard = (props: {
    columnHeader: string,
    aggregationType: AggregationType
    editValueAggregationSelection: (columnHeader: string, operation: SelectionOperation, aggregationType?: AggregationType) => void
}): JSX.Element => {

    // Create a list of the possible aggregation methods
    const aggregationTypeList = Object.values(AggregationType);
    
    const setAggregationType = (aggregationType: string): void => {
        // Declare the aggregationType param of type AggregationType and then make sure that it is
        const aggregationTypeCast = aggregationType as AggregationType
        if (aggregationTypeList.includes(aggregationTypeCast)) {
            props.editValueAggregationSelection(props.columnHeader, SelectionOperation.ADD, aggregationTypeCast);
        }
    }

    return (
        <div className='pivot-table-column-header-card-div'> 
            <div className='pivot-table-value-aggregation-card-aggregation-info-div'>
                <SmallSelect
                    startingValue={props.aggregationType}
                    optionsArray={aggregationTypeList}
                    setValue={setAggregationType}
                    titleColor={TitleColor.DARK}
                />
                <p className='pivot-table-value-aggregation-card-div-text ml-5'>
                    of {props.columnHeader}
                </p>  
            </div>
            <div 
                className='pivot-table-column-header-card-exit-div' 
                onClick={() => props.editValueAggregationSelection(props.columnHeader, SelectionOperation.REMOVE)}
            >
                <svg width="15" height="15" viewBox="0 0 7 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <line x1="0.353553" y1="0.646447" x2="5.66601" y2="5.9589" stroke="#343434"/>
                    <line x1="0.354943" y1="5.95895" x2="5.66739" y2="0.646497" stroke="#343434"/>
                </svg>
            </div>
        </div>    
    )
} 

export default PivotTableValueAggregationCard