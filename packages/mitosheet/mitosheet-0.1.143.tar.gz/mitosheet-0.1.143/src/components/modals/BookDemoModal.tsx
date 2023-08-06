// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { FormEvent } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';

// import css
import "../../../css/margins.css";
import "../../../css/default-modal.css"


/*
    A modal that asks the user to sign up for a demo
*/
const BookDemoModal = (
    props: {
        setModal: (modalInfo: ModalInfo) => void
        userEmail: string
    }): JSX.Element => {

    const bookDemo = (e: FormEvent<HTMLFormElement>): void => {
        // Prevent the page from reloading when the form submits
        e.preventDefault()

        // Open a new tab to the Hubspot demo booking screen w/ the email already filled in
        window.open(`https://meetings.hubspot.com/nate301/mito-early-access-check-in?utm_campaign=Mito&utm_source=in-app-demo-signup&email=${props.userEmail}`, '_blank')
        props.setModal({type: ModalEnum.None});
    }

    return (
        <div className='modal-container'>
            <div className='modal'>
                <div className='modal-header-text-div'>
                    <p>{'Help us Improve Mito'}</p>
                </div>
                <div className="modal-message">
                    <p>
                        Book an onboarding. Once we get to know you, we can help you with your analysis and build new features just for you! 
                    </p>
                    <div className='modal-buttons'>
                        <div className='modal-close-button modal-dual-button-left' onClick={() => {props.setModal({type: ModalEnum.None})}}> Close </div>
                        <form onSubmit={(e) => bookDemo(e)}>
                            <button className='modal-action-button' type='submit' autoFocus> {"Book a Demo"}</button>  
                        </form>
                    </div>
                </div>
            </div> 
        </div>
    );
};

export default BookDemoModal;