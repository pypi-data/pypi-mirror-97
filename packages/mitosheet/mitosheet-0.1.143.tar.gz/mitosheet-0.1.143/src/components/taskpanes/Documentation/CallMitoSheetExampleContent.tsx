// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { useState } from 'react';

// Import Components 
import Tooltip from '../../Tooltip';

import '../../../../css/documentation-basic-example.css';


/*
    Returns a documentation entry for displaying your first
    mito sheet - with copyable Python code!
*/
const CallMitoSheetExampleContent = (): JSX.Element => {

    const [copyStatus, setCopyStatus] = useState('Click to copy!');

    const copyToClipBoard = () => {
        // We create a temporary element to make copying to the clipboard easy!
        const elem = document.createElement("textarea");
        document.body.appendChild(elem);
        elem.value = 'import pandas as pd\nimport mitosheet\ndf = pd.DataFrame(data={\'Data\': [\'ABC\', \'DEF\']})\nmitosheet.sheet(df)';
        elem.select();
        document.execCommand("copy");
        document.body.removeChild(elem);

        setCopyStatus('Copied!');
    }

    return (        
        <React.Fragment>
            <div className='documentation-basic-example-title'>
                Basic Example Documentation
            </div>
            <p>
                To edit a Mito sheet, you first have to display your data inside one!
            </p>
            <div className='documentation-basic-example-section-title'>
                Instructions
            </div>
            <p>
                Copy the following code into a cell in your notebook, and run it:
            </p>
            <div className='documentation-basic-example-python'>
                <div className='documentation-basic-example-python-code mb-1' onClick={copyToClipBoard} onMouseLeave={() => {setCopyStatus('Click to copy!')}}>
                    {/* NOTE: If you change this code, make sure to update the code that is copied in copyToClipBoard! */}
                    <div>
                        import pandas as pd
                    </div>
                    <div>
                        import mitosheet
                    </div>
                    <div>
                        df = pd.DataFrame(data={'{'}&apos;Data&apos;: [&apos;ABC&apos;, &apos;DEF&apos;]{'}'}
                    </div>
                    <div>
                        mitosheet.sheet(df)
                    </div>
                </div>
                <Tooltip tooltip={copyStatus}/>
            </div>
        </React.Fragment>
    );    
};

export default CallMitoSheetExampleContent;