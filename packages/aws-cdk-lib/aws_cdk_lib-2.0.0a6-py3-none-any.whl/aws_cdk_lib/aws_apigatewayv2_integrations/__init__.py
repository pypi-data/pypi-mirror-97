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
from ..aws_apigatewayv2 import (
    HttpConnectionType as _HttpConnectionType_bc1bb8f0,
    HttpIntegrationType as _HttpIntegrationType_7d4c1d58,
    HttpMethod as _HttpMethod_7c149b49,
    HttpRouteIntegrationBindOptions as _HttpRouteIntegrationBindOptions_89ef40f4,
    HttpRouteIntegrationConfig as _HttpRouteIntegrationConfig_f24a98b3,
    IHttpRoute as _IHttpRoute_b43dd68d,
    IHttpRouteIntegration as _IHttpRouteIntegration_90d9e4f2,
    IVpcLink as _IVpcLink_52176974,
    PayloadFormatVersion as _PayloadFormatVersion_8785bd89,
)
from ..aws_elasticloadbalancingv2 import (
    IApplicationListener as _IApplicationListener_ac5c9deb,
    INetworkListener as _INetworkListener_b2af895f,
)
from ..aws_lambda import IFunction as _IFunction_9c701b6f
from ..aws_servicediscovery import IService as _IService_9b3ba648


@jsii.implements(_IHttpRouteIntegration_90d9e4f2)
class HttpAlbIntegration(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_apigatewayv2_integrations.HttpAlbIntegration",
):
    '''(experimental) The Application Load Balancer integration resource for HTTP API.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        listener: _IApplicationListener_ac5c9deb,
        method: typing.Optional[_HttpMethod_7c149b49] = None,
        vpc_link: typing.Optional[_IVpcLink_52176974] = None,
    ) -> None:
        '''
        :param listener: (experimental) The listener to the application load balancer used for the integration.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        props = HttpAlbIntegrationProps(
            listener=listener, method=method, vpc_link=vpc_link
        )

        jsii.create(HttpAlbIntegration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IHttpRoute_b43dd68d,
        scope: constructs.Construct,
    ) -> _HttpRouteIntegrationConfig_f24a98b3:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _HttpRouteIntegrationBindOptions_89ef40f4(route=route, scope=scope)

        return typing.cast(_HttpRouteIntegrationConfig_f24a98b3, jsii.invoke(self, "bind", [options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> _HttpConnectionType_bc1bb8f0:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpConnectionType_bc1bb8f0, jsii.get(self, "connectionType"))

    @_connection_type.setter
    def _connection_type(self, value: _HttpConnectionType_bc1bb8f0) -> None:
        jsii.set(self, "connectionType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> _HttpMethod_7c149b49:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpMethod_7c149b49, jsii.get(self, "httpMethod"))

    @_http_method.setter
    def _http_method(self, value: _HttpMethod_7c149b49) -> None:
        jsii.set(self, "httpMethod", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="integrationType")
    def _integration_type(self) -> _HttpIntegrationType_7d4c1d58:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpIntegrationType_7d4c1d58, jsii.get(self, "integrationType"))

    @_integration_type.setter
    def _integration_type(self, value: _HttpIntegrationType_7d4c1d58) -> None:
        jsii.set(self, "integrationType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(self) -> _PayloadFormatVersion_8785bd89:
        '''
        :stability: experimental
        '''
        return typing.cast(_PayloadFormatVersion_8785bd89, jsii.get(self, "payloadFormatVersion"))

    @_payload_format_version.setter
    def _payload_format_version(self, value: _PayloadFormatVersion_8785bd89) -> None:
        jsii.set(self, "payloadFormatVersion", value)


@jsii.implements(_IHttpRouteIntegration_90d9e4f2)
class HttpNlbIntegration(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_apigatewayv2_integrations.HttpNlbIntegration",
):
    '''(experimental) The Network Load Balancer integration resource for HTTP API.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        listener: _INetworkListener_b2af895f,
        method: typing.Optional[_HttpMethod_7c149b49] = None,
        vpc_link: typing.Optional[_IVpcLink_52176974] = None,
    ) -> None:
        '''
        :param listener: (experimental) The listener to the network load balancer used for the integration.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        props = HttpNlbIntegrationProps(
            listener=listener, method=method, vpc_link=vpc_link
        )

        jsii.create(HttpNlbIntegration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IHttpRoute_b43dd68d,
        scope: constructs.Construct,
    ) -> _HttpRouteIntegrationConfig_f24a98b3:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _HttpRouteIntegrationBindOptions_89ef40f4(route=route, scope=scope)

        return typing.cast(_HttpRouteIntegrationConfig_f24a98b3, jsii.invoke(self, "bind", [options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> _HttpConnectionType_bc1bb8f0:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpConnectionType_bc1bb8f0, jsii.get(self, "connectionType"))

    @_connection_type.setter
    def _connection_type(self, value: _HttpConnectionType_bc1bb8f0) -> None:
        jsii.set(self, "connectionType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> _HttpMethod_7c149b49:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpMethod_7c149b49, jsii.get(self, "httpMethod"))

    @_http_method.setter
    def _http_method(self, value: _HttpMethod_7c149b49) -> None:
        jsii.set(self, "httpMethod", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="integrationType")
    def _integration_type(self) -> _HttpIntegrationType_7d4c1d58:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpIntegrationType_7d4c1d58, jsii.get(self, "integrationType"))

    @_integration_type.setter
    def _integration_type(self, value: _HttpIntegrationType_7d4c1d58) -> None:
        jsii.set(self, "integrationType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(self) -> _PayloadFormatVersion_8785bd89:
        '''
        :stability: experimental
        '''
        return typing.cast(_PayloadFormatVersion_8785bd89, jsii.get(self, "payloadFormatVersion"))

    @_payload_format_version.setter
    def _payload_format_version(self, value: _PayloadFormatVersion_8785bd89) -> None:
        jsii.set(self, "payloadFormatVersion", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_apigatewayv2_integrations.HttpPrivateIntegrationOptions",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "vpc_link": "vpcLink"},
)
class HttpPrivateIntegrationOptions:
    def __init__(
        self,
        *,
        method: typing.Optional[_HttpMethod_7c149b49] = None,
        vpc_link: typing.Optional[_IVpcLink_52176974] = None,
    ) -> None:
        '''(experimental) Base options for private integration.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[_HttpMethod_7c149b49]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_HttpMethod_7c149b49], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[_IVpcLink_52176974]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[_IVpcLink_52176974], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpPrivateIntegrationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IHttpRouteIntegration_90d9e4f2)
class HttpProxyIntegration(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_apigatewayv2_integrations.HttpProxyIntegration",
):
    '''(experimental) The HTTP Proxy integration resource for HTTP API.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        url: builtins.str,
        method: typing.Optional[_HttpMethod_7c149b49] = None,
    ) -> None:
        '''
        :param url: (experimental) The full-qualified HTTP URL for the HTTP integration.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY

        :stability: experimental
        '''
        props = HttpProxyIntegrationProps(url=url, method=method)

        jsii.create(HttpProxyIntegration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IHttpRoute_b43dd68d,
        scope: constructs.Construct,
    ) -> _HttpRouteIntegrationConfig_f24a98b3:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        _ = _HttpRouteIntegrationBindOptions_89ef40f4(route=route, scope=scope)

        return typing.cast(_HttpRouteIntegrationConfig_f24a98b3, jsii.invoke(self, "bind", [_]))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_apigatewayv2_integrations.HttpProxyIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={"url": "url", "method": "method"},
)
class HttpProxyIntegrationProps:
    def __init__(
        self,
        *,
        url: builtins.str,
        method: typing.Optional[_HttpMethod_7c149b49] = None,
    ) -> None:
        '''(experimental) Properties to initialize a new ``HttpProxyIntegration``.

        :param url: (experimental) The full-qualified HTTP URL for the HTTP integration.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "url": url,
        }
        if method is not None:
            self._values["method"] = method

    @builtins.property
    def url(self) -> builtins.str:
        '''(experimental) The full-qualified HTTP URL for the HTTP integration.

        :stability: experimental
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def method(self) -> typing.Optional[_HttpMethod_7c149b49]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_HttpMethod_7c149b49], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpProxyIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IHttpRouteIntegration_90d9e4f2)
class HttpServiceDiscoveryIntegration(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_apigatewayv2_integrations.HttpServiceDiscoveryIntegration",
):
    '''(experimental) The Service Discovery integration resource for HTTP API.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        service: _IService_9b3ba648,
        method: typing.Optional[_HttpMethod_7c149b49] = None,
        vpc_link: typing.Optional[_IVpcLink_52176974] = None,
    ) -> None:
        '''
        :param service: (experimental) The discovery service used for the integration.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        props = HttpServiceDiscoveryIntegrationProps(
            service=service, method=method, vpc_link=vpc_link
        )

        jsii.create(HttpServiceDiscoveryIntegration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IHttpRoute_b43dd68d,
        scope: constructs.Construct,
    ) -> _HttpRouteIntegrationConfig_f24a98b3:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        _ = _HttpRouteIntegrationBindOptions_89ef40f4(route=route, scope=scope)

        return typing.cast(_HttpRouteIntegrationConfig_f24a98b3, jsii.invoke(self, "bind", [_]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> _HttpConnectionType_bc1bb8f0:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpConnectionType_bc1bb8f0, jsii.get(self, "connectionType"))

    @_connection_type.setter
    def _connection_type(self, value: _HttpConnectionType_bc1bb8f0) -> None:
        jsii.set(self, "connectionType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> _HttpMethod_7c149b49:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpMethod_7c149b49, jsii.get(self, "httpMethod"))

    @_http_method.setter
    def _http_method(self, value: _HttpMethod_7c149b49) -> None:
        jsii.set(self, "httpMethod", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="integrationType")
    def _integration_type(self) -> _HttpIntegrationType_7d4c1d58:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpIntegrationType_7d4c1d58, jsii.get(self, "integrationType"))

    @_integration_type.setter
    def _integration_type(self, value: _HttpIntegrationType_7d4c1d58) -> None:
        jsii.set(self, "integrationType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(self) -> _PayloadFormatVersion_8785bd89:
        '''
        :stability: experimental
        '''
        return typing.cast(_PayloadFormatVersion_8785bd89, jsii.get(self, "payloadFormatVersion"))

    @_payload_format_version.setter
    def _payload_format_version(self, value: _PayloadFormatVersion_8785bd89) -> None:
        jsii.set(self, "payloadFormatVersion", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_apigatewayv2_integrations.HttpServiceDiscoveryIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={"method": "method", "vpc_link": "vpcLink", "service": "service"},
)
class HttpServiceDiscoveryIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[_HttpMethod_7c149b49] = None,
        vpc_link: typing.Optional[_IVpcLink_52176974] = None,
        service: _IService_9b3ba648,
    ) -> None:
        '''(experimental) Properties to initialize ``HttpServiceDiscoveryIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created
        :param service: (experimental) The discovery service used for the integration.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "service": service,
        }
        if method is not None:
            self._values["method"] = method
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[_HttpMethod_7c149b49]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_HttpMethod_7c149b49], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[_IVpcLink_52176974]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[_IVpcLink_52176974], result)

    @builtins.property
    def service(self) -> _IService_9b3ba648:
        '''(experimental) The discovery service used for the integration.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(_IService_9b3ba648, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpServiceDiscoveryIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IHttpRouteIntegration_90d9e4f2)
class LambdaProxyIntegration(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_apigatewayv2_integrations.LambdaProxyIntegration",
):
    '''(experimental) The Lambda Proxy integration resource for HTTP API.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        handler: _IFunction_9c701b6f,
        payload_format_version: typing.Optional[_PayloadFormatVersion_8785bd89] = None,
    ) -> None:
        '''
        :param handler: (experimental) The handler for this integration.
        :param payload_format_version: (experimental) Version of the payload sent to the lambda handler. Default: PayloadFormatVersion.VERSION_2_0

        :stability: experimental
        '''
        props = LambdaProxyIntegrationProps(
            handler=handler, payload_format_version=payload_format_version
        )

        jsii.create(LambdaProxyIntegration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IHttpRoute_b43dd68d,
        scope: constructs.Construct,
    ) -> _HttpRouteIntegrationConfig_f24a98b3:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _HttpRouteIntegrationBindOptions_89ef40f4(route=route, scope=scope)

        return typing.cast(_HttpRouteIntegrationConfig_f24a98b3, jsii.invoke(self, "bind", [options]))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_apigatewayv2_integrations.LambdaProxyIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "handler": "handler",
        "payload_format_version": "payloadFormatVersion",
    },
)
class LambdaProxyIntegrationProps:
    def __init__(
        self,
        *,
        handler: _IFunction_9c701b6f,
        payload_format_version: typing.Optional[_PayloadFormatVersion_8785bd89] = None,
    ) -> None:
        '''(experimental) Lambda Proxy integration properties.

        :param handler: (experimental) The handler for this integration.
        :param payload_format_version: (experimental) Version of the payload sent to the lambda handler. Default: PayloadFormatVersion.VERSION_2_0

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "handler": handler,
        }
        if payload_format_version is not None:
            self._values["payload_format_version"] = payload_format_version

    @builtins.property
    def handler(self) -> _IFunction_9c701b6f:
        '''(experimental) The handler for this integration.

        :stability: experimental
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(_IFunction_9c701b6f, result)

    @builtins.property
    def payload_format_version(self) -> typing.Optional[_PayloadFormatVersion_8785bd89]:
        '''(experimental) Version of the payload sent to the lambda handler.

        :default: PayloadFormatVersion.VERSION_2_0

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
        :stability: experimental
        '''
        result = self._values.get("payload_format_version")
        return typing.cast(typing.Optional[_PayloadFormatVersion_8785bd89], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaProxyIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_apigatewayv2_integrations.HttpAlbIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={"method": "method", "vpc_link": "vpcLink", "listener": "listener"},
)
class HttpAlbIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[_HttpMethod_7c149b49] = None,
        vpc_link: typing.Optional[_IVpcLink_52176974] = None,
        listener: _IApplicationListener_ac5c9deb,
    ) -> None:
        '''(experimental) Properties to initialize ``HttpAlbIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created
        :param listener: (experimental) The listener to the application load balancer used for the integration.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "listener": listener,
        }
        if method is not None:
            self._values["method"] = method
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[_HttpMethod_7c149b49]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_HttpMethod_7c149b49], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[_IVpcLink_52176974]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[_IVpcLink_52176974], result)

    @builtins.property
    def listener(self) -> _IApplicationListener_ac5c9deb:
        '''(experimental) The listener to the application load balancer used for the integration.

        :stability: experimental
        '''
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return typing.cast(_IApplicationListener_ac5c9deb, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpAlbIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_apigatewayv2_integrations.HttpNlbIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={"method": "method", "vpc_link": "vpcLink", "listener": "listener"},
)
class HttpNlbIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[_HttpMethod_7c149b49] = None,
        vpc_link: typing.Optional[_IVpcLink_52176974] = None,
        listener: _INetworkListener_b2af895f,
    ) -> None:
        '''(experimental) Properties to initialize ``HttpNlbIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created
        :param listener: (experimental) The listener to the network load balancer used for the integration.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "listener": listener,
        }
        if method is not None:
            self._values["method"] = method
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[_HttpMethod_7c149b49]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_HttpMethod_7c149b49], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[_IVpcLink_52176974]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[_IVpcLink_52176974], result)

    @builtins.property
    def listener(self) -> _INetworkListener_b2af895f:
        '''(experimental) The listener to the network load balancer used for the integration.

        :stability: experimental
        '''
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return typing.cast(_INetworkListener_b2af895f, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpNlbIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HttpAlbIntegration",
    "HttpAlbIntegrationProps",
    "HttpNlbIntegration",
    "HttpNlbIntegrationProps",
    "HttpPrivateIntegrationOptions",
    "HttpProxyIntegration",
    "HttpProxyIntegrationProps",
    "HttpServiceDiscoveryIntegration",
    "HttpServiceDiscoveryIntegrationProps",
    "LambdaProxyIntegration",
    "LambdaProxyIntegrationProps",
]

publication.publish()
