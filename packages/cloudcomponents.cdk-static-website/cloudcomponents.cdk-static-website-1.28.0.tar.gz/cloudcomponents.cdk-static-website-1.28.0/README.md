[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-static-website

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-static-website)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-static-website/)
[![Mentioned in Awesome CDK](https://awesome.re/mentioned-badge.svg)](https://github.com/kolomied/awesome-cdk)

> Cdk component that creates a static website using S3, configures CloudFront (CDN) and maps a custom domain via Route53 (DNS)

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-static-website
```

Python:

```bash
pip install cloudcomponents.cdk-static-website
```

## How to use

### Example 1: With an existing certificate

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, RemovalPolicy, Stack, StackProps
from aws_cdk.aws_ssm import StringParameter
from aws_cdk.aws_cloudfront import SecurityPolicyProtocol
from cloudcomponents.cdk_static_website import StaticWebsite
from cloudcomponents.cdk_lambda_at_edge_pattern import HttpHeaders

class StaticWebsiteStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        certificate_arn = StringParameter.value_from_lookup(self, "/certificate/cloudcomponents.org")

        website = StaticWebsite(self, "StaticWebsite",
            bucket_configuration=WebsiteBucketProps(
                removal_policy=RemovalPolicy.DESTROY
            ),
            alias_configuration=AliasProps(
                domain_name="cloudcomponents.org",
                names=["www.cloudcomponents.org", "cloudcomponents.org"],
                acm_cert_ref=certificate_arn
            )
        )

        # A us-east-1 stack is generated under the hood
        http_headers = HttpHeaders(self, "HttpHeaders",
            http_headers={
                "Content-Security-Policy": "default-src 'none'; img-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; object-src 'none'; connect-src 'self'",
                "Strict-Transport-Security": "max-age=31536000; includeSubdomains; preload",
                "Referrer-Policy": "same-origin",
                "X-XSS-Protection": "1; mode=block",
                "X-Frame-Options": "DENY",
                "X-Content-Type-Options": "nosniff",
                "Cache-Control": "no-cache"
            }
        )

        website.add_lambda_function_association(http_headers)
```

### Example 2: Cloudfront URL with existing sources and up to date Securitypolicy

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, RemovalPolicy, Stack, StackProps
from aws_cdk.aws_ssm import StringParameter
from cloudcomponents.cdk_static_website import StaticWebsite
from aws_cdk.aws_cloudfront import SecurityPolicyProtocol

class StaticWebsiteWithExistingSourcesAndSecurityPolicyStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        certificate_arn = StringParameter.value_from_lookup(self, "/certificate/cloudcomponents.org")

        StaticWebsite(self, "StaticWebsite",
            bucket_configuration=WebsiteBucketProps(
                source="../path/to/your/static/webpage",
                removal_policy=RemovalPolicy.DESTROY
            ),
            alias_configuration=AliasProps(
                domain_name="cloudcomponents.org",
                names=["www.cloudcomponents.org", "cloudcomponents.org"],
                acm_cert_ref=certificate_arn,
                security_policy=SecurityPolicyProtocol.TLS_V1_2_2018
            )
        )
```

### Lambda@Edge function

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
website.add_lambda_function_association(
    event_type=LambdaEdgeEventType.ORIGIN_REQUEST,
    lambda_function=Version.from_version_arn(stack, "LambdaEdge", "arn:aws:lambda:us-east-1:123456789012:function:my-function:1")
)
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-static-website/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-static-website/LICENSE)
