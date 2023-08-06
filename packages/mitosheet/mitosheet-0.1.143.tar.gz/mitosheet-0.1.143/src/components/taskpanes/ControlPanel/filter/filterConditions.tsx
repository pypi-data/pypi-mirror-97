// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { DatetimeFilterCondition, NumberFilterCondition, StringFilterCondition } from './filterTypes';

export const NUMBER_DROPDOWN_OPTIONS: JSX.Element[] = [
    <option key={NumberFilterCondition.NUMBER_EXACTLY} value={NumberFilterCondition.NUMBER_EXACTLY}>=</option>,
    <option key={NumberFilterCondition.GREATER} value={NumberFilterCondition.GREATER}>&gt;</option>,
    <option key={NumberFilterCondition.GREATER_THAN_OR_EQUAL} value={NumberFilterCondition.GREATER_THAN_OR_EQUAL}>&ge;</option>,
    <option key={NumberFilterCondition.LESS} value={NumberFilterCondition.LESS}>&lt;</option>,
    <option key={NumberFilterCondition.LESS_THAN_OR_EQUAL} value={NumberFilterCondition.LESS_THAN_OR_EQUAL}>&le;</option>,
    <option key={NumberFilterCondition.EMPTY} value={NumberFilterCondition.EMPTY}>is empty</option>,
    <option key={NumberFilterCondition.NOT_EMPTY} value={NumberFilterCondition.NOT_EMPTY}>is not empty</option>,
]

export const STRING_DROPDOWN_OPTIONS: JSX.Element[] = [
    <option key={StringFilterCondition.CONTAINS} value={StringFilterCondition.CONTAINS}>contains</option>,
    <option key={StringFilterCondition.DOES_NOT_CONTAIN} value={StringFilterCondition.DOES_NOT_CONTAIN}>does not contain</option>,
    <option key={StringFilterCondition.STRING_EXACTLY} value={StringFilterCondition.STRING_EXACTLY}>is exactly</option>,
    <option key={StringFilterCondition.EMPTY} value={StringFilterCondition.EMPTY}>is empty</option>,
    <option key={StringFilterCondition.NOT_EMPTY} value={StringFilterCondition.NOT_EMPTY}>is not empty</option>,
]

export const DATETIME_DROPDOWN_OPTIONS: JSX.Element[] = [
    <option key={DatetimeFilterCondition.DATETIME_EXTACTLY} value={DatetimeFilterCondition.DATETIME_EXTACTLY}>=</option>,
    <option key={DatetimeFilterCondition.DATETIME_GREATER_THAN} value={DatetimeFilterCondition.DATETIME_GREATER_THAN}>&gt;</option>,
    <option key={DatetimeFilterCondition.DATETIME_GREATER_THAN_OR_EQUAL} value={DatetimeFilterCondition.DATETIME_GREATER_THAN_OR_EQUAL}>&ge;</option>,
    <option key={DatetimeFilterCondition.DATETIME_LESS} value={DatetimeFilterCondition.DATETIME_LESS}>&lt;</option>,
    <option key={DatetimeFilterCondition.DATETIME_LESS_THAN_OR_EQUAL} value={DatetimeFilterCondition.DATETIME_LESS_THAN_OR_EQUAL}>&le;</option>,
    <option key={DatetimeFilterCondition.EMPTY} value={StringFilterCondition.EMPTY}>is empty</option>,
    <option key={DatetimeFilterCondition.NOT_EMPTY} value={StringFilterCondition.NOT_EMPTY}>is not empty</option>,
]

export const CONDITIONS_WITH_NO_INPUT = [
    NumberFilterCondition.EMPTY,
    NumberFilterCondition.NOT_EMPTY,
    StringFilterCondition.EMPTY,
    StringFilterCondition.NOT_EMPTY,
    DatetimeFilterCondition.EMPTY,
    DatetimeFilterCondition.NOT_EMPTY,
]