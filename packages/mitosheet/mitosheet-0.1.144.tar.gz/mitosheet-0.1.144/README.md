
# mito-sheet

The Mito Spreadsheet

## Installation for Development

Run all the following commands in the Mito folder. 

First create an enter a python venv, for replicability

- On Mac:
```bash
python3 -m venv venv;
source venv/bin/activate;
```

- On Windows:
```bash
python3 -m venv venv
venv\Scripts\activate.bat
```

Once the virtual enviornment is running, then install Jupyter and Jupyterlab and pandas and analytics python
```bash
pip install -r requirements.txt
```

Then install the python package. This will also build the JS packages.
```bash
pip install -e ".[test, examples]"
```

When developing your extensions, you need to manually enable your extensions with the
notebook / lab frontend. For lab, this is done by the command:
```
jupyter labextension install @jupyter-widgets/jupyterlab-manager@2 --no-build
jupyter labextension install .
```

Here, it is reccomended to clean your Yarn cache, which for some reason fills up after the above command (eventually bricking your computer, lol).
```
yarn cache clean
```

Lastly, start your dev server by running:
```
jupyter lab --watch
```

### All as one command for Mac

Make sure you run this from the Mito folder!

```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && pip install -e ".[test, examples]" && jupyter labextension install @jupyter-widgets/jupyterlab-manager@2 --no-build && jupyter labextension install . && yarn cache clean && jupyter lab --watch
```

### How to see your changes
#### Typescript:
To continuously monitor the project for changes and automatically trigger a rebuild, start Jupyter in watch mode:
```bash
jupyter lab --watch
```
And in a separate session, begin watching the source directory for changes:
```bash
npm run watch:lib
```

When you make a change to the code and save it, the `npm run watch:lib` command will cause TypeScript to compile, resulting in a message that says "Found 0 errors." Then, the `jupyter lab --watch` command will recompile Jupyter, and generate some yellow success text.

Then refresh your browser and the changes should take effect. If you changed the Python code, you will have to restart your kernel as well. 

#### Python:
If you make a change to the python code then you will need to restart the notebook kernel to have it take effect.

### Testing

There are both manual tests and automated tests. 

#### Automated Tests


##### Backend Tests

Run automated backend tests with
```
pytest
```
Automated tests can be found in  `mitosheet/test`. These are tests written using standard `pytest` tools, and include tests like testing the evaluate function, the MitoWidget, and all other pure Python code. 

##### Frontend Tests

Run automated frontend tests with
```
npm run test:remote
```
NOTE: if this command doesn't work, you probably haven't `npm install`ed the new testing dependencies. Try that :) Furthermore, this command currently only works on Mac.

This will open a Chrome browser that runs the frontend tests. _If you want the tests to pass, you have to keep the Chrome browser up + not be doing other things (it should be the focused on application on your computer)_. 

NOTE: there is currently a bug in `testcafe` (our testing framework) that causes _tons_ of warnings when the tests are run. Just scroll up to see what tests actually failed - and ignore these Warnings for now.

See `tests/README.md` for more instructions on writing tests.

You can also run local tests on Mac with
```
npm run test:local
```
###### Testing on Windows

Testing on Windows is fairly straight forward. Currently, you can only test locally on Windows. First, start the server with:
```
jupyter lab --NotebookApp.token="" --NotebookApp.password="" &
```

Then, run the tests with
```
npm run test:local:noauth
```

#### Manual Tests

Run manual tests by opening `examples/manual_tests` in `jupyter lab`, and selecting each workbook. Each workbook contains instructions on how to run the test and the expected outputs. 

To write a manual test of your own, simply create a new notebook in the `examples/manual` folder and write a test here - or in a subfolder, if it fits better there. 

These tests should be run _before releases_ - but need not be run to merge things into the dev branch. 

### Linting

This project has linting set up for both (Python)[https://flake8.pycqa.org/en/latest/index.html] and (typescript)[https://github.com/typescript-eslint/typescript-eslint]. 

Run typescript linting with the command 
```
npx eslint . --ext .tsx --fix
```

### Documentation

To learn more about writing documentation, see the README in the `/docs` folder!

## Installing the Extension

TODO! These instructions will apply in the future.

You can install using `pip`:

```bash
pip install mitosheet
```

Or if you use jupyterlab:

```bash
pip install mitosheet
jupyter labextension install @jupyter-widgets/jupyterlab-manager@2
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] mitosheet
```

