'''
# aws-cloudfront-s3 module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Reference Documentation**:| <span style="font-weight: normal">https://docs.aws.amazon.com/solutions/latest/constructs/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_cloudfront_s3`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-cloudfront-s3`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.cloudfronts3`|

This AWS Solutions Construct implements an AWS CloudFront fronting an AWS S3 Bucket.

Here is a minimal deployable pattern definition in Typescript:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_solutions_constructs.aws_cloudfront_s3 import CloudFrontToS3

CloudFrontToS3(self, "test-cloudfront-s3")
```

## Initializer

```text
new CloudFrontToS3(scope: Construct, id: string, props: CloudFrontToS3Props);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`CloudFrontToS3Props`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|existingBucketObj?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Existing instance of S3 Bucket object, if this is set then the bucketProps is ignored.|
|bucketProps?|[`s3.BucketProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.BucketProps.html)|User provided props to override the default props for the S3 Bucket.|
|cloudFrontDistributionProps?|[`cloudfront.DistributionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudfront.DistributionProps.html)|Optional user provided props to override the default props for CloudFront Distribution|
|insertHttpSecurityHeaders?|`boolean`|Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all responses from CloudFront|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|cloudFrontWebDistribution|[`cloudfront.CloudFrontWebDistribution`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudfront.CloudFrontWebDistribution.html)|Returns an instance of cloudfront.CloudFrontWebDistribution created by the construct|
|edgeLambdaFunctionVersion|[`lambda.Version`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Version.html)|Returns an instance of the edge Lambda function version created by the pattern.|
|cloudFrontLoggingBucket|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-s3-readme.html)|Returns an instance of the logging bucket for CloudFront WebDistribution.|
|s3Bucket?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Returns an instance of s3.Bucket created by the construct.|
|s3LoggingBucket?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Returns an instance of s3.Bucket created by the construct as the logging bucket for the primary bucket.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon CloudFront

* Configure Access logging for CloudFront WebDistribution
* Enable automatic injection of best practice HTTP security headers in all responses from CloudFront WebDistribution

### Amazon S3 Bucket

* Configure Access logging for S3 Bucket
* Enable server-side encryption for S3 Bucket using AWS managed KMS Key
* Enforce encryption of data in transit
* Turn on the versioning for S3 Bucket
* Don't allow public access for S3 Bucket
* Retain the S3 Bucket when deleting the CloudFormation stack
* Applies Lifecycle rule to move noncurrent object versions to Glacier storage after 90 days

## Architecture

![Architecture Diagram](architecture.png)

---


© Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import aws_cdk.aws_cloudfront
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.core


class CloudFrontToS3(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-cloudfront-s3.CloudFrontToS3",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps] = None,
        cloud_front_distribution_props: typing.Any = None,
        existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket] = None,
        insert_http_security_headers: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param bucket_props: User provided props to override the default props for the S3 Bucket. Default: - Default props are used
        :param cloud_front_distribution_props: Optional user provided props to override the default props. Default: - Default props are used
        :param existing_bucket_obj: Existing instance of S3 Bucket object, if this is set then the bucketProps is ignored. Default: - None
        :param insert_http_security_headers: Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all responses from cloudfront. Default: - true

        :access: public
        :since: 0.8.0
        :summary: Constructs a new instance of the CloudFrontToS3 class.
        '''
        props = CloudFrontToS3Props(
            bucket_props=bucket_props,
            cloud_front_distribution_props=cloud_front_distribution_props,
            existing_bucket_obj=existing_bucket_obj,
            insert_http_security_headers=insert_http_security_headers,
        )

        jsii.create(CloudFrontToS3, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cloudFrontWebDistribution")
    def cloud_front_web_distribution(self) -> aws_cdk.aws_cloudfront.Distribution:
        return typing.cast(aws_cdk.aws_cloudfront.Distribution, jsii.get(self, "cloudFrontWebDistribution"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cloudFrontLoggingBucket")
    def cloud_front_logging_bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        return typing.cast(typing.Optional[aws_cdk.aws_s3.Bucket], jsii.get(self, "cloudFrontLoggingBucket"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="edgeLambdaFunctionVersion")
    def edge_lambda_function_version(
        self,
    ) -> typing.Optional[aws_cdk.aws_lambda.Version]:
        return typing.cast(typing.Optional[aws_cdk.aws_lambda.Version], jsii.get(self, "edgeLambdaFunctionVersion"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        return typing.cast(typing.Optional[aws_cdk.aws_s3.Bucket], jsii.get(self, "s3Bucket"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="s3LoggingBucket")
    def s3_logging_bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        return typing.cast(typing.Optional[aws_cdk.aws_s3.Bucket], jsii.get(self, "s3LoggingBucket"))


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-cloudfront-s3.CloudFrontToS3Props",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_props": "bucketProps",
        "cloud_front_distribution_props": "cloudFrontDistributionProps",
        "existing_bucket_obj": "existingBucketObj",
        "insert_http_security_headers": "insertHttpSecurityHeaders",
    },
)
class CloudFrontToS3Props:
    def __init__(
        self,
        *,
        bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps] = None,
        cloud_front_distribution_props: typing.Any = None,
        existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket] = None,
        insert_http_security_headers: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param bucket_props: User provided props to override the default props for the S3 Bucket. Default: - Default props are used
        :param cloud_front_distribution_props: Optional user provided props to override the default props. Default: - Default props are used
        :param existing_bucket_obj: Existing instance of S3 Bucket object, if this is set then the bucketProps is ignored. Default: - None
        :param insert_http_security_headers: Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all responses from cloudfront. Default: - true

        :summary: The properties for the CloudFrontToS3 Construct
        '''
        if isinstance(bucket_props, dict):
            bucket_props = aws_cdk.aws_s3.BucketProps(**bucket_props)
        self._values: typing.Dict[str, typing.Any] = {}
        if bucket_props is not None:
            self._values["bucket_props"] = bucket_props
        if cloud_front_distribution_props is not None:
            self._values["cloud_front_distribution_props"] = cloud_front_distribution_props
        if existing_bucket_obj is not None:
            self._values["existing_bucket_obj"] = existing_bucket_obj
        if insert_http_security_headers is not None:
            self._values["insert_http_security_headers"] = insert_http_security_headers

    @builtins.property
    def bucket_props(self) -> typing.Optional[aws_cdk.aws_s3.BucketProps]:
        '''User provided props to override the default props for the S3 Bucket.

        :default: - Default props are used
        '''
        result = self._values.get("bucket_props")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.BucketProps], result)

    @builtins.property
    def cloud_front_distribution_props(self) -> typing.Any:
        '''Optional user provided props to override the default props.

        :default: - Default props are used
        '''
        result = self._values.get("cloud_front_distribution_props")
        return typing.cast(typing.Any, result)

    @builtins.property
    def existing_bucket_obj(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        '''Existing instance of S3 Bucket object, if this is set then the bucketProps is ignored.

        :default: - None
        '''
        result = self._values.get("existing_bucket_obj")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.Bucket], result)

    @builtins.property
    def insert_http_security_headers(self) -> typing.Optional[builtins.bool]:
        '''Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all responses from cloudfront.

        :default: - true
        '''
        result = self._values.get("insert_http_security_headers")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFrontToS3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudFrontToS3",
    "CloudFrontToS3Props",
]

publication.publish()
