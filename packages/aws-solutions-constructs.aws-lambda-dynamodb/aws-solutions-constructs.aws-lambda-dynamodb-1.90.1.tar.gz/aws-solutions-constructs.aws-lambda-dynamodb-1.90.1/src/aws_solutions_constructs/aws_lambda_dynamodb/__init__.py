'''
# aws-lambda-dynamodb module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_lambda_dynamodb`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-lambda-dynamodb`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.lambdadynamodb`|

This AWS Solutions Construct implements the AWS Lambda function and Amazon DynamoDB table with the least privileged permissions.

Here is a minimal deployable pattern definition in Typescript:

```javascript
const { LambdaToDynamoDBProps,  LambdaToDynamoDB } from '@aws-solutions-constructs/aws-lambda-dynamodb';

const props: LambdaToDynamoDBProps = {
    lambdaFunctionProps: {
        code: lambda.Code.fromAsset(`${__dirname}/lambda`),
        runtime: lambda.Runtime.NODEJS_12_X,
        handler: 'index.handler'
    },
};

new LambdaToDynamoDB(this, 'test-lambda-dynamodb-stack', props);

```

## Initializer

```text
new LambdaToDynamoDB(scope: Construct, id: string, props: LambdaToDynamoDBProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`LambdaToDynamoDBProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored.|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|User provided props to override the default props for the Lambda function.|
|dynamoTableProps?|[`dynamodb.TableProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-dynamodb.TableProps.html)|Optional user provided props to override the default props for DynamoDB Table|
|existingTableObj?|[`dynamodb.Table`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-dynamodb.Table.html)|Existing instance of DynamoDB table object, If this is set then the dynamoTableProps is ignored|
|tablePermissions?|`string`|Optional table permissions to grant to the Lambda function. One of the following may be specified: `All`, `Read`, `ReadWrite`, `Write`.|
|tableEnvironmentVariableName?|`string`|Optional Name for the DynamoDB table environment variable set for the Lambda function.|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|lambdaFunction|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of lambda.Function created by the construct|
|dynamoTable|[`dynamodb.Table`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-dynamodb.Table.html)|Returns an instance of dynamodb.Table created by the construct|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### AWS Lambda Function

* Configure limited privilege access IAM role for Lambda function
* Enable reusing connections with Keep-Alive for NodeJs Lambda function
* Enable X-Ray Tracing
* Set Environment Variables

  * (default) DDB_TABLE_NAME
  * AWS_NODEJS_CONNECTION_REUSE_ENABLED (for Node 10.x and higher functions)

### Amazon DynamoDB Table

* Set the billing mode for DynamoDB Table to On-Demand (Pay per request)
* Enable server-side encryption for DynamoDB Table using AWS managed KMS Key
* Creates a partition key called 'id' for DynamoDB Table
* Retain the Table when deleting the CloudFormation stack
* Enable continuous backups and point-in-time recovery

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

import aws_cdk.aws_dynamodb
import aws_cdk.aws_lambda
import aws_cdk.core


class LambdaToDynamoDB(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-lambda-dynamodb.LambdaToDynamoDB",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        dynamo_table_props: typing.Optional[aws_cdk.aws_dynamodb.TableProps] = None,
        existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function] = None,
        existing_table_obj: typing.Optional[aws_cdk.aws_dynamodb.Table] = None,
        lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps] = None,
        table_environment_variable_name: typing.Optional[builtins.str] = None,
        table_permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param dynamo_table_props: Optional user provided props to override the default props. Default: - Default props are used
        :param existing_lambda_obj: Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored. Default: - None
        :param existing_table_obj: Existing instance of DynamoDB table object, If this is set then the dynamoTableProps is ignored. Default: - None
        :param lambda_function_props: User provided props to override the default props for the Lambda function. Default: - Default props are used
        :param table_environment_variable_name: Optional Name for the DynamoDB table environment variable set for the Lambda function. Default: - None
        :param table_permissions: Optional table permissions to grant to the Lambda function. One of the following may be specified: "All", "Read", "ReadWrite", "Write". Default: - Read/write access is given to the Lambda function if no value is specified.

        :access: public
        :since: 0.8.0
        :summary: Constructs a new instance of the LambdaToDynamoDB class.
        '''
        props = LambdaToDynamoDBProps(
            dynamo_table_props=dynamo_table_props,
            existing_lambda_obj=existing_lambda_obj,
            existing_table_obj=existing_table_obj,
            lambda_function_props=lambda_function_props,
            table_environment_variable_name=table_environment_variable_name,
            table_permissions=table_permissions,
        )

        jsii.create(LambdaToDynamoDB, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dynamoTable")
    def dynamo_table(self) -> aws_cdk.aws_dynamodb.Table:
        return typing.cast(aws_cdk.aws_dynamodb.Table, jsii.get(self, "dynamoTable"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        return typing.cast(aws_cdk.aws_lambda.Function, jsii.get(self, "lambdaFunction"))


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-lambda-dynamodb.LambdaToDynamoDBProps",
    jsii_struct_bases=[],
    name_mapping={
        "dynamo_table_props": "dynamoTableProps",
        "existing_lambda_obj": "existingLambdaObj",
        "existing_table_obj": "existingTableObj",
        "lambda_function_props": "lambdaFunctionProps",
        "table_environment_variable_name": "tableEnvironmentVariableName",
        "table_permissions": "tablePermissions",
    },
)
class LambdaToDynamoDBProps:
    def __init__(
        self,
        *,
        dynamo_table_props: typing.Optional[aws_cdk.aws_dynamodb.TableProps] = None,
        existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function] = None,
        existing_table_obj: typing.Optional[aws_cdk.aws_dynamodb.Table] = None,
        lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps] = None,
        table_environment_variable_name: typing.Optional[builtins.str] = None,
        table_permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dynamo_table_props: Optional user provided props to override the default props. Default: - Default props are used
        :param existing_lambda_obj: Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored. Default: - None
        :param existing_table_obj: Existing instance of DynamoDB table object, If this is set then the dynamoTableProps is ignored. Default: - None
        :param lambda_function_props: User provided props to override the default props for the Lambda function. Default: - Default props are used
        :param table_environment_variable_name: Optional Name for the DynamoDB table environment variable set for the Lambda function. Default: - None
        :param table_permissions: Optional table permissions to grant to the Lambda function. One of the following may be specified: "All", "Read", "ReadWrite", "Write". Default: - Read/write access is given to the Lambda function if no value is specified.

        :summary: The properties for the LambdaToDynamoDB Construct
        '''
        if isinstance(dynamo_table_props, dict):
            dynamo_table_props = aws_cdk.aws_dynamodb.TableProps(**dynamo_table_props)
        if isinstance(lambda_function_props, dict):
            lambda_function_props = aws_cdk.aws_lambda.FunctionProps(**lambda_function_props)
        self._values: typing.Dict[str, typing.Any] = {}
        if dynamo_table_props is not None:
            self._values["dynamo_table_props"] = dynamo_table_props
        if existing_lambda_obj is not None:
            self._values["existing_lambda_obj"] = existing_lambda_obj
        if existing_table_obj is not None:
            self._values["existing_table_obj"] = existing_table_obj
        if lambda_function_props is not None:
            self._values["lambda_function_props"] = lambda_function_props
        if table_environment_variable_name is not None:
            self._values["table_environment_variable_name"] = table_environment_variable_name
        if table_permissions is not None:
            self._values["table_permissions"] = table_permissions

    @builtins.property
    def dynamo_table_props(self) -> typing.Optional[aws_cdk.aws_dynamodb.TableProps]:
        '''Optional user provided props to override the default props.

        :default: - Default props are used
        '''
        result = self._values.get("dynamo_table_props")
        return typing.cast(typing.Optional[aws_cdk.aws_dynamodb.TableProps], result)

    @builtins.property
    def existing_lambda_obj(self) -> typing.Optional[aws_cdk.aws_lambda.Function]:
        '''Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored.

        :default: - None
        '''
        result = self._values.get("existing_lambda_obj")
        return typing.cast(typing.Optional[aws_cdk.aws_lambda.Function], result)

    @builtins.property
    def existing_table_obj(self) -> typing.Optional[aws_cdk.aws_dynamodb.Table]:
        '''Existing instance of DynamoDB table object, If this is set then the dynamoTableProps is ignored.

        :default: - None
        '''
        result = self._values.get("existing_table_obj")
        return typing.cast(typing.Optional[aws_cdk.aws_dynamodb.Table], result)

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
    def table_environment_variable_name(self) -> typing.Optional[builtins.str]:
        '''Optional Name for the DynamoDB table environment variable set for the Lambda function.

        :default: - None
        '''
        result = self._values.get("table_environment_variable_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_permissions(self) -> typing.Optional[builtins.str]:
        '''Optional table permissions to grant to the Lambda function.

        One of the following may be specified: "All", "Read", "ReadWrite", "Write".

        :default: - Read/write access is given to the Lambda function if no value is specified.
        '''
        result = self._values.get("table_permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaToDynamoDBProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LambdaToDynamoDB",
    "LambdaToDynamoDBProps",
]

publication.publish()
