# Assume STS Role

A simple Python CLI script to assume a role from AWS STS.

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [AWS CLI](https://aws.amazon.com/cli/)

## How to run

You can call the CLI tool by running the following from your console:

```bash
python3 aws-session-token.py
```

Here is the documentation for the CLI tool:

```bash
python3 aws-session-token.py --help                     
usage: aws-session-token.py [-h] [-x EXPIRY] [-e ENV_FILE] [-p PROFILE] [-d DEVICE] [-t TOKEN] [-r ROLE_ARN] [-s] [-v]

Get AWS Session Token

options:
  -h, --help            show this help message and exit
  -x EXPIRY, --expiry EXPIRY
                        Expiry time in seconds.
  -e ENV_FILE, --env-file ENV_FILE
                        Path to env file with AWS credentials
  -p PROFILE, --profile PROFILE
                        AWS profile to set token for. Can also be set as AWS_SET_PROFILE environment variable. Default: default
  -d DEVICE, --device DEVICE
                        MFA device identifier. Can also be set as AWS_MFA_DEVICE environment variable. Required if MFA token is set
  -t TOKEN, --token TOKEN
                        MFA token from your device. Required if MFA device is set
  -r ROLE_ARN, --role-arn ROLE_ARN
                        Role ARN to assume. Can also be set as AWS_ROLE_ARN environment variable
  -s, --save            Saves STS tokens to AWS profile. Default: false
  -v, --verbose         Verbose output. Default: false
```

## Environment variables

As seen above, you can use environment variables in place of some fields such as `PROFILE`, `DEVICE` and `ROLE_ARN`. These values can be stored inside a file called `aws.env`, and the CLI tool will import the environment variables from this file.

Here is a template for the `aws.env` file:

```
AWS_MFA_DEVICE=arn:aws:iam::1234567890:mfa/my_device
AWS_ROLE_ARN=arn:aws:iam::1234567890:role/cli_role
AWS_SET_PROFILE=my-profile
```
