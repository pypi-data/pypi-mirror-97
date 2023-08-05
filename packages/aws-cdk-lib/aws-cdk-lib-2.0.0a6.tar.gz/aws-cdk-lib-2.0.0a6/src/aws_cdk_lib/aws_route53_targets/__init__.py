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
from ..aws_apigateway import (
    IDomainName as _IDomainName_362b8f1b, RestApi as _RestApi_8fb613ef
)
from ..aws_apigatewayv2 import IDomainName as _IDomainName_eabece2f
from ..aws_cloudfront import IDistribution as _IDistribution_d112ed76
from ..aws_cognito import UserPoolDomain as _UserPoolDomain_3cc8c5cb
from ..aws_ec2 import IInterfaceVpcEndpoint as _IInterfaceVpcEndpoint_92997d82
from ..aws_elasticloadbalancing import LoadBalancer as _LoadBalancer_f68c9597
from ..aws_elasticloadbalancingv2 import ILoadBalancerV2 as _ILoadBalancerV2_4d58258a
from ..aws_route53 import (
    AliasRecordTargetConfig as _AliasRecordTargetConfig_0147fa3a,
    IAliasRecordTarget as _IAliasRecordTarget_1a0bcfba,
    IRecordSet as _IRecordSet_913b1822,
)
from ..aws_s3 import IBucket as _IBucket_feab190d


@jsii.implements(_IAliasRecordTarget_1a0bcfba)
class ApiGatewayDomain(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.ApiGatewayDomain",
):
    '''(experimental) Defines an API Gateway domain name as the alias target.

    Use the ``ApiGateway`` class if you wish to map the alias to an REST API with a
    domain name defined through the ``RestApiProps.domainName`` prop.

    :stability: experimental
    '''

    def __init__(self, domain_name: _IDomainName_362b8f1b) -> None:
        '''
        :param domain_name: -

        :stability: experimental
        '''
        jsii.create(ApiGatewayDomain, self, [domain_name])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_913b1822) -> _AliasRecordTargetConfig_0147fa3a:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_0147fa3a, jsii.invoke(self, "bind", [_record]))


@jsii.implements(_IAliasRecordTarget_1a0bcfba)
class ApiGatewayv2Domain(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.ApiGatewayv2Domain",
):
    '''(experimental) Defines an API Gateway V2 domain name as the alias target.

    :stability: experimental
    '''

    def __init__(self, domain_name: _IDomainName_eabece2f) -> None:
        '''
        :param domain_name: -

        :stability: experimental
        '''
        jsii.create(ApiGatewayv2Domain, self, [domain_name])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_913b1822) -> _AliasRecordTargetConfig_0147fa3a:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_0147fa3a, jsii.invoke(self, "bind", [_record]))


@jsii.implements(_IAliasRecordTarget_1a0bcfba)
class BucketWebsiteTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.BucketWebsiteTarget",
):
    '''(experimental) Use a S3 as an alias record target.

    :stability: experimental
    '''

    def __init__(self, bucket: _IBucket_feab190d) -> None:
        '''
        :param bucket: -

        :stability: experimental
        '''
        jsii.create(BucketWebsiteTarget, self, [bucket])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_913b1822) -> _AliasRecordTargetConfig_0147fa3a:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_0147fa3a, jsii.invoke(self, "bind", [_record]))


@jsii.implements(_IAliasRecordTarget_1a0bcfba)
class ClassicLoadBalancerTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.ClassicLoadBalancerTarget",
):
    '''(experimental) Use a classic ELB as an alias record target.

    :stability: experimental
    '''

    def __init__(self, load_balancer: _LoadBalancer_f68c9597) -> None:
        '''
        :param load_balancer: -

        :stability: experimental
        '''
        jsii.create(ClassicLoadBalancerTarget, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_913b1822) -> _AliasRecordTargetConfig_0147fa3a:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_0147fa3a, jsii.invoke(self, "bind", [_record]))


@jsii.implements(_IAliasRecordTarget_1a0bcfba)
class CloudFrontTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.CloudFrontTarget",
):
    '''(experimental) Use a CloudFront Distribution as an alias record target.

    :stability: experimental
    '''

    def __init__(self, distribution: _IDistribution_d112ed76) -> None:
        '''
        :param distribution: -

        :stability: experimental
        '''
        jsii.create(CloudFrontTarget, self, [distribution])

    @jsii.member(jsii_name="getHostedZoneId") # type: ignore[misc]
    @builtins.classmethod
    def get_hosted_zone_id(cls, scope: constructs.IConstruct) -> builtins.str:
        '''(experimental) Get the hosted zone id for the current scope.

        :param scope: - scope in which this resource is defined.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getHostedZoneId", [scope]))

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_913b1822) -> _AliasRecordTargetConfig_0147fa3a:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_0147fa3a, jsii.invoke(self, "bind", [_record]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CLOUDFRONT_ZONE_ID")
    def CLOUDFRONT_ZONE_ID(cls) -> builtins.str:
        '''(experimental) The hosted zone Id if using an alias record in Route53.

        This value never changes.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CLOUDFRONT_ZONE_ID"))


@jsii.implements(_IAliasRecordTarget_1a0bcfba)
class InterfaceVpcEndpointTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.InterfaceVpcEndpointTarget",
):
    '''(experimental) Set an InterfaceVpcEndpoint as a target for an ARecord.

    :stability: experimental
    '''

    def __init__(self, vpc_endpoint: _IInterfaceVpcEndpoint_92997d82) -> None:
        '''
        :param vpc_endpoint: -

        :stability: experimental
        '''
        jsii.create(InterfaceVpcEndpointTarget, self, [vpc_endpoint])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_913b1822) -> _AliasRecordTargetConfig_0147fa3a:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_0147fa3a, jsii.invoke(self, "bind", [_record]))


@jsii.implements(_IAliasRecordTarget_1a0bcfba)
class LoadBalancerTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.LoadBalancerTarget",
):
    '''(experimental) Use an ELBv2 as an alias record target.

    :stability: experimental
    '''

    def __init__(self, load_balancer: _ILoadBalancerV2_4d58258a) -> None:
        '''
        :param load_balancer: -

        :stability: experimental
        '''
        jsii.create(LoadBalancerTarget, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_913b1822) -> _AliasRecordTargetConfig_0147fa3a:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_0147fa3a, jsii.invoke(self, "bind", [_record]))


@jsii.implements(_IAliasRecordTarget_1a0bcfba)
class UserPoolDomainTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.UserPoolDomainTarget",
):
    '''(experimental) Use a user pool domain as an alias record target.

    :stability: experimental
    '''

    def __init__(self, domain: _UserPoolDomain_3cc8c5cb) -> None:
        '''
        :param domain: -

        :stability: experimental
        '''
        jsii.create(UserPoolDomainTarget, self, [domain])

    @jsii.member(jsii_name="bind")
    def bind(self, _record: _IRecordSet_913b1822) -> _AliasRecordTargetConfig_0147fa3a:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -

        :stability: experimental
        '''
        return typing.cast(_AliasRecordTargetConfig_0147fa3a, jsii.invoke(self, "bind", [_record]))


class ApiGateway(
    ApiGatewayDomain,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_route53_targets.ApiGateway",
):
    '''(experimental) Defines an API Gateway REST API as the alias target. Requires that the domain name will be defined through ``RestApiProps.domainName``.

    You can direct the alias to any ``apigateway.DomainName`` resource through the
    ``ApiGatewayDomain`` class.

    :stability: experimental
    '''

    def __init__(self, api: _RestApi_8fb613ef) -> None:
        '''
        :param api: -

        :stability: experimental
        '''
        jsii.create(ApiGateway, self, [api])


__all__ = [
    "ApiGateway",
    "ApiGatewayDomain",
    "ApiGatewayv2Domain",
    "BucketWebsiteTarget",
    "ClassicLoadBalancerTarget",
    "CloudFrontTarget",
    "InterfaceVpcEndpointTarget",
    "LoadBalancerTarget",
    "UserPoolDomainTarget",
]

publication.publish()
