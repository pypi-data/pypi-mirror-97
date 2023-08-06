// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';


const MergeIcon = (props: {width?: string}): JSX.Element => {
    return (
        <svg width={props.width || "40"} height="30" viewBox="0 0 17 11" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11.6467 5.12789C11.6467 7.78833 9.13157 10.0058 5.94835 10.0058C2.76513 10.0058 0.25 7.78833 0.25 5.12789C0.25 2.46744 2.76513 0.25 5.94835 0.25C9.13157 0.25 11.6467 2.46744 11.6467 5.12789Z" fill="#C8C8C8" stroke="#343434" strokeWidth="0.6"/>
            <path d="M16.4784 5.12789C16.4784 7.78833 13.9632 10.0058 10.78 10.0058C7.59679 10.0058 5.08167 7.78833 5.08167 5.12789C5.08167 2.46744 7.59679 0.25 10.78 0.25C13.9632 0.25 16.4784 2.46744 16.4784 5.12789Z" stroke="#343434" strokeWidth="0.6"/>
        </svg>
    )
}

export default MergeIcon;

