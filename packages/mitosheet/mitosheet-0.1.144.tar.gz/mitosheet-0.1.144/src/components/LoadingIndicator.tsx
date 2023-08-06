// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useEffect, useState } from 'react';

// import css
import "../../css/loading-indicator.css";

/*
    A tiny, upper left modal that tells the user that the operation is
    loading.

    By default, does not displaying anything for the first .5 seconds it
    is rendered, so that only long running ops actually display a loading
    bar.
*/
const LoadingIndicator = (): JSX.Element => {
    // We use a count to track the number of ...s to display.
    // 0 -> '', 1 -> '.', 2 -> '..', 3 -> '...'. Wraps % 4.
    const [indicatorState, setIndicatorState] = useState(-1);

    // Schedule a change to update the loading indicator, every .5 seconds
    useEffect(() => {
        const interval = setInterval(() => {
            setIndicatorState(indicatorState => indicatorState + 1);
        }, 500);
        return () => clearInterval(interval);
    }, []);

    // We start the indicator at -1, so that we don't display anything
    // for the first half second. This makes us only display the indicator
    // for actually long running operations.
    if (indicatorState < 0) {
        return <React.Fragment/>
    }

    const someNumberOfDots = '.'.repeat(indicatorState % 4);

    return (
        <div className='loading-indicator-container'>
            <p className='loading-indicator-text'>
                Loading{someNumberOfDots}
            </p>
        </div>
    );
};

export default LoadingIndicator;