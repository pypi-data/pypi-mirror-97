// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

// import css
import "../../css/default-modal.css"
import "../../css/margins.css"

import { ModalEnum } from './Mito';


/*
    DefaultModal is a higher-order component that
    takes a modal and a header, and displays it as a component.

    The modal has props
    - a header string to be shown at the top of the modal
    - a modalType to indicate the font color of the header string
    - a viewComponent, a react fragment which is the center segment of the modal. 
        ie: an input field or text
    - a buttons component, react divs which have onclick functions to apply functions. 
        the modal is designed to take either 1 or 2 buttons where the left button is always 
        the close button. 
*/
const DefaultModal = (
    props: {
        header: string;
        modalType: ModalEnum
        viewComponent: React.ReactFragment;
        buttons: React.ReactFragment;
    }): JSX.Element => {

    const headerColor = props.modalType === ModalEnum.Error ? '#ED4747' : '#343434' 
    return (
        <div className='modal-container'>
            <div className='modal'>
                <div className='modal-header-text-div' style={{color: headerColor}}>
                    <p>{props.header}</p>
                </div>
                <div className="modal-message">
                    {props.viewComponent}
                </div>
                <div className="modal-buttons">
                    {props.buttons}       
                </div>
            </div> 
        </div>
    )
};

export default DefaultModal;