// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { StepData, StepType } from '../../../types/StepTypes';
import { MitoAPI } from '../../../api';

// Icons

import ImportIcon from '../../icons/ImportIcon';
import MergeIcon from '../../icons/MergeIcon';
import PivotIcon from '../../icons/PivotIcon'; 
import DeleteColumnIcon from '../../icons/DeleteColumnIcon';
import AddColumnIcon from '../../icons/AddColumnIcon';
import CustomDropdown from '../../elements/CustomDropdown';
import DropdownIcon from '../../icons/DropdownIcon';
import { FilterEmptyIcon } from '../../icons/FilterIcons';
import EditIcon from '../../icons/EditIcon';
import MitoIcon from '../../icons/MitoIcon';


export type StepDataElementProps = {
    beforeCurrIdx: boolean;
    stepData: StepData;
    openedDropdown: boolean;
    setOpenedDropdown: (openedDropdown: boolean) => void; 
    mitoAPI: MitoAPI;
};

/* 
    Gets an icon for a specific step type, to display
    with that step
*/
export function getStepIcon(stepType: StepType): JSX.Element {
    switch (stepType) {
        case StepType.Initialize: return (
            <MitoIcon/>
        )
        case StepType.AddColumn: return (
            <AddColumnIcon/>
        )
        case StepType.DeleteColumn: return (
            <DeleteColumnIcon/>
        )
        case StepType.RenameColumn: return (
            <EditIcon/>
        )
        case StepType.ReorderColumn: return (
            <EditIcon/>
        )
        case StepType.FilterColumn: return (
            <FilterEmptyIcon
                height='20'
                width='20'
            />
        )
        case StepType.SetColumnFormula: return (
            <div className='step-taskpane-missing-icon'>
                Fx
            </div>
        )
        case StepType.DataframeDelete: return (
            <DeleteColumnIcon/>
        )
        case StepType.DataframeDuplicate: return (
            <EditIcon/>
        )
        case StepType.DataframeRename: return (
            <EditIcon/>
        )
        case StepType.SimpleImport: return (
            <ImportIcon/>
        )
        case StepType.RawPythonImport: return (
            <ImportIcon/>
        )
        case StepType.Sort: return (
            <EditIcon/>
        )
        case StepType.Pivot: return (
            <PivotIcon
                width='20'
            />
        )
        case StepType.Merge: return (
            <MergeIcon
                width='27'
            />
        )
        default: return (
            <EditIcon/>
        )
    }
}


/* 
    An element in a list that displays information about a step, and
    eventually will allow the user to interact with that step (e.g. 
    to start editing it).
*/
function StepDataElement(props: StepDataElementProps): JSX.Element {

    const rollBackToStep = (): void => {
        props.setOpenedDropdown(false);
        void props.mitoAPI.checkoutStepByIndex(props.stepData.step_idx);
    }

    return (
        <div className='step-taskpane-step-container'>
            {/* We grey out any steps that are before the current step */}
            <div 
                className='step-taskpane-step-container-left' 
                style={{opacity: props.beforeCurrIdx ? '1': '.5'}}
                onClick={rollBackToStep}
            >
                <div className='step-taskpane-step-icon'>
                    {getStepIcon(props.stepData.step_type)}
                </div>
                <div className='step-taskpane-step-text'>
                    <div className='step-taskpane-step-header'>
                        {props.stepData.step_display_name}
                    </div>
                    <div className='step-taskpane-step-subtext'>
                        {props.stepData.step_description}
                    </div>
                </div>
            </div>
            <div className='step-taskpane-step-container-right' onClick={() => {
                props.setOpenedDropdown(!props.openedDropdown)
            }}>
                <DropdownIcon/>
            </div>
            {props.openedDropdown && 
                <CustomDropdown
                    closeDropdown={() => {props.setOpenedDropdown(false)}}
                >
                    <div onClick={rollBackToStep}>
                        View this step
                    </div>
                    <div className='custom-dropdown-inactive'>
                        Edit this step (coming soon)
                    </div>
                </CustomDropdown>
            }
        </div>
    )

}

export default StepDataElement;