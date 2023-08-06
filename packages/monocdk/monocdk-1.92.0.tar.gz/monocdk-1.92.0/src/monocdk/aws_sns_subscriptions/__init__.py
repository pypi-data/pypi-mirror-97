import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_sns import (
    ITopic as _ITopic_465e36b9,
    ITopicSubscription as _ITopicSubscription_2a04646f,
    SubscriptionFilter as _SubscriptionFilter_1f5c48ae,
    SubscriptionProtocol as _SubscriptionProtocol_2074d6f2,
    TopicSubscriptionConfig as _TopicSubscriptionConfig_74c52451,
)
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.implements(_ITopicSubscription_2a04646f)
class EmailSubscription(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns_subscriptions.EmailSubscription",
):
    '''(experimental) Use an email address as a subscription target.

    Email subscriptions require confirmation.

    :stability: experimental
    '''

    def __init__(
        self,
        email_address: builtins.str,
        *,
        json: typing.Optional[builtins.bool] = None,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''
        :param email_address: -
        :param json: (experimental) Indicates if the full notification JSON should be sent to the email address or just the message text. Default: false (Message text)
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        props = EmailSubscriptionProps(
            json=json, dead_letter_queue=dead_letter_queue, filter_policy=filter_policy
        )

        jsii.create(EmailSubscription, self, [email_address, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _topic: _ITopic_465e36b9) -> _TopicSubscriptionConfig_74c52451:
        '''(experimental) Returns a configuration for an email address to subscribe to an SNS topic.

        :param _topic: -

        :stability: experimental
        '''
        return typing.cast(_TopicSubscriptionConfig_74c52451, jsii.invoke(self, "bind", [_topic]))


@jsii.implements(_ITopicSubscription_2a04646f)
class LambdaSubscription(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns_subscriptions.LambdaSubscription",
):
    '''(experimental) Use a Lambda function as a subscription target.

    :stability: experimental
    '''

    def __init__(
        self,
        fn: _IFunction_6e14f09e,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''
        :param fn: -
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        props = LambdaSubscriptionProps(
            dead_letter_queue=dead_letter_queue, filter_policy=filter_policy
        )

        jsii.create(LambdaSubscription, self, [fn, props])

    @jsii.member(jsii_name="bind")
    def bind(self, topic: _ITopic_465e36b9) -> _TopicSubscriptionConfig_74c52451:
        '''(experimental) Returns a configuration for a Lambda function to subscribe to an SNS topic.

        :param topic: -

        :stability: experimental
        '''
        return typing.cast(_TopicSubscriptionConfig_74c52451, jsii.invoke(self, "bind", [topic]))


@jsii.implements(_ITopicSubscription_2a04646f)
class SmsSubscription(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns_subscriptions.SmsSubscription",
):
    '''(experimental) Use an sms address as a subscription target.

    :stability: experimental
    '''

    def __init__(
        self,
        phone_number: builtins.str,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''
        :param phone_number: -
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        props = SmsSubscriptionProps(
            dead_letter_queue=dead_letter_queue, filter_policy=filter_policy
        )

        jsii.create(SmsSubscription, self, [phone_number, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _topic: _ITopic_465e36b9) -> _TopicSubscriptionConfig_74c52451:
        '''(experimental) Returns a configuration used to subscribe to an SNS topic.

        :param _topic: -

        :stability: experimental
        '''
        return typing.cast(_TopicSubscriptionConfig_74c52451, jsii.invoke(self, "bind", [_topic]))


@jsii.implements(_ITopicSubscription_2a04646f)
class SqsSubscription(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns_subscriptions.SqsSubscription",
):
    '''(experimental) Use an SQS queue as a subscription target.

    :stability: experimental
    '''

    def __init__(
        self,
        queue: _IQueue_45a01ab4,
        *,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''
        :param queue: -
        :param raw_message_delivery: (experimental) The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        props = SqsSubscriptionProps(
            raw_message_delivery=raw_message_delivery,
            dead_letter_queue=dead_letter_queue,
            filter_policy=filter_policy,
        )

        jsii.create(SqsSubscription, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, topic: _ITopic_465e36b9) -> _TopicSubscriptionConfig_74c52451:
        '''(experimental) Returns a configuration for an SQS queue to subscribe to an SNS topic.

        :param topic: -

        :stability: experimental
        '''
        return typing.cast(_TopicSubscriptionConfig_74c52451, jsii.invoke(self, "bind", [topic]))


@jsii.data_type(
    jsii_type="monocdk.aws_sns_subscriptions.SubscriptionProps",
    jsii_struct_bases=[],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
    },
)
class SubscriptionProps:
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''(experimental) Options to subscribing to an SNS topic.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_ITopicSubscription_2a04646f)
class UrlSubscription(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sns_subscriptions.UrlSubscription",
):
    '''(experimental) Use a URL as a subscription target.

    The message will be POSTed to the given URL.

    :see: https://docs.aws.amazon.com/sns/latest/dg/sns-http-https-endpoint-as-subscriber.html
    :stability: experimental
    '''

    def __init__(
        self,
        url: builtins.str,
        *,
        protocol: typing.Optional[_SubscriptionProtocol_2074d6f2] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''
        :param url: -
        :param protocol: (experimental) The subscription's protocol. Default: - Protocol is derived from url
        :param raw_message_delivery: (experimental) The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        props = UrlSubscriptionProps(
            protocol=protocol,
            raw_message_delivery=raw_message_delivery,
            dead_letter_queue=dead_letter_queue,
            filter_policy=filter_policy,
        )

        jsii.create(UrlSubscription, self, [url, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _topic: _ITopic_465e36b9) -> _TopicSubscriptionConfig_74c52451:
        '''(experimental) Returns a configuration for a URL to subscribe to an SNS topic.

        :param _topic: -

        :stability: experimental
        '''
        return typing.cast(_TopicSubscriptionConfig_74c52451, jsii.invoke(self, "bind", [_topic]))


@jsii.data_type(
    jsii_type="monocdk.aws_sns_subscriptions.UrlSubscriptionProps",
    jsii_struct_bases=[SubscriptionProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
        "protocol": "protocol",
        "raw_message_delivery": "rawMessageDelivery",
    },
)
class UrlSubscriptionProps(SubscriptionProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
        protocol: typing.Optional[_SubscriptionProtocol_2074d6f2] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for URL subscriptions.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered
        :param protocol: (experimental) The subscription's protocol. Default: - Protocol is derived from url
        :param raw_message_delivery: (experimental) The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if protocol is not None:
            self._values["protocol"] = protocol
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    @builtins.property
    def protocol(self) -> typing.Optional[_SubscriptionProtocol_2074d6f2]:
        '''(experimental) The subscription's protocol.

        :default: - Protocol is derived from url

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_SubscriptionProtocol_2074d6f2], result)

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The message to the queue is the same as it was sent to the topic.

        If false, the message will be wrapped in an SNS envelope.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("raw_message_delivery")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UrlSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns_subscriptions.EmailSubscriptionProps",
    jsii_struct_bases=[SubscriptionProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
        "json": "json",
    },
)
class EmailSubscriptionProps(SubscriptionProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
        json: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for email subscriptions.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered
        :param json: (experimental) Indicates if the full notification JSON should be sent to the email address or just the message text. Default: false (Message text)

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if json is not None:
            self._values["json"] = json

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    @builtins.property
    def json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates if the full notification JSON should be sent to the email address or just the message text.

        :default: false (Message text)

        :stability: experimental
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns_subscriptions.LambdaSubscriptionProps",
    jsii_struct_bases=[SubscriptionProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
    },
)
class LambdaSubscriptionProps(SubscriptionProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''(experimental) Properties for a Lambda subscription.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns_subscriptions.SmsSubscriptionProps",
    jsii_struct_bases=[SubscriptionProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
    },
)
class SmsSubscriptionProps(SubscriptionProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''(experimental) Options for SMS subscriptions.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SmsSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_sns_subscriptions.SqsSubscriptionProps",
    jsii_struct_bases=[SubscriptionProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
        "raw_message_delivery": "rawMessageDelivery",
    },
)
class SqsSubscriptionProps(SubscriptionProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
        raw_message_delivery: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for an SQS subscription.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered
        :param raw_message_delivery: (experimental) The message to the queue is the same as it was sent to the topic. If false, the message will be wrapped in an SNS envelope. Default: false

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    @builtins.property
    def raw_message_delivery(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The message to the queue is the same as it was sent to the topic.

        If false, the message will be wrapped in an SNS envelope.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("raw_message_delivery")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EmailSubscription",
    "EmailSubscriptionProps",
    "LambdaSubscription",
    "LambdaSubscriptionProps",
    "SmsSubscription",
    "SmsSubscriptionProps",
    "SqsSubscription",
    "SqsSubscriptionProps",
    "SubscriptionProps",
    "UrlSubscription",
    "UrlSubscriptionProps",
]

publication.publish()
