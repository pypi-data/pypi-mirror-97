// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState, useEffect, Fragment } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';
import DefaultModal from '../DefaultModal';
import { ImportSummaries, MitoAPI, RawPythonImportSummary, SimpleImportSummary } from '../../api';

// import css
import "../../../css/all-modals.css"
import "../../../css/import-modal.css"
import { getDfNameError } from './ImportModal';
import LargeSelects from '../elements/LargeSelects';

type ReplayImportModalProps = {
    setModal: (modalInfo: ModalInfo) => void;
    dfNames: string[];
    api: MitoAPI;
    importSummaries: ImportSummaries;
    analysisName: string;
    mitoAPI: MitoAPI
};

/* 
  A modal that allows a user to change what files they import when
  replaying an analysis.
*/
const ReplayImportModal = (props: ReplayImportModalProps): JSX.Element => {
    // Params for a simple import
    const [fileNames, setFileNames] = useState<string[]>([]);
    const [importedFilesByStep, setImportedFilesByStep] = useState<ImportSummaries>(props.importSummaries);
    const [dfNameErrors, setDfNameErrors] = useState<{[key: string]: string}>({});

    // save the original imported step summary so we can display the original dataframe names
    // because the importedFilesByStep gets updated
    const originalImportedFilesByStep = props.importSummaries;

    async function getDataFiles() {
        const dataFiles = await props.api.getDataFiles();
        setFileNames(dataFiles);
    }

    useEffect(() => {
        // To see an explination, read here: https://medium.com/better-programming/how-to-fetch-data-from-an-api-with-react-hooks-9e7202b8afcd
        // TL;DR: we load the data after the component renders
        void getDataFiles();
    }, []) // empty array is key to have this run only once
 

    /*
        For a simple import, updates the imported file that is saved for that specific import
    */
    const updateImportedFile = (stepId: string, index: number, newImport: string): void => {
        // Save the new file name outside the setState callback, as react does funky things w/ synthetic events
        const newFileName = newImport;
        setImportedFilesByStep(prevImportedFilesByStep => {
            const step = prevImportedFilesByStep[stepId] as SimpleImportSummary;
            const newFilesForStep = [...step.file_names]
            newFilesForStep[index] = newFileName;

            return {
                ...prevImportedFilesByStep,
                [stepId]: {
                    'step_type': 'simple_import',
                    'file_names': newFilesForStep
                }
            };
        });
    }


    /*
        For a raw python import, updates the python code in that import step
    */
    const updatePythonCode = (event: React.ChangeEvent<HTMLTextAreaElement>, stepId: string): void => {
        // Save the new file name outside the setState callback, as react does funky things w/ synthetic events
        const newPythonCode = event.target.value;
        setImportedFilesByStep(prevImportedFilesByStep => {
            const step = prevImportedFilesByStep[stepId] as RawPythonImportSummary;

            return {
                ...prevImportedFilesByStep,
                [stepId]: {
                    'step_type': 'raw_python_import',
                    'python_code': newPythonCode,
                    'new_df_names': step.new_df_names
                }
            };
        });
    }

    /*
        For a raw python import, updates the dataframe name string
    */
    const updateDfNameString = (event: React.ChangeEvent<HTMLInputElement>, stepId: string): void => {
        // Save the new file name outside the setState callback, as react does funky things w/ synthetic events
        const dfNameString = event.target.value;
        setImportedFilesByStep(prevImportedFilesByStep => {
            const step = prevImportedFilesByStep[stepId] as RawPythonImportSummary;

            return {
                ...prevImportedFilesByStep,
                [stepId]: {
                    'step_type': 'raw_python_import',
                    'python_code': step.python_code,
                    'new_df_names': dfNameString.split(',').map(dfName => dfName.trim())
                }
            };
        });
    }

    const getPreviousFileNamesLabels = (previousFileNames: string[]): JSX.Element[] => {
        return previousFileNames.map(fileName => (<p className='previous-file-name-label' key={fileName}> {fileName} </p>));
    }

    const clickImport = async () => {

        // First, we check and make sure that all the Python code steps are valid, and throw an 
        // error message if they are not
        const stepIds = Object.keys(importedFilesByStep);
        let errorFound = false;
        for (let i = 0; i < stepIds.length; i++) {
            const stepId = stepIds[i];
            const step = importedFilesByStep[stepId];
            if (step.step_type === 'raw_python_import') {
                const dfNameError = getDfNameError(step.python_code, step.new_df_names, props.dfNames);
                if (dfNameError !== undefined) {
                    errorFound = true;
                    setDfNameErrors(prevDfNameErrors => {
                        return {
                            ...prevDfNameErrors,
                            [stepId]: dfNameError
                        }
                    })
                }
            }
        }
        // Short-curcit if any of the df names have errors
        if (errorFound) {
            return
        }

        await props.mitoAPI.sendUseExistingAnalysisUpdateMessage(
            props.analysisName,
            importedFilesByStep
        )

        props.setModal({type: ModalEnum.None});
    };


    return (
        <DefaultModal
            header={`Update Imported Data`}
            modalType={ModalEnum.ReplayImport}
            viewComponent= {
                <Fragment>
                    <p>
                    Change your previously-used data source to re-run this analysis on new data.
                    </p>
                    {Object.keys(importedFilesByStep).map((stepId) => {
                        const stepSummary = importedFilesByStep[stepId];
                        const originalStepSummary = originalImportedFilesByStep[stepId]
                        if (stepSummary.step_type == 'simple_import') {
                            const previousFileNames = stepSummary.file_names;

                            // make sure the type checks pass
                            const originalFileNames = originalStepSummary.step_type == 'simple_import' ? originalStepSummary.file_names : ['']
                            const originalFileNamesLabels = getPreviousFileNamesLabels(originalFileNames)
                            return (
                                <div key={stepId}>
                                    <div className='modal-element-label mt-2'>
                                        Select the new version of each file for Step {stepId}.
                                    </div>
                                    <div className='import-files-old-and-new-container'>
                                        <div className='previous-file-name-labels-container'>
                                            {originalFileNamesLabels}
                                        </div>
                                        <div className='import-files-select'>
                                            <LargeSelects
                                                numSelects={previousFileNames.length}
                                                startingValue={undefined}
                                                optionsArray={fileNames}
                                                setValue={(index: number, value: string) => {updateImportedFile(stepId, index, value)}}
                                                extraLarge={true}
                                            />
                                        </div>
                                    </div>
                                </div>
                            )
                        } else {
                            const pythonCode = stepSummary.python_code;
                            const dfNameString = stepSummary.new_df_names.join(', ');
                            return (
                                <div key={stepId}>
                                    <div className='modal-element-label mt-2'>
                                    Python Code for for Step {stepId}
                                    </div>
                                    <textarea 
                                        className='raw-python-textarea'
                                        rows={5} 
                                        value={pythonCode} 
                                        onChange={(e) => {updatePythonCode(e, stepId)}}
                                        autoFocus />
                                    <div className='modal-element-label'>
                                    Dataframe Variable Names to Import (comma seperated) for Step {stepId}
                                    </div>
                                    <input 
                                        className="modal-input"
                                        type="text" 
                                        placeholder='df1, df2' 
                                        value={dfNameString} 
                                        onChange={(e) => {updateDfNameString(e, stepId)}} />
                                    {dfNameErrors[stepId] !== undefined && 
                                    <div className='modal-error'>
                                        {dfNameErrors[stepId]}
                                    </div>
                                    }
                                </div>
                            )

                        }

                    
                    })}
                </Fragment>
            }
            buttons = {
                <Fragment>
                    <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                    <div className='modal-action-button modal-dual-button-right' onClick={clickImport}> Replay </div>
                </Fragment>
            }
        />
    )
} 

export default ReplayImportModal;