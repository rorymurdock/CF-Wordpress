import boto3
import argparse

# Setup args
PARSER = argparse.ArgumentParser()
REQUIRED = PARSER.add_argument_group('Required arguments')
OPTIONAL = PARSER.add_argument_group('Optional arguments')
REQUIRED.add_argument("-env", help="Environment", required=True)
ARGS = PARSER.parse_args()

print('Deploying to %s environment' % ARGS.env)

ec2 = boto3.client('ec2')

response = ec2.describe_regions()
print('Regions:')
[print(region['RegionName']) for region in response['Regions']]


# aws sts get-caller-identity