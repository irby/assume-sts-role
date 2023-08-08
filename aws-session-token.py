import boto3, argparse, uuid, os, dotenv, logging

parser = argparse.ArgumentParser(description='Get AWS Session Token')
parser.add_argument('-x', '--expiry', required=False, help="Expiry time in seconds.", default=3600, type=int)
parser.add_argument('-e', '--env-file', required=False, help="Path to env file with AWS credentials")
parser.add_argument('-p', '--profile', required=False, help="AWS profile to set token for. Can also be set as AWS_SET_PROFILE environment variable.")
parser.add_argument('-d', '--device', required=False, help="MFA device identifier. Can also be set as AWS_MFA_DEVICE environment variable. Required if MFA token is set")
parser.add_argument('-t', '--token', required=False, help="MFA token from your device. Required if MFA device is set")
parser.add_argument('-r', '--role-arn', required=False, help="Role ARN to assume. Can also be set as AWS_ROLE_ARN environment variable")
parser.add_argument('-s', '--save', required=False, action="store_true", help="Saves STS tokens to AWS profile. Default: false")
parser.add_argument('-v', '--verbose', required=False, action="store_true", help="Verbose output. Default: false")

args = parser.parse_args()
config = vars(args)

logging_format = '%(asctime)s - %(levelname)s - %(message)s'
if config['verbose']:
    logging.basicConfig(level=logging.INFO, format=logging_format)
else:
    logging.basicConfig(format=logging_format)
logger = logging.getLogger(__name__)

if config['env_file'] is not None:
    if os.path.exists(config['env_file']) is False:
        raise FileNotFoundError("Env file {} not found".format(config['env_file']))
    else:
        dotenv.load_dotenv(config['env_file'])


mfa_token = config['token']
mfa_device = config['device'] or os.getenv("AWS_MFA_DEVICE")
profile = config['profile'] or os.getenv("AWS_SET_PROFILE")
role_arn = config['role_arn'] or os.getenv("AWS_ROLE_ARN")
expiry_time = config['expiry']
save_token = config['save']


if role_arn is None:
    raise KeyError("Role ARN not set. Please set AWS_ROLE_ARN environment variable or use -r/--role-arn argument")

if profile is None and save_token:
    raise KeyError("Profile not set. Please set AWS_SET_PROFILE environment variable or use -p/--profile argument")

if (mfa_device is not None and mfa_token is None) or (mfa_device is None and mfa_token is not None):
    raise KeyError("Both MFA device and token must be set. Please set AWS_MFA_DEVICE and AWS_MFA_TOKEN environment variables or use -d/--device and -t/--token arguments")

client = boto3.client('sts')

try:
    logger.info("Assuming role {} with MFA device {}...".format(role_arn, mfa_device))

    if mfa_device is None:
        response = client.assume_role(RoleArn=role_arn, RoleSessionName='admin_access_cli_'+uuid.uuid4().hex, DurationSeconds=expiry_time)
    else:
        response = client.assume_role(RoleArn=role_arn, RoleSessionName='admin_access_cli_'+uuid.uuid4().hex, DurationSeconds=expiry_time, SerialNumber=mfa_device, TokenCode=mfa_token)
    
    if save_token is False:
        print(response)
        exit(0)
    
    logger.info("Setting AWS credentials for profile {}...".format(profile))

    os.system('aws configure set {} {} --profile {}'.format('aws_access_key_id', response['Credentials']['AccessKeyId'], profile))
    os.system('aws configure set {} {} --profile {}'.format('aws_secret_access_key', response['Credentials']['SecretAccessKey'], profile))
    os.system('aws configure set {} {} --profile {}'.format('aws_session_token', response['Credentials']['SessionToken'], profile))

    print('AWS credentials set for profile {}.'.format(profile))
except Exception as e:
    logger.error("Error assuming role: {}".format(role_arn))
    print(e)
    exit(-1)
