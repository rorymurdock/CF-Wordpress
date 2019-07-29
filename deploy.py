import string
import random
import argparse
from CFDeploy import wordpress

# Setup args
PARSER = argparse.ArgumentParser()
REQUIRED = PARSER.add_argument_group('Required arguments')
OPTIONAL = PARSER.add_argument_group('Optional arguments')
REQUIRED.add_argument("-env", help="Environment", required=True)
ARGS = PARSER.parse_args()

def random_id(length=8):
    """Generate a random string of fixed length """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(length))


wp = wordpress('%s%s' % (ARGS.env, random_id()), ARGS.env)
if wp.check_stack_exists():
    wp.delete_stack()

wp.create_stack()

wp.check_stack_created(10, 100)

print('URL: %s' % wp.get_output_url())
