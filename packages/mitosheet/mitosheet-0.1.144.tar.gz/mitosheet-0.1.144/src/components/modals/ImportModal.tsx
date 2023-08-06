// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState, useEffect, Fragment } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';
import DefaultModal from '../DefaultModal';

import LargeSelects from '../elements/LargeSelects';

// import css
import "../../../css/all-modals.css"
import "../../../css/import-modal.css"
import { MitoAPI } from '../../api';
import LargeSelect from '../elements/LargeSelect';

export enum ImportEnum {
    SimpleImport = 'Simple Import',
    RawPythonImport = 'Raw Python Import',
}

export const getDfNameError = (pythonCode: string, newDfNames: string[], existingDfNames: string[]): string | undefined => {
    for (let i = 0; i < newDfNames.length; i++) {
        // Invalid if it's not in the Python
        if (!pythonCode.includes(newDfNames[i])) {
            return `Error: ${newDfNames[i]} is not a name of a variable in your code.`;
        }
        // Or if it's already the name of a sheet
        if (existingDfNames.indexOf(newDfNames[i]) !== -1) {
            return `Error: ${newDfNames[i]} is already the name of a sheet. Please choose a different name.`;
        }
    }
    return undefined;
}


type ImportModalProps = {
    setModal: (modalInfo: ModalInfo) => void;
    dfNames: string[];
    mitoAPI: MitoAPI;
};

/* 
  A modal that allows a user to import data into the sheet.
*/
const ImportModal = (props: ImportModalProps): JSX.Element => {
    const [importType, setImportType] = useState<ImportEnum>(ImportEnum.SimpleImport);

    // Params for a simple import
    const [fileNames, setFileNames] = useState<string[]>([]);
    const [importedFiles, setImportedFiles] = useState<string[]>([]);
    const [importedFilesError, setImportedFilesError] = useState<string>('');


    // Params for a raw Python import
    const [pythonCode, setPythonCode] = useState<string>('');
    const [dfNamesString, setDfNamesString] = useState<string>('');
    const [dfNameError, setDfNameError] = useState<string>('');

    async function getDataFiles() {
        const dataFiles = await props.mitoAPI.getDataFiles();
        setFileNames(dataFiles);
    }

    useEffect(() => {
        // To see an explination, read here: https://medium.com/better-programming/how-to-fetch-data-from-an-api-with-react-hooks-9e7202b8afcd
        // TL;DR: we load the data after the component renders
        void getDataFiles();
    }, []) // empty array is necessary to have this run only once

    const updateImportedFile = (index: number, newImport: string): void => {
        const newImports = [...importedFiles];
        newImports[index] = newImport;
        setImportedFiles(newImports);
    }

    const addNewFileImport = (): void => {
        const newImports = [...importedFiles];
        newImports.push(fileNames[0]);
        setImportedFiles(newImports);
    }

    /*
        Completes the import step, casing on which sort of import is occuring
    */
    const clickImport = async () => {
        if (importType === ImportEnum.SimpleImport) {
            // Don't let them continue if they didn't import
            if (importedFiles.length === 0) {
                setImportedFilesError('Please upload at least one file before continuing.');
                return;
            }

            await props.mitoAPI.sendSimpleImportMessage(
                importedFiles
            )
            props.setModal({type: ModalEnum.None});
        } else {
            // Short curcit early if the user provides an invalid name
            const dfNames = dfNamesString.split(',').map(dfName => dfName.trim());
            const dfNameError = getDfNameError(pythonCode, dfNames, props.dfNames);
            if (dfNameError !== undefined) {
                return setDfNameError(dfNameError);
            }

            await props.mitoAPI.sendRawPythonImportMessage(
                pythonCode, 
                dfNames
            )
    
            props.setModal({type: ModalEnum.None});
        }
    };

    return (
        <DefaultModal
            header={`Import Data`}
            modalType={ModalEnum.Import}
            viewComponent= {
                <Fragment>
                    <div className='modal-element-label'>
                    Import Method
                    </div>
                    <LargeSelect
                        startingValue={undefined}
                        optionsArray={[ImportEnum.SimpleImport, ImportEnum.RawPythonImport]}
                        setValue={(value) => setImportType(value as ImportEnum)}
                        extraLarge={true}
                    />
                    {importType === ImportEnum.SimpleImport &&
                    <div>
                        <div className='modal-element-label mt-2'>
                            Files to Import
                        </div>
                        <div className='import-files-select'>
                            <LargeSelects
                                numSelects={importedFiles.length}
                                startingValue={undefined}
                                optionsArray={fileNames}
                                setValue={updateImportedFile}
                                extraLarge={true}
                            />
                        </div>
                        <div className='modal-add' onClick={addNewFileImport}>
                            + Add File
                        </div>
                        {importedFilesError !== '' && 
                            <div className='modal-error'>
                                {importedFilesError}
                            </div>
                        }
                    </div>
                    }
                    {importType === ImportEnum.RawPythonImport &&
                    <div>
                        <div className='modal-element-label mt-2'>
                            Python Code
                        </div>
                        <textarea 
                            className='raw-python-textarea'
                            rows={5} 
                            value={pythonCode} 
                            onChange={(e) => {setPythonCode(e.target.value)}}
                            autoFocus />
                        <div className='modal-element-label mt-2'>
                            Dataframe Variable Names to Import (comma seperated)
                        </div>
                        <input 
                            className="modal-input"
                            type="text" 
                            placeholder='df1, df2' 
                            value={dfNamesString} 
                            onChange={(e) => {setDfNamesString(e.target.value)}} />
                        {dfNameError !== '' && 
                            <div className='modal-error'>
                                {dfNameError}
                            </div>
                        }
                    </div> 
                    }
                </Fragment>
            }
            buttons = {
                <Fragment>
                    <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                    <div className='modal-action-button modal-dual-button-right' onClick={clickImport}> Import </div>
                </Fragment>
            }
        />
    )
} 

export default ImportModal;