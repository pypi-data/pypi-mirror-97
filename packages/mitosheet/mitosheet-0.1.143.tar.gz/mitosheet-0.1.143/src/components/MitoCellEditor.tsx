// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Component } from 'react';
import { ICellEditorParams } from 'ag-grid-community';
import { functionDocumentationObjects, FunctionDocumentationObject } from '../data/function_documentation';
import { getColumnHeaderSuggestions, getFunctionSuggestions, endsInColumnHeader } from '../utils/suggestions';

import DocumentationBox from './editor/DocumentationBox';
import SuggestionBox from './editor/SuggestionBox';

export type SuggestionType = 'function' | 'columnHeader'

export interface SuggestionItem {
    match: string,
    suggestion: string,
    subtitle: string,
    type: SuggestionType
}

type CellEditorState = {
    formula: string,
    input: HTMLInputElement | null,
    suggestionIndex: number
};

type CellEditorProps = ICellEditorParams & {
    setEditingMode: (on: boolean, column: string, rowIndex: number) => void
    setEditingFormula: (formula: string) => void,
    setCursorIndex: (index: number) => void,
    cursorIndex: number,
    formula: string,
    columns: string[]
}

const keyboardKeys = {
    ENTER_KEY: "Enter",
    TAB_KEY: "Tab",
    ESCAPE_KEY: "Escape",
    UP: 'ArrowUp',
    DOWN: 'ArrowDown',
    LEFT: 'ArrowLeft',
    RIGHT: 'ArrowRight',
    // These events have IE/Edge differences
    IE_UP: 'Up',
    IE_DOWN: 'Down',
    IE_LEFT: 'Left',
    IE_RIGHT: 'Right'
}

export const TAKE_SUGGESTION_KEYS = [keyboardKeys.ENTER_KEY, keyboardKeys.TAB_KEY];
const CLOSE_INPUT_KEYS = [keyboardKeys.ENTER_KEY, keyboardKeys.TAB_KEY, keyboardKeys.ESCAPE_KEY];
export const ARROW_UP_KEYS = [keyboardKeys.UP, keyboardKeys.IE_UP];
export const ARROW_DOWN_KEYS = [keyboardKeys.DOWN, keyboardKeys.IE_DOWN];
export const ARROW_LEFT_KEYS = [keyboardKeys.LEFT, keyboardKeys.IE_LEFT];
export const ARROW_RIGHT_KEYS = [keyboardKeys.RIGHT, keyboardKeys.IE_RIGHT];


export default class MitoCellEditor extends Component<CellEditorProps, CellEditorState> {
    constructor(props: CellEditorProps) {
        super(props);

        /*
     We turn editing mode on first to ensure that any future calls to 
     set editing formula set the formula of the correct column.
    */
        const column = props.colDef.field ? props.colDef.field : "";
        props.setEditingMode(true, column, props.rowIndex);

        // Set the editor's state
        if (props.charPress != null) {

            /* 
      The charPress param is used to tell the cell editor which character was pressed to enter cell editing mode. 
      When the cell editor is entered through a charPress, we overwrite the formula to the character pressed
      */
            props.setEditingFormula(props.charPress);

            this.state = {
                formula: props.charPress,
                input: null,
                suggestionIndex: 0
            }
        } else {
            // otherwise keep the original value
            this.state = {
                formula: props.formula,
                input: null,
                suggestionIndex: 0
            }
        }

        this.getValue = this.getValue.bind(this);
        this.isPopup = this.isPopup.bind(this);
        this.handleOnChange = this.handleOnChange.bind(this);
        this.afterGuiAttached = this.afterGuiAttached.bind(this);
        this.getCurrentSuggestions = this.getCurrentSuggestions.bind(this);
        this.getDocumentationBoxFunction = this.getDocumentationBoxFunction.bind(this);
        this.onKeyDown = this.onKeyDown.bind(this);
        this.onClick = this.onClick.bind(this);
        this.onMouseEnterSuggestion = this.onMouseEnterSuggestion.bind(this);
        this.selectSuggestion = this.selectSuggestion.bind(this);
        this.getAdjustedIndex = this.getAdjustedIndex.bind(this);
    }

    getValue(): string {
        return this.state.formula;
    }

    /*
    set the cursor location so that if the user uses mouse to reference 
    column, we append the column to the correct location
  */
    // eslint-disable-next-line @typescript-eslint/no-inferrable-types
    updateCursorIndex(adjustment: number): void {
        if (this.state.input?.selectionEnd) {
            this.props.setCursorIndex(this.state.input?.selectionEnd + adjustment)
        }
    }

    /* Make the cell editor a popup, so we can display suggestion/documentation box */ 
    isPopup(): boolean {
        return true;
    }

    /* update the cell value while typing */
    handleOnChange(event: React.ChangeEvent<HTMLInputElement>): void {
        this.updateFormulaState(event.target.value)
        this.updateCursorIndex(0);
    }

    /* 
    this function updates the state of both the mitoCelEditor formula and the formulaBar
    of in Mito.tsx. We update in both locations so that the formula can persist across
    opening and closing the cell editor
  */
 
    updateFormulaState(newFormula: string): void {
        this.setState({
            formula: newFormula
        }, () => {
            this.props.setEditingFormula(this.state.formula);
        });
    }
  

    /*
    This function is called by ag-grid after this component
    is rendered; we simply focus on the input feild rendered
    below so the user can begin typing immediately!

    NOTE: There is a bug that requires us to also call focus 
    _after_ we define the ref in the setState callback. For some reason,
    the ref is not always defined after the gui is attached - and so
    we need to focus then as well!
  */
    afterGuiAttached(): void {
        this.state.input?.focus();

        // when the cell editor loads, set the Cursor (cursor) to be in the last position it was in
        // if the cell editor was just closed
        this.state.input?.setSelectionRange(this.props.cursorIndex, this.props.cursorIndex)
    }

    /* when the user clicks to move the Cursor, update the Cursor location*/
    onClick(): void {
        this.updateCursorIndex(0)
    }

    /*
    This function handles key presses on the cell editor input.

    If the suggestion box is open currently, than this function first checks 
    if this key press effects the suggestion box (e.g. scrolling or selecting a suggestion).

    Otherwise, we check if this event closes the cell editor.

    NOTE: we event.preventDefault() to stop events from having unintended
    consequences if they cause effects we handle ourselves. For example, this
    prevents TAB from selecting the next form field.

    NOTE: the events handled by this functions should correspond to the events 
    suppressed in editing mode in the ag-grid, to avoid unintended behavior
  */
    onKeyDown(event: React.KeyboardEvent<HTMLInputElement>): void {

        /* 
      if the arrow keys are used to move the Cursor location, update the cursor location

      Note: Idk why, but when moving the cursor with the arrow keys, there is a one index lag
      in the direction the cursor is moving. ie: if moving to the left, the index will be 1 higher than 
      it should be. We work around this by using the adjustments passed as params to the updateCursorIndex function below. 
    */
        if (ARROW_LEFT_KEYS.includes(event.key)) {
            this.updateCursorIndex(-1);
        } else if (ARROW_RIGHT_KEYS.includes(event.key)) {
            this.updateCursorIndex(1);
        } 
    
        const suggestions = this.getCurrentSuggestions();
        if (suggestions !== undefined) {
            if (TAKE_SUGGESTION_KEYS.includes(event.key)) {
                event.preventDefault();
                // We mod below just as one last safety check for an out of bound index, which we
                // also ensure with the getAdjustedIndex function
                const selectedSuggestion = suggestions[this.state.suggestionIndex % suggestions.length];
                const restOfSuggestion = selectedSuggestion.suggestion.substring(selectedSuggestion.match.length);
                return this.selectSuggestion(selectedSuggestion.match, restOfSuggestion, selectedSuggestion.type);
            } else if (ARROW_UP_KEYS.includes(event.key)) {
                event.preventDefault();
                return this.setState((prevState) => {
                    return {suggestionIndex: this.getAdjustedIndex(prevState.suggestionIndex - 1, suggestions)};
                });
            } else if (ARROW_DOWN_KEYS.includes(event.key)) {
                event.preventDefault();
                return this.setState((prevState) => {
                    return {suggestionIndex: this.getAdjustedIndex(prevState.suggestionIndex + 1, suggestions)};
                });
            } 
        }
    
        // NOTE: we should always check the close events _last_, in case the keypresses
        // were trying to do other things!
        if (CLOSE_INPUT_KEYS.includes(event.key)) {
            event.preventDefault();
            this.props.setEditingMode(
                false, 
                this.props.column.getColId(), 
                this.props.rowIndex
            );
        }
    }

    /*
    This function returns the current suggestions, which are:
    2. Any column who is prepended by the current ending string, which may not be all alphabetic 
    characters (and can be any valid column). 
    1. Any functions who are prepended by the current ending string, which
    must be all alphabetic characters. Case-insensitive.
    
    Returns undefined if there are no suggestions, or if the end of the formula 
    is a perfect column match - so the user can submit in this case!
  */
    getCurrentSuggestions(): SuggestionItem[] | undefined {

        if (typeof this.state.formula === 'string') {
            // If you have a column header that is matched exactly, we _do show no suggestions_, as 
            // we want you to be able to enter it in
            if (endsInColumnHeader(this.state.formula, this.props.columns)) {
                return undefined;
            }

            const columnHeaderSuggestions = getColumnHeaderSuggestions(this.state.formula, this.props.columns);
            const functionSuggestions = getFunctionSuggestions(this.state.formula);

            const suggestions: SuggestionItem[] = [];
            // Add the column headers first, then the functions
            if (columnHeaderSuggestions !== undefined) {
                suggestions.push(...columnHeaderSuggestions);
            }
            if (functionSuggestions !== undefined) {
                suggestions.push(...functionSuggestions);
            }
            if (suggestions.length > 0) {
                return suggestions;
            }

        }

        return undefined;
    }

    /*
    Keeps the selected index for the suggestion box inbounds; the index
    should be the index of one of the suggestions!
  */
    getAdjustedIndex(
        index: number, 
        suggestions: SuggestionItem[] 
    ): number {

        // Fancy expression to keep it as a valid index
        return Math.min(Math.max(0, index), suggestions.length - 1);
    }

    /*
    This function returns the current function that should
    be displayed in the documentation box, based on if the
    documentation box open condition is met. 

    If the documentation box open condition is not met, this 
    returns undefined. 
  */
    getDocumentationBoxFunction(): FunctionDocumentationObject | undefined {
    // Finds all instances of functions that are not followed by a closing paren
    // e.g. all functions that are still being edited.
        const docBoxRe = /[A-Za-z]+\((?![^)]*\))/g;

        if (typeof this.state.formula == 'string') {
            const functionMatches = this.state.formula?.match(docBoxRe);
            if (!functionMatches) {
                return undefined;
            }
            // We take the _last_ function that has been written, as this is the funciton
            // being edited currently.
            const lastFunction = functionMatches[functionMatches.length - 1];
            // Strip off the last ( from the function name
            const lastFunctionClean = lastFunction.substring(0, lastFunction.length - 1).toUpperCase();

            return functionDocumentationObjects.find((funcDocObject) => {
                return funcDocObject.function === lastFunctionClean;
            });
        }
        return undefined;
    }

    // If you mouseover a suggestion, this selects it
    onMouseEnterSuggestion(suggestionIndex: number): void {
        this.setState({suggestionIndex: suggestionIndex})
    }

    selectSuggestion(endingString: string, restOfSuggestion: string, type: SuggestionType): void {
    // We fill in the rest of the suggestion, and reset the suggestion box
        const stripped = this.state.formula.substring(0, this.state.formula.length - endingString.length);
        let newFormula;
        if (type === 'function') {
            // Upper case, add paren, if a function
            newFormula = stripped + endingString.toUpperCase() + restOfSuggestion.toUpperCase() + '(';
        } else {
            // Just add column header, if column header
            newFormula = stripped + endingString + restOfSuggestion;
        }

        this.updateFormulaState(newFormula);

        this.setState({
            suggestionIndex: 0
        }, () => {
            // TODO: add documentation about when this runs... (A close?)
            // We also refocus on the input feild
            this.state.input?.focus();
            // And then make sure the cursor index is at the right location
            this.updateCursorIndex(0);
        })
    }
  
    render(): JSX.Element {
        const suggestions = this.getCurrentSuggestions();
        const documentationBoxFunction = this.getDocumentationBoxFunction();

        return (
            <div>
                <input 
                    ref={(input) => {
                        if (!this.state.input) {
                            this.setState({input: input}, () => {
                                // See note in afterGuiAttached. This is a workaround that makes sure 
                                // the input is always focused on after it is displayed to the user. 
                                // Possibly related: https://stackoverflow.com/questions/44074747/componentdidmount-called-before-ref-callback
                                this.state.input?.focus()
                            })
                        }
                    }}
                    className="mito-cell-editor ag-cell-inline-editing"
                    name="value" 
                    autoComplete="off"
                    value={this.state.formula} 
                    onChange={this.handleOnChange} 
                    onKeyDown={this.onKeyDown}
                    onClick={this.onClick}
                    tabIndex={1}/>
                {
                    suggestions !== undefined &&
          <SuggestionBox
              suggestions={suggestions}
              index={this.state.suggestionIndex}
              onMouseEnterSuggestion={this.onMouseEnterSuggestion}
              onSelectSuggestion={this.selectSuggestion}
          />
                }
                { /* Note: the suggestion box _always_ takes precendence over the documentation box */
                    suggestions === undefined && documentationBoxFunction &&
          <DocumentationBox
              funcDocObject={documentationBoxFunction}
          />
                }
            </div>
        );
    }
}