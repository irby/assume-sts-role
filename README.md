# Assume STS Role

A simple Python CLI script to assume a role from AWS STS with an MFA token.

By default, it will store the temporary credentials in the AWS profile of your choice. For example, if you want to store it for the profile `my-profile`, it will store the temporary STS tokens under `my-profile-token` in your `~/.aws/credentials` file.

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
usage: aws-session-token.py [-h] -t TOKEN [-p PROFILE] [-d DEVICE] [-r ROLE_ARN] [-o] [-v]

Get AWS Session Token

options:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        MFA token from your device (default: None)
  -p PROFILE, --profile PROFILE
                        AWS profile to set token for. Can also be set as AWS_PROFILE environment variable (default: None)
  -d DEVICE, --device DEVICE
                        MFA device identifier. Can also be set as AWS_MFA_DEVICE environment variable (default: None)
  -r ROLE_ARN, --role-arn ROLE_ARN
                        Role ARN to assume. Can also be set as AWS_ROLE_ARN environment variable (default: None)
  -o, --output          Output STS response without overwriting AWS credentials file (default: False)
  -v, --verbose         Verbose output (default: False)
```

## Environment variables

As seen above, you can use environment variables in place of some fields such as `PROFILE`, `DEVICE` and `ROLE_ARN`. These values can be stored inside a file called `aws.env`, and the CLI tool will import the environment variables from this file.

Here is a template for the `aws.env` file:

```
AWS_MFA_DEVICE=arn:aws:iam::1234567890:mfa/my_device
AWS_ROLE_ARN=arn:aws:iam::1234567890:role/cli_role
AWS_PROFILE=my-profile
```
