

/*
    These ENV variables are set in the npm test scripts. To run a test locally, simply
    call npm run test:local. By default, tests run on the local server.
*/

export const JUPYTER_LAB_LOCAL_TOKEN = process.env.JUPYTER_LAB_LOCAL_TOKEN;
export const LOCAL_TEST = process.env.LOCAL_TEST !== 'False';

// We only need to take a token if there is one
let local_url = 'http://localhost:8888/lab/tree/examples/tests'
if (JUPYTER_LAB_LOCAL_TOKEN !== undefined) {
    local_url = `${local_url}?token=${JUPYTER_LAB_LOCAL_TOKEN}`;
}
export const LOCAL_URL = local_url;
export const REMOTE_URL = 'https://staging.trymito.io'

export const CURRENT_URL = LOCAL_TEST ? LOCAL_URL : REMOTE_URL;