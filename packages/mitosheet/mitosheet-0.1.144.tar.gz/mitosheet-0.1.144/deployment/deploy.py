#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
File that contains utilities for deploying a new version of Mito to 
app.trymito.io. See main for running instructions
"""
import sys
import subprocess
from string import Template
import json
from time import sleep
import os
from string import Template, ascii_lowercase
import random
from typing import List

def safe_run_command(command: List[str]):
    """
    Helper function for running a command in the terminal. Throws
    an exception of the command returns an exception. Returns a tuple
    of (stdout, stderr).
    """

    results = subprocess.run(
        command,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    if results.returncode != 0:
        raise Exception(f'Exception running {" ".join(command)}:', results.stdout, results.stderr)

    return results.stdout, results.stderr


def build_dockerfile_from_template(mito_version) -> str:
    """
    Helper function that builds a Mito dockerfile from the template
    in deployment/templates/Dockerfile.

    Notably, includes all the files in tutorial in the dockerfile itself
    to be put on the users account. 
    """

    # Make sure no folders in the tutorial (for now)
    root_dir = 'deployment/tutorial'
    tutorial_files = set()

    for dir_, _, files in os.walk(root_dir):
        for file_name in files:
            rel_dir = os.path.relpath(dir_, root_dir)
            rel_file = os.path.join(rel_dir, file_name)
            tutorial_files.add(rel_file)

    if '.DS_Store' in tutorial_files:
        tutorial_files.remove('.DS_Store') 
    
    tutorial_copies = '\n'.join([f'COPY {f} /tutorial/{f}' for f in tutorial_files])

    # Read in template, replace with version and the tutorial
    with open('deployment/templates/docker_template.txt', 'r') as f:
        return Template(f.read()).substitute({
            'version': mito_version,
            'tutorial_copies': tutorial_copies
        })

def auth_with_aws():
    """
    Authenticates the docker CLI with AWS, so we can push to AWS ECR
    """
    print("Authenticating with AWS...")
    aws_ecr = subprocess.Popen(["aws", "ecr", "get-login-password", "--region", "us-east-1"], stdout=subprocess.PIPE)
    output = subprocess.check_output(["docker", "login", "--username", "AWS", "--password-stdin", "308734690614.dkr.ecr.us-east-1.amazonaws.com"], stdin=aws_ecr.stdout) # pipe them together
    aws_ecr.wait()


def build_and_upload_docker_image(mito_version):
    """
    Builds the docker image defined by the template docker file in templates, 
    as well as the files in the tutorial, and deploys it to AWS ECR.
    """
    dockerfile_string = build_dockerfile_from_template(mito_version)
    with open('deployment/tutorial/Dockerfile', 'w+') as f:
        f.write(dockerfile_string)
    
    # Go into the folder, and build the docker image
    print('Building a new docker image... this might take a bit.')
    os.chdir('deployment/tutorial')
    try:
        stdout, stderr = safe_run_command(["docker", "build", "."])
    except:
        # If there is an error during build, remove the dockerfile from the tutorial
        os.remove('Dockerfile')
        # and raise the error
        raise
    os.chdir('../..')

    # Remove the docker file
    os.remove('deployment/tutorial/Dockerfile')

    # Get the image id to actually deploy it to AWS ECR. 
    # stdout looks like:
    # Step 5/5 : COPY test.txt /tutorial/test.txt
    # ---> d6e2cb5b2899
    # Successfully built d6e2cb5b2899 
    image_id = [line for line in stdout.split('\n') if line.strip()][-1].strip().split(' ')[-1].strip()

    # Authenticate with ECR, so we can push the new image
    auth_with_aws()
    
    # NOTE: we add a random tag onto the end of the version tag, so that we get a new version if we redeploy it.
    # This makes the configs differ, and so ensures that JHub restarts
    tag_end = ''.join(random.choice(ascii_lowercase) for i in range(10))
    tag = f'{mito_version}.{tag_end}'

    # Tag the new image locally
    safe_run_command(
        ["docker", "tag", image_id, f'308734690614.dkr.ecr.us-east-1.amazonaws.com/mito-images:{tag}']
    )

    # And push the image
    print("Uploading the image to AWS... this might take a bit.")
    safe_run_command(
        ["docker", "push", f'308734690614.dkr.ecr.us-east-1.amazonaws.com/mito-images:{tag}']
    )
    return tag

def get_package_version() -> str:
    with open('package.json') as f:
        return json.loads(f.read())['version']

def check_files_on_version(version):
    """
    A helper function that checks that the version has been updated properly
    in all the correct places:
    - package.json
    - mitosheet/_version.py

    If the verison is not correctly updated, returns the offending file
    """
    files_to_check = [
        'package.json',
    ]

    for file_name in files_to_check:
        with open(file_name) as f:
            if version not in f.read():
                print(f'File {file_name} not updated to version {version}')
                return False
    
    # The mitosheet/_version.py file stores the version in a tuple, and so we read from that
    version_info_tuple = ', '.join(version.split('.'))
    with open('mitosheet/_version.py') as f:
        if version_info_tuple not in f.read():
            print(f'File mitosheet/_version.py not updated to version {version}')
            return False
    
    return True

def deploy_current_mito_version_to_pypi():
    """
    Deploys the current local version of Mito to PyPi.
    """
    deploy_results = subprocess.run(
        ["python3", "setup.py", "sdist", "bdist_wheel", "upload"],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    if deploy_results.returncode != 0:
        raise Exception("Failed to deploy to PyPi with output:", deploy_results.stdout, deploy_results.stderr)


def deploy_version_on_staging(tag):
    """
    Deploys the new version of staging!
    """
    print("Deploying on staging")
    
    # First, switch to the correct cluster!
    safe_run_command(
        ["aws", "eks", "--region", "us-east-1", "update-kubeconfig", "--name", "staging"]
    )

    # First, read in the secret token for the config
    with open('deployment/secrets.json', 'r') as f:
        secret_token = json.loads(f.read())['staging']['secretToken']

    with open('deployment/templates/template-staging-config.yaml', 'r') as f:
        staging_config_string = Template(f.read()).substitute({
            'secretToken': secret_token,
            'tag': tag
        })

    with open('staging-config.yaml', 'w+') as f:
        print("Writing...")
        f.write(staging_config_string)

    safe_run_command(
        ["helm", "upgrade", "--cleanup-on-fail", "--install", "jhub", "jupyterhub/jupyterhub", "--version", "0.10.2", "--values", "staging-config.yaml"]
    )

    # Note: we leave the config files there so that you can see what was deployed!

    print("Run \'aws eks --region us-east-1 update-kubeconfig --name staging; kubectl get pods\' to see the progress of this update.")


def deploy_version_on_app(tag):
    """
    Deploys the new version of the app on app!
    """
    print("Deploying on app")

    # First, switch to the right cluster
    safe_run_command(
        ["aws", "eks", "--region", "us-east-1", "update-kubeconfig", "--name", "app"]
    )

    # First, read in the secret token for the config
    with open('deployment/secrets.json', 'r') as f:
        secrets = json.loads(f.read())['app']
        secret_token = secrets['secretToken']
        client_id = secrets['google']['clientId']
        client_secret = secrets['google']['clientSecret']

    with open('deployment/templates/template-config.yaml', 'r') as f:
        config_string = Template(f.read()).substitute({
            'secretToken': secret_token,
            'tag': tag,
            'clientId': client_id,
            'clientSecret': client_secret
        })

    with open('config.yaml', 'w+') as f:
        f.write(config_string)

    safe_run_command(
        ["helm", "upgrade", "--cleanup-on-fail", "--install", "jhub", "jupyterhub/jupyterhub", "--version", "0.10.2", "--values", "config.yaml"]
    )

    # Note: we leave the config files there so that you can see what was deployed!

    print("Run \'kubectl get pods\' to see the progress of this update.")


def main():
    """
    This deploys the current Mito version on either staging, app, or all. Simply
    run this script with `python3 deployment/deploy.py [staging | app | all]`.

    To change the tutorial that new users get, simply change the files in the tutorial folder.
    """

    # We either deploy app, staging, or all (both app and staging)
    deploy_location = sys.argv[1]
    if deploy_location not in ['app', 'staging', 'all']:
        raise Exception(f'Invalid deploy location: {deploy_location}. Please choose from app, staging, or all.')

    # Make sure all the files have been updated to the right version
    mito_version = get_package_version()
    if not check_files_on_version(mito_version):
        raise Exception(f'At least one file has not been updated to the proper version. Please update!')

    # Then, we actually deploy Mito to PyPi, if it has not been deployed yet
    try:
        print(f'Trying to deploy Mito {mito_version} on PyPi... might take a moment')
        deploy_current_mito_version_to_pypi()
    except Exception as e:
        print(e)
        print("Failed to deploy to PyPi. Assuming this is because you deployed already, so continuing... but we may be doomed.")

    # We wait, just in case ECR needs to update
    print("Sleeping for 3 minutes, to allow things to update on PyPi...")
    sleep(60 * 3)

    # Then, we build a new Mito image on Docker to AWS ECR
    docker_tag = build_and_upload_docker_image(mito_version)

    # We wait, just in case ECR needs to update
    print("Sleeping for 20 seconds, to allow things to update on AWS's end...")
    sleep(20)

    # Finially, we case and deploy
    if deploy_location == 'staging':
        deploy_version_on_staging(docker_tag)
    if deploy_location == 'app':
        deploy_version_on_app(docker_tag)
    if deploy_location == 'all':
        deploy_version_on_staging(docker_tag)
        deploy_version_on_app(docker_tag)

    # Always switch back to the correct cluster!
    safe_run_command(
        ["aws", "eks", "--region", "us-east-1", "update-kubeconfig", "--name", "app"]
    )

if __name__ == '__main__':
    main()