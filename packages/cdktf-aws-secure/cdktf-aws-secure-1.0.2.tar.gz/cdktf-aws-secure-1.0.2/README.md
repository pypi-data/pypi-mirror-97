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

        policy = secure.EnableAccountPasswordPolicy(self, "DefaultAccountPwdPolicy")

        policy.add_config_rule()# and also add Config rule.

        # enable guardduty
        secure.EnableGuardduty(self, "EnableGuardduty")

        # enable cloudtrail
        secure.EnableCloudTrail(self, "EnableCloudTrail")

        # enable ebs encrypt default
        secure.EnableEbsEncryption(self, "EnableEbsEncryption")secure.EnableGuardduty(self, "EnableGuardduty")

        # enable vpc flow log
        secure.EnableVpcFlowLog(self, "EnableVpcFlowLog",
            vpc_id="vpc-0123456789"
        )

        # enable security hub
        secure.EnableSecurityHub(self, "EnableSecurityHub")
```

## Docs

See [API Docs](./API.md)
