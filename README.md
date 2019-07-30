# CF Wordpress

[![Build Status](https://travis-ci.org/rorymurdock/CF-Wordpress.svg?branch=master)](https://travis-ci.org/rorymurdock/CF-Wordpress)
[![Coverage Status](https://coveralls.io/repos/github/rorymurdock/CF-Wordpress/badge.svg?branch=master)](https://coveralls.io/github/rorymurdock/CF-Wordpress?branch=master)
[![Requirements Status](https://requires.io/github/rorymurdock/CF-Wordpress/requirements.svg?branch=master)](https://requires.io/github/rorymurdock/CF-Wordpress/requirements/?branch=master)

Build and deploy Wordpress using CloudFormation

Getting started:

Create a user in IAM that has the below permissions:

- AmazonEC2FullAccess

- AmazonS3ReadOnlyAccess

- AmazonRoute53FullAccess

- AWSCloudFormationFullAccess

Install python requirements:

```python
python3 -m pip install -r requirements.txt
```

You may need to instal AWS CLI:

```shell
sudo apt-get install awscli -y
```

Setup AWSCLI config:

```shell
aws configure set profile.default.aws_access_key_id <aws_access_key_id>
aws configure set profile.default.aws_secret_access_key <aws_secret_access_key>
aws configure set profile.default.region ap-southeast-2
aws configure set profile.default.output json
```

Create a Key Pair if you don't already have one:

```python
python3 create_keypair.py
```

Deploy your wordpress instance

```python
python3 deploy.py -env {Staging|Production}
````

The stack will create a security group with port 80 open and 22 open to the IP range you specify. It will output the URL which will be <rand>.staging.itmatic.com.au (or your domain)

Extra resources

[List of AWS regions](https://docs.aws.amazon.com/general/latest/gr/rande.html)
