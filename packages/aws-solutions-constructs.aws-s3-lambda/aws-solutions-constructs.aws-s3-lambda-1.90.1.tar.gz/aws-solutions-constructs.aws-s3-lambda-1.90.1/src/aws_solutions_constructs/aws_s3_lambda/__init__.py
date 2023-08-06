'''
# aws-s3-lambda module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_s3_lambda`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-s3-lambda`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.s3lambda`|

This AWS Solutions Construct implements an Amazon S3 bucket connected to an AWS Lambda function.

Here is a minimal deployable pattern definition in Typescript:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_solutions_constructs.aws_s3_lambda import S3ToLambdaProps, S3ToLambda

S3ToLambda(self, "test-s3-lambda",
    lambda_function_props=FunctionProps(
        code=lambda_.Code.from_asset(f"{__dirname}/lambda"),
        runtime=lambda_.Runtime.NODEJS_12_X,
        handler="index.handler"
    )
)
```

## Initializer

```text
new S3ToLambda(scope: Construct, id: string, props: S3ToLambdaProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`S3ToLambdaProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored.|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|User provided props to override the default props for the Lambda function.|
|existingBucketObj?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Existing instance of S3 Bucket object, if this is set then the bucketProps is ignored.|
|bucketProps?|[`s3.BucketProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.BucketProps.html)|User provided props to override the default props for the S3 Bucket.|
|s3EventSourceProps?|[`S3EventSourceProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda-event-sources.S3EventSourceProps.html)|Optional user provided props to override the default props for S3EventSourceProps|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|lambdaFunction|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of the lambda.Function created by the construct|
|s3Bucket?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Returns an instance of the s3.Bucket created by the construct|
|s3LoggingBucket?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Returns an instance of s3.Bucket created by the construct as the logging bucket for the primary bucket.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon S3 Bucket

* Configure Access logging for S3 Bucket
* Enable server-side encryption for S3 Bucket using AWS managed KMS Key
* Enforce encryption of data in transit
* Turn on the versioning for S3 Bucket
* Don't allow public access for S3 Bucket
* Retain the S3 Bucket when deleting the CloudFormation stack
* Applies Lifecycle rule to move noncurrent object versions to Glacier storage after 90 days

### AWS Lambda Function

* Configure limited privilege access IAM role for Lambda function
* Enable reusing connections with Keep-Alive for NodeJs Lambda function
* Enable X-Ray Tracing
* Set Environment Variables

  * AWS_NODEJS_CONNECTION_REUSE_ENABLED (for Node 10.x and higher functions)

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

import aws_cdk.aws_lambda
import aws_cdk.aws_lambda_event_sources
import aws_cdk.aws_s3
import aws_cdk.core


class S3ToLambda(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-s3-lambda.S3ToLambda",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps] = None,
        existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket] = None,
        existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function] = None,
        lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps] = None,
        s3_event_source_props: typing.Optional[aws_cdk.aws_lambda_event_sources.S3EventSourceProps] = None,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param bucket_props: User provided props to override the default props for the S3 Bucket. Default: - Default props are used
        :param existing_bucket_obj: Existing instance of S3 Bucket object, if this is set then the bucketProps is ignored. Default: - None
        :param existing_lambda_obj: Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored. Default: - None
        :param lambda_function_props: User provided props to override the default props for the Lambda function. Default: - Default props are used
        :param s3_event_source_props: Optional user provided props to override the default props. Default: - Default props are used

        :access: public
        :since: 0.8.0
        :summary: Constructs a new instance of the S3ToLambda class.
        '''
        props = S3ToLambdaProps(
            bucket_props=bucket_props,
            existing_bucket_obj=existing_bucket_obj,
            existing_lambda_obj=existing_lambda_obj,
            lambda_function_props=lambda_function_props,
            s3_event_source_props=s3_event_source_props,
        )

        jsii.create(S3ToLambda, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        return typing.cast(aws_cdk.aws_lambda.Function, jsii.get(self, "lambdaFunction"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        return typing.cast(typing.Optional[aws_cdk.aws_s3.Bucket], jsii.get(self, "s3Bucket"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="s3LoggingBucket")
    def s3_logging_bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        return typing.cast(typing.Optional[aws_cdk.aws_s3.Bucket], jsii.get(self, "s3LoggingBucket"))


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-s3-lambda.S3ToLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_props": "bucketProps",
        "existing_bucket_obj": "existingBucketObj",
        "existing_lambda_obj": "existingLambdaObj",
        "lambda_function_props": "lambdaFunctionProps",
        "s3_event_source_props": "s3EventSourceProps",
    },
)
class S3ToLambdaProps:
    def __init__(
        self,
        *,
        bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps] = None,
        existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket] = None,
        existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function] = None,
        lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps] = None,
        s3_event_source_props: typing.Optional[aws_cdk.aws_lambda_event_sources.S3EventSourceProps] = None,
    ) -> None:
        '''
        :param bucket_props: User provided props to override the default props for the S3 Bucket. Default: - Default props are used
        :param existing_bucket_obj: Existing instance of S3 Bucket object, if this is set then the bucketProps is ignored. Default: - None
        :param existing_lambda_obj: Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored. Default: - None
        :param lambda_function_props: User provided props to override the default props for the Lambda function. Default: - Default props are used
        :param s3_event_source_props: Optional user provided props to override the default props. Default: - Default props are used

        :summary: The properties for the S3ToLambda class.
        '''
        if isinstance(bucket_props, dict):
            bucket_props = aws_cdk.aws_s3.BucketProps(**bucket_props)
        if isinstance(lambda_function_props, dict):
            lambda_function_props = aws_cdk.aws_lambda.FunctionProps(**lambda_function_props)
        if isinstance(s3_event_source_props, dict):
            s3_event_source_props = aws_cdk.aws_lambda_event_sources.S3EventSourceProps(**s3_event_source_props)
        self._values: typing.Dict[str, typing.Any] = {}
        if bucket_props is not None:
            self._values["bucket_props"] = bucket_props
        if existing_bucket_obj is not None:
            self._values["existing_bucket_obj"] = existing_bucket_obj
        if existing_lambda_obj is not None:
            self._values["existing_lambda_obj"] = existing_lambda_obj
        if lambda_function_props is not None:
            self._values["lambda_function_props"] = lambda_function_props
        if s3_event_source_props is not None:
            self._values["s3_event_source_props"] = s3_event_source_props

    @builtins.property
    def bucket_props(self) -> typing.Optional[aws_cdk.aws_s3.BucketProps]:
        '''User provided props to override the default props for the S3 Bucket.

        :default: - Default props are used
        '''
        result = self._values.get("bucket_props")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.BucketProps], result)

    @builtins.property
    def existing_bucket_obj(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        '''Existing instance of S3 Bucket object, if this is set then the bucketProps is ignored.

        :default: - None
        '''
        result = self._values.get("existing_bucket_obj")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.Bucket], result)

    @builtins.property
    def existing_lambda_obj(self) -> typing.Optional[aws_cdk.aws_lambda.Function]:
        '''Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored.

        :default: - None
        '''
        result = self._values.get("existing_lambda_obj")
        return typing.cast(typing.Optional[aws_cdk.aws_lambda.Function], result)

    @builtins.property
    def lambda_function_props(
        self,
    ) -> typing.Optional[aws_cdk.aws_lambda.FunctionProps]:
        '''User provided props to override the default props for the Lambda function.

        :default: - Default props are used
        '''
        result = self._values.get("lambda_function_props")
        return typing.cast(typing.Optional[aws_cdk.aws_lambda.FunctionProps], result)

    @builtins.property
    def s3_event_source_props(
        self,
    ) -> typing.Optional[aws_cdk.aws_lambda_event_sources.S3EventSourceProps]:
        '''Optional user provided props to override the default props.

        :default: - Default props are used
        '''
        result = self._values.get("s3_event_source_props")
        return typing.cast(typing.Optional[aws_cdk.aws_lambda_event_sources.S3EventSourceProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ToLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "S3ToLambda",
    "S3ToLambdaProps",
]

publication.publish()
