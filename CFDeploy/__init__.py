"""Deploy CloudFormation in AWS"""
import sys
import time
import string
import random
import boto3

TimeoutInMinutes = 60
OnFailure = 'DELETE' # DO_NOTHING, ROLLBACK, or DELETE
EnableTerminationProtection = False
KeyPair = 'Wordpress Staging'
debug = True

## WARNING
overrideTerminationProtection = True

def random_string(length=15):
    """Generate a random string of fixed length """
    return ''.join(
        random.choice(
            string.ascii_lowercase + string.ascii_uppercase)
        for i in range(length)
    )

def random_id(length=8):
    """Generate a random string of fixed length """
    return ''.join(
        random.choice(
            string.ascii_uppercase + string.digits)
        for i in range(length)
    )

def random_password(length=15):
    """Generate a random string of fixed length """
    return ''.join(
        random.choice(
            string.ascii_lowercase + string.ascii_uppercase + string.digits)
        for i in range(length)
    )

def debug_print(message):
    """If debugging enabled, print message"""
    if debug:
        print(message)

class AWS():
    """Deploy to AWS using CloudFormation"""
    def __init__(self, stackName, environment):
        """init"""
        if environment not in ['Production', 'Staging']:
            print('Environment must be Production or Staging')
            sys.exit(1)

        print('Deploying %s to %s environment' % (stackName, environment))

        if environment == 'Production':
            # Using sample URL for testing
            self.templateURL = ''  #TODO Update URLs to correct jsons
        else:
            self.templateURL = 'https://cfwordpress.s3-ap-southeast-2.amazonaws.com/Staging.json'
        self.stackName = stackName
        self.environment = environment

        # Create shared instances of AWS API
        self.ec2 = boto3.client('ec2')
        self.cf = boto3.client('cloudformation')

    def get_ec2_regions(self):
        """Returns a list of all regions"""
        response = self.ec2.describe_regions()

        return response['Regions']

    def get_all_stacks(self):
        """Returns a list of all stacks"""
        stacks = self.cf.describe_stacks()['Stacks']
        return stacks

    def get_stack(self, StackName=None):
        """Gets a stacks details by name"""
        if StackName is None:
            StackName = self.stackName

        return self.cf.describe_stacks(StackName=StackName)['Stacks']

    def return_dict(self, name, key, value):
        """Creates a dict given a name, key, and value"""
        parameter = {}
        parameter['%sKey' % name] = key
        parameter['%sValue' % name] = value

        return parameter

    def create_stack(self):
        """Create a CF Stack"""
        parameters_export = []
        parameters = [
            ['KeyName', KeyPair],
            ['DBUser', random_string(16)],
            ['DBPassword', random_password(41)],
            ['DBRootPassword', random_password(41)],
            ['InstanceType', 't1.micro'],
            ['WPAdminUsername', 'wpadmin1'],
            ['WPAdminPassword', random_password(15)],
            ['WPAdminEmail', 'noreply@itmatic.com.au']
        ]

        for parameter in parameters:
            parameters_export.append(self.return_dict('Parameter', parameter[0], parameter[1]))

        tags_export = []

        tags = [
            ['Env', self.environment]
        ]

        for tag in tags:
            tags_export.append(self.return_dict('', tag[0], tag[1]))

        response = self.cf.create_stack(
            StackName=self.stackName,
            TemplateURL=self.templateURL,
            Parameters=parameters_export,
            TimeoutInMinutes=TimeoutInMinutes,
            OnFailure=OnFailure,
            Tags=tags_export,
            EnableTerminationProtection=False
            )

        if self.check_response(response):
            print('Job submitted')
            return True

    def check_stack_created(self, delay=10, max_attempts=10):
        """Check and wait for a stack to be created, returns bool"""
        print('Waiting for Stack to be created')
        waiter = self.cf.get_waiter('stack_create_complete')

        waiter.wait(
            StackName=self.stackName,
            # NextToken='string',
            WaiterConfig={
                'Delay': delay,
                'MaxAttempts': max_attempts
            }
        )

        if self.get_stack()[0]['StackStatus'] == 'CREATE_COMPLETE':
            print('Stack created succesfully')
            print('Stack ID: %s' % self.get_stack()[0]['StackId'])
            return True

    def check_stack_exists(self):
        """Checks for a stack name conflict"""
        for stack in self.get_all_stacks():
            if stack['StackName'] == self.stackName:
                debug_print('Stack %s exists' % self.stackName)
                return True
        return False

    def check_termination_protection(self):
        """Checks if a stack has termination protection enabled"""
        stack = self.get_stack(self.stackName)[0]
        return stack['EnableTerminationProtection']

    def delete_stack(self):
        """Deletes a stack"""
        if self.check_termination_protection() and not overrideTerminationProtection:
            print('Error: Termination protection is enabled')
            sys.exit(1)
        elif self.check_termination_protection() and overrideTerminationProtection:
            if self.update_termination_protection(False):
                print('Removed termination protection from %s' % self.stackName)
                print('Waiting for Stack to update')
                while self.check_termination_protection:
                    # FIX: Never seems to update status
                    print('.')
                    time.sleep(2)
            else:
                print('Unable to remove termination protection on stack')
                print('Remove protection and try again')
                sys.exit(1)

        print('Deleting stack %s' % self.stackName)
        response = self.cf.delete_stack(StackName='string')

        return self.check_response(response)

        #TODO Add delete checker
        # waiter = client.get_waiter('stack_delete_complete')
        # waiter.wait(
        #     StackName='string',
        #     NextToken='string',
        #     WaiterConfig={
        #         'Delay': 123,
        #         'MaxAttempts': 123
        #     }
        # )

    def update_termination_protection(self, enabled: bool):
        """Add or remove termination protection"""
        response = self.cf.update_termination_protection(
            StackName=self.stackName,
            EnableTerminationProtection=enabled
        )

        return self.check_response(response)

    def get_output_url(self):
        """Gets the output URL"""
        for output in self.get_stack()[0]['Outputs']:
            if output['OutputKey'] == 'WebsiteURL':
                return output['OutputValue']

    def check_response(self, response):
        """Checks if the response is 200 OK"""
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        return False
