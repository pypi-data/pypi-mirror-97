'''
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
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import cdktf
import constructs


@jsii.data_type(
    jsii_type="cdktf-aws-secure.AcceptMemberAccountOptions",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId", "email": "email"},
)
class AcceptMemberAccountOptions:
    def __init__(self, *, account_id: builtins.str, email: builtins.str) -> None:
        '''
        :param account_id: 
        :param email: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "account_id": account_id,
            "email": email,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> builtins.str:
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcceptMemberAccountOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-aws-secure.AddSecurityHubMemberAccountOptions",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId", "email": "email"},
)
class AddSecurityHubMemberAccountOptions:
    def __init__(self, *, account_id: builtins.str, email: builtins.str) -> None:
        '''
        :param account_id: 
        :param email: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "account_id": account_id,
            "email": email,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> builtins.str:
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddSecurityHubMemberAccountOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BaseLine(
    cdktf.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-aws-secure.BaseLine",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        vpc_id: builtins.str,
        enable_guardduty: typing.Optional[builtins.bool] = None,
        enable_iam_account_password_policy: typing.Optional[builtins.bool] = None,
        enable_vpc_flow_log: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param vpc_id: 
        :param enable_guardduty: 
        :param enable_iam_account_password_policy: 
        :param enable_vpc_flow_log: 
        '''
        props = BaseLineProps(
            vpc_id=vpc_id,
            enable_guardduty=enable_guardduty,
            enable_iam_account_password_policy=enable_iam_account_password_policy,
            enable_vpc_flow_log=enable_vpc_flow_log,
        )

        jsii.create(BaseLine, self, [scope, name, props])


@jsii.data_type(
    jsii_type="cdktf-aws-secure.BaseLineProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc_id": "vpcId",
        "enable_guardduty": "enableGuardduty",
        "enable_iam_account_password_policy": "enableIamAccountPasswordPolicy",
        "enable_vpc_flow_log": "enableVpcFlowLog",
    },
)
class BaseLineProps:
    def __init__(
        self,
        *,
        vpc_id: builtins.str,
        enable_guardduty: typing.Optional[builtins.bool] = None,
        enable_iam_account_password_policy: typing.Optional[builtins.bool] = None,
        enable_vpc_flow_log: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param vpc_id: 
        :param enable_guardduty: 
        :param enable_iam_account_password_policy: 
        :param enable_vpc_flow_log: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "vpc_id": vpc_id,
        }
        if enable_guardduty is not None:
            self._values["enable_guardduty"] = enable_guardduty
        if enable_iam_account_password_policy is not None:
            self._values["enable_iam_account_password_policy"] = enable_iam_account_password_policy
        if enable_vpc_flow_log is not None:
            self._values["enable_vpc_flow_log"] = enable_vpc_flow_log

    @builtins.property
    def vpc_id(self) -> builtins.str:
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_guardduty(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_guardduty")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_iam_account_password_policy(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_iam_account_password_policy")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_vpc_flow_log(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_vpc_flow_log")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseLineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnableAccountPasswordPolicy(
    cdktf.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-aws-secure.EnableAccountPasswordPolicy",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        allow_users_to_change_password: typing.Optional[builtins.bool] = None,
        max_password_age: typing.Optional[jsii.Number] = None,
        minimum_password_length: typing.Optional[jsii.Number] = None,
        password_reuse_prevention: typing.Optional[jsii.Number] = None,
        require_lowercase_characters: typing.Optional[builtins.bool] = None,
        require_numbers: typing.Optional[builtins.bool] = None,
        require_symbols: typing.Optional[builtins.bool] = None,
        require_uppercase_characters: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param allow_users_to_change_password: 
        :param max_password_age: 
        :param minimum_password_length: 
        :param password_reuse_prevention: 
        :param require_lowercase_characters: 
        :param require_numbers: 
        :param require_symbols: 
        :param require_uppercase_characters: 
        '''
        props = EnableAccountPasswordPolicyProps(
            allow_users_to_change_password=allow_users_to_change_password,
            max_password_age=max_password_age,
            minimum_password_length=minimum_password_length,
            password_reuse_prevention=password_reuse_prevention,
            require_lowercase_characters=require_lowercase_characters,
            require_numbers=require_numbers,
            require_symbols=require_symbols,
            require_uppercase_characters=require_uppercase_characters,
        )

        jsii.create(EnableAccountPasswordPolicy, self, [scope, name, props])

    @jsii.member(jsii_name="addConfigRule")
    def add_config_rule(self, tags: typing.Any = None) -> None:
        '''Add Config Rule for Account Password policy.

        :param tags: Config Rule tags.
        '''
        return typing.cast(None, jsii.invoke(self, "addConfigRule", [tags]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="expirePasswords")
    def expire_passwords(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "expirePasswords"))


@jsii.data_type(
    jsii_type="cdktf-aws-secure.EnableAccountPasswordPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_users_to_change_password": "allowUsersToChangePassword",
        "max_password_age": "maxPasswordAge",
        "minimum_password_length": "minimumPasswordLength",
        "password_reuse_prevention": "passwordReusePrevention",
        "require_lowercase_characters": "requireLowercaseCharacters",
        "require_numbers": "requireNumbers",
        "require_symbols": "requireSymbols",
        "require_uppercase_characters": "requireUppercaseCharacters",
    },
)
class EnableAccountPasswordPolicyProps:
    def __init__(
        self,
        *,
        allow_users_to_change_password: typing.Optional[builtins.bool] = None,
        max_password_age: typing.Optional[jsii.Number] = None,
        minimum_password_length: typing.Optional[jsii.Number] = None,
        password_reuse_prevention: typing.Optional[jsii.Number] = None,
        require_lowercase_characters: typing.Optional[builtins.bool] = None,
        require_numbers: typing.Optional[builtins.bool] = None,
        require_symbols: typing.Optional[builtins.bool] = None,
        require_uppercase_characters: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param allow_users_to_change_password: 
        :param max_password_age: 
        :param minimum_password_length: 
        :param password_reuse_prevention: 
        :param require_lowercase_characters: 
        :param require_numbers: 
        :param require_symbols: 
        :param require_uppercase_characters: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if allow_users_to_change_password is not None:
            self._values["allow_users_to_change_password"] = allow_users_to_change_password
        if max_password_age is not None:
            self._values["max_password_age"] = max_password_age
        if minimum_password_length is not None:
            self._values["minimum_password_length"] = minimum_password_length
        if password_reuse_prevention is not None:
            self._values["password_reuse_prevention"] = password_reuse_prevention
        if require_lowercase_characters is not None:
            self._values["require_lowercase_characters"] = require_lowercase_characters
        if require_numbers is not None:
            self._values["require_numbers"] = require_numbers
        if require_symbols is not None:
            self._values["require_symbols"] = require_symbols
        if require_uppercase_characters is not None:
            self._values["require_uppercase_characters"] = require_uppercase_characters

    @builtins.property
    def allow_users_to_change_password(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("allow_users_to_change_password")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_password_age(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_password_age")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_password_length(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("minimum_password_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_reuse_prevention(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("password_reuse_prevention")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def require_lowercase_characters(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("require_lowercase_characters")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def require_numbers(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("require_numbers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def require_symbols(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("require_symbols")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def require_uppercase_characters(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("require_uppercase_characters")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnableAccountPasswordPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnableCloudTrail(
    cdktf.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-aws-secure.EnableCloudTrail",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        bucket_key_prefix: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param bucket_key_prefix: 
        :param bucket_name: 
        :param tags: 
        '''
        props = EnableCloudTrailProps(
            bucket_key_prefix=bucket_key_prefix, bucket_name=bucket_name, tags=tags
        )

        jsii.create(EnableCloudTrail, self, [scope, name, props])

    @jsii.member(jsii_name="addConfigRule")
    def add_config_rule(self, tags: typing.Any = None) -> None:
        '''Add Config Rule for Cloudtrail enabled.

        :param tags: Config Rule tags.
        '''
        return typing.cast(None, jsii.invoke(self, "addConfigRule", [tags]))


@jsii.data_type(
    jsii_type="cdktf-aws-secure.EnableCloudTrailProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_key_prefix": "bucketKeyPrefix",
        "bucket_name": "bucketName",
        "tags": "tags",
    },
)
class EnableCloudTrailProps:
    def __init__(
        self,
        *,
        bucket_key_prefix: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param bucket_key_prefix: 
        :param bucket_name: 
        :param tags: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if bucket_key_prefix is not None:
            self._values["bucket_key_prefix"] = bucket_key_prefix
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def bucket_key_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnableCloudTrailProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnableEbsEncryption(
    cdktf.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-aws-secure.EnableEbsEncryption",
):
    def __init__(self, scope: constructs.Construct, name: builtins.str) -> None:
        '''
        :param scope: -
        :param name: -
        '''
        jsii.create(EnableEbsEncryption, self, [scope, name])

    @jsii.member(jsii_name="addConfigRule")
    def add_config_rule(self, tags: typing.Any = None) -> None:
        '''Add Config Rule for EBS default encrypt enabled.

        :param tags: Config Rule tags.
        '''
        return typing.cast(None, jsii.invoke(self, "addConfigRule", [tags]))


class EnableGuardduty(
    cdktf.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-aws-secure.EnableGuardduty",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        finding_publishing_frequency: typing.Optional[builtins.str] = None,
        members: typing.Any = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param finding_publishing_frequency: 
        :param members: 
        :param tags: 
        '''
        props = EnableGuarddutyProps(
            finding_publishing_frequency=finding_publishing_frequency,
            members=members,
            tags=tags,
        )

        jsii.create(EnableGuardduty, self, [scope, name, props])

    @jsii.member(jsii_name="acceptMemberAccount")
    def accept_member_account(
        self,
        id: builtins.str,
        *,
        account_id: builtins.str,
        email: builtins.str,
    ) -> None:
        '''Accept Member Account.

        :param id: Guardduty member id.
        :param account_id: 
        :param email: 
        '''
        options = AcceptMemberAccountOptions(account_id=account_id, email=email)

        return typing.cast(None, jsii.invoke(self, "acceptMemberAccount", [id, options]))

    @jsii.member(jsii_name="addConfigRule")
    def add_config_rule(self, tags: typing.Any = None) -> None:
        '''Add Config Rule for Guardduty.

        :param tags: Config Rule tags.
        '''
        return typing.cast(None, jsii.invoke(self, "addConfigRule", [tags]))

    @jsii.member(jsii_name="inviteAccepterMemberAccount")
    def invite_accepter_member_account(
        self,
        id: builtins.str,
        *,
        master_account_id: builtins.str,
    ) -> None:
        '''Accept Member Account.

        :param id: Guardduty member id.
        :param master_account_id: 
        '''
        options = InviteAccepterMemberAccountOptions(
            master_account_id=master_account_id
        )

        return typing.cast(None, jsii.invoke(self, "inviteAccepterMemberAccount", [id, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))


@jsii.data_type(
    jsii_type="cdktf-aws-secure.EnableGuarddutyProps",
    jsii_struct_bases=[],
    name_mapping={
        "finding_publishing_frequency": "findingPublishingFrequency",
        "members": "members",
        "tags": "tags",
    },
)
class EnableGuarddutyProps:
    def __init__(
        self,
        *,
        finding_publishing_frequency: typing.Optional[builtins.str] = None,
        members: typing.Any = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param finding_publishing_frequency: 
        :param members: 
        :param tags: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if finding_publishing_frequency is not None:
            self._values["finding_publishing_frequency"] = finding_publishing_frequency
        if members is not None:
            self._values["members"] = members
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def finding_publishing_frequency(self) -> typing.Optional[builtins.str]:
        result = self._values.get("finding_publishing_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def members(self) -> typing.Any:
        result = self._values.get("members")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnableGuarddutyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnableSecurityHub(
    cdktf.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-aws-secure.EnableSecurityHub",
):
    def __init__(self, scope: constructs.Construct, name: builtins.str) -> None:
        '''
        :param scope: -
        :param name: -
        '''
        jsii.create(EnableSecurityHub, self, [scope, name])

    @jsii.member(jsii_name="addConfigRule")
    def add_config_rule(self, tags: typing.Any = None) -> None:
        '''Add Config Rule for Security Hub enabled.

        :param tags: Config Rule tags.
        '''
        return typing.cast(None, jsii.invoke(self, "addConfigRule", [tags]))

    @jsii.member(jsii_name="addSecurityHubMemberAccount")
    def add_security_hub_member_account(
        self,
        id: builtins.str,
        *,
        account_id: builtins.str,
        email: builtins.str,
    ) -> None:
        '''Add Member Account of Security Hub.

        :param id: Security Hub member id.
        :param account_id: 
        :param email: 
        '''
        options = AddSecurityHubMemberAccountOptions(
            account_id=account_id, email=email
        )

        return typing.cast(None, jsii.invoke(self, "addSecurityHubMemberAccount", [id, options]))


class EnableVpcFlowLog(
    cdktf.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-aws-secure.EnableVpcFlowLog",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        vpc_id: builtins.str,
        log_destination: typing.Optional[builtins.str] = None,
        log_destination_type: typing.Optional[builtins.str] = None,
        log_format: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        traffic_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param vpc_id: 
        :param log_destination: 
        :param log_destination_type: 
        :param log_format: 
        :param tags: 
        :param traffic_type: 
        '''
        props = EnableVpcFlowLogProps(
            vpc_id=vpc_id,
            log_destination=log_destination,
            log_destination_type=log_destination_type,
            log_format=log_format,
            tags=tags,
            traffic_type=traffic_type,
        )

        jsii.create(EnableVpcFlowLog, self, [scope, name, props])

    @jsii.member(jsii_name="addConfigRule")
    def add_config_rule(self, tags: typing.Any = None) -> None:
        '''Add Config Rule for Vpc flow log.

        :param tags: Config Rule tags.
        '''
        return typing.cast(None, jsii.invoke(self, "addConfigRule", [tags]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cwLogGroupArn")
    def cw_log_group_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cwLogGroupArn"))


@jsii.data_type(
    jsii_type="cdktf-aws-secure.EnableVpcFlowLogProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc_id": "vpcId",
        "log_destination": "logDestination",
        "log_destination_type": "logDestinationType",
        "log_format": "logFormat",
        "tags": "tags",
        "traffic_type": "trafficType",
    },
)
class EnableVpcFlowLogProps:
    def __init__(
        self,
        *,
        vpc_id: builtins.str,
        log_destination: typing.Optional[builtins.str] = None,
        log_destination_type: typing.Optional[builtins.str] = None,
        log_format: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        traffic_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vpc_id: 
        :param log_destination: 
        :param log_destination_type: 
        :param log_format: 
        :param tags: 
        :param traffic_type: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "vpc_id": vpc_id,
        }
        if log_destination is not None:
            self._values["log_destination"] = log_destination
        if log_destination_type is not None:
            self._values["log_destination_type"] = log_destination_type
        if log_format is not None:
            self._values["log_format"] = log_format
        if tags is not None:
            self._values["tags"] = tags
        if traffic_type is not None:
            self._values["traffic_type"] = traffic_type

    @builtins.property
    def vpc_id(self) -> builtins.str:
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_destination(self) -> typing.Optional[builtins.str]:
        result = self._values.get("log_destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_destination_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("log_destination_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_format(self) -> typing.Optional[builtins.str]:
        result = self._values.get("log_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def traffic_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("traffic_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnableVpcFlowLogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-aws-secure.InviteAccepterMemberAccountOptions",
    jsii_struct_bases=[],
    name_mapping={"master_account_id": "masterAccountId"},
)
class InviteAccepterMemberAccountOptions:
    def __init__(self, *, master_account_id: builtins.str) -> None:
        '''
        :param master_account_id: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "master_account_id": master_account_id,
        }

    @builtins.property
    def master_account_id(self) -> builtins.str:
        result = self._values.get("master_account_id")
        assert result is not None, "Required property 'master_account_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InviteAccepterMemberAccountOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AcceptMemberAccountOptions",
    "AddSecurityHubMemberAccountOptions",
    "BaseLine",
    "BaseLineProps",
    "EnableAccountPasswordPolicy",
    "EnableAccountPasswordPolicyProps",
    "EnableCloudTrail",
    "EnableCloudTrailProps",
    "EnableEbsEncryption",
    "EnableGuardduty",
    "EnableGuarddutyProps",
    "EnableSecurityHub",
    "EnableVpcFlowLog",
    "EnableVpcFlowLogProps",
    "InviteAccepterMemberAccountOptions",
]

publication.publish()
