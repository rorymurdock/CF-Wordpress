# CF Wordpress
[![Build Status](https://travis-ci.org/rorymurdock/CF-Wordpress.svg?branch=master)](https://travis-ci.org/rorymurdock/CF-Wordpress)
[![Coverage Status](https://coveralls.io/repos/github/rorymurdock/CF-Wordpress/badge.svg?branch=master)](https://coveralls.io/github/rorymurdock/CF-Wordpress?branch=master)
[![Requirements Status](https://requires.io/github/rorymurdock/CF-Wordpress/requirements.svg?branch=master)](https://requires.io/github/rorymurdock/CF-Wordpress/requirements/?branch=master)

Build and deploy Wordpress using CloudFormation

Getting started:

Create a user in IAM that as the below permissions:
-  TBA

Setup AWSCLI config:
```
aws configure set profile.testing.aws_access_key_id
aws configure set profile.testing.aws_secret_access_key
aws configure set profile.testing.region ap-southeast-2
aws configure set profile.testing.output json
```

Create a Key Pair if you don't already have one:
```
python3 create_keypair.py
```

Deploy your wordpress instance
```
python3 deploy.py -env {Staging|Production}
````

Extra resources

List of AWS regions: https://docs.aws.amazon.com/general/latest/gr/rande.html