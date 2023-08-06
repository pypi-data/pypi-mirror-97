[![NPM version](https://badge.fury.io/js/cdktf-aws-secure.svg)](https://badge.fury.io/js/cdktf-aws-secure)
[![PyPI version](https://badge.fury.io/py/cdktf-aws-secure.svg)](https://badge.fury.io/py/cdktf-aws-secure)
![Release](https://github.com/shazi7804/cdktf-aws-secure-constructs/workflows/Release/badge.svg)

# Terraform CDK - AWS Secure constructs

The Level 2 construct can be used to set up your AWS account with the reasonably secure configuration baseline. Internally it uses the [Terraform CDK](https://cdk.tf/) and the [AWS Provider](https://cdk.tf/provider/aws).

## Features

* Account password policies
* Cloudtrail
* Guardduty
* EBS encrypt default
* VPC flow log
* Security Hub
* Enable Config rules above

## Install

Just the constructs

```
npm install cdktf-aws-secure
```

## Examples

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from constructs import Construct
from cdktf import Resource
from cdktf_aws_secure import secure

class AwsSecure(Resource):
    def __init__(self, scope, name):
        super().__init__(scope, name)

        # Enable account password policy
        policy = secure.CreateAccountPasswordPolicy(self, "DefaultAccountPwdPolicy")

        # and also add Config rule.
        policy.add_config_rule()
```

## Docs

See [API Docs](./API.md)
