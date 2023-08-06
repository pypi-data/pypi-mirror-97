// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

// import css
import "../../../../css/margins.css"
import "../../../../css/column-header-modal.css";
import "../../../../css/column-name-card.css"

import TaskpaneError from '../TaskpaneError';
import { TaskpaneInfo, TaskpaneType } from '../taskpanes';
import { MitoAPI } from '../../../api';
import { isValidHeader, getHeaderErrorMessage } from './renameUtils';


type ColumnNameCardProps = {
    columnHeader: string,
    openEditingColumnHeader: boolean
    selectedSheetIndex: number
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void,
    mitoAPI: MitoAPI
}

interface ColumnNameCardState {
    columnHeader: string,
    unsubmittedNewColumnHeader: string,
    invalidInputError: string,
    isRename: boolean,
    stepID: string
}

/*
    A modal that allows a user to sort a column
*/
class ColumnNameCard extends React.Component<ColumnNameCardProps, ColumnNameCardState> {

    constructor(props: ColumnNameCardProps) {
        super(props);

        this.state = {
            columnHeader: props.columnHeader,
            unsubmittedNewColumnHeader: props.columnHeader,
            invalidInputError: '',
            isRename: props.openEditingColumnHeader,
            stepID: ''
        }

        this.setColumnHeader = this.setColumnHeader.bind(this);
        this.updateUnsubmittedNewColumnHeader = this.updateUnsubmittedNewColumnHeader.bind(this);
        this.setInvalidInputError = this.setInvalidInputError.bind(this);
        this.setIsRename = this.setIsRename.bind(this);
    }

    setColumnHeader(columnHeader: string): void {
        this.setState({
            columnHeader: columnHeader
        });
    }

    setInvalidInputError(errorMessage: string): void {
        this.setState({
            invalidInputError: errorMessage
        });
    }

    setIsRename(isRename: boolean): void {
        this.setState(prevState => {
            return {
                isRename: isRename,
                unsubmittedNewColumnHeader: prevState.columnHeader
            }
        })
    }

    updateUnsubmittedNewColumnHeader = (e: React.ChangeEvent<HTMLInputElement>): void => {
        const newColumnHeader = e.target.value;
        // Update the saved unsubmittedColumnHeader
        this.setState({
            unsubmittedNewColumnHeader: newColumnHeader
        });
        // Display an error message, if it has one
        this.setInvalidInputError(getHeaderErrorMessage(newColumnHeader));
    }

    changeColumnHeader = async (): Promise<void> => {
        if (!isValidHeader(this.state.unsubmittedNewColumnHeader)) {
            // We make sure the new column header is a valid mito column,
            // and we don't allow the user to submit if it's not! 
            // We also update the error to tell them to fix the issue.
            this.setInvalidInputError(
                `Please fix issues before submitting: ${getHeaderErrorMessage(this.state.unsubmittedNewColumnHeader)}`
            );
            return;
        }

        // If the column header did not change, just stop renaming without updating the name to avoid error
        if (this.state.columnHeader == this.state.unsubmittedNewColumnHeader) {
            this.setState({
                isRename: false
            })
            return;
        }

        const stepID = await this.props.mitoAPI.sendRenameColumn(
            this.props.selectedSheetIndex,
            this.state.columnHeader,
            this.state.unsubmittedNewColumnHeader,
            this.state.stepID
        );

        this.setState(prevState => {
            return {
                stepID: stepID,
                isRename: false,
                columnHeader: prevState.unsubmittedNewColumnHeader,
                unsubmittedNewColumnHeader: prevState.unsubmittedNewColumnHeader
            }
        });

        this.props.setCurrOpenTaskpane({type: TaskpaneType.CONTROL_PANEL, columnHeader: this.state.columnHeader, openEditingColumnHeader: false});
    }

    render (): JSX.Element {
        return (
            <div className='column-name-card-container'>
                <div className='default-taskpane-header-div'>
                    <div className='column-name-card-column-name-div' onClick={() => {
                        if (!this.state.isRename) {
                            this.setIsRename(!this.state.isRename); 
                            this.setInvalidInputError('');
                        }
                    }}>
                        {this.state.isRename && 
                            <form 
                                onSubmit={(e) => {e.preventDefault(); void this.changeColumnHeader()}}
                                onBlur={(e) => {e.preventDefault(); void this.changeColumnHeader()}}>
                                <input 
                                    type='text'
                                    className='column-name-card-input-text'
                                    value={this.state.unsubmittedNewColumnHeader} 
                                    onChange={(e) => {this.updateUnsubmittedNewColumnHeader(e)}}
                                    autoFocus
                                />
                            </form>
                        }
                        {!this.state.isRename &&
                            <p className='column-name-card-column-header'>
                                {this.state.columnHeader} 
                            </p>
                        }
                    </div>
                    <div className='default-taskpane-header-exit-button-div' onClick={() => this.props.setCurrOpenTaskpane({type: TaskpaneType.NONE})}>
                        <svg width="18" height="18" viewBox="0 0 13 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <line x1="0.707107" y1="1.29289" x2="11.3136" y2="11.8994" stroke="#343434" strokeWidth="2"/>
                            <line x1="0.7072" y1="11.8995" x2="11.3137" y2="1.29297" stroke="#343434" strokeWidth="2"/>
                        </svg>
                    </div>
                </div>
                <TaskpaneError
                    message={this.state.invalidInputError}
                />
            </div>
        );
    }
    
}

export default ColumnNameCard;