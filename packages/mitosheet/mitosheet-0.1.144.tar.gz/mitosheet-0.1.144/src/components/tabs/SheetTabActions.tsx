// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

// import css
import "../../../css/sheet-tab.css"
import { MitoAPI } from '../../api';

/*
    Displays a set of actions one can perform on a sheet tab, including
    deleting, duplicating, or renaming.
*/
export default function SheetTabActions(props: {
    setCurrOpenSheetTabActions: (sheetIndex: number | undefined) => void;
    setIsRename: React.Dispatch<React.SetStateAction<boolean>>;
    setSelectedSheetIndex: (newIndex: number) => void;
    dfName: string, 
    sheetIndex: number,
    selectedSheetIndex: number,
    getLeftShift: () => number,
    mitoAPI: MitoAPI
}): JSX.Element {

    const onDelete = async (e: React.MouseEvent<HTMLDivElement, MouseEvent>): Promise<void> => {
        // We stop this click from propagating, so that we don't call the callback 
        // that selects this sheet
        e.stopPropagation();

        // If we are deleting the sheet index that is currently selected & it is not sheetIndex 0, update the selected sheet index
        if (props.sheetIndex === props.selectedSheetIndex && props.selectedSheetIndex !== 0) {
            props.setSelectedSheetIndex(props.sheetIndex - 1)
        }

        await props.mitoAPI.sendDataframeDeleteMessage(props.sheetIndex)
        props.setCurrOpenSheetTabActions(undefined);
    }

    const onDuplicate = async (): Promise<void> => {
        await props.mitoAPI.sendDataframeDuplicateMessage(props.sheetIndex)
        props.setCurrOpenSheetTabActions(undefined);
    }

    /* Rename helper, which requires changes to the sheet tab itself */
    const onRename = (): void => {
        props.setCurrOpenSheetTabActions(undefined);
        props.setIsRename(true);
    }

    return (
        <div className='sheet-tab-actions-dropdown' style={{left: props.getLeftShift()}}>
            {/* NOTE: we shift with the location of the actions, so it is placed properly */}
            <div className='sheet-tab-action' onClick={onDelete}>
                Delete
            </div>
            <div className='sheet-tab-action' onClick={onDuplicate}>
                Duplicate
            </div >
            <div className='sheet-tab-action' onClick={onRename}>
                Rename
            </div>
        </div>
    )
}
