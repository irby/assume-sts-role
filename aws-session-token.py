import boto3, argparse, uuid, os, dotenv, logging

parser = argparse.ArgumentParser(description='Get AWS Session Token', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-t', '--token', required=True, help="MFA token from your device")
parser.add_argument('-p', '--profile', required=False, help="AWS profile to set token for. Can also be set as AWS_PROFILE environment variable")
parser.add_argument('-d', '--device', required=False, help="MFA device identifier. Can also be set as AWS_MFA_DEVICE environment variable")
parser.add_argument('-r', '--role-arn', required=False, help="Role ARN to assume. Can also be set as AWS_ROLE_ARN environment variable")
parser.add_argument('-o', '--output', required=False, action="store_true", help="Output STS response without overwriting AWS credentials file")
parser.add_argument('-v', '--verbose', required=False, action="store_true", help="Verbose output")

args = parser.parse_args()
config = vars(args)

logging_format = '%(asctime)s - %(levelname)s - %(message)s'
aws_file_str = 'aws.env'

if config['verbose']:
    logging.basicConfig(level=logging.INFO, format=logging_format)
else:
    logging.basicConfig(format=logging_format)

logger = logging.getLogger(__name__)

if os.path.exists(aws_file_str):
    dotenv.load_dotenv(aws_file_str)

mfa_token = config['token']

mfa_device = os.getenv("AWS_MFA_DEVICE") or config['device']
profile = os.getenv("AWS_PROFILE") or config['profile']
role_arn = os.getenv("AWS_ROLE_ARN") or config['role_arn']
output_only = config['output']



if mfa_device is None:
    raise KeyError("MFA device identifier not set. Please set AWS_MFA_DEVICE environment variable or use -d/--device argument")

if role_arn is None:
    raise KeyError("Role ARN not set. Please set AWS_ROLE_ARN environment variable or use -r/--role-arn argument")

if profile is None:
    raise KeyError("AWS profile not set. Please set AWS_PROFILE environment variable or use -p/--profile argument")

if 'token' in profile:
    raise KeyError("AWS profile cannot contain 'token' in the name")



profile = profile + '-token'
client = boto3.client('sts')

try:
    logger.info("Assuming role {} with MFA device {}...".format(role_arn, mfa_device))

    response = client.assume_role(RoleArn=role_arn, RoleSessionName='admin_access_cli_'+uuid.uuid4().hex, SerialNumber=mfa_device, TokenCode=mfa_token)
    
    if output_only:
        print(response)
        exit(0)
    
    logger.info("Setting AWS credentials for profile {}...".format(profile))

    os.system('aws configure set {} {} --profile {}'.format('aws_access_key_id', response['Credentials']['AccessKeyId'], profile))
    os.system('aws configure set {} {} --profile {}'.format('aws_secret_access_key', response['Credentials']['SecretAccessKey'], profile))
    os.system('aws configure set {} {} --profile {}'.format('aws_session_token', response['Credentials']['SessionToken'], profile))

    print('AWS credentials set for profile {}.'.format(profile))
    exit(0)
except Exception as e:
    logger.error("Error assuming role: {}".format(role_arn))
    print(e)
    exit(-1)
