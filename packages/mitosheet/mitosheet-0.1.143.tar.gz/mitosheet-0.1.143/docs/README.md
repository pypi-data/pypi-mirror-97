# Generating Documentation

Currently, we support in-app documentation. Practically, this means that users can open a taskpane and see a list of all the functions that we support, examples of their usage, and an in-depth description of their syntax.

To avoid duplicating documentation, we directly generate documentation from `mitosheet/sheet_functions.py` - where the functions are documented in their doc strings.

## Documentation Format

Each function has a single function documentation object in its docstring, which looks like:
```
{
    "function": "SUM",
    "description": "Returns the sum of a series of numbers and/or columns.",
    "examples": [
        "SUM(10, 11)",
        "SUM(A, B, D, F)",
        "SUM(A, B, D, F)"
    ],
    "syntax": "SUM(value1, [value2, ...])",
    "syntax_elements": [{
            "element": "value1",
            "description": "The first number or column to add together."
        },
        {
            "element": "value2, ... [OPTIONAL]",
            "description": "Additional numbers or columns to sum."
        }
    ]
}
```

As a TypeScript type:
```
interface FunctionDocumentationObject {
    function: string;
    description: string;
    examples?: (string)[] | null;
    syntax: string;
    syntax_elements?: (SyntaxElementsEntity)[] | null;
}

interface SyntaxElementsEntity {
    element: string;
    description: string;
}
```

## Updating Documentation

If you added a new function, and you want to update the documentation to include that function, first make sure you have written the function doc string correctly under the function. See `SUM` in `/mitosheet/sheet_functions.py` as an example. 

Then, from the `mito` folder, simply run:
```
python3 docs/make_function_docs.py
```
