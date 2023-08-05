import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

import constructs
from ..aws_kinesis import IStream as _IStream_778702ee
from ..aws_lambda import IFunction as _IFunction_9c701b6f
from ..aws_logs import (
    ILogGroup as _ILogGroup_030ec5ca,
    ILogSubscriptionDestination as _ILogSubscriptionDestination_23aa206a,
    LogSubscriptionDestinationConfig as _LogSubscriptionDestinationConfig_6c33d4b4,
)


@jsii.implements(_ILogSubscriptionDestination_23aa206a)
class KinesisDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_logs_destinations.KinesisDestination",
):
    '''(experimental) Use a Kinesis stream as the destination for a log subscription.

    :stability: experimental
    '''

    def __init__(self, stream: _IStream_778702ee) -> None:
        '''
        :param stream: -

        :stability: experimental
        '''
        jsii.create(KinesisDestination, self, [stream])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.Construct,
        _source_log_group: _ILogGroup_030ec5ca,
    ) -> _LogSubscriptionDestinationConfig_6c33d4b4:
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
        return typing.cast(_LogSubscriptionDestinationConfig_6c33d4b4, jsii.invoke(self, "bind", [scope, _source_log_group]))


@jsii.implements(_ILogSubscriptionDestination_23aa206a)
class LambdaDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_logs_destinations.LambdaDestination",
):
    '''(experimental) Use a Lamda Function as the destination for a log subscription.

    :stability: experimental
    '''

    def __init__(self, fn: _IFunction_9c701b6f) -> None:
        '''
        :param fn: -

        :stability: experimental
        '''
        jsii.create(LambdaDestination, self, [fn])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.Construct,
        log_group: _ILogGroup_030ec5ca,
    ) -> _LogSubscriptionDestinationConfig_6c33d4b4:
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
        return typing.cast(_LogSubscriptionDestinationConfig_6c33d4b4, jsii.invoke(self, "bind", [scope, log_group]))


__all__ = [
    "KinesisDestination",
    "LambdaDestination",
]

publication.publish()
