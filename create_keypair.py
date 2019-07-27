import sys
import boto3

name = input('Key Pair name: ')
deleteExistingKey = True

ec2 = boto3.client('ec2')

# Get existing keys
key_pairs = ec2.describe_key_pairs()

# Check if the key already exists
for key_pair in key_pairs['KeyPairs']:
    if key_pair['KeyName'] == name:
        # Key exists, print details
        print('%s already exists' % name)
        if deleteExistingKey:
            deleteKey = ec2.delete_key_pair(KeyName='Wordpress Staging')
            if deleteKey['ResponseMetadata']['HTTPStatusCode'] == 200:
                print('Key Pair deleted')
        else:
            print('Check for key %s' % key_pair['KeyFingerprint'])
            sys.exit(1)

newKey = ec2.create_key_pair(KeyName='Wordpress Staging')
if newKey['ResponseMetadata']['HTTPStatusCode'] == 200:
    print('Your new Key Pair has been created, note down your private key as it won\'t be shown again')
    print(newKey['KeyName'])
    print(newKey['KeyMaterial'])
