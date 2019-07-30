"""Deploy a CloudFormation template into AWS"""
import sys
import json
import string
import random
import argparse
from CFDeploy import AWS

# Setup args
PARSER = argparse.ArgumentParser()
REQUIRED = PARSER.add_argument_group('Required arguments')
OPTIONAL = PARSER.add_argument_group('Optional arguments')
REQUIRED.add_argument("-env", help="Environment", required=True)
ARGS = PARSER.parse_args()

# Used for creating unique stack IDs
def random_id(length=8):
    """Generate a random string of fixed length """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(length))

# Initialise function with random stack ID
AWS = AWS('%s%s' % (ARGS.env, random_id()), ARGS.env)

# Check for stack collisions
if AWS.check_stack_exists():
    # If delete stacks is enabled the stack will be deleted
    if not AWS.delete_stack():
        print('Unable to delete conflicting stack')
        sys.exit(1)

# Create the stack
AWS.create_stack()

# Wait for the stack to initialise
AWS.check_stack_created(10, 100)

# Output the URL for this new stack
print('URL: %s' % AWS.get_output_url())

# Save locally for tests to pick up
URL = {}
URL['url'] = AWS.get_output_url()

# Removes any trailing dots
url = "StagingJE0ZJYUH.staging.itmatic.com.au.".rstrip('.')

# Write to json file for pytests to pick up
with open('url.json', 'w') as outfile:
    json.dump(URL, outfile)
