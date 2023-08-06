## Tutorials are now available!

[Check the tutorials out!](https://web.microsoftstream.com/channel/c390cb39-d9f1-4490-8174-0f9616c30961)

## Requirements
 * Node.js 10+ (https://nodejs.org/en/)
 * Python3 and Pip3
 * AWS account on AWS
 * AWS CLI installed and configured
 * GAST plugin to retrieve AWS Session Token (https://www.npmjs.com/package/get-aws-session-token)
 * AWS CDK CLI installed (https://www.npmjs.com/package/aws-cdk)

## Getting started

### Bitbucket
 * Create a repo for IAC on bitbucket
 * Enable pipelines for the repo

### Local project initialization
 * Clone repo locally
 * Initialize CDK project with "cdk init sample-app --language python" command
 * Follow the auto-generated instruction to enable the Python Virtual env contained in the README file. It's important that the virtual env is not called ".env". In case the auto generation of the python env generates a ".env" virtual env, re-create it following the instaruction in the README with a different name
 * Activate the python virtual env following the README file
 * Install the project dependencies following the README file
 * Test that everything is working with the command "cdk synth"

### Let's start coding
 * Install the AWS CDK constucts as project dependencies "pip install aws_cdk_constructs"
 * Install any other python dependency (e.g. "python-dotenv")
 * Create the .env.example and .env file according to AWS standard (you can extend the set of variables as you like)
 * Configure the .env file according to application needs

### Let's configure CD/CI
 * Create the CDK service user from AWS CDK consturct
 * Deploy the infrastructure using CDK 
 * Retrieve the newly created User credentials from AWS console > IAM > Users > select your user > Security Credentials tab > Create Access Keys
 * Configure the Bitbucket pipeline environment variables
 * Create and develop the bitbucket-pipeline.yml file
 * On push, the pipeline will run automatically

## Bootstrap you project

Your project is set up like a standard Python project. The initialization process should also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

### Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
 * `cdk ls`: to list the available stacks in the projects
 * `cdk synth MY_STACK --profile my-dev`: to synthetize (generate) the cloud formation template of MY_STACK stack
 * `cdk deploy MY_STACK --profile my-dev`: to deploy the the MY_STACK stack

### How to generate the AWS CDK costructs documention
The documentation follows Google format.

 * Browse the `./docs` directory
 * Run the `make html` to generate the static HTML documentation in the  `/docs/_build/` directory