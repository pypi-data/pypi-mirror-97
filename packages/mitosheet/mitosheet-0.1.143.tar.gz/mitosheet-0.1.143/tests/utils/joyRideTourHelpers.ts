// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all useful selectors and helpers for interacting the JoyRide tour modal 
*/


import { Selector } from 'testcafe';

export const JoyRideNextButton = Selector('button')
    .withAttribute('title', 'Next');

export const JoyRideCloseButton = Selector('button')
    .withAttribute('title', 'Close');

export const JoyRideLastButton = Selector('button')
    .withAttribute('title', 'Last');
