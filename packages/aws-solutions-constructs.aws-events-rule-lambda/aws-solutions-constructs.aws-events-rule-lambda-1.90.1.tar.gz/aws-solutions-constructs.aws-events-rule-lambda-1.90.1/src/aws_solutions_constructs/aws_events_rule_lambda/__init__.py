'''
# aws-events-rule-lambda module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_events_rule_lambda`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-events-rule-lambda`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.eventsrulelambda`|

This AWS Solutions Construct implements an AWS Events rule and an AWS Lambda function.

Here is a minimal deployable pattern definition in Typescript:

```javascript
const { EventsRuleToLambdaProps, EventsRuleToLambda } from '@aws-solutions-constructs/aws-events-rule-lambda';

const props: EventsRuleToLambdaProps = {
    lambdaFunctionProps: {
        code: lambda.Code.fromAsset(`${__dirname}/lambda`),
        runtime: lambda.Runtime.NODEJS_12_X,
        handler: 'index.handler'
    },
    eventRuleProps: {
      schedule: events.Schedule.rate(Duration.minutes(5))
    }
};

new EventsRuleToLambda(this, 'test-events-rule-lambda', props);
```

## Initializer

```text
new EventsRuleToLambda(scope: Construct, id: string, props: EventsRuleToLambdaProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`EventsRuleToLambdaProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored.|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|User provided props to override the default props for the Lambda function.|
|eventRuleProps|[`events.RuleProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.RuleProps.html)|User provided eventRuleProps to override the defaults|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|eventsRule|[`events.Rule`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.Rule.html)|Returns an instance of events.Rule created by the construct|
|lambdaFunction|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of lambda.Function created by the construct|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon CloudWatch Events Rule

* Grant least privilege permissions to CloudWatch Events to trigger the Lambda Function

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

import aws_cdk.aws_events
import aws_cdk.aws_lambda
import aws_cdk.core


class EventsRuleToLambda(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-events-rule-lambda.EventsRuleToLambda",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        event_rule_props: aws_cdk.aws_events.RuleProps,
        existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function] = None,
        lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps] = None,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param existing_lambda_obj: Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored. Default: - None
        :param lambda_function_props: User provided props to override the default props for the Lambda function. Default: - Default props are used

        :access: public
        :since: 0.8.0
        :summary: Constructs a new instance of the EventsRuleToLambda class.
        '''
        props = EventsRuleToLambdaProps(
            event_rule_props=event_rule_props,
            existing_lambda_obj=existing_lambda_obj,
            lambda_function_props=lambda_function_props,
        )

        jsii.create(EventsRuleToLambda, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="eventsRule")
    def events_rule(self) -> aws_cdk.aws_events.Rule:
        return typing.cast(aws_cdk.aws_events.Rule, jsii.get(self, "eventsRule"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        return typing.cast(aws_cdk.aws_lambda.Function, jsii.get(self, "lambdaFunction"))


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-events-rule-lambda.EventsRuleToLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_rule_props": "eventRuleProps",
        "existing_lambda_obj": "existingLambdaObj",
        "lambda_function_props": "lambdaFunctionProps",
    },
)
class EventsRuleToLambdaProps:
    def __init__(
        self,
        *,
        event_rule_props: aws_cdk.aws_events.RuleProps,
        existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function] = None,
        lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps] = None,
    ) -> None:
        '''
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param existing_lambda_obj: Existing instance of Lambda Function object, if this is set then the lambdaFunctionProps is ignored. Default: - None
        :param lambda_function_props: User provided props to override the default props for the Lambda function. Default: - Default props are used

        :summary: The properties for the CloudFrontToApiGateway Construct
        '''
        if isinstance(event_rule_props, dict):
            event_rule_props = aws_cdk.aws_events.RuleProps(**event_rule_props)
        if isinstance(lambda_function_props, dict):
            lambda_function_props = aws_cdk.aws_lambda.FunctionProps(**lambda_function_props)
        self._values: typing.Dict[str, typing.Any] = {
            "event_rule_props": event_rule_props,
        }
        if existing_lambda_obj is not None:
            self._values["existing_lambda_obj"] = existing_lambda_obj
        if lambda_function_props is not None:
            self._values["lambda_function_props"] = lambda_function_props

    @builtins.property
    def event_rule_props(self) -> aws_cdk.aws_events.RuleProps:
        '''User provided eventRuleProps to override the defaults.

        :default: - None
        '''
        result = self._values.get("event_rule_props")
        assert result is not None, "Required property 'event_rule_props' is missing"
        return typing.cast(aws_cdk.aws_events.RuleProps, result)

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

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventsRuleToLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EventsRuleToLambda",
    "EventsRuleToLambdaProps",
]

publication.publish()
