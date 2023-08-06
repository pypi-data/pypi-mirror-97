// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import { SuggestionItem } from '../components/MitoCellEditor'
import { functionDocumentationObjects } from '../data/function_documentation';

/*
    Gets the prefix of any possible column headers at the end of the formula. E.g.

    - header -> header
    - header_123 -> header_123
    - function(header_123 -> header_123
    - func(data, 100 -> undefined
*/
export function getEndingColumnHeader(formula: string): string | undefined {
    /* 
        Returns the maximal column header at the end of the formula, 
        that meets the column_header validity condition.
    */
   
    let i = formula.length;
    for (i; i--; i >= 0) {
        const char = formula[i];
        if (!char.match(/[0-9A-Za-z_]+/g)) {
            // Stop as soon as we find a character that can't be in a column header
            break;
        }
    }
    const possibleColumnHeader = formula.substr(i + 1)

    return possibleColumnHeader.length === 0 ? undefined : possibleColumnHeader;
}

/*
    Returns true iff the formula has a column header as a suffix.
*/
export function endsInColumnHeader(
    formula: string, 
    columns: (string | number)[]
): boolean {
    const endingColumnHeader = getEndingColumnHeader(formula);
    if (endingColumnHeader === undefined) {
        return false;
    }

    return columns.findIndex((columnHeader) => columnHeader === endingColumnHeader) >= 0;
}

/*
    Returns a list of suggestions for column headers to append onto the given
    formula. These column headers must be prefixed by the ending column header.
    Case sensitive.

    Returns undefined if there are no suggestions.
*/
export function getColumnHeaderSuggestions(
    formula: string, 
    columns: (string | number)[]
): SuggestionItem[] | undefined {
    const endingColumnHeader = getEndingColumnHeader(formula);
    if (endingColumnHeader === undefined) {
        return undefined;
    }

    const matchingColumnHeaders = columns.filter((columnHeader) => {
        return (typeof columnHeader == 'string') && (columnHeader.startsWith(endingColumnHeader));
    }) as string[];
    const suggestions: SuggestionItem[] = matchingColumnHeaders.map(columnHeader => {
        return {
            match: endingColumnHeader,
            suggestion: columnHeader as string,
            subtitle: 'A column in this sheet.',
            type: 'columnHeader'
        }
    });
    if (suggestions.length == 0) {
        return undefined;
    }

    return suggestions;
}

/*
    Gets the prefix of any function at the end of the formula. E.g.

    - func -> func
    - func123 -> undefined
    - function(newfunc -> newfunc
*/
export function getEndingFunction(formula: string): string | undefined {
    /* 
        Returns the maximal formula at the end of the formula. 
    */
   
    let i = formula.length;
    for (i; i--; i >= 0) {
        const char = formula[i];
        if (!char.match(/[A-Za-z]+/g)) {
            // Stop as soon as we find a character that can't be in a column header
            break;
        }
    }
    const possibleFunction = formula.substr(i + 1)

    return possibleFunction.length === 0 ? undefined : possibleFunction;
}

/*
    Returns all the function suggestions for the given formula, which
    it matches at the end of the formula. Case insensitive.
*/
export function getFunctionSuggestions(
    formula: string
): SuggestionItem[] | undefined {
    const endingFunction = getEndingFunction(formula);
    if (endingFunction === undefined) {
        return undefined;
    }

    const matchingFunctionDocObjects = functionDocumentationObjects.filter((funcDocObject) => {
        return funcDocObject.function.startsWith(endingFunction.toUpperCase())
    });
    const suggestions: SuggestionItem[] = matchingFunctionDocObjects.map(funcDocObject => {
        return {
            match: endingFunction,
            suggestion: funcDocObject.function,
            subtitle: funcDocObject.description,
            type: 'function'
        }
    })
    if (suggestions.length == 0) {
        return undefined;
    }
    return suggestions;
}
