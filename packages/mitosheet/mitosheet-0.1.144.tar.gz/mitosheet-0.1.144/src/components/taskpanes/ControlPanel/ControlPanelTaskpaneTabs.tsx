// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

// import css
import "../../../../css/margins.css";

/* 
    The tabs at the bottom of the column control panel that allows users to switch
    from sort/filter to seeing summary statistics about the column
*/
function ControlPanelTaskpaneTabs(
    props: {
        selectedTab: number, 
        setSelectedTab: (index: number) => void
    }): JSX.Element {

    return (
        <div className='control-panel-taskpane-tab-container'>
            <div className={'control-panel-taskpane-tab' + (props.selectedTab === 0 ? ' selected' : ' unselected')} onClick={() => props.setSelectedTab(0)}>
                <p>
                    Filter/Sort
                </p>
            </div>
            <div className={'control-panel-taskpane-tab' + (props.selectedTab === 1 ? ' selected' : ' unselected')} onClick={() => props.setSelectedTab(1)}>
                <p>
                    Summary Stats
                </p>
            </div>
        </div> 
    )
} 

export default ControlPanelTaskpaneTabs;