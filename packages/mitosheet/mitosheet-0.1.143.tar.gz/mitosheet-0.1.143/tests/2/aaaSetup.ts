// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains initial tests for logging in, whcih also is responsible for
    setting up the kuberenetes pod, so the rest of the tests pass

    NOTE: this file is prefixed with aaa so it runs first.
*/

import { CURRENT_URL } from '../config';
import { setup } from '../utils/helpers';

fixture `Setup`
    .page(CURRENT_URL)
    
test('Log in, clean, and create empty notebook', async t => {
    await setup(t);
    
});

