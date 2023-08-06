// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

// import css
import "../../../css/top-left-popup.css";

/*
    A small upper-left modal that displays a message to the user
    so they know what's going on
*/
const TopLeftPopup = (props: {message: string}): JSX.Element => {

    return (
        <div className='top-left-popup-container'>
            {props.message}
        </div>
    );
};

export default TopLeftPopup;