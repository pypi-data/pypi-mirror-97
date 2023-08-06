// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';

// import css
import "../../../css/margins.css";
import "../../../css/default-modal.css"
import DefaultModal from '../DefaultModal';
import { MitoAPI } from '../../api';

/*
    A modal that appears and tells the user to upgrade to the 
    new version of Mito, by going to the documentation
*/
const UpgradeModal = (props: {
    setModal: (modalInfo: ModalInfo) => void,
    mitoAPI: MitoAPI
}): JSX.Element => {

    const onUpgrade = (): void => {

        // We log the opening of the documentation taskpane
        void props.mitoAPI.sendLogMessage(
            'upgrade_button_clicked'
        );

        // Open the upgrading docs
        window.open(`https://docs.trymito.io/`, '_blank')
        props.setModal({type: ModalEnum.None});
    }

    return (
        <DefaultModal
            header={`Upgrade for New Functionality`}
            modalType={ModalEnum.Upgrade}
            viewComponent= {
                <Fragment>
                    <p>
                        The Mito team moves fast. Since you last updated, we’ve added a bunch of shiny new things to play with, and polished the old stuff. Upgrade now to try it out!                    
                    </p>
                </Fragment>
            }
            buttons = {
                <Fragment>
                    <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                    <div className='modal-action-button modal-dual-button-right' onClick={onUpgrade}> Upgrade</div>
                </Fragment>
            }
        />
    );
};

export default UpgradeModal;