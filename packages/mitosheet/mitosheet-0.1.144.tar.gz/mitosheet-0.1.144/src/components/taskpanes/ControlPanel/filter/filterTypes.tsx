// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

export type Operator = 'And' | 'Or';

export enum StringFilterCondition {
    CONTAINS = 'contains',
    DOES_NOT_CONTAIN = 'string_does_not_contain',
    STRING_EXACTLY = 'string_exactly',
    EMPTY = 'empty',
    NOT_EMPTY = 'not_empty',
}

export enum NumberFilterCondition {
    NUMBER_EXACTLY = 'number_exactly',
    GREATER = 'greater',
    GREATER_THAN_OR_EQUAL = 'greater_than_or_equal',
    LESS = 'less',
    LESS_THAN_OR_EQUAL = 'less_than_or_equal',
    EMPTY = 'empty',
    NOT_EMPTY = 'not_empty',
}

export enum DatetimeFilterCondition {
    DATETIME_EXTACTLY = 'datetime_exactly',
    DATETIME_GREATER_THAN = 'datetime_greater',
    DATETIME_GREATER_THAN_OR_EQUAL = 'datetime_greater_than_or_equal',
    DATETIME_LESS = 'datetime_less',
    DATETIME_LESS_THAN_OR_EQUAL = 'datetime_less_than_or_equal',
    EMPTY = 'empty',
    NOT_EMPTY = 'not_empty',
}

export interface StringFilterType {
    type: 'string',
    condition: StringFilterCondition;
    value: string;
}

export interface NumberFilterType {
    type: 'number',
    condition: NumberFilterCondition;
    /* 
        We allow number filters to contain a number or a string, as the frontend
        always stores them as a string (when the user edits them), and thus
        allows us to support negative numnbers, decimals, etc - e.g. numbers that 
        don't parse well while they are being typed
    */
    value: number | string;
}

export interface DatetimeFilterType {
    type: 'datetime',
    condition: DatetimeFilterCondition;
    value: string;
}

export type FilterType = 
    | StringFilterType
    | NumberFilterType
    | DatetimeFilterType


export interface FilterGroupType {
    filters: FilterType[];
    operator: Operator
}

// See: https://www.typescriptlang.org/docs/handbook/advanced-types.html#user-defined-type-guards
export function isFilterGroup(filter: FilterType | FilterGroupType): filter is FilterGroupType {
    return (filter as FilterGroupType).filters !== undefined;
}

