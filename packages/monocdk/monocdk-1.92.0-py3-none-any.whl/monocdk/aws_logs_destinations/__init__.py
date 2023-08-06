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
from ..aws_kinesis import IStream as _IStream_14c6ec7f
from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_logs import (
    ILogGroup as _ILogGroup_846e17a0,
    ILogSubscriptionDestination as _ILogSubscriptionDestination_4c87195f,
    LogSubscriptionDestinationConfig as _LogSubscriptionDestinationConfig_29b34d24,
)


@jsii.implements(_ILogSubscriptionDestination_4c87195f)
class KinesisDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs_destinations.KinesisDestination",
):
    '''(experimental) Use a Kinesis stream as the destination for a log subscription.

    :stability: experimental
    '''

    def __init__(self, stream: _IStream_14c6ec7f) -> None:
        '''
        :param stream: -

        :stability: experimental
        '''
        jsii.create(KinesisDestination, self, [stream])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        _source_log_group: _ILogGroup_846e17a0,
    ) -> _LogSubscriptionDestinationConfig_29b34d24:
        '''(experimental) Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param _source_log_group: -

        :stability: experimental
        '''
        return typing.cast(_LogSubscriptionDestinationConfig_29b34d24, jsii.invoke(self, "bind", [scope, _source_log_group]))


@jsii.implements(_ILogSubscriptionDestination_4c87195f)
class LambdaDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs_destinations.LambdaDestination",
):
    '''(experimental) Use a Lamda Function as the destination for a log subscription.

    :stability: experimental
    '''

    def __init__(self, fn: _IFunction_6e14f09e) -> None:
        '''
        :param fn: -

        :stability: experimental
        '''
        jsii.create(LambdaDestination, self, [fn])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        log_group: _ILogGroup_846e17a0,
    ) -> _LogSubscriptionDestinationConfig_29b34d24:
        '''(experimental) Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param log_group: -

        :stability: experimental
        '''
        return typing.cast(_LogSubscriptionDestinationConfig_29b34d24, jsii.invoke(self, "bind", [scope, log_group]))


__all__ = [
    "KinesisDestination",
    "LambdaDestination",
]

publication.publish()
