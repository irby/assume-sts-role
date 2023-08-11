# Assume STS Role

A simple Python CLI script to assume a role from AWS STS.

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [AWS CLI](https://aws.amazon.com/cli/)

## Setup

To install the requirements for the Python CLI, please run the following:

```bash
pip3 install -r requirements.txt
```

## How to run

You can call the CLI tool by running the following from your console:

```bash
python3 aws-session-token.py
```

Here is the documentation for the CLI tool:

```bash
python3 aws-session-token.py --help
usage: aws-session-token.py [-h] [-x EXPIRY] [-a ACTING_AS] [-e ENV_FILE] [-d DEVICE] [-t TOKEN] [-r ROLE_ARN] [-s] [-p PROFILE] [-v] [--version]

Get AWS Session Token

options:
  -h, --help            show this help message and exit
  -x EXPIRY, --expiry EXPIRY
                        Expiry time in seconds. Default: 3600
  -a ACTING_AS, --acting-as ACTING_AS
                        AWS profile to act as to execute STS call. Can also be set as AWS_PROFILE environment variable
  -e ENV_FILE, --env-file ENV_FILE
                        Path to env file with AWS configuration.
  -d DEVICE, --device DEVICE
                        MFA device identifier. Can also be set as AWS_MFA_DEVICE environment variable
  -t TOKEN, --token TOKEN
                        MFA token from your device. Required if MFA device is set
  -r ROLE_ARN, --role-arn ROLE_ARN
                        Role ARN to assume. Can also be set as AWS_ROLE_ARN environment variable
  -s, --save            Saves STS tokens to AWS profile. Default: false
  -p PROFILE, --profile PROFILE
                        AWS profile to set token for. Can also be set as AWS_SET_PROFILE environment variable
  -v, --verbose         Verbose output. Default: false
  --version             show program's version number and exit
```

## Environment variables

As seen above, you can use environment variables in place of some fields such as `PROFILE`, `DEVICE` and `ROLE_ARN`. These values can be stored inside an environment file (`.env`) and the CLI tool will import the environment variable if the file path is provided with the `-e` flag.

Here is a template for the `.env` file:

```
AWS_MFA_DEVICE=arn:aws:iam::1234567890:mfa/my_device
AWS_ROLE_ARN=arn:aws:iam::1234567890:role/cli_role
AWS_PROFILE=my-profile
AWS_SET_PROFILE=my-profile-token
```

## Example usage

Assuming a `.env` file has been setup with the values defined above, you can use the following command to save the credentials generated by STS to your `~/.aws/credentials` file under the profile `app-dev-token` with the MFA one-time token `123456`:

```bash
python3 aws-session-token.py -e .env --save -t 123456
```
