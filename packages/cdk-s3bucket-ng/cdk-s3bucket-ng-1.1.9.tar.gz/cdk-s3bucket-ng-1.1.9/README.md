[![NPM version](https://badge.fury.io/js/cdk-s3bucket-ng.svg)](https://badge.fury.io/js/cdk-s3bucket-ng)
[![PyPI version](https://badge.fury.io/py/cdk-s3bucket-ng.svg)](https://badge.fury.io/py/cdk-s3bucket-ng)
![Release](https://github.com/guan840912/cdk-s3bucket/workflows/Release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-s3bucket-ng?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-s3bucket-ng?label=pypi&color=blue)

# cdk-s3bucket-ng

cdk-s3bucket-ng is an AWS CDK construct library that provides a drop-in replacement for the Bucket construct with the capability to remove non-empty S3 buckets.

# Why

Sometime we just do some lab , create a S3 Bucket.
Want to destroy resource , after Lab finished.
But We forget delete Object in S3 Bucket first , so destroy will fail.

`cdk-s3bucket-ng`  can help delete object when cdk destroy , just add `removalPolicy: RemovalPolicy.DESTROY`  property .

You never have to delete objects yourself, and the usage is almost the same as the native @aws-cdk/aws-s3.Bucket

## Now Try It !!!

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import App, Stack, CfnOutput, RemovalPolicy
from cdk_s3bucket_ng import BucketNg
import aws_cdk.aws_s3_deployment as s3deploy

# Create a S3 , add props "removalPolicy: RemovalPolicy.DESTROY".
bucket = BucketNg(stack, "Bucket",
    removal_policy=RemovalPolicy.DESTROY
)

# Upload temp file .
s3deploy.BucketDeployment(stack, "addResource",
    sources=[s3deploy.Source.asset("./testdir")],
    destination_bucket=bucket
)
# Get S3 Resource via bucket.s3Bucket ...
CfnOutput(stack, "BucketName", value=bucket.bucket_name)
```

```bash
# create temp file .
mkdir ./testdir
touch ./testdir/{a.txt,b.txt,c.txt}
ls ./testdir
a.txt  b.txt  c.txt
```

### To deploy

```bash
cdk deploy
```

### To destroy

```bash
# will delete object in S3 , and delete S3 Bucket
cdk destroy
```

## :clap:  Supporters

[![Stargazers repo roster for @guan840912/cdk-s3bucket](https://reporoster.com/stars/guan840912/cdk-s3bucket)](https://github.com/guan840912/cdk-s3bucket/stargazers)
