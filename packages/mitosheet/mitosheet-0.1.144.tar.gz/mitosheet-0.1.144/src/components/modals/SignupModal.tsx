// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { ModalEnum, ModalInfo } from '../Mito';

// import css
import "../../../css/margins.css";
import "../../../css/default-modal.css"
import { MitoAPI } from '../../api';
import { useState } from 'react';


/*
    A modal that requests the user's email to sign up
*/
const SignUpModal = (
    props: {
        setModal: (modalInfo: ModalInfo) => void,
        mitoAPI: MitoAPI
    }): JSX.Element => {

    const [userEmail, setUserEmail] = useState('');

    const signUp = async (): Promise<void> => {
        await props.mitoAPI.sendSignUp(userEmail);

        props.setModal({type: ModalEnum.BookDemo, userEmail: userEmail});
    }

    return (
        <div className='modal-container'>
            <div className='modal'>
                <div className='modal-header-text-div'>
                    <p>{'Sign Up to Get Started with Mito'}</p>
                </div>
                <div className="modal-message">
                    <form onSubmit={signUp}>
                        <div>
                            <p className='modal-input-label'>Email</p>
                            <input 
                                className="modal-input"
                                type="email" 
                                placeholder='example@gmail.com' 
                                value={userEmail} 
                                onChange={(e) => setUserEmail(e.target.value)} 
                                required
                                autoFocus />
                            <p className='mt-2'>
                                We&apos;ll only email you about Mito. We&apos;ll send you information about new features and your free trial. We&apos;ll never share you email with anyone! 
                            </p>
                        </div>
                        <div className='modal-buttons'>
                            <button className='modal-action-button' type='submit'> {"Sign Up"}</button>  
                        </div>
                    </form>
                </div>
            </div> 
        </div>
    );
};

export default SignUpModal;