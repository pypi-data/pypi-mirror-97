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
from ..aws_lambda import IFunction as _IFunction_9c701b6f
from ..aws_s3 import (
    BucketNotificationDestinationConfig as _BucketNotificationDestinationConfig_f1fc004d,
    IBucket as _IBucket_feab190d,
    IBucketNotificationDestination as _IBucketNotificationDestination_9eeda6d4,
)
from ..aws_sns import ITopic as _ITopic_2a3c8549
from ..aws_sqs import IQueue as _IQueue_728eee9f


@jsii.implements(_IBucketNotificationDestination_9eeda6d4)
class LambdaDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_s3_notifications.LambdaDestination",
):
    '''(experimental) Use a Lambda function as a bucket notification destination.

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
        _scope: constructs.Construct,
        bucket: _IBucket_feab190d,
    ) -> _BucketNotificationDestinationConfig_f1fc004d:
        '''(experimental) Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        :param _scope: -
        :param bucket: -

        :stability: experimental
        '''
        return typing.cast(_BucketNotificationDestinationConfig_f1fc004d, jsii.invoke(self, "bind", [_scope, bucket]))


@jsii.implements(_IBucketNotificationDestination_9eeda6d4)
class SnsDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_s3_notifications.SnsDestination",
):
    '''(experimental) Use an SNS topic as a bucket notification destination.

    :stability: experimental
    '''

    def __init__(self, topic: _ITopic_2a3c8549) -> None:
        '''
        :param topic: -

        :stability: experimental
        '''
        jsii.create(SnsDestination, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.Construct,
        bucket: _IBucket_feab190d,
    ) -> _BucketNotificationDestinationConfig_f1fc004d:
        '''(experimental) Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        :param _scope: -
        :param bucket: -

        :stability: experimental
        '''
        return typing.cast(_BucketNotificationDestinationConfig_f1fc004d, jsii.invoke(self, "bind", [_scope, bucket]))


@jsii.implements(_IBucketNotificationDestination_9eeda6d4)
class SqsDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_s3_notifications.SqsDestination",
):
    '''(experimental) Use an SQS queue as a bucket notification destination.

    :stability: experimental
    '''

    def __init__(self, queue: _IQueue_728eee9f) -> None:
        '''
        :param queue: -

        :stability: experimental
        '''
        jsii.create(SqsDestination, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: constructs.Construct,
        bucket: _IBucket_feab190d,
    ) -> _BucketNotificationDestinationConfig_f1fc004d:
        '''(experimental) Allows using SQS queues as destinations for bucket notifications.

        Use ``bucket.onEvent(event, queue)`` to subscribe.

        :param _scope: -
        :param bucket: -

        :stability: experimental
        '''
        return typing.cast(_BucketNotificationDestinationConfig_f1fc004d, jsii.invoke(self, "bind", [_scope, bucket]))


__all__ = [
    "LambdaDestination",
    "SnsDestination",
    "SqsDestination",
]

publication.publish()
