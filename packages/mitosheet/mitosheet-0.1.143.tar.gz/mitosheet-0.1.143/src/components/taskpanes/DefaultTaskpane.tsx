// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

// import css
import "../../../css/default-taskpane.css"
import { TaskpaneInfo, TaskpaneType } from './taskpanes';

/*
    DefaultTaskpane is a higher-order component that
    takes a header and a taskpaneBbody, and displays it as a component.

    The modal has props
    - a header string to be shown at the top of the taskpane
    - a taskpaneBody, a react fragment which is the center segment of the taskpane
    - a setTaskpaneOpenOrClosed function to close the taskpane
*/
const DefaultTaskpane = (
    props: {
        header: string
        taskpaneBody: React.ReactFragment
        setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void;
    }): JSX.Element => {

    return (
        <div className='default-taskpane-div'>
            <div className='default-taskpane-header-div'>
                <p className='default-taskpane-header-text'>
                    {props.header}
                </p>        
                <div className='default-taskpane-header-exit-button-div' onClick={() => props.setCurrOpenTaskpane({type: TaskpaneType.NONE})}>
                    <svg width="18" height="18" viewBox="0 0 13 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <line x1="0.707107" y1="1.29289" x2="11.3136" y2="11.8994" stroke="#343434" strokeWidth="2"/>
                        <line x1="0.7072" y1="11.8995" x2="11.3137" y2="1.29297" stroke="#343434" strokeWidth="2"/>
                    </svg>
                </div>
            </div>
            <div className='default-taskpane-body-div'> 
                {props.taskpaneBody}
            </div>
        </div>
    )
};

export default DefaultTaskpane;