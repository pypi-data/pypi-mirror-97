// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState } from 'react';
import fscreen from 'fscreen';

// Import CSS
import "../../css/mito-toolbar.css"
import "../../css/margins.css"


// Import Types
import { SheetJSON } from '../widget';
import { ModalInfo, ModalEnum } from './Mito';

// Import Components 
import Tooltip from './Tooltip';
import { TaskpaneInfo, TaskpaneType } from './taskpanes/taskpanes';
import { MitoAPI } from '../api';

// Icons!
import UndoIcon from './icons/UndoIcon';
import ImportIcon from './icons/ImportIcon';
import ExportIcon from './icons/ExportIcon';
import ReplayIcon from './icons/ReplayIcon';
import SaveIcon from './icons/SaveIcon';
import MergeIcon from './icons/MergeIcon';
import PivotIcon from './icons/PivotIcon';
import DeleteColumnIcon from './icons/DeleteColumnIcon';
import AddColumnIcon from './icons/AddColumnIcon';
import DocumentationIcon from './icons/DocumentationIcon';
import { CloseFullscreenIcon, OpenFullscreenIcon } from './icons/FullscreenIcons';
import StepsIcon from './icons/StepsIcon';
import FastForwardIcon from './icons/FastForwardIcon';

const MitoToolbar = (
    props: {
        mitoContainerRef: HTMLDivElement | undefined | null,
        sheetJSON: SheetJSON, 
        selectedSheetIndex: number,
        setEditingMode: (on: boolean, column: string, rowIndex: number) => void,
        setModal: (modal: ModalInfo) => void,
        model_id: string,
        selectedColumn: string,
        setCurrOpenTaskpane: (newCurrTaskpane: TaskpaneInfo) => void;
        mitoAPI: MitoAPI
        closeOpenEditingPopups: () => void;
        currStepIdx: number;
        numSteps: number;
    }): JSX.Element => {

    /* Adds a new column onto the end of a sheet, with A, B, C... as the name */
    const addColumn = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        /*
        * Helper function that, given a number, returns Excel column that corresponds to this number (1-indexed)
        */
        function toColumnName(num: number): string {
            let ret;
            let a = 1;
            let b = 26;
            for (ret = ''; (num -= a) >= 0; a = b, b *= 26) {
                ret = String.fromCharCode(Math.round((num % b) / a) + 65) + ret;
            }
            return ret;
        }

        let inc = 1;
        let newColumnHeader = toColumnName(props.sheetJSON.columns.length + inc);
        // If the column header is in the sheet already, we bump and keep trying
        while (props.sheetJSON.columns.includes(newColumnHeader)) {
            inc++;
            newColumnHeader = toColumnName(props.sheetJSON.columns.length + inc);
        }
        void props.mitoAPI.sendColumnAddMessage(
            props.selectedSheetIndex,
            newColumnHeader
        );
    }


    /* Undoes the last step that was created */
    const undo = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        void props.mitoAPI.sendUndoMessage();
    }

    /* Saves the current file as as an exported analysis */
    const downloadAnalysis = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();
        
        props.setModal({type: ModalEnum.Download});
    }

    
    const [fullscreen, setFullscreen] = useState(false);
    fscreen.onfullscreenchange = () => {
        setFullscreen(!!fscreen.fullscreenElement)
        
        void props.mitoAPI.sendLogMessage(
            'button_toggle_fullscreen',
            {
                // Note that this is true when _end_ in fullscreen mode, and 
                // false when we _end_ not in fullscreen mode, which is much
                // more natural than the alternative
                fullscreen: !!fscreen.fullscreenElement
            }
        )
    };
    
    /* 
        Toggles if Mito is full screen or not
    */
    const toggleFullscreen = () => {
        // We toggle to the opposite of whatever the fullscreen actually is (as detected by the
        // fscreen library), and then we set the fullscreen state variable to that state (in the callback
        // above), so that the component rerenders propery
        const isNotFullscreen = fscreen.fullscreenElement === undefined || fscreen.fullscreenElement === null;
        if (isNotFullscreen && props.mitoContainerRef) {
            fscreen.requestFullscreen(props.mitoContainerRef);
        } else {
            fscreen.exitFullscreen();
        }
    }

    const openDocumentation = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // We log the opening of the documentation taskpane
        void props.mitoAPI.sendLogMessage(
            'button_documentation_log_event',
            {
                stage: 'opened'
            }
        );

        // we open the documentation taskpane
        props.setCurrOpenTaskpane({type: TaskpaneType.DOCUMENTATION});
    }

    const openMerge = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // We open the merge taskpane
        props.setCurrOpenTaskpane({type: TaskpaneType.MERGE});
    }

    const openPivotTable = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        props.setCurrOpenTaskpane({type: TaskpaneType.PIVOT});
    }

    const openDeleteColumn = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        // TODO: log here, and in all the rest of these functions

        props.setModal({type: ModalEnum.DeleteColumn, columnHeader: props.selectedColumn});
    }

    const openSave = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        props.setModal({type: ModalEnum.SaveAnalysis});
    }

    
    const openReplay = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();
        
        props.setCurrOpenTaskpane({type: TaskpaneType.REPLAY_ANALYSIS});
    }
    
    const openImport = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        props.setModal({type: ModalEnum.Import});
    }

    const openSteps = () => {
        void props.mitoAPI.sendLogMessage('click_open_steps')
        props.setCurrOpenTaskpane({type: TaskpaneType.STEPS});
    }


    const fastForward = () => {
        // Fast forwards to the most recent step, allowing editing
        void props.mitoAPI.sendLogMessage('click_fast_forward')
        void props.mitoAPI.checkoutStepByIndex(props.numSteps - 1);
    }

    return (
        <div className='mito-toolbar-container'>
            <div className='mito-toolbar-container-left'>
                <button className='mito-toolbar-item vertical-align-content' onClick={undo}>
                    <UndoIcon/>
                    {/* Extra styling to make sure the tooltip doesn't float off the screen*/}
                    <Tooltip tooltip={"Undo"} style={{'marginLeft': '-15px'}}/>
                </button>

                <div className="vertical-line mt-1"/>

                <button className='mito-toolbar-item vertical-align-content' id='tour-import-button-id' onClick={openImport}>
                    <ImportIcon/>
                    <Tooltip tooltip={"Import Data"}/>
                </button>

                <button className='mito-toolbar-item vertical-align-content' onClick={downloadAnalysis}>
                    <ExportIcon/>
                    <Tooltip tooltip={"Download Sheet"}/>
                </button>

                <div className="vertical-line mt-1"/>

                <button className='mito-toolbar-item vertical-align-content' onClick={addColumn}>
                    <AddColumnIcon/>
                    <Tooltip tooltip={"Add Column"}/>
                </button>
                <button className='mito-toolbar-item vertical-align-content' onClick={openDeleteColumn}>
                    <DeleteColumnIcon/>
                    <Tooltip tooltip={"Delete Column"}/>
                </button>
                <div className="vertical-line mt-1"></div>
                <button className='mito-toolbar-item' onClick={openPivotTable}>
                    <PivotIcon/>
                    <Tooltip tooltip={"Pivot Table"}/>
                </button>
                <button className='mito-toolbar-item' onClick={openMerge}>
                    <MergeIcon/>
                    <Tooltip tooltip={"Merge"}/>
                </button>
                <div className="vertical-line mt-1"></div>
                <button className='mito-toolbar-item' onClick={openSave}>
                    <SaveIcon/>
                    <Tooltip tooltip={"Save"}/>
                </button>
                <button className='mito-toolbar-item' onClick={openReplay}>
                    <ReplayIcon/>
                    <Tooltip tooltip={"Repeat Saved Analysis"}/>
                </button>
            </div>
            <div className='mito-toolbar-container-right mr-1'>
                {/* 
                    Only when we are not caught up do we display the fast forward button
                */}
                {props.currStepIdx !== props.numSteps - 1 &&
                    <button className='mito-toolbar-item' onClick={fastForward}>
                        <FastForwardIcon/>
                        <Tooltip tooltip={"Fast forward to apply all steps"} />
                    </button>
                }
                
                <button className='mito-toolbar-item' onClick={openSteps}>
                    <StepsIcon/>
                    <Tooltip tooltip={"Step History"} />
                </button>
                <button className='mito-toolbar-item' onClick={openDocumentation}>
                    <DocumentationIcon/>
                    <Tooltip tooltip={"Documentation"} />
                </button>
                <button className='mito-toolbar-item' onClick={toggleFullscreen}>
                    {/* We show a different icon depending if it is fullscreen or not*/}
                    {fullscreen &&
                        <CloseFullscreenIcon/>
                    }
                    {!fullscreen &&
                        <OpenFullscreenIcon/>
                    }
                    
                    {/* Extra styling to make sure the full screen tooltip doesn't float off the screen*/}
                    <Tooltip tooltip={fullscreen ? "Close Full Screen": "Full Screen"} style={{'marginLeft': '-80.5px'}}/>
                </button>
            </div>
        </div>
    );
};

export default MitoToolbar;