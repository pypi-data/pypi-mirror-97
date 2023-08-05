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
from ..aws_autoscaling import (
    ILifecycleHook as _ILifecycleHook_6857ef43,
    ILifecycleHookTarget as _ILifecycleHookTarget_ff0564e9,
    LifecycleHookTargetConfig as _LifecycleHookTargetConfig_a17c4e99,
)
from ..aws_kms import IKey as _IKey_8849766e
from ..aws_lambda import IFunction as _IFunction_9c701b6f
from ..aws_sns import ITopic as _ITopic_2a3c8549
from ..aws_sqs import IQueue as _IQueue_728eee9f


@jsii.implements(_ILifecycleHookTarget_ff0564e9)
class FunctionHook(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_autoscaling_hooktargets.FunctionHook",
):
    '''(experimental) Use a Lambda Function as a hook target.

    Internally creates a Topic to make the connection.

    :stability: experimental
    '''

    def __init__(
        self,
        fn: _IFunction_9c701b6f,
        encryption_key: typing.Optional[_IKey_8849766e] = None,
    ) -> None:
        '''
        :param fn: Function to invoke in response to a lifecycle event.
        :param encryption_key: If provided, this key is used to encrypt the contents of the SNS topic.

        :stability: experimental
        '''
        jsii.create(FunctionHook, self, [fn, encryption_key])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.Construct,
        lifecycle_hook: _ILifecycleHook_6857ef43,
    ) -> _LifecycleHookTargetConfig_a17c4e99:
        '''(experimental) Called when this object is used as the target of a lifecycle hook.

        :param scope: -
        :param lifecycle_hook: -

        :stability: experimental
        '''
        return typing.cast(_LifecycleHookTargetConfig_a17c4e99, jsii.invoke(self, "bind", [scope, lifecycle_hook]))


@jsii.implements(_ILifecycleHookTarget_ff0564e9)
class QueueHook(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_autoscaling_hooktargets.QueueHook",
):
    '''(experimental) Use an SQS queue as a hook target.

    :stability: experimental
    '''

    def __init__(self, queue: _IQueue_728eee9f) -> None:
        '''
        :param queue: -

        :stability: experimental
        '''
        jsii.create(QueueHook, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.Construct,
        lifecycle_hook: _ILifecycleHook_6857ef43,
    ) -> _LifecycleHookTargetConfig_a17c4e99:
        '''(experimental) Called when this object is used as the target of a lifecycle hook.

        :param _scope: -
        :param lifecycle_hook: -

        :stability: experimental
        '''
        return typing.cast(_LifecycleHookTargetConfig_a17c4e99, jsii.invoke(self, "bind", [_scope, lifecycle_hook]))


@jsii.implements(_ILifecycleHookTarget_ff0564e9)
class TopicHook(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_autoscaling_hooktargets.TopicHook",
):
    '''(experimental) Use an SNS topic as a hook target.

    :stability: experimental
    '''

    def __init__(self, topic: _ITopic_2a3c8549) -> None:
        '''
        :param topic: -

        :stability: experimental
        '''
        jsii.create(TopicHook, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.Construct,
        lifecycle_hook: _ILifecycleHook_6857ef43,
    ) -> _LifecycleHookTargetConfig_a17c4e99:
        '''(experimental) Called when this object is used as the target of a lifecycle hook.

        :param _scope: -
        :param lifecycle_hook: -

        :stability: experimental
        '''
        return typing.cast(_LifecycleHookTargetConfig_a17c4e99, jsii.invoke(self, "bind", [_scope, lifecycle_hook]))


__all__ = [
    "FunctionHook",
    "QueueHook",
    "TopicHook",
]

publication.publish()
