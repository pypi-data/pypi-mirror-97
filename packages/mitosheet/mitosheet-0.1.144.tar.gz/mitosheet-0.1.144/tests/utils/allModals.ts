// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all useful selectors and helpers for interacting with shared components
    between all modals.
*/

import { Selector } from 'testcafe';


export const modalSelector = Selector('div.modal')
export const modalHeaderSelector = Selector('div.modal-header-text-div')
export const modalInput = Selector('input.modal-input')
export const modalCloseButtonSelector = Selector('div.modal-dual-button-left')
export const modalAdvanceButtonSelector = Selector('div.modal-dual-button-right')
export const modalAddSelector = Selector('div.modal-add');