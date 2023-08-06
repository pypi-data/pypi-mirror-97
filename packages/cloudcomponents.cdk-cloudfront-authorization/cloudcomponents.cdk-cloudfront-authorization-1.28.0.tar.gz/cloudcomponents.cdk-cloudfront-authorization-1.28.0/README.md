[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-cloudfront-authorization

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-cloudfront-authorization)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-cloudfront-authorization/)
[![Mentioned in Awesome CDK](https://awesome.re/mentioned-badge.svg)](https://github.com/kolomied/awesome-cdk)

> CloudFront with Cognito authentication using Lambda@Edge

This construct is based on https://github.com/aws-samples/cloudfront-authorization-at-edge.

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-cloudfront-authorization
```

Python:

```bash
pip install cloudcomponents.cdk-cloudfront-authorization
```

## How to use SPA

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from aws_cdk.aws_cognito import UserPool
from cloudcomponents.cdk_cloudfront_authorization import SpaAuthorization, SpaDistribution

class CloudFrontAuthorizationStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        user_pool = UserPool(self, "UserPool",
            self_sign_up_enabled=False,
            user_pool_name="cloudfront-authorization-userpool"
        )

        # UserPool must have a domain!
        user_pool.add_domain("Domain",
            cognito_domain=CognitoDomainOptions(
                domain_prefix="cloudcomponents"
            )
        )

        authorization = SpaAuthorization(self, "Authorization",
            user_pool=user_pool
        )

        SpaDistribution(self, "Distribution",
            authorization=authorization
        )
```

## How to use StaticSite

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from aws_cdk.aws_cognito import UserPool
from cloudcomponents.cdk_cloudfront_authorization import StaticSiteAuthorization, StaticSiteDistribution

class CloudFrontAuthorizationStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        user_pool = UserPool(self, "UserPool",
            self_sign_up_enabled=False,
            user_pool_name="cloudfront-authorization-userpool"
        )

        # UserPool must have a domain!
        user_pool.add_domain("Domain",
            cognito_domain=CognitoDomainOptions(
                domain_prefix="cloudcomponents"
            )
        )

        authorization = StaticSiteAuthorization(self, "Authorization",
            user_pool=user_pool
        )

        StaticSiteDistribution(self, "Distribution",
            authorization=authorization
        )
```

## Legacy CloudFrontWebDistribution

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_cloudfront import CloudFrontWebDistribution, OriginAccessIdentity
from aws_cdk.aws_cognito import UserPool
from aws_cdk.aws_s3 import Bucket
from aws_cdk.core import Construct, Stack, StackProps, RemovalPolicy
from cloudcomponentscdk_cloudfront_authorization import SpaAuthorization

class CloudFrontAuthorizationStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        user_pool = UserPool(self, "UserPool",
            self_sign_up_enabled=False,
            user_pool_name="cloudfront-authorization-userpool"
        )

        user_pool.add_domain("Domain",
            cognito_domain=CognitoDomainOptions(
                domain_prefix="cloudcomponents"
            )
        )

        authorization = SpaAuthorization(self, "Authorization",
            user_pool=user_pool
        )

        bucket = Bucket(self, "Bucket",
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        origin_access_identity = OriginAccessIdentity(self, "OriginAccessIdentity",
            comment=f"CloudFront OriginAccessIdentity for {bucket.bucketName}"
        )

        CloudFrontWebDistribution(self, "Distribution",
            origin_configs=[SourceConfiguration(
                s3_origin_source=S3OriginConfig(
                    s3_bucket_source=bucket,
                    origin_access_identity=origin_access_identity
                ),
                behaviors=[authorization.create_legacy_default_behavior(), (SpreadElement ...authorization.createLegacyAdditionalBehaviors()
                  authorization.create_legacy_additional_behaviors())]
            )
            ]
        )
```

## Identity Providers

Identity providers can be specified in the authorization object. To make sure that the user pool client is created after the identity provider, please specify a dependency using "addDependency".

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
identity_provider = UserPoolIdentityProviderAmazon(self, "IdentityProvider")
authorization = SpaAuthorization(self, "Authorization_SPA",
    # ...
    identity_providers=[cognito.UserPoolClientIdentityProvider.AMAZON]
)
authorization.user_pool_client.node.add_dependency(identity_provider)
```

## SPA mode vs. Static Site mode

### SPA

* User Pool client does not use a client secret
* The cookies with JWT's are not "http only", so that they can be read and used by the SPA (e.g. to display the user name, or to refresh tokens)
* 404's (page not found on S3) will return index.html, to enable SPA-routing

### Static Site

* Enforce use of a client secret
* Set cookies to be http only by default (unless you've provided other cookie settings explicitly)
* No special error handling

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-cloudfront-authorization/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-cloudfront-authorization/LICENSE)
