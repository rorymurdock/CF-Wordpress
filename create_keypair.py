"""Create a keypair in AWS"""
import sys
import boto3

# If an existing key is found delete it?
DELETE_EXISITING_KEY = True # Bool

# Create the ec2 client
EC2 = boto3.client('ec2')

def create_key_pair():
    """Function to check and create keypair"""
    name = input('Key Pair name: ')

    # Get existing keys
    key_pairs = EC2.describe_key_pairs()

    # Check if the key already exists
    for key_pair in key_pairs['KeyPairs']:
        if key_pair['KeyName'] == name:
            # Key exists, print details
            print('%s already exists' % name)
            if DELETE_EXISITING_KEY:
                # If deleted key is enabled, delete the key
                delete_key = EC2.delete_key_pair(KeyName='Wordpress Staging')
                if delete_key['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print('Key Pair deleted')
            else:
                # Key found but don't delete, show fingerprint of key
                print('Check for key %s' % key_pair['KeyFingerprint'])
                sys.exit(1)

    # Create the keypair
    new_key = EC2.create_key_pair(KeyName='Wordpress Staging')

    # If the key was created successfully
    if new_key['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Your new Key Pair has been created, '
              'note down your private key as it won\'t be shown again')
        print(new_key['KeyName'])
        print(new_key['KeyMaterial'])

# If main start the script
if __name__ == "__main__":
    create_key_pair()
