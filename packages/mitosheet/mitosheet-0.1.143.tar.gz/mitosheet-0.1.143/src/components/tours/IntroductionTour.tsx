// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import Joyride, { Step, CallBackProps, EVENTS, STATUS, ACTIONS } from 'react-joyride';

const steps: Step[] = [
    {
        // Step 0 
        title: 'Welcome to Mito!',
        content: <p>Do you want to take a short tour? I&apos;ll show you how
        to load some data into Mito.</p>,
        placement: 'top-start',
        target: '.mito-main-sheet-div',
        disableBeacon: true
    },
    {
        // Step 1
        content: <p>Import data to start your analysis.</p>,
        placement: 'right',
        target: '#tour-import-button-id',
        hideFooter: true
    },
    {
        // Step 2
        title: 'Importing Data',
        content: <p>Click the <b>Add File</b> button, <b>select a csv</b> from the dropdown, and then press <b>import.</b></p>,
        placement: 'left',
        target: '.modal',
        hideFooter: true
    },
    {
        // Step 3
        title: <p>&#127881; Congrats! &#127881;</p>,
        content: (
            <div>
                <p>You&apos;ve uploaded data to Mito. You&apos;re now ready to start automating your analyses. </p>
                <br></br>
                <p>Edit your data by writing formulas, sorting, filtering, and creating pivot tables.</p>
            </div>
        ),                
        placement: 'top',
        target: '.mito-main-sheet-div'
    },
]

type IntroductionTourProps = {
    run: boolean;
    isImportModalOpen: boolean;
    stepIndex: number;
    setTourInfo: (runTour: boolean, stepIndex: number) => void;
}

type IntroductionTourState = {
    isImportModalOpen: boolean;
    stepIndex: number;
}

class IntroductionTour extends React.Component<IntroductionTourProps, IntroductionTourState> {

    constructor(props: IntroductionTourProps) {
        super(props);

        this.state = {
            isImportModalOpen: props.isImportModalOpen,
            stepIndex: props.stepIndex
        }
        this.handleJoyrideCallback = this.handleJoyrideCallback.bind(this);
    }

    /* 
        Callback called when Joyride state changes. Because we have a controlled tour, 
        we need to manually update the step index.
    */
    private handleJoyrideCallback = (data: CallBackProps) => {
        const { index, type, status, action } = data;

        // if the tour is finished, skipped, or closed, turn off runTour and reset indexes
        if (([STATUS.FINISHED, STATUS.SKIPPED] as string[]).includes(status) || ACTIONS.CLOSE === action) {
            this.props.setTourInfo(false, 0);
            return;
        }

        let newIndex = index
                    
        // If the user presses the next button while on step 0, advance to step 1 
        if (index === 0 && EVENTS.STEP_AFTER === type) {
            newIndex = 1
            this.setState({ stepIndex: newIndex })
        } 
        
        // If the user is on step 1 and the import modal opens, advance to step 2 
        if (index == 1 && EVENTS.STEP_BEFORE === type && this.state.isImportModalOpen) {
            newIndex = 2
            this.setState({ stepIndex: newIndex})
        }

        // If the user is on step 2 and the import modal closes, advance to step 3
        if (index == 2 && !this.state.isImportModalOpen) {
            newIndex = 3
            this.setState({ stepIndex: newIndex})
        }

        // If the user is on step 3 and ends the tour, end the tour
        if (index === 3 && EVENTS.STEP_AFTER === type) {
            this.props.setTourInfo(false, 0);
            return
        } 

        // Register tour step index with Mito state
        this.props.setTourInfo(true, newIndex)
    }

    render (): JSX.Element {
        return (
            <Joyride
                run={this.props.run}
                steps={steps}
                stepIndex={this.state.stepIndex}
                continuous={true}
                showProgress={true}
                showSkipButton={true}
                hideBackButton={true}
                disableScrolling={this.props.run} // disable scrolling only when the tour is running
                disableOverlayClose={true} // When the user clicks outside of the tour, don't close it
                spotlightClicks={true} // Allow mouse and touch events thru the spotlight.
                callback={this.handleJoyrideCallback} // Use Callback to move from state to state
                styles={{
                    options: {
                        primaryColor: '#0081DE',
                        textColor: '#343434',
                    }
                }}
            />
        );
    }
}

export default IntroductionTour;

