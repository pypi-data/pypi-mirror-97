// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';


const PivotIcon = (props: {width?: string}): JSX.Element => {
    return (
        <svg width={props.width || "30"} height="30" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="1.25" y="8.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.6"/>
            <rect x="1.25" y="1.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.6"/>
            <rect x="8.25" y="8.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.6"/>
            <rect x="8.25" y="1.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.6"/>
            <circle cx="3" cy="3" r="1" fill="#343434"/>
            <circle cx="5" cy="5" r="1" fill="#343434"/>
            <path d="M9.49994 2.49992L9.49992 5.5M12.5 2.5L12.4999 5.50008M10.9999 2.50014L10.9999 5.50022" stroke="#343434" strokeWidth="0.6"/>
            <path d="M5.63898 9.5L2.32331 9.5M5.63901 12.3181L3.97868 12.3182L2.31834 12.3183M5.63898 10.8809L2.31834 10.8809" stroke="#343434" strokeWidth="0.6"/>
        </svg>
    )
}

export default PivotIcon;

