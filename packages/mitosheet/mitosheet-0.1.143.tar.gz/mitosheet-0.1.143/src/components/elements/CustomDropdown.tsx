// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useEffect, useRef } from 'react';

import '../../../css/custom-dropdown.css';


// Adapted from https://stackoverflow.com/questions/54560790/detect-click-outside-react-component-using-hooks
function useComponentVisible(closeDropdown: () => void) {
    const ref = useRef<null | HTMLDivElement>(null);

    const handleClickOutside = (event: any) => {
        // We check if the current click is outside the element, and call close if so
        if (ref.current && !ref.current.contains(event.target)) {
            /* 
                We delay actually closing by 100 seconds, just in case the user has clicked
                outside the dropdown, but on the button that closes the dropdown itself. This 
                makes sure that we don't close and then immediately reopen the component.

                It is an ugly hack, but it appears to work for now!
            */
            setTimeout(() => {
                closeDropdown();
            }, 100)
            
        }
    };

    useEffect(() => {
        document.addEventListener('click', handleClickOutside, true);
        return () => {
            document.removeEventListener('click', handleClickOutside, true);
        };
    });

    return { ref };
}

type CustomDropdown = {
    closeDropdown: () => void;
    children: React.ReactNode;
}


/* 
    A custom dropdown item that performs similarly to a select, in that
    when it is displayed, if the user clicks anywhere other than selecting
    one of the options, it will close. 

    SOME NOTES:
    1. Currently, the way that this is placed is very manual, and won't work
       when this component will need to be reused. We'll have to make it's 
       placement a parameter to this component!
    2. The div that this CustomDropdown is a child of must have non-static positioning,
       so that this will scroll with it!
*/
function CustomDropdown(props: CustomDropdown): JSX.Element {
    const { ref } = useComponentVisible(props.closeDropdown);

    return (
        <React.Fragment>
            <div className='custom-dropdown' ref={ref}>
                {props.children}
            </div>
        </React.Fragment>
        
    );
}

export default CustomDropdown;