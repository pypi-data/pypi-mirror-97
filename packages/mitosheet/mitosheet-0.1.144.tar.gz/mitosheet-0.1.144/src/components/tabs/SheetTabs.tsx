// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { SheetShape } from '../../widget';
import SheetTab from './SheetTab';

// import css
import "../../../css/sheet-tab.css"
import { MitoAPI } from '../../api';

type SheetTabsProps = {
    setCurrOpenSheetTabActions: (sheetIndex: number | undefined) => void;
    currOpenSheetTabActions: number | undefined;
    mitoContainerRef: HTMLDivElement | undefined | null;
    dfNames: string[];
    sheetShapeArray: SheetShape[];
    selectedSheetIndex: number;
    setSelectedSheetIndex: (newIndex: number) => void;
    mitoAPI: MitoAPI;
    closeOpenEditingPopups: () => void;
};

/*
    Wrapper component that displays the entire bottom of the sheet, including
    the sheet tabs, as well as the shape of the currently selected dataframe.
*/
function SheetTabs(props: SheetTabsProps): JSX.Element {
    return (
        <div className='sheet-bottom'>
            <div className="sheet-tab-bar">
                {props.dfNames.map((dfName, idx) => {
                    return (
                        <SheetTab
                            setCurrOpenSheetTabActions={props.setCurrOpenSheetTabActions}
                            currOpenSheetTabActions={props.currOpenSheetTabActions}
                            key={idx}
                            mitoContainerRef={props.mitoContainerRef}
                            dfName={dfName}
                            sheetShape={props.sheetShapeArray[idx]}
                            sheetIndex={idx}
                            selectedSheetIndex={props.selectedSheetIndex}
                            setSelectedSheetIndex={props.setSelectedSheetIndex}
                            mitoAPI={props.mitoAPI}
                            closeOpenEditingPopups={props.closeOpenEditingPopups}
                        />
                    )
                })}
            </div>
            {props.sheetShapeArray[props.selectedSheetIndex] !== undefined && 
                <div className='sheet-shape'>
                    ({props.sheetShapeArray[props.selectedSheetIndex].rows}, {props.sheetShapeArray[props.selectedSheetIndex].cols})
                </div>
            }
        </div>
    );
}

export default SheetTabs;
