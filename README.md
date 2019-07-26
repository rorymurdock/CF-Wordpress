# CF Wordpress
Build and deploy Wordpress using CloudFormation

Getting started:

Create a user in IAM that as the below permissions:
-  TBA

Setup AWSCLI config:
```
aws configure set profile.testing.aws_access_key_id
aws configure set profile.testing.aws_secret_access_key
aws configure set profile.testing.region eu-west-1
aws configure set profile.testing.output json
```

Deploy your wordpress instance
```
python3 deploy.py
````

Extra resources

List of AWS regions: https://docs.aws.amazon.com/general/latest/gr/rande.html