// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useEffect, useState } from 'react';
import { ColumnType } from '../../Mito';

// import css
import "../../../../css/margins.css";
import "../../../../css/default-taskpane.css";
import "../../../../css/control-panel-taskpane.css"
import "../../../../css/column-graph-and-describe.css"

import { TaskpaneInfo } from '../taskpanes';
import { FilterType, FilterGroupType } from './filter/filterTypes';
import FilterCard from './filter/FilterCard';
import SortCard from './SortCard';
import ColumnSummaryGraph from './ColumnSummaryGraph';
import ColumnNameCard from './ColumnNameCard';
import { MitoAPI } from '../../../api';
import ColumnSummaryStatistics from './ColumnSummaryStatistics';
import ControlPanelTaskpaneTabs from './ControlPanelTaskpaneTabs';


type ControlPanelTaskpaneProps = {
    selectedSheetIndex: number,
    columnHeader: string,
    openEditingColumnHeader: boolean,
    filters: (FilterType | FilterGroupType)[],
    columnType: ColumnType;
    operator: 'And' | 'Or',
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void,
    mitoAPI: MitoAPI,
}


/*
    A modal that allows a user to rename, sort, and filter a column.
*/
function ControlPanelTaskpane(props: ControlPanelTaskpaneProps): JSX.Element {
    const [selectedTab, setSelectedTab] = useState(0);
    const [columnDtype, setColumnDtype] = useState('');

    async function loadColumnDtype() {
        const loadedColumnDtype = await props.mitoAPI.getColumnDtype(
            props.selectedSheetIndex, props.columnHeader
        );
        setColumnDtype(loadedColumnDtype);
    }

    useEffect(() => {
        void loadColumnDtype();
    }, [])

    const setSelectedTabCallback = (tabNumber: number): void => {
        setSelectedTab(tabNumber);
        if (tabNumber == 0) {
            void props.mitoAPI.sendLogMessage(
                'clicked_sort_and_filter_tab',
                {
                    'column_header': props.columnHeader
                }
            )
        } else {
            void props.mitoAPI.sendLogMessage(
                'clicked_summary_statistics_tab',
                {
                    'column_header': props.columnHeader
                }
            )
        }
    }

    return (
        <React.Fragment>
            <div className='control-panel-taskpane-container default-taskpane-div'>
                <ColumnNameCard
                    columnHeader={props.columnHeader}
                    openEditingColumnHeader={props.openEditingColumnHeader}
                    selectedSheetIndex={props.selectedSheetIndex}
                    mitoAPI={props.mitoAPI}
                    setCurrOpenTaskpane={props.setCurrOpenTaskpane}
                />
                <div>
                    dtype: {columnDtype}
                </div>
                {/* We add an extra margin to the bottom so filter items aren't cut off by the tabs */}
                <div className='default-taskpane-body-div mb-30px'>
                    {selectedTab === 0 &&
                    <React.Fragment>
                        <SortCard
                            selectedSheetIndex={props.selectedSheetIndex}
                            columnHeader={props.columnHeader} 
                            columnType={props.columnType} 
                            mitoAPI={props.mitoAPI}
                        />
                        <FilterCard
                            selectedSheetIndex={props.selectedSheetIndex}
                            columnHeader={props.columnHeader}
                            filters={props.filters}
                            columnType={props.columnType}
                            operator={props.operator}
                            mitoAPI={props.mitoAPI}
                        />
                    </React.Fragment>
                    }
                    {selectedTab === 1 &&
                    <React.Fragment>
                        <ColumnSummaryGraph
                            selectedSheetIndex={props.selectedSheetIndex}
                            columnHeader={props.columnHeader}
                            mitoAPI={props.mitoAPI}
                        />
                        <ColumnSummaryStatistics
                            selectedSheetIndex={props.selectedSheetIndex}
                            columnHeader={props.columnHeader}
                            mitoAPI={props.mitoAPI}
                        />
                    </React.Fragment>
                    }
                </div>
            </div> 
            {/* 
                We put the tabs outside the taskpane body so they aren't effected by the 
                margins that are on the taskpane body and can fill the whole container
            */}
            <ControlPanelTaskpaneTabs
                selectedTab={selectedTab}
                setSelectedTab={setSelectedTabCallback}
            />
        </React.Fragment>
    );
}

export default ControlPanelTaskpane;