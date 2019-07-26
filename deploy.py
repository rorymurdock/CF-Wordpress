import boto3

ec2 = boto3.client('ec2')

response = ec2.describe_regions()
print('Regions:')
[print(region['RegionName']) for region in response['Regions']]
