// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import LargeSelect from '../../elements/LargeSelect';

// import css
import '../../../../css/merge-sheet-and-key-selection.css'
import { MergeSheet } from './MergeTaskpane';

/* 
  A custom component that allows you to select a sheet from the list of
  possible sheets, as well as a column header from that sheet.
*/
const MergeSheetAndKeySelection = (props: {
    dfNames: string[],
    sheetIndex: number,
    otherSheetIndex: number,
    sheetNum: MergeSheet;
    setNewSheetIndex: (newSheetIndex: number) => void,
    columnHeaders: string[],
    mergeKey: string,
    setNewMergeKey: (newMergeKey: string) => void,
}): JSX.Element => {

    const sheetNumStr = props.sheetNum == MergeSheet.First ? 'First' : 'Second'

    return (
        <div className='merge-sheet-and-key'>
            <div>
                <p className='default-taskpane-body-section-title-text'>
                    {sheetNumStr} Sheet
                </p>
                <LargeSelect
                    startingValue={props.dfNames[props.sheetIndex]}
                    key={props.sheetIndex} // To update the display when you change selections
                    optionsArray={props.dfNames}
                    setValue={(value: string) => {
                        const newSheetIndex = props.dfNames.indexOf(value);
                        props.setNewSheetIndex(newSheetIndex);
                    }}
                />
            </div>
            <div>
                <p className='default-taskpane-body-section-title-text'>
                    Merge Key
                </p>
                <LargeSelect
                    startingValue={props.mergeKey}
                    key={props.mergeKey} // To update the display when you change selections
                    optionsArray={props.columnHeaders}
                    setValue={(newMergeKey: string) => {props.setNewMergeKey(newMergeKey)}}
                />
            </div>
        </div>
    )
} 

export default MergeSheetAndKeySelection