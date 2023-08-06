import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import Construct as _Construct_e78e779f
from ..aws_events import IEventBus as _IEventBus_2ca38c95
from ..aws_lambda import (
    DestinationConfig as _DestinationConfig_40b85fbc,
    DestinationOptions as _DestinationOptions_31232a3a,
    DestinationType as _DestinationType_0222745b,
    IDestination as _IDestination_7f253ff1,
    IFunction as _IFunction_6e14f09e,
)
from ..aws_sns import ITopic as _ITopic_465e36b9
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.implements(_IDestination_7f253ff1)
class EventBridgeDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_destinations.EventBridgeDestination",
):
    '''(experimental) Use an Event Bridge event bus as a Lambda destination.

    If no event bus is specified, the default event bus is used.

    :stability: experimental
    '''

    def __init__(self, event_bus: typing.Optional[_IEventBus_2ca38c95] = None) -> None:
        '''
        :param event_bus: -

        :default: - use the default event bus

        :stability: experimental
        '''
        jsii.create(EventBridgeDestination, self, [event_bus])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        fn: _IFunction_6e14f09e,
        *,
        type: _DestinationType_0222745b,
    ) -> _DestinationConfig_40b85fbc:
        '''(experimental) Returns a destination configuration.

        :param _scope: -
        :param fn: -
        :param type: (experimental) The destination type.

        :stability: experimental
        '''
        _options = _DestinationOptions_31232a3a(type=type)

        return typing.cast(_DestinationConfig_40b85fbc, jsii.invoke(self, "bind", [_scope, fn, _options]))


@jsii.implements(_IDestination_7f253ff1)
class LambdaDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_destinations.LambdaDestination",
):
    '''(experimental) Use a Lambda function as a Lambda destination.

    :stability: experimental
    '''

    def __init__(
        self,
        fn: _IFunction_6e14f09e,
        *,
        response_only: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param fn: -
        :param response_only: (experimental) Whether the destination function receives only the ``responsePayload`` of the source function. When set to ``true`` and used as ``onSuccess`` destination, the destination function will be invoked with the payload returned by the source function. When set to ``true`` and used as ``onFailure`` destination, the destination function will be invoked with the error object returned by source function. See the README of this module to see a full explanation of this option. Default: false The destination function receives the full invocation record.

        :stability: experimental
        '''
        options = LambdaDestinationOptions(response_only=response_only)

        jsii.create(LambdaDestination, self, [fn, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        fn: _IFunction_6e14f09e,
        *,
        type: _DestinationType_0222745b,
    ) -> _DestinationConfig_40b85fbc:
        '''(experimental) Returns a destination configuration.

        :param scope: -
        :param fn: -
        :param type: (experimental) The destination type.

        :stability: experimental
        '''
        options = _DestinationOptions_31232a3a(type=type)

        return typing.cast(_DestinationConfig_40b85fbc, jsii.invoke(self, "bind", [scope, fn, options]))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_destinations.LambdaDestinationOptions",
    jsii_struct_bases=[],
    name_mapping={"response_only": "responseOnly"},
)
class LambdaDestinationOptions:
    def __init__(self, *, response_only: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options for a Lambda destination.

        :param response_only: (experimental) Whether the destination function receives only the ``responsePayload`` of the source function. When set to ``true`` and used as ``onSuccess`` destination, the destination function will be invoked with the payload returned by the source function. When set to ``true`` and used as ``onFailure`` destination, the destination function will be invoked with the error object returned by source function. See the README of this module to see a full explanation of this option. Default: false The destination function receives the full invocation record.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if response_only is not None:
            self._values["response_only"] = response_only

    @builtins.property
    def response_only(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the destination function receives only the ``responsePayload`` of the source function.

        When set to ``true`` and used as ``onSuccess`` destination, the destination
        function will be invoked with the payload returned by the source function.

        When set to ``true`` and used as ``onFailure`` destination, the destination
        function will be invoked with the error object returned by source function.

        See the README of this module to see a full explanation of this option.

        :default: false The destination function receives the full invocation record.

        :stability: experimental
        '''
        result = self._values.get("response_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDestinationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IDestination_7f253ff1)
class SnsDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_destinations.SnsDestination",
):
    '''(experimental) Use a SNS topic as a Lambda destination.

    :stability: experimental
    '''

    def __init__(self, topic: _ITopic_465e36b9) -> None:
        '''
        :param topic: -

        :stability: experimental
        '''
        jsii.create(SnsDestination, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        fn: _IFunction_6e14f09e,
        *,
        type: _DestinationType_0222745b,
    ) -> _DestinationConfig_40b85fbc:
        '''(experimental) Returns a destination configuration.

        :param _scope: -
        :param fn: -
        :param type: (experimental) The destination type.

        :stability: experimental
        '''
        _options = _DestinationOptions_31232a3a(type=type)

        return typing.cast(_DestinationConfig_40b85fbc, jsii.invoke(self, "bind", [_scope, fn, _options]))


@jsii.implements(_IDestination_7f253ff1)
class SqsDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_destinations.SqsDestination",
):
    '''(experimental) Use a SQS queue as a Lambda destination.

    :stability: experimental
    '''

    def __init__(self, queue: _IQueue_45a01ab4) -> None:
        '''
        :param queue: -

        :stability: experimental
        '''
        jsii.create(SqsDestination, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        fn: _IFunction_6e14f09e,
        *,
        type: _DestinationType_0222745b,
    ) -> _DestinationConfig_40b85fbc:
        '''(experimental) Returns a destination configuration.

        :param _scope: -
        :param fn: -
        :param type: (experimental) The destination type.

        :stability: experimental
        '''
        _options = _DestinationOptions_31232a3a(type=type)

        return typing.cast(_DestinationConfig_40b85fbc, jsii.invoke(self, "bind", [_scope, fn, _options]))


__all__ = [
    "EventBridgeDestination",
    "LambdaDestination",
    "LambdaDestinationOptions",
    "SnsDestination",
    "SqsDestination",
]

publication.publish()
