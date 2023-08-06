// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';


export const FilterEmptyIcon = (props: {height?: string, width?: string}): JSX.Element => {
    return (
        <svg width={props.width || "13"} height={props.height || "10"} viewBox="0 0 9 7" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3.63486 6.75C3.49679 6.75 3.38486 6.63807 3.38486 6.5V4.18709C3.38486 4.00613 3.31943 3.83127 3.20064 3.69476L0.781003 0.91411C0.640219 0.75232 0.755131 0.5 0.969598 0.5L8.30011 0.5C8.51458 0.5 8.62949 0.75232 8.48871 0.91411L6.06907 3.69476C5.95028 3.83127 5.88486 4.00613 5.88486 4.18709L5.88486 6.5C5.88486 6.63807 5.77293 6.75 5.63486 6.75H3.63486Z" stroke="#343434" strokeWidth="0.5" />
        </svg> 
    )
}

export const FilterNonEmptyIcon = (): JSX.Element => {
    return (
        <svg width="13" height="10" viewBox="0 0 9 7" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3.63481 6.75C3.49674 6.75 3.38481 6.63807 3.38481 6.5V4.18709C3.38481 4.00613 3.31939 3.83127 3.2006 3.69476L0.780957 0.91411C0.640173 0.75232 0.755085 0.5 0.969552 0.5L8.30007 0.5C8.51453 0.5 8.62945 0.75232 8.48866 0.91411L6.06903 3.69476C5.95024 3.83127 5.88481 4.00613 5.88481 4.18709L5.88481 6.5C5.88481 6.63807 5.77288 6.75 5.63481 6.75H3.63481Z" fill="#0081DE" stroke="#343434" strokeWidth="0.5"/>
        </svg>
    )
}