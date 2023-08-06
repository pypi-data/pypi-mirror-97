// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState } from "react"
import { Fragment } from "react"
import { MitoAPI } from "../../../api"
import CustomDropdown from "../../elements/CustomDropdown"
import DropdownIcon from "../../icons/DropdownIcon"
import { ModalEnum, ModalInfo } from "../../Mito"
import { SavedAnalysisStepDescription } from "./ReplayAnalysisTaskpane"

/* 
    Helper function for validating saved analysis renames. Valid renames are:
    - not duplicated names
    - not empty
*/ 
const getAnalysisNameError = (savedAnalysisNames: string[], newAnalysisName: string): string => {
    if (newAnalysisName === '') {
        return 'The analysis cannot be empty.'
    } else if (savedAnalysisNames.includes(newAnalysisName)) {
        return 'That name is taken by another analysis.'
    } else {
        return ''
    }
}

const SavedAnalysisCard = (props: {
    isDescribedAnalysis: boolean,
    savedAnalysisName: string,
    savedAnalysisNames: string[],
    openedDropdown: boolean,
    setOpenedDropdown: (savedAnalysisName: string | undefined) => void,
    setSelectedAnalysisAndDescription(savedAnalysisName: string | undefined, savedAnalysisDescription: SavedAnalysisStepDescription[] | undefined): void,
    setModal: (modal: ModalInfo) => void,
    mitoAPI: MitoAPI
}): JSX.Element => {
    const [isRename, setIsRename] = useState<boolean>(false);
    const [newSavedAnalysisName, setNewSavedAnalysisName] = useState<string>(props.savedAnalysisName);
    const [renameError, setRenameError] = useState<string>('');
    const [savedAnalysisDescription, setSavedAnalysisDescription] = useState<SavedAnalysisStepDescription[] | undefined>(undefined)

    // This function applies the saved analysis
    const applySavedAnalysis = async (): Promise<void> => {
        // First, we check if there are any simple import steps that we need to handle with special
        // care, specifically by asking the users to switch out the files for new files.
        const importSummary = await props.mitoAPI.getImportSummary(props.savedAnalysisName);
        if (Object.keys(importSummary).length !== 0) {
            props.setModal({type: ModalEnum.ReplayImport, analysisName: props.savedAnalysisName, importSummary: importSummary});
            return;
        }

        await props.mitoAPI.sendUseExistingAnalysisUpdateMessage(props.savedAnalysisName)
    }

    // This function deletes the saved analysis
    const deleteSavedAnalysis = async (): Promise<void> => {
        props.setSelectedAnalysisAndDescription(undefined, undefined)
        await props.mitoAPI.sendDeleteSavedAnalysisMessage(props.savedAnalysisName)
    }

    // This function renames the saved analysis after making sure the name is valid
    const renameSavedAnalysis = async (): Promise<void> => {
        // If the new name is the same as the old name, turn off the error and close renaming
        if (props.savedAnalysisName === newSavedAnalysisName) {
            setRenameError('')
            setIsRename(false)
            return
        }
        
        // Validate the rename
        const renameAnalysisError = getAnalysisNameError(props.savedAnalysisNames, newSavedAnalysisName)
        setRenameError(renameAnalysisError)

        // If the new name is valid, send rename event
        if (renameAnalysisError === '') {
            await props.mitoAPI.sendRenameSavedAnalysisMessage(props.savedAnalysisName, newSavedAnalysisName)
            props.setSelectedAnalysisAndDescription(newSavedAnalysisName, savedAnalysisDescription)
            setIsRename(false)
        }
    }

    // This function receives the steps of the saved analysis to be displayed by the taskpane
    const getSavedAnalysisDescription = async (): Promise<void> => {
        const savedAnalysisDescription: SavedAnalysisStepDescription[]  = await props.mitoAPI.getSavedAnalysisDescription(props.savedAnalysisName)
        setSavedAnalysisDescription(savedAnalysisDescription)
        props.setSelectedAnalysisAndDescription(newSavedAnalysisName, savedAnalysisDescription)
        props.setOpenedDropdown(undefined)

        /*
            We use a log event here, but not in the other functions, because the other functions
            are update events that are automatically logged. This function goes through api.py and therefore
            needs manual logging. 
        */ 
        void props.mitoAPI.sendLogMessage(
            'clicked_saved_analysis_name_log_event',
            {
                saved_analysis_name: props.savedAnalysisName,
            }
        )
    }

    return (
        <Fragment>
            <div>
                <div className='saved-analysis-card'>
                    <div 
                        className='saved-analysis-card-analysis-name'
                        onClick={() => {void getSavedAnalysisDescription()}}
                        onDoubleClick={() => {setIsRename(true)}}>
                        {isRename && 
                            <form onSubmit={async (e) => {e.preventDefault(); await renameSavedAnalysis()}}>
                                <input 
                                    type='text'
                                    value={newSavedAnalysisName} 
                                    onChange={(e) => {setNewSavedAnalysisName(e.target.value)}}
                                    onBlur={renameSavedAnalysis}
                                    autoFocus
                                />
                            </form>
                        }
                        {!isRename &&
                            props.savedAnalysisName 
                        }
                    </div>
                    <div>
                        <div 
                            className='saved-analysis-card-dropdown-div'
                            onClick={() => {
                                /* 
                                    If the saved analysis card that is clicked is the analysis card in the summary section
                                    of the taskpane, mark it using '-described-analysis', so that we can determine whether the 
                                    user clicked on the CustomDropdown that is part of the list of saved analyses or if it was 
                                    the analysis card used in the summary section. 

                                    We do this so only one dropdown opens instead of the one in the list and the summary section.
                                */ 
                                if (props.isDescribedAnalysis) {
                                    props.setOpenedDropdown(props.savedAnalysisName + '-described-analysis')
                                } else {
                                    props.setOpenedDropdown(props.savedAnalysisName)
                                }
                            }}
                        >
                            <DropdownIcon/>
                        </div>
                        {props.openedDropdown && 
                            <CustomDropdown
                                closeDropdown={() => {props.setOpenedDropdown(undefined)}}
                            >
                                <div onClick={() => {
                                    void applySavedAnalysis()
                                    props.setOpenedDropdown(undefined);
                                }}>
                                    Apply this Analysis
                                </div>
                                <div onClick={() => {
                                    setIsRename(true);
                                    props.setOpenedDropdown(undefined);
                                }}>
                                    Rename this Analysis
                                </div>
                                <div onClick={deleteSavedAnalysis}>
                                    Delete this Analysis
                                </div>
                            </CustomDropdown>
                        }
                    </div>
                </div>
                {renameError !== '' && 
                    <p className='replay-analysis-rename-error'>
                        {renameError}
                    </p>
                }
            </div>

        </Fragment>
    )
}

export default SavedAnalysisCard