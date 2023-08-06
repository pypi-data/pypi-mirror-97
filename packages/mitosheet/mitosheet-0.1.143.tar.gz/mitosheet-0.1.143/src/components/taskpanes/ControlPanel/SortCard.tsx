// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { ColumnType } from '../../Mito';

// import css
import "../../../../css/margins.css";
import { MitoAPI } from '../../../api';

export enum SortDirection {
    ASCENDING = 'ascending',
    DESCENDING = 'descending',
    NONE = 'none'
}

type SortCardProps = {
    selectedSheetIndex: number;
    columnHeader: string;
    columnType: ColumnType;
    mitoAPI: MitoAPI;
}

interface SortCardState {
    sortDirection: SortDirection,
    stepID: string
}

/*
    A modal that allows a user to sort a column
*/
class SortCard extends React.Component<SortCardProps, SortCardState> {

    constructor(props: SortCardProps) {
        super(props);

        this.state = {
            sortDirection: SortDirection.NONE,
            stepID: ''
        }

        this.sendSortUpdateMessage = this.sendSortUpdateMessage.bind(this);
        this.setSortDirection = this.setSortDirection.bind(this);
    }

    setSortDirection = (sortDirection: SortDirection): void => {
        // if the user toggled the button that was already selected, turn off the sort
        if (sortDirection == this.state.sortDirection) {
            this.setState({
                sortDirection: SortDirection.NONE
            });
            return;
        } 

        // otherwise the user selected a new direction, so set that as the sortDirection
        this.setState({
            sortDirection: sortDirection
        }, () => {
            // then sort the column
            void this.sendSortUpdateMessage()
        });
    }

    sendSortUpdateMessage = async (): Promise<void> => {
        // sort the columns if the sortDirection is not None
        if (this.state.sortDirection != SortDirection.NONE) {

            const stepID = await this.props.mitoAPI.sendSortMessage(
                this.props.selectedSheetIndex,
                this.props.columnHeader,
                this.state.sortDirection,
                this.state.stepID,
            )

            this.setState({stepID: stepID})
        }
    }

    render(): JSX.Element {

        // determine css styling of sort buttons
        const ascendingButtonClass = this.state.sortDirection == SortDirection.ASCENDING ? 'sort-button sort-button-selected' : 'sort-button sort-button-unselected';
        const descendingButtonClass = this.state.sortDirection == SortDirection.DESCENDING ? 'sort-button sort-button-selected' : 'sort-button sort-button-unselected';

        return (
            <div>
                <div className='filter-modal-section-title'>
                    <p> Sort </p>
                </div>
                <div className="filter-modal-centering-container">
                    <div className='sort-buttons-div'>
                        <button 
                            className={ascendingButtonClass}
                            onClick={() => this.setSortDirection(SortDirection.ASCENDING)}> 
                                Ascending 
                        </button>
                        <button 
                            className={descendingButtonClass}
                            onClick={() => this.setSortDirection(SortDirection.DESCENDING)}>
                                    Descending 
                        </button>
                    </div>
                </div>
            </div>
        );
    }
}


export default SortCard;