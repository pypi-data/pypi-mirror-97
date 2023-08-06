// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState, useEffect } from 'react';

// import css
import "../../../../css/margins.css";
import { MitoAPI } from '../../../api';


type ColumnSummaryGraphProps = {
    selectedSheetIndex: number;
    columnHeader: string;
    mitoAPI: MitoAPI;
}

/*
    Displays the column summary graph in the column control panel
*/
function ColumnSummaryGraph(props: ColumnSummaryGraphProps): JSX.Element {
    const [base64PNGImage, setBase64PNGImage] = useState('');
    const [alt, setAlt] = useState('Graph is loading...');

    async function loadBase64PNGImage() {
        const loadedBase64PNGImage = await props.mitoAPI.getColumnSummaryGraph(props.selectedSheetIndex, props.columnHeader);
        if (loadedBase64PNGImage === '') {
            setAlt('Sorry, it looks like there are too many items in this column to display them well.')
            await props.mitoAPI.sendLogMessage('too_many_items_to_display_graph')
        } else {
            setBase64PNGImage(loadedBase64PNGImage);
        }
    }

    useEffect(() => {
        void loadBase64PNGImage();
    }, [])

    return (
        <React.Fragment>


            <div className='filter-modal-section-title'>
                <p> Column Summary Graph </p>

                {base64PNGImage !== '' &&
                    <div>
                        <a 
                            className='mr-30px'
                            href={'data:image/png;base64, ' + base64PNGImage}
                            download={props.columnHeader + '-frequency-graph.png'}
                            onClick={() => {
                                // We log the download of the graph
                                void props.mitoAPI.sendLogMessage('click_download_column_summary_graph', {
                                    'column_header': props.columnHeader
                                });
                            }}
                        > 
                            <svg width="20" height="16" viewBox="0 0 20 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect x="0.384615" y="8.077" width="0.769231" height="6.92308" fill="#C4C4C4" stroke="#343434" strokeWidth="0.769231"/>
                                <rect x="18.4615" y="7.69238" width="1.53846" height="7.69231" fill="#343434"/>
                                <rect x="20" y="13.8462" width="1.53846" height="20" transform="rotate(90 20 13.8462)" fill="#343434"/>
                                <path d="M9.46967 12.0688C9.76256 12.3617 10.2374 12.3617 10.5303 12.0688L15.3033 7.29582C15.5962 7.00293 15.5962 6.52805 15.3033 6.23516C15.0104 5.94227 14.5355 5.94227 14.2426 6.23516L10 10.4778L5.75736 6.23516C5.46447 5.94227 4.98959 5.94227 4.6967 6.23516C4.40381 6.52805 4.40381 7.00293 4.6967 7.29582L9.46967 12.0688ZM9.25 0V11.5385H10.75V0L9.25 0Z" fill="#343434"/>
                            </svg>
                        </a>
                    </div>
                }
            </div>

            <img className='mb-2' src={'data:image/png;base64, ' + base64PNGImage} alt={alt}/>

        </React.Fragment>
    );
}


export default ColumnSummaryGraph;