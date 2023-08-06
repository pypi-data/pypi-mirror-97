# CDK-SPA-Deploy

[![npm](https://img.shields.io/npm/dt/cdk-spa-deploy)](https://www.npmjs.com/package/cdk-spa-deploy)
[![Vulnerabilities](https://img.shields.io/snyk/vulnerabilities/npm/cdk-spa-deploy)](https://www.npmjs.com/package/cdk-spa-deploy)

This is an AWS CDK Construct to make deploying a single page website (Angular/React/Vue) to AWS S3 behind SSL/Cloudfront as easy as 5 lines of code.

## Installation and Usage

### Typescript

```console
npm install --save cdk-spa-deploy
```

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_spa_deploy import SPADeploy

class CdkStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        SPADeploy(self, "spaDeploy").create_basic_site(
            index_doc="index.html",
            website_folder="../blog/dist/blog"
        )

        SPADeploy(self, "cfDeploy").create_site_with_cloudfront(
            index_doc="index.html",
            website_folder="../blog/dist/blog"
        )
```

### Python

```console
pip install cdk-spa-deploy
```

```python
from aws_cdk import core
from spa_deploy import SPADeploy

class PythonStack(core.Stack):
  def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)

    SPADeploy(self, 'spaDeploy').create_basic_site(
      index_doc='index.html',
      website_folder='../blog/blog/dist/blog'
    )


    SPADeploy(self, 'cfDeploy').create_site_with_cloudfront(
      index_doc='index.html',
      website_folder='../blog/blog/dist/blog'
    )
```

### Dotnet / C#

This project has now been published to nuget, more details to follow soon but you can find it [here](https://www.nuget.org/packages/CDKSPADeploy/1.80.0)

```bash
# package manager
Install-Package CDKSPADeploy -Version 1.80.0
# .NET CLI
dotnet add package CDKSPADeploy --version 1.80.0
# Package reference
<PackageReference Include="CDKSPADeploy" Version="1.80.0" />
# Paket CLI
paket add CDKSPADeploy --version 1.80.0
```

### Java

A version has now been published to maven

```xml
<dependency>
  <groupId>com.cdkpatterns</groupId>
  <artifactId>CDKSPADeploy</artifactId>
  <version>1.81.0</version>
</dependency>
```

## Advanced Usage

### Auto Deploy From Hosted Zone Name

If you purchased your domain through route 53 and already have a hosted zone then just use the name to deploy your site behind cloudfront. This handles the SSL cert and everything for you.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
SPADeploy(self, "spaDeploy", encrypt_bucket=True).create_site_from_hosted_zone(
    zone_name="cdkpatterns.com",
    index_doc="index.html",
    website_folder="../website/dist/website"
)
```

### Custom Domain and SSL Certificates

You can also pass the ARN for an SSL certification and your alias routes to cloudfront

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_spa_deploy import SPADeploy

class CdkStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        SPADeploy(self, "cfDeploy").create_site_with_cloudfront(
            index_doc="../blog/dist/blog",
            certificate_aRN="arn:...",
            cf_aliases=["www.alias.com"]
        )
```

### Encrypted S3 Bucket

Pass in one boolean to tell SPA Deploy to encrypt your website bucket

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
SPADeploy(self, "cfDeploy", encrypt_bucket=True).create_basic_site(
    index_doc="index.html",
    website_folder="website"
)
```

### Custom Origin Behaviors

Pass in an array of CloudFront Behaviors

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
SPADeploy(self, "cfDeploy").create_site_with_cloudfront(
    index_doc="index.html",
    website_folder="website",
    cf_behaviors=[{
        "is_default_behavior": True,
        "allowed_methods": cf.CloudFrontAllowedMethods.ALL,
        "forwarded_values": {
            "query_string": True,
            "cookies": {"forward": "all"},
            "headers": ["*"]
        }
    }, {
        "path_pattern": "/virtual-path",
        "allowed_methods": cf.CloudFrontAllowedMethods.GET_HEAD,
        "cached_methods": cf.CloudFrontAllowedCachedMethods.GET_HEAD
    }
    ]
)
```

### Restrict Access to Known IPs

Pass in a boolean and an array of IP addresses and your site is locked down!

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
SPADeploy(stack, "spaDeploy",
    encrypt_bucket=True,
    ip_filter=True,
    ip_list=["1.1.1.1"]
).create_basic_site(
    index_doc="index.html",
    website_folder="website"
)
```

### Modifying S3 Bucket Created in Construct

An object is now returned containing relevant artifacts created if you need to make any further modifications:

* The S3 bucket is present for all of the methods
* When a CloudFront Web distribution is created it will be present in the return object

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
```

## Issues / Feature Requests

https://github.com/nideveloper/CDK-SPA-Deploy
