import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import Duration as _Duration_070aa057
from ..aws_apigateway import (
    AuthorizationType as _AuthorizationType_0ef85b12,
    IAuthorizer as _IAuthorizer_6ddd4da0,
    IModel as _IModel_f4167163,
    IRequestValidator as _IRequestValidator_8d44748f,
    MethodOptions as _MethodOptions_285920d7,
    MethodResponse as _MethodResponse_bb921d07,
    RequestValidatorOptions as _RequestValidatorOptions_b89e3f10,
)
from ..aws_dynamodb import ITable as _ITable_24826f7e
from ..aws_kinesis import IStream as _IStream_14c6ec7f
from ..aws_lambda import (
    DlqDestinationConfig as _DlqDestinationConfig_563cae69,
    EventSourceMappingOptions as _EventSourceMappingOptions_36519f99,
    IEventSource as _IEventSource_7914870e,
    IEventSourceDlq as _IEventSourceDlq_f5ae73e7,
    IEventSourceMapping as _IEventSourceMapping_b4960cf6,
    IFunction as _IFunction_6e14f09e,
    StartingPosition as _StartingPosition_9192859a,
)
from ..aws_s3 import (
    Bucket as _Bucket_aa378085,
    EventType as _EventType_5af33d27,
    NotificationKeyFilter as _NotificationKeyFilter_7f4bf31a,
)
from ..aws_sns import (
    ITopic as _ITopic_465e36b9, SubscriptionFilter as _SubscriptionFilter_1f5c48ae
)
from ..aws_sns_subscriptions import (
    LambdaSubscriptionProps as _LambdaSubscriptionProps_d5f9085e
)
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.implements(_IEventSource_7914870e)
class ApiEventSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.ApiEventSource",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        method: builtins.str,
        path: builtins.str,
        *,
        api_key_required: typing.Optional[builtins.bool] = None,
        authorization_scopes: typing.Optional[typing.List[builtins.str]] = None,
        authorization_type: typing.Optional[_AuthorizationType_0ef85b12] = None,
        authorizer: typing.Optional[_IAuthorizer_6ddd4da0] = None,
        method_responses: typing.Optional[typing.List[_MethodResponse_bb921d07]] = None,
        operation_name: typing.Optional[builtins.str] = None,
        request_models: typing.Optional[typing.Mapping[builtins.str, _IModel_f4167163]] = None,
        request_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        request_validator: typing.Optional[_IRequestValidator_8d44748f] = None,
        request_validator_options: typing.Optional[_RequestValidatorOptions_b89e3f10] = None,
    ) -> None:
        '''
        :param method: -
        :param path: -
        :param api_key_required: (experimental) Indicates whether the method requires clients to submit a valid API key. Default: false
        :param authorization_scopes: (experimental) A list of authorization scopes configured on the method. The scopes are used with a COGNITO_USER_POOLS authorizer to authorize the method invocation. Default: - no authorization scopes
        :param authorization_type: (experimental) Method authorization. If the value is set of ``Custom``, an ``authorizer`` must also be specified. If you're using one of the authorizers that are available via the {@link Authorizer} class, such as {@link Authorizer#token()}, it is recommended that this option not be specified. The authorizer will take care of setting the correct authorization type. However, specifying an authorization type using this property that conflicts with what is expected by the {@link Authorizer} will result in an error. Default: - open access unless ``authorizer`` is specified
        :param authorizer: (experimental) If ``authorizationType`` is ``Custom``, this specifies the ID of the method authorizer resource. If specified, the value of ``authorizationType`` must be set to ``Custom``
        :param method_responses: (experimental) The responses that can be sent to the client who calls the method. Default: None This property is not required, but if these are not supplied for a Lambda proxy integration, the Lambda function must return a value of the correct format, for the integration response to be correctly mapped to a response to the client.
        :param operation_name: (experimental) A friendly operation name for the method. For example, you can assign the OperationName of ListPets for the GET /pets method.
        :param request_models: (experimental) The models which describe data structure of request payload. When combined with ``requestValidator`` or ``requestValidatorOptions``, the service will validate the API request payload before it reaches the API's Integration (including proxies). Specify ``requestModels`` as key-value pairs, with a content type (e.g. ``'application/json'``) as the key and an API Gateway Model as the value.
        :param request_parameters: (experimental) The request parameters that API Gateway accepts. Specify request parameters as key-value pairs (string-to-Boolean mapping), with a source as the key and a Boolean as the value. The Boolean specifies whether a parameter is required. A source must match the format method.request.location.name, where the location is querystring, path, or header, and name is a valid, unique parameter name. Default: None
        :param request_validator: (experimental) The ID of the associated request validator. Only one of ``requestValidator`` or ``requestValidatorOptions`` must be specified. Works together with ``requestModels`` or ``requestParameters`` to validate the request before it reaches integration like Lambda Proxy Integration. Default: - No default validator
        :param request_validator_options: (experimental) Request validator options to create new validator Only one of ``requestValidator`` or ``requestValidatorOptions`` must be specified. Works together with ``requestModels`` or ``requestParameters`` to validate the request before it reaches integration like Lambda Proxy Integration. Default: - No default validator

        :stability: experimental
        '''
        options = _MethodOptions_285920d7(
            api_key_required=api_key_required,
            authorization_scopes=authorization_scopes,
            authorization_type=authorization_type,
            authorizer=authorizer,
            method_responses=method_responses,
            operation_name=operation_name,
            request_models=request_models,
            request_parameters=request_parameters,
            request_validator=request_validator,
            request_validator_options=request_validator_options,
        )

        jsii.create(ApiEventSource, self, [method, path, options])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))


@jsii.implements(_IEventSource_7914870e)
class S3EventSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.S3EventSource",
):
    '''(experimental) Use S3 bucket notifications as an event source for AWS Lambda.

    :stability: experimental
    '''

    def __init__(
        self,
        bucket: _Bucket_aa378085,
        *,
        events: typing.List[_EventType_5af33d27],
        filters: typing.Optional[typing.List[_NotificationKeyFilter_7f4bf31a]] = None,
    ) -> None:
        '''
        :param bucket: -
        :param events: (experimental) The s3 event types that will trigger the notification.
        :param filters: (experimental) S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules.

        :stability: experimental
        '''
        props = S3EventSourceProps(events=events, filters=filters)

        jsii.create(S3EventSource, self, [bucket, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _Bucket_aa378085:
        '''
        :stability: experimental
        '''
        return typing.cast(_Bucket_aa378085, jsii.get(self, "bucket"))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.S3EventSourceProps",
    jsii_struct_bases=[],
    name_mapping={"events": "events", "filters": "filters"},
)
class S3EventSourceProps:
    def __init__(
        self,
        *,
        events: typing.List[_EventType_5af33d27],
        filters: typing.Optional[typing.List[_NotificationKeyFilter_7f4bf31a]] = None,
    ) -> None:
        '''
        :param events: (experimental) The s3 event types that will trigger the notification.
        :param filters: (experimental) S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "events": events,
        }
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def events(self) -> typing.List[_EventType_5af33d27]:
        '''(experimental) The s3 event types that will trigger the notification.

        :stability: experimental
        '''
        result = self._values.get("events")
        assert result is not None, "Required property 'events' is missing"
        return typing.cast(typing.List[_EventType_5af33d27], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[_NotificationKeyFilter_7f4bf31a]]:
        '''(experimental) S3 object key filter rules to determine which objects trigger this event.

        Each filter must include a ``prefix`` and/or ``suffix`` that will be matched
        against the s3 object key. Refer to the S3 Developer Guide for details
        about allowed filter rules.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[_NotificationKeyFilter_7f4bf31a]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3EventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IEventSourceDlq_f5ae73e7)
class SnsDlq(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.SnsDlq",
):
    '''(experimental) An SNS dead letter queue destination configuration for a Lambda event source.

    :stability: experimental
    '''

    def __init__(self, topic: _ITopic_465e36b9) -> None:
        '''
        :param topic: -

        :stability: experimental
        '''
        jsii.create(SnsDlq, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _target: _IEventSourceMapping_b4960cf6,
        target_handler: _IFunction_6e14f09e,
    ) -> _DlqDestinationConfig_563cae69:
        '''(experimental) Returns a destination configuration for the DLQ.

        :param _target: -
        :param target_handler: -

        :stability: experimental
        '''
        return typing.cast(_DlqDestinationConfig_563cae69, jsii.invoke(self, "bind", [_target, target_handler]))


@jsii.implements(_IEventSource_7914870e)
class SnsEventSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.SnsEventSource",
):
    '''(experimental) Use an Amazon SNS topic as an event source for AWS Lambda.

    :stability: experimental
    '''

    def __init__(
        self,
        topic: _ITopic_465e36b9,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''
        :param topic: -
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        props = SnsEventSourceProps(
            dead_letter_queue=dead_letter_queue, filter_policy=filter_policy
        )

        jsii.create(SnsEventSource, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="topic")
    def topic(self) -> _ITopic_465e36b9:
        '''
        :stability: experimental
        '''
        return typing.cast(_ITopic_465e36b9, jsii.get(self, "topic"))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.SnsEventSourceProps",
    jsii_struct_bases=[_LambdaSubscriptionProps_d5f9085e],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
    },
)
class SnsEventSourceProps(_LambdaSubscriptionProps_d5f9085e):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''(experimental) Properties forwarded to the Lambda Subscription.

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
        return "SnsEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IEventSourceDlq_f5ae73e7)
class SqsDlq(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.SqsDlq",
):
    '''(experimental) An SQS dead letter queue destination configuration for a Lambda event source.

    :stability: experimental
    '''

    def __init__(self, queue: _IQueue_45a01ab4) -> None:
        '''
        :param queue: -

        :stability: experimental
        '''
        jsii.create(SqsDlq, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _target: _IEventSourceMapping_b4960cf6,
        target_handler: _IFunction_6e14f09e,
    ) -> _DlqDestinationConfig_563cae69:
        '''(experimental) Returns a destination configuration for the DLQ.

        :param _target: -
        :param target_handler: -

        :stability: experimental
        '''
        return typing.cast(_DlqDestinationConfig_563cae69, jsii.invoke(self, "bind", [_target, target_handler]))


@jsii.implements(_IEventSource_7914870e)
class SqsEventSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.SqsEventSource",
):
    '''(experimental) Use an Amazon SQS queue as an event source for AWS Lambda.

    :stability: experimental
    '''

    def __init__(
        self,
        queue: _IQueue_45a01ab4,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param queue: -
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10. Default: 10
        :param enabled: (experimental) If the SQS event source mapping should be enabled. Default: true

        :stability: experimental
        '''
        props = SqsEventSourceProps(batch_size=batch_size, enabled=enabled)

        jsii.create(SqsEventSource, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> builtins.str:
        '''(experimental) The identifier for this EventSourceMapping.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventSourceMappingId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="queue")
    def queue(self) -> _IQueue_45a01ab4:
        '''
        :stability: experimental
        '''
        return typing.cast(_IQueue_45a01ab4, jsii.get(self, "queue"))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.SqsEventSourceProps",
    jsii_struct_bases=[],
    name_mapping={"batch_size": "batchSize", "enabled": "enabled"},
)
class SqsEventSourceProps:
    def __init__(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10. Default: 10
        :param enabled: (experimental) If the SQS event source mapping should be enabled. Default: true

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range: Minimum value of 1. Maximum value of 10.

        :default: 10

        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the SQS event source mapping should be enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IEventSource_7914870e)
class StreamEventSource(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_lambda_event_sources.StreamEventSource",
):
    '''(experimental) Use an stream as an event source for AWS Lambda.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_StreamEventSourceProxy"]:
        return _StreamEventSourceProxy

    def __init__(
        self,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        props = StreamEventSourceProps(
            starting_position=starting_position,
            batch_size=batch_size,
            bisect_batch_on_error=bisect_batch_on_error,
            enabled=enabled,
            max_batching_window=max_batching_window,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            retry_attempts=retry_attempts,
        )

        jsii.create(StreamEventSource, self, [props])

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, _target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param _target: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="enrichMappingOptions")
    def _enrich_mapping_options(
        self,
        *,
        event_source_arn: builtins.str,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        kafka_topic: typing.Optional[builtins.str] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        starting_position: typing.Optional[_StartingPosition_9192859a] = None,
    ) -> _EventSourceMappingOptions_36519f99:
        '''
        :param event_source_arn: (experimental) The Amazon Resource Name (ARN) of the event source. Any record added to this stream can invoke the Lambda function.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10000. Default: - Amazon Kinesis, Amazon DynamoDB, and Amazon MSK is 100 records. Both the default and maximum for Amazon SQS are 10 messages.
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) Set to false to disable the event source upon creation. Default: true
        :param kafka_topic: (experimental) The name of the Kafka topic. Default: - no topic
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: - infinite or until the record expires.
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Set to ``undefined`` if you want lambda to keep retrying infinitely or until the record expires. Valid Range: - Minimum value of 0 - Maximum value of 10000 Default: - infinite or until the record expires.
        :param starting_position: (experimental) The position in the DynamoDB, Kinesis or MSK stream where AWS Lambda should start reading. Default: - Required for Amazon Kinesis, Amazon DynamoDB, and Amazon MSK Streams sources.

        :stability: experimental
        '''
        options = _EventSourceMappingOptions_36519f99(
            event_source_arn=event_source_arn,
            batch_size=batch_size,
            bisect_batch_on_error=bisect_batch_on_error,
            enabled=enabled,
            kafka_topic=kafka_topic,
            max_batching_window=max_batching_window,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            retry_attempts=retry_attempts,
            starting_position=starting_position,
        )

        return typing.cast(_EventSourceMappingOptions_36519f99, jsii.invoke(self, "enrichMappingOptions", [options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="props")
    def _props(self) -> "StreamEventSourceProps":
        '''
        :stability: experimental
        '''
        return typing.cast("StreamEventSourceProps", jsii.get(self, "props"))


class _StreamEventSourceProxy(StreamEventSource):
    @jsii.member(jsii_name="bind")
    def bind(self, _target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param _target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [_target]))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.StreamEventSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "bisect_batch_on_error": "bisectBatchOnError",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "max_record_age": "maxRecordAge",
        "on_failure": "onFailure",
        "parallelization_factor": "parallelizationFactor",
        "retry_attempts": "retryAttempts",
    },
)
class StreamEventSourceProps:
    def __init__(
        self,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) The set of properties for event sources that follow the streaming model, such as, Dynamo and Kinesis.

        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None:
            self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None:
            self._values["max_record_age"] = max_record_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def starting_position(self) -> _StartingPosition_9192859a:
        '''(experimental) Where to begin consuming the stream.

        :stability: experimental
        '''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_StartingPosition_9192859a, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the function returns an error, split the batch in two and retry.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("bisect_batch_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the stream event source mapping should be enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)

        :stability: experimental
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("max_record_age")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_IEventSourceDlq_f5ae73e7]:
        '''(experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        :default: discarded records are ignored

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_IEventSourceDlq_f5ae73e7], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        :default: 10000

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DynamoEventSource(
    StreamEventSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.DynamoEventSource",
):
    '''(experimental) Use an Amazon DynamoDB stream as an event source for AWS Lambda.

    :stability: experimental
    '''

    def __init__(
        self,
        table: _ITable_24826f7e,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param table: -
        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        props = DynamoEventSourceProps(
            starting_position=starting_position,
            batch_size=batch_size,
            bisect_batch_on_error=bisect_batch_on_error,
            enabled=enabled,
            max_batching_window=max_batching_window,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            retry_attempts=retry_attempts,
        )

        jsii.create(DynamoEventSource, self, [table, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> builtins.str:
        '''(experimental) The identifier for this EventSourceMapping.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventSourceMappingId"))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.DynamoEventSourceProps",
    jsii_struct_bases=[StreamEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "bisect_batch_on_error": "bisectBatchOnError",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "max_record_age": "maxRecordAge",
        "on_failure": "onFailure",
        "parallelization_factor": "parallelizationFactor",
        "retry_attempts": "retryAttempts",
    },
)
class DynamoEventSourceProps(StreamEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None:
            self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None:
            self._values["max_record_age"] = max_record_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def starting_position(self) -> _StartingPosition_9192859a:
        '''(experimental) Where to begin consuming the stream.

        :stability: experimental
        '''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_StartingPosition_9192859a, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the function returns an error, split the batch in two and retry.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("bisect_batch_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the stream event source mapping should be enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)

        :stability: experimental
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("max_record_age")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_IEventSourceDlq_f5ae73e7]:
        '''(experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        :default: discarded records are ignored

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_IEventSourceDlq_f5ae73e7], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        :default: 10000

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamoEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisEventSource(
    StreamEventSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.KinesisEventSource",
):
    '''(experimental) Use an Amazon Kinesis stream as an event source for AWS Lambda.

    :stability: experimental
    '''

    def __init__(
        self,
        stream: _IStream_14c6ec7f,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param stream: -
        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        props = KinesisEventSourceProps(
            starting_position=starting_position,
            batch_size=batch_size,
            bisect_batch_on_error=bisect_batch_on_error,
            enabled=enabled,
            max_batching_window=max_batching_window,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            retry_attempts=retry_attempts,
        )

        jsii.create(KinesisEventSource, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> builtins.str:
        '''(experimental) The identifier for this EventSourceMapping.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventSourceMappingId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stream")
    def stream(self) -> _IStream_14c6ec7f:
        '''
        :stability: experimental
        '''
        return typing.cast(_IStream_14c6ec7f, jsii.get(self, "stream"))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.KinesisEventSourceProps",
    jsii_struct_bases=[StreamEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "bisect_batch_on_error": "bisectBatchOnError",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "max_record_age": "maxRecordAge",
        "on_failure": "onFailure",
        "parallelization_factor": "parallelizationFactor",
        "retry_attempts": "retryAttempts",
    },
)
class KinesisEventSourceProps(StreamEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None:
            self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None:
            self._values["max_record_age"] = max_record_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def starting_position(self) -> _StartingPosition_9192859a:
        '''(experimental) Where to begin consuming the stream.

        :stability: experimental
        '''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_StartingPosition_9192859a, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the function returns an error, split the batch in two and retry.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("bisect_batch_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the stream event source mapping should be enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)

        :stability: experimental
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("max_record_age")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_IEventSourceDlq_f5ae73e7]:
        '''(experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        :default: discarded records are ignored

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_IEventSourceDlq_f5ae73e7], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        :default: 10000

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ApiEventSource",
    "DynamoEventSource",
    "DynamoEventSourceProps",
    "KinesisEventSource",
    "KinesisEventSourceProps",
    "S3EventSource",
    "S3EventSourceProps",
    "SnsDlq",
    "SnsEventSource",
    "SnsEventSourceProps",
    "SqsDlq",
    "SqsEventSource",
    "SqsEventSourceProps",
    "StreamEventSource",
    "StreamEventSourceProps",
]

publication.publish()
