// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment, useState } from 'react';
import DefaultTaskpane from '../DefaultTaskpane';
import { StepData } from '../../../types/StepTypes';
import { MitoAPI } from '../../../api';

import '../../../../css/step-taskpane.css'


// Import 
import { TaskpaneInfo } from '../taskpanes';
import StepDataElement from './StepDataElement';


export type StepTaskpaneProps = {
    stepDataList: StepData[];
    currStepIdx: number;
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void,
    mitoAPI: MitoAPI
};

/* 
    Taskpane containing a list of all the steps and allowing
    a user to interact with them
*/
function StepTaskpane(props: StepTaskpaneProps): JSX.Element {
    const [openedDropdownIndex, setOpenedDropdownIndex] = useState<undefined | number>(undefined);

    return (
        <DefaultTaskpane
            header = {'Step History'}
            setCurrOpenTaskpane={props.setCurrOpenTaskpane}
            taskpaneBody = {
                <Fragment>
                    {props.stepDataList.map((stepData, index) => {
                        return (
                            <StepDataElement
                                key={stepData.step_id}
                                beforeCurrIdx={index <= props.currStepIdx}
                                openedDropdown={index === openedDropdownIndex}
                                setOpenedDropdown={(openedDropdown) => {
                                    if (!openedDropdown) {
                                        setOpenedDropdownIndex(undefined);
                                    } else {
                                        setOpenedDropdownIndex(index);
                                    }
                                }}
                                stepData={stepData}
                                mitoAPI={props.mitoAPI}
                            />
                        )
                    })}
                </Fragment>
            }
        />
    )

}

export default StepTaskpane;