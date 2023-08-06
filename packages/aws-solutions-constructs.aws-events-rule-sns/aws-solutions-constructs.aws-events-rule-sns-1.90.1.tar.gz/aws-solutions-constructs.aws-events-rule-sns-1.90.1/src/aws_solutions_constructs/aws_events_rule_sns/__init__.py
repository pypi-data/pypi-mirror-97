'''
# aws-events-rule-sns module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_events_rule_sns`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-events-rule-sns`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.eventsrulesns`|

This AWS Solutions Construct implements an AWS Events rule and an AWS SNS Topic.

Here is a minimal deployable pattern definition in Typescript:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Duration
import aws_cdk.aws_events as events
import aws_cdk.aws_iam as iam
from aws_solutions_constructs.aws_events_rule_sns import EventsRuleToSnsProps, EventsRuleToSns

props = EventsRuleToSnsProps(
    event_rule_props=RuleProps(
        schedule=events.Schedule.rate(Duration.minutes(5))
    )
)

construct_stack = EventsRuleToSns(self, "test-construct", props)

# Grant yourself permissions to use the Customer Managed KMS Key
policy_statement = iam.PolicyStatement(
    actions=["kms:Encrypt", "kms:Decrypt"],
    effect=iam.Effect.ALLOW,
    principals=[iam.AccountRootPrincipal()],
    resources=["*"]
)

construct_stack.encryption_key.add_to_resource_policy(policy_statement)
```

## Initializer

```text
new EventsRuleToSns(scope: Construct, id: string, props: EventsRuleToSnsProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`EventsRuleToSnsProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|eventRuleProps|[`events.RuleProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.RuleProps.html)|User provided eventRuleProps to override the defaults. |
|existingTopicObj?|[`sns.Topic`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Existing instance of SNS Topic object, if this is set then the topicProps is ignored.|
|topicProps?|[`sns.TopicProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sns.TopicProps.html)|User provided props to override the default props for the SNS Topic. |
|enableEncryptionWithCustomerManagedKey?|`boolean`|Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct.|
|encryptionKey?|[`kms.Key`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kms.Key.html)|An optional, imported encryption key to encrypt the SNS Topic.|
|encryptionKeyProps?|[`kms.KeyProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kms.KeyProps.html)|An optional, user provided properties to override the default properties for the KMS encryption key.|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|eventsRule|[`events.Rule`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.Rule.html)|Returns an instance of events.Rule created by the construct|
|snsTopic|[`sns.Topic`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sns.Topic.html)|Returns an instance of sns.Topic created by the construct|
|encryptionKey?|[`kms.Key`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kms.Key.html)|Returns an instance of kms Key used for the SNS Topic.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon CloudWatch Events Rule

* Grant least privilege permissions to CloudWatch Events to publish to the SNS Topic.

### Amazon SNS Topic

* Configure least privilege access permissions for SNS Topic.
* Enable server-side encryption forSNS Topic using Customer managed KMS Key.
* Enforce encryption of data in transit.

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
import aws_cdk.aws_kms
import aws_cdk.aws_sns
import aws_cdk.core


class EventsRuleToSns(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-events-rule-sns.EventsRuleToSns",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        event_rule_props: aws_cdk.aws_events.RuleProps,
        enable_encryption_with_customer_managed_key: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.Key] = None,
        encryption_key_props: typing.Optional[aws_cdk.aws_kms.KeyProps] = None,
        existing_topic_obj: typing.Optional[aws_cdk.aws_sns.Topic] = None,
        topics_props: typing.Optional[aws_cdk.aws_sns.TopicProps] = None,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param enable_encryption_with_customer_managed_key: Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct. Default: - true (encryption enabled, managed by this CDK app).
        :param encryption_key: An optional, imported encryption key to encrypt the SQS queue, and SNS Topic. Default: - not specified.
        :param encryption_key_props: Optional user-provided props to override the default props for the encryption key. Default: - Default props are used.
        :param existing_topic_obj: Existing instance of SNS Topic object, if this is set then topicProps is ignored. Default: - Default props are used
        :param topics_props: User provided props to override the default props for the SNS Topic. Default: - Default props are used

        :access: public
        :since: 1.62.0
        :summary: Constructs a new instance of the EventRuleToSns class.
        '''
        props = EventsRuleToSnsProps(
            event_rule_props=event_rule_props,
            enable_encryption_with_customer_managed_key=enable_encryption_with_customer_managed_key,
            encryption_key=encryption_key,
            encryption_key_props=encryption_key_props,
            existing_topic_obj=existing_topic_obj,
            topics_props=topics_props,
        )

        jsii.create(EventsRuleToSns, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="eventsRule")
    def events_rule(self) -> aws_cdk.aws_events.Rule:
        return typing.cast(aws_cdk.aws_events.Rule, jsii.get(self, "eventsRule"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="snsTopic")
    def sns_topic(self) -> aws_cdk.aws_sns.Topic:
        return typing.cast(aws_cdk.aws_sns.Topic, jsii.get(self, "snsTopic"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.Key]:
        return typing.cast(typing.Optional[aws_cdk.aws_kms.Key], jsii.get(self, "encryptionKey"))


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-events-rule-sns.EventsRuleToSnsProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_rule_props": "eventRuleProps",
        "enable_encryption_with_customer_managed_key": "enableEncryptionWithCustomerManagedKey",
        "encryption_key": "encryptionKey",
        "encryption_key_props": "encryptionKeyProps",
        "existing_topic_obj": "existingTopicObj",
        "topics_props": "topicsProps",
    },
)
class EventsRuleToSnsProps:
    def __init__(
        self,
        *,
        event_rule_props: aws_cdk.aws_events.RuleProps,
        enable_encryption_with_customer_managed_key: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.Key] = None,
        encryption_key_props: typing.Optional[aws_cdk.aws_kms.KeyProps] = None,
        existing_topic_obj: typing.Optional[aws_cdk.aws_sns.Topic] = None,
        topics_props: typing.Optional[aws_cdk.aws_sns.TopicProps] = None,
    ) -> None:
        '''
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param enable_encryption_with_customer_managed_key: Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct. Default: - true (encryption enabled, managed by this CDK app).
        :param encryption_key: An optional, imported encryption key to encrypt the SQS queue, and SNS Topic. Default: - not specified.
        :param encryption_key_props: Optional user-provided props to override the default props for the encryption key. Default: - Default props are used.
        :param existing_topic_obj: Existing instance of SNS Topic object, if this is set then topicProps is ignored. Default: - Default props are used
        :param topics_props: User provided props to override the default props for the SNS Topic. Default: - Default props are used
        '''
        if isinstance(event_rule_props, dict):
            event_rule_props = aws_cdk.aws_events.RuleProps(**event_rule_props)
        if isinstance(encryption_key_props, dict):
            encryption_key_props = aws_cdk.aws_kms.KeyProps(**encryption_key_props)
        if isinstance(topics_props, dict):
            topics_props = aws_cdk.aws_sns.TopicProps(**topics_props)
        self._values: typing.Dict[str, typing.Any] = {
            "event_rule_props": event_rule_props,
        }
        if enable_encryption_with_customer_managed_key is not None:
            self._values["enable_encryption_with_customer_managed_key"] = enable_encryption_with_customer_managed_key
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if encryption_key_props is not None:
            self._values["encryption_key_props"] = encryption_key_props
        if existing_topic_obj is not None:
            self._values["existing_topic_obj"] = existing_topic_obj
        if topics_props is not None:
            self._values["topics_props"] = topics_props

    @builtins.property
    def event_rule_props(self) -> aws_cdk.aws_events.RuleProps:
        '''User provided eventRuleProps to override the defaults.

        :default: - None
        '''
        result = self._values.get("event_rule_props")
        assert result is not None, "Required property 'event_rule_props' is missing"
        return typing.cast(aws_cdk.aws_events.RuleProps, result)

    @builtins.property
    def enable_encryption_with_customer_managed_key(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''Use a KMS Key, either managed by this CDK app, or imported.

        If importing an encryption key, it must be specified in
        the encryptionKey property for this construct.

        :default: - true (encryption enabled, managed by this CDK app).
        '''
        result = self._values.get("enable_encryption_with_customer_managed_key")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.Key]:
        '''An optional, imported encryption key to encrypt the SQS queue, and SNS Topic.

        :default: - not specified.
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.Key], result)

    @builtins.property
    def encryption_key_props(self) -> typing.Optional[aws_cdk.aws_kms.KeyProps]:
        '''Optional user-provided props to override the default props for the encryption key.

        :default: - Default props are used.
        '''
        result = self._values.get("encryption_key_props")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.KeyProps], result)

    @builtins.property
    def existing_topic_obj(self) -> typing.Optional[aws_cdk.aws_sns.Topic]:
        '''Existing instance of SNS Topic object, if this is set then topicProps is ignored.

        :default: - Default props are used
        '''
        result = self._values.get("existing_topic_obj")
        return typing.cast(typing.Optional[aws_cdk.aws_sns.Topic], result)

    @builtins.property
    def topics_props(self) -> typing.Optional[aws_cdk.aws_sns.TopicProps]:
        '''User provided props to override the default props for the SNS Topic.

        :default: - Default props are used
        '''
        result = self._values.get("topics_props")
        return typing.cast(typing.Optional[aws_cdk.aws_sns.TopicProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventsRuleToSnsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EventsRuleToSns",
    "EventsRuleToSnsProps",
]

publication.publish()
