// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment, useState } from "react";
import { MitoAPI } from "../../../api";
import DefaultTaskpane from "../DefaultTaskpane";
import { TaskpaneInfo } from "../taskpanes";
import SavedAnalysisCard from "./SavedAnalysisCard";
import { getStepIcon } from "../Steps/StepDataElement";
import { StepType } from "../../../types/StepTypes";

// Import css
import '../../../../css/replay-analysis-taskpane.css'
import { ModalInfo } from "../../Mito";

export type SavedAnalysisStepDescription = {
    step_type: StepType,
    step_description: string
}

const ReplayAnalysisTaskpane = (props: {
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void,
    mitoAPI: MitoAPI,
    savedAnalysisNames: string[],
    setModal: (modal: ModalInfo) => void
}): JSX.Element => {
    const [openedDropdown, setOpenedDropdown] = useState<string | undefined>(undefined)
    const [savedAnalysisDescription, setSavedAnalysisDescription] = useState<SavedAnalysisStepDescription[] | undefined>(undefined)
    const [selectedSavedAnalysis, setSelectedSavedAnalysis] = useState<string | undefined>(undefined)

    const setSelectedAnalysisAndDescription = (
        _savedAnalysisName: string | undefined, 
        _savedAnalysisDescription: SavedAnalysisStepDescription[] | undefined
    ): void => {
        setSelectedSavedAnalysis(_savedAnalysisName)
        setSavedAnalysisDescription(_savedAnalysisDescription)
    }

    // Create the saved analysis name cards
    const savedAnalysisCards = props.savedAnalysisNames.map(savedAnalysisName => {
        return (
            <SavedAnalysisCard
                key={savedAnalysisName}
                isDescribedAnalysis={false}
                savedAnalysisName={savedAnalysisName}
                savedAnalysisNames={props.savedAnalysisNames}
                openedDropdown={openedDropdown === savedAnalysisName}
                setOpenedDropdown={setOpenedDropdown}
                setSelectedAnalysisAndDescription={setSelectedAnalysisAndDescription}
                setModal={props.setModal}
                mitoAPI={props.mitoAPI}
            />
        )
    });

    // Create the saved analysis step descriptions
    let savedAnalysisStepDescriptionDivs: JSX.Element[] = []
    if (savedAnalysisDescription !== undefined) {
        savedAnalysisStepDescriptionDivs = savedAnalysisDescription.map((step: SavedAnalysisStepDescription, index: number) => {
            return (
                <div 
                    className='saved-analysis-taskpane-step' 
                    key={index}
                >
                    <div className='saved-analysis-taskpane-step-icon'>
                        {getStepIcon(step['step_type'])}
                    </div>
                    <div className='saved-analysis-step-text-div'>
                        {step['step_description']}
                    </div>
                </div>
            )
        })
    }  
    
    return(
        <DefaultTaskpane
            header = {'Apply a Saved Analysis'}
            setCurrOpenTaskpane={props.setCurrOpenTaskpane}
            taskpaneBody = {
                <Fragment>
                    {props.savedAnalysisNames.length !== 0 &&
                        <Fragment>
                            <div className='saved-analyses-container'>
                                {savedAnalysisCards}
                            </div>
                            <div className='saved-analysis-divider-line-container'>
                                <hr className='saved-analysis-divider-line' /> 
                            </div>
                            {selectedSavedAnalysis !== undefined && 
                                <Fragment>
                                    <SavedAnalysisCard
                                        key={selectedSavedAnalysis}
                                        isDescribedAnalysis={true}
                                        savedAnalysisName={selectedSavedAnalysis}
                                        savedAnalysisNames={props.savedAnalysisNames}
                                        openedDropdown={openedDropdown === (selectedSavedAnalysis + '-described-analysis')}
                                        setOpenedDropdown={setOpenedDropdown}
                                        setSelectedAnalysisAndDescription={setSelectedAnalysisAndDescription}
                                        setModal={props.setModal}
                                        mitoAPI={props.mitoAPI}
                                    />
                                    <div className='saved-analysis-taskpane-step-container'>
                                        {savedAnalysisStepDescriptionDivs}
                                    </div>
                                </Fragment>
                            }
                            {savedAnalysisDescription === undefined &&
                                <div className='saved-analysis-taskpane-empty-section-text-container'>
                                    Click an analysis to see the steps it contains.
                                </div>
                            }
                        </Fragment>
                    }
                    {props.savedAnalysisNames.length === 0 &&
                        <div className='saved-analysis-taskpane-empty-section-text-container'>
                            You don&apos;t have any saved analyses. Save one, then come back to apply it to your dataframes!
                        </div>
                    }
                </Fragment>
            }
        />
    )
}

export default ReplayAnalysisTaskpane;