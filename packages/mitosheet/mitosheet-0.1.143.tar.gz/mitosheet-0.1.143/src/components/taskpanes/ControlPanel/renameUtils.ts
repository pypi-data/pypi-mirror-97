// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.


export const isFullyNumeric = (s: string): boolean => {
    // Returns true if the given string is a number
    for (let i = 0; i < s.length; i++) {
        const c = s.charAt(i);
        if (c < '0' || c > '9') {
            return false;
        }
    }
    return true;
}

export const isValidHeader = (columnHeader: string): boolean => {
    // To be a valid header:
    // 1. Matches the regex [A-z0-9_]+ (just once, the entire string)
    // 2. Is not all digits (aka cannot be mistake for a number)

    // Check (1)
    const re = /[A-z0-9_]+/;
    const matches = re.exec(columnHeader);
    if (matches === null || matches.length != 1 || matches[0] !== columnHeader) {
        return false;
    }

    // Check (2) (all digits)
    return !isFullyNumeric(columnHeader);
}  

export const getHeaderErrorMessage = (columnHeader: string): string => {
    /* 
        Given a column header, returns a message about _how_ that columnHeader is invalid, 
        where it can detect three cases currently:
        1. The column header includes whitespace.
        2. The column header includes _only_ numbers.
        3. The column header includes a "-". 
        4. A catch-all: the column header is invalid in other ways.

        Note: We can expand these as we see users make more invalid column headers
        and see what types of errors are common!

        If the columnHeader is valid returns the empty string. 
    
    */
    if (isValidHeader(columnHeader) || columnHeader.length === 0) {
        return '';
    }

    // Check for whitespace
    if (columnHeader.indexOf(' ') >= 0) {
        return `Invalid column name. Please remove all spaces.`
    }

    // Check if it's got a -
    if (columnHeader.indexOf('-') >= 0) {
        return `Invalid column name. Try switching "-" for "_".`
    }

    // Check if it's only numbers
    if (isFullyNumeric(columnHeader)) {
        return `Invalid column name. Add at least one non-digit.`
    }

    // Catch the rest... :( )
    return 'Invalid column name. All characters must be letters, digits, and "_".';
}