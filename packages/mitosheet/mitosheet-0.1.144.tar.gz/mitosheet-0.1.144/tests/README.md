# Running Frontend Tests

See the main `README.md` for instructions on running the tests!

# Getting Started Writing Testcafe Tests

When writing tests, there are a few things to watch out for:
1. Testcafe tests are not very consistent. For this reason, we wrap all our tests inside a `tryTest` function, which will try to run a test mulitple times before giving up. This greatly reduces the false failures of the test.
2. There are multiple folders containing tests. There are two reasons for this:
    - JupyterLab on Windows onlyhandles a limited number of websockets opened within a short period of time, and Jupyter Widgets (of which Mito is one), uses websockets.
    - Testcafe CI on a Github Action can only be run on Windows.
3. For these reasons, we split our tests up into mulitple folders. If you are adding a new file of tests with lots of tests in it, consider breaking it out into it's own folder (make sure to copy over the `aaaSetup` file). When you break it into it's own folder, you must also go to the `monorepo/.github/workflows/testcafe.yml`, and add a a new step to the action that runs this folder. See the script for examples - and note you have to update `mito/package.json` as well!

NOTE: there can be at most 17 tests in a folder!

NOTE: sometimes, tests fail on Windows only. In this case, automated testing may fail, and you may have to debug on Windows! Not sure in which cases these occur, but we should keep an eye on it.

The documentation for TestCafe tests is pretty good - and you can see it [here](https://devexpress.github.io/testcafe/documentation/guides/).

# Writing Selectors

Writing selectors is hard, sometimes. It takes a bit to get the hang of it. For this reason, I've tried to write selectors for some common items - and you can just reuse them!

Also, write and write some of your own. It can be really challenging, but you will learn a lot. See the testcafe documentation [here](https://devexpress.github.io/testcafe/documentation/guides/basic-guides/select-page-elements.html).

# Common Gotchas

1. NOTE: when writing a new test, do `test.only(` to just run that single test. This will _dramatically_ speed up your development. 
2. _Make sure you write/debug tests in the browser you're running them in_. Not everything is the same everywhere, so keeping things static is absolutely essential.
3. Make sure to check out existing tests to see the easiest ways to write a formula, check a column header, and check the value of a cell. There are lot of useful utilities.
4. The tests are much more robust than reflect, but they sometimes fail. If you see a test fail randomly, see if you can figure out why and fix it, so we can keep making these tests more robust!