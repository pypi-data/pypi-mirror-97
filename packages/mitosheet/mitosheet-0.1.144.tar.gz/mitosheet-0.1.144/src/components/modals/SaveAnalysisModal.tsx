// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState, Fragment } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';
import DefaultModal from '../DefaultModal';


// import css
import "../../../css/save-analysis-modal.css"
import { MitoAPI } from '../../api';

// A set of characters we don't allow in analysis names,
// just to avoid file name issues
// Taken from: https://www.mtu.edu/umc/services/digital/writing/characters-avoid/
const ILLEGAL_FILENAME_CHARACTERS = [
    '#',
    '%',
    '&',
    '{', '}',
    '/', '\\',
    '<', '>',
    '*',
    '?',
    '$',
    '!',
    '\'', '"',
    ':',
    '@'
]


function getAnalysisNameError(analysisName: string): string {
    /*
        Helper function for validating named analyses. Avoids a set of illegal characters.

        Returns the empty string if there is no error.
    */
    if (analysisName.length == 0) {
        return 'Please enter a name for your analysis';
    }

    for (let i = 0; i < ILLEGAL_FILENAME_CHARACTERS.length; i++) {
        if (analysisName.indexOf(ILLEGAL_FILENAME_CHARACTERS[i]) > -1) {
            return `Invalid analysis name. Please remove the "${ILLEGAL_FILENAME_CHARACTERS[i]}"`
        }
    }

    return '';
}


type SaveAnalysisProps = {
    setModal: (modalInfo: ModalInfo) => void;
    savedAnalysisNames: string[];
    saveAnalysisName?: string;
    mitoAPI: MitoAPI;
};

/* 
  A modal that allows a user to save an analysis with the input
  name.
*/
const SaveAnalysis = (props: SaveAnalysisProps): JSX.Element => {
    const [saveAnalysisName, setSaveAnalysisName] = useState(props.saveAnalysisName !== undefined ? props.saveAnalysisName : '');
    const [analysisNameError, setAnalysisNameError] = useState('');

    const clickSave = async () => {
        // Don't let the user submit if they have an invalid analysis name!
        if (getAnalysisNameError(saveAnalysisName) !== '') {
            setAnalysisNameError(
                `Please fix before saving: ${getAnalysisNameError(saveAnalysisName)}`
            );
            return;
        }

        if (props.savedAnalysisNames.indexOf(saveAnalysisName) > -1) {
            // If user is overwriting an analysis, we display a popup to let them know. 
            props.setModal({
                type: ModalEnum.SaveAnalysisOverwrite, 
                saveAnalysisName: saveAnalysisName
            })
        } else {
            // Otherwise, we just log and save the analysis
            await props.mitoAPI.sendSaveAnalysisMessage(
                saveAnalysisName
            )
            props.setModal({type: ModalEnum.None});
        }
    }

    const onChangeAnalysisName = (newAnalysisName: string) => {
        setSaveAnalysisName(newAnalysisName)
        setAnalysisNameError(getAnalysisNameError(newAnalysisName))
    }

    return (
        <DefaultModal
            header={`Save your current analysis`}
            modalType={ModalEnum.SaveAnalysis}
            viewComponent= {
                <Fragment>
                    <div>
                        <div>
                            <div className='save-analysis-label'>
                            Name your analysis
                            </div>
                            <input 
                                className="modal-input"
                                type="text" 
                                placeholder='Monthly Sales Analysis' 
                                value={saveAnalysisName} 
                                onChange={(e) => onChangeAnalysisName(e.target.value)} 
                                autoFocus />
                            {analysisNameError !== '' && 
                            <p className='save-analysis-name-error'>
                                {analysisNameError}
                            </p>
                            }
                        </div>
                        <div className='mt-2 save-analysis-analysis-selection-container'>
                            <div className='save-analysis-label'>
                            Existing analyses
                            </div>
                            <div className='save-analysis-analysis-selection'>
                                {props.savedAnalysisNames.length == 0 &&
                                <p>
                                    Save an analysis to have it appear here.
                                </p>
                                }
                                {props.savedAnalysisNames.map((savedAnalysisName) => {
                                    return (
                                        <div 
                                            className='save-analysis-analysis-name' 
                                            key={savedAnalysisName} 
                                            onClick={() => {onChangeAnalysisName(savedAnalysisName)}} >
                                            {savedAnalysisName}
                                        </div>
                                    )
                                })}
                            </div>
                        </div>
                    </div>
                
                </Fragment>
            }
            buttons = {
                <Fragment>
                    <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                    <div className='modal-action-button modal-dual-button-right' onClick={clickSave}> {"Save"}</div>
                </Fragment>
            }
        />
    )
} 

export default SaveAnalysis;