// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import { ColumnType } from '../../../Mito';
import { DatetimeFilterCondition, FilterType, NumberFilterCondition, StringFilterCondition } from './filterTypes';


export function getEmptyFilterData(columnType: ColumnType): FilterType {
    switch (columnType) {
        case 'string': return {
            type: 'string',
            condition: StringFilterCondition.CONTAINS,
            value: ''
        }
        case 'number': return {
            type: 'number',
            condition: NumberFilterCondition.GREATER,
            value: ''
        }
        case 'datetime': return {
            type: 'datetime',
            condition: DatetimeFilterCondition.DATETIME_EXTACTLY,
            value: ''
        }
    }

}