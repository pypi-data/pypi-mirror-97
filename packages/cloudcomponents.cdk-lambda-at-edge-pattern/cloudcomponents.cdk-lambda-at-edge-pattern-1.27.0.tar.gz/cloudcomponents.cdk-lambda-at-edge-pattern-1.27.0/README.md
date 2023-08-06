[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-lambda-at-edge-pattern

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-lambda-at-edge-pattern)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-lambda-at-edge-pattern/)

> CDK Constructs for Lambda@Edge pattern: HttpHeaders

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-lambda-at-edge-pattern
```

Python:

```bash
pip install cloudcomponents.cdk-lambda-at-edge-pattern
```

## How to use

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

### Cloudfront Distribution

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cloudfront.Distribution(self, "myDist",
    default_behavior={
        "origin": origins.S3Origin(my_bucket),
        "edge_lambdas": [http_headers]
    }
)
```

### Cloudfront WebDistribution

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cloudfront.CloudFrontWebDistribution(self, "MyDistribution",
    origin_configs=[{
        "s3_origin_source": {
            "s3_bucket_source": source_bucket
        },
        "behaviors": [{
            "is_default_behavior": True,
            "lambda_function_associations": [http_headers]
        }
        ]
    }
    ]
)
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-lambda-at-edge-pattern/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-lambda-at-edge-pattern/LICENSE)
