import boto3
boto3.client('ec2')

def test_ec2_list_regions():
    response = boto3.client('ec2').describe_regions()
    response['ResponseMetadata']['HTTPStatusCode'] == 200