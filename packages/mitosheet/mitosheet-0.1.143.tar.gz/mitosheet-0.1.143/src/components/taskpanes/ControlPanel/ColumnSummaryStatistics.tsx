// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState, useEffect } from 'react';

// import css
import "../../../../css/margins.css";
import { MitoAPI } from '../../../api';

type ColumnDescribeChartProps = {
    selectedSheetIndex: number;
    columnHeader: string;
    mitoAPI: MitoAPI;
}

/*
    Displays the column summary statistics gotten from 
    a call to .describe

    See examples here: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.describe.html
*/
function ColumnSummaryStatistics(props: ColumnDescribeChartProps): JSX.Element {
    const [describe, setDescribe] = useState<Record<string, string>>({});
    const [loading, setLoading] = useState(true)

    async function loadDescribe() {
        const loadedDescribe = await props.mitoAPI.getColumnDescribe(props.selectedSheetIndex, props.columnHeader);
        setDescribe(loadedDescribe);
        setLoading(false);
    }

    useEffect(() => {
        void loadDescribe();
    }, [])

    return (
        <React.Fragment>
            <div className='filter-modal-section-title'>
                <p> Column Summary Statistics </p>
            </div>
            <div key={loading.toString()}>
                {!loading &&
                    <table className='column-describe-table-container'>
                        {Object.keys(describe).map(key => {
                            return (
                                <tr className='column-describe-table-row' key={key}>
                                    <th>
                                        {key}
                                    </th>
                                    <th>
                                        {/* We clip data at 15 letters for now */}
                                        {describe[key].substring(0, 15) + (describe[key].length > 15 ? '...' : '')}
                                    </th>
                                </tr>
                            )
                        })}
                    </table> 
                }
                {loading && 
                    <p>
                        Column Summary statistics are loading...
                    </p>
                }
            </div>
            
        </React.Fragment>
    );
}


export default ColumnSummaryStatistics;