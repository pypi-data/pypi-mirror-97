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
from ..aws_lambda import LayerVersion as _LayerVersion_aa33f566


class AwsCliLayer(
    _LayerVersion_aa33f566,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.lambda_layer_awscli.AwsCliLayer",
):
    '''(experimental) An AWS Lambda layer that includes the AWS CLI.

    :stability: experimental
    '''

    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        jsii.create(AwsCliLayer, self, [scope, id])


__all__ = [
    "AwsCliLayer",
]

publication.publish()
