// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';
import DefaultModal from '../DefaultModal';

// import css
import "../../../css/margins.css";
import "../../../css/delete-column-modal.css";
import { MitoAPI } from '../../api';


/*
    A modal that confirms that you want to delete a column.
*/
const DeleteColumnModal = (
    props: {
        setModal: (modalInfo: ModalInfo) => void,
        columnHeader: string,
        selectedSheetIndex: number,
        mitoAPI: MitoAPI
    }): JSX.Element => {

    const deleteColumn = async (): Promise<void> => {
        await props.mitoAPI.sendDeleteColumn(
            props.selectedSheetIndex,
            props.columnHeader
        )

        props.setModal({type: ModalEnum.None});
    }

    return (
        <DefaultModal
            header={`Do you want to delete column ${props.columnHeader}?`}
            modalType={ModalEnum.RepeatAnalysis}
            viewComponent={<Fragment/>}
            buttons = {
                <Fragment>
                    <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                    <div className='modal-action-button modal-dual-button-right' onClick={deleteColumn}> {"Delete Column"}</div>
                </Fragment>
            }
        />
    );
};

export default DeleteColumnModal;