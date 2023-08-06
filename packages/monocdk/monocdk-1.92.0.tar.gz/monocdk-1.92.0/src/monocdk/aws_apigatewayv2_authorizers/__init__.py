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
    HttpRouteAuthorizerBindOptions as _HttpRouteAuthorizerBindOptions_290d6475,
    HttpRouteAuthorizerConfig as _HttpRouteAuthorizerConfig_cd6b9e02,
    IHttpRoute as _IHttpRoute_bfbdc841,
    IHttpRouteAuthorizer as _IHttpRouteAuthorizer_717e7ba3,
)
from ..aws_cognito import (
    IUserPool as _IUserPool_5e500460, IUserPoolClient as _IUserPoolClient_4cdf19bd
)


@jsii.implements(_IHttpRouteAuthorizer_717e7ba3)
class HttpJwtAuthorizer(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_apigatewayv2_authorizers.HttpJwtAuthorizer",
):
    '''(experimental) Authorize Http Api routes on whether the requester is registered as part of an AWS Cognito user pool.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        jwt_audience: typing.List[builtins.str],
        jwt_issuer: builtins.str,
        authorizer_name: typing.Optional[builtins.str] = None,
        identity_source: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''
        :param jwt_audience: (experimental) A list of the intended recipients of the JWT. A valid JWT must provide an aud that matches at least one entry in this list.
        :param jwt_issuer: (experimental) The base domain of the identity provider that issues JWT.
        :param authorizer_name: (experimental) The name of the authorizer. Default: 'JwtAuthorizer'
        :param identity_source: (experimental) The identity source for which authorization is requested. Default: ['$request.header.Authorization']

        :stability: experimental
        '''
        props = HttpJwtAuthorizerProps(
            jwt_audience=jwt_audience,
            jwt_issuer=jwt_issuer,
            authorizer_name=authorizer_name,
            identity_source=identity_source,
        )

        jsii.create(HttpJwtAuthorizer, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IHttpRoute_bfbdc841,
        scope: constructs.Construct,
    ) -> _HttpRouteAuthorizerConfig_cd6b9e02:
        '''(experimental) Bind this authorizer to a specified Http route.

        :param route: (experimental) The route to which the authorizer is being bound.
        :param scope: (experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        '''
        options = _HttpRouteAuthorizerBindOptions_290d6475(route=route, scope=scope)

        return typing.cast(_HttpRouteAuthorizerConfig_cd6b9e02, jsii.invoke(self, "bind", [options]))


@jsii.data_type(
    jsii_type="monocdk.aws_apigatewayv2_authorizers.HttpJwtAuthorizerProps",
    jsii_struct_bases=[],
    name_mapping={
        "jwt_audience": "jwtAudience",
        "jwt_issuer": "jwtIssuer",
        "authorizer_name": "authorizerName",
        "identity_source": "identitySource",
    },
)
class HttpJwtAuthorizerProps:
    def __init__(
        self,
        *,
        jwt_audience: typing.List[builtins.str],
        jwt_issuer: builtins.str,
        authorizer_name: typing.Optional[builtins.str] = None,
        identity_source: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties to initialize HttpJwtAuthorizer.

        :param jwt_audience: (experimental) A list of the intended recipients of the JWT. A valid JWT must provide an aud that matches at least one entry in this list.
        :param jwt_issuer: (experimental) The base domain of the identity provider that issues JWT.
        :param authorizer_name: (experimental) The name of the authorizer. Default: 'JwtAuthorizer'
        :param identity_source: (experimental) The identity source for which authorization is requested. Default: ['$request.header.Authorization']

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "jwt_audience": jwt_audience,
            "jwt_issuer": jwt_issuer,
        }
        if authorizer_name is not None:
            self._values["authorizer_name"] = authorizer_name
        if identity_source is not None:
            self._values["identity_source"] = identity_source

    @builtins.property
    def jwt_audience(self) -> typing.List[builtins.str]:
        '''(experimental) A list of the intended recipients of the JWT.

        A valid JWT must provide an aud that matches at least one entry in this list.

        :stability: experimental
        '''
        result = self._values.get("jwt_audience")
        assert result is not None, "Required property 'jwt_audience' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def jwt_issuer(self) -> builtins.str:
        '''(experimental) The base domain of the identity provider that issues JWT.

        :stability: experimental
        '''
        result = self._values.get("jwt_issuer")
        assert result is not None, "Required property 'jwt_issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the authorizer.

        :default: 'JwtAuthorizer'

        :stability: experimental
        '''
        result = self._values.get("authorizer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_source(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The identity source for which authorization is requested.

        :default: ['$request.header.Authorization']

        :stability: experimental
        '''
        result = self._values.get("identity_source")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpJwtAuthorizerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IHttpRouteAuthorizer_717e7ba3)
class HttpUserPoolAuthorizer(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_apigatewayv2_authorizers.HttpUserPoolAuthorizer",
):
    '''(experimental) Authorize Http Api routes on whether the requester is registered as part of an AWS Cognito user pool.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        user_pool: _IUserPool_5e500460,
        user_pool_client: _IUserPoolClient_4cdf19bd,
        authorizer_name: typing.Optional[builtins.str] = None,
        identity_source: typing.Optional[typing.List[builtins.str]] = None,
        user_pool_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param user_pool: (experimental) The associated user pool.
        :param user_pool_client: (experimental) The user pool client that should be used to authorize requests with the user pool.
        :param authorizer_name: (experimental) The name of the authorizer. Default: 'UserPoolAuthorizer'
        :param identity_source: (experimental) The identity source for which authorization is requested. Default: ['$request.header.Authorization']
        :param user_pool_region: (experimental) The AWS region in which the user pool is present. Default: - same region as the Route the authorizer is attached to.

        :stability: experimental
        '''
        props = UserPoolAuthorizerProps(
            user_pool=user_pool,
            user_pool_client=user_pool_client,
            authorizer_name=authorizer_name,
            identity_source=identity_source,
            user_pool_region=user_pool_region,
        )

        jsii.create(HttpUserPoolAuthorizer, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IHttpRoute_bfbdc841,
        scope: constructs.Construct,
    ) -> _HttpRouteAuthorizerConfig_cd6b9e02:
        '''(experimental) Bind this authorizer to a specified Http route.

        :param route: (experimental) The route to which the authorizer is being bound.
        :param scope: (experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        '''
        options = _HttpRouteAuthorizerBindOptions_290d6475(route=route, scope=scope)

        return typing.cast(_HttpRouteAuthorizerConfig_cd6b9e02, jsii.invoke(self, "bind", [options]))


@jsii.data_type(
    jsii_type="monocdk.aws_apigatewayv2_authorizers.UserPoolAuthorizerProps",
    jsii_struct_bases=[],
    name_mapping={
        "user_pool": "userPool",
        "user_pool_client": "userPoolClient",
        "authorizer_name": "authorizerName",
        "identity_source": "identitySource",
        "user_pool_region": "userPoolRegion",
    },
)
class UserPoolAuthorizerProps:
    def __init__(
        self,
        *,
        user_pool: _IUserPool_5e500460,
        user_pool_client: _IUserPoolClient_4cdf19bd,
        authorizer_name: typing.Optional[builtins.str] = None,
        identity_source: typing.Optional[typing.List[builtins.str]] = None,
        user_pool_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to initialize UserPoolAuthorizer.

        :param user_pool: (experimental) The associated user pool.
        :param user_pool_client: (experimental) The user pool client that should be used to authorize requests with the user pool.
        :param authorizer_name: (experimental) The name of the authorizer. Default: 'UserPoolAuthorizer'
        :param identity_source: (experimental) The identity source for which authorization is requested. Default: ['$request.header.Authorization']
        :param user_pool_region: (experimental) The AWS region in which the user pool is present. Default: - same region as the Route the authorizer is attached to.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "user_pool": user_pool,
            "user_pool_client": user_pool_client,
        }
        if authorizer_name is not None:
            self._values["authorizer_name"] = authorizer_name
        if identity_source is not None:
            self._values["identity_source"] = identity_source
        if user_pool_region is not None:
            self._values["user_pool_region"] = user_pool_region

    @builtins.property
    def user_pool(self) -> _IUserPool_5e500460:
        '''(experimental) The associated user pool.

        :stability: experimental
        '''
        result = self._values.get("user_pool")
        assert result is not None, "Required property 'user_pool' is missing"
        return typing.cast(_IUserPool_5e500460, result)

    @builtins.property
    def user_pool_client(self) -> _IUserPoolClient_4cdf19bd:
        '''(experimental) The user pool client that should be used to authorize requests with the user pool.

        :stability: experimental
        '''
        result = self._values.get("user_pool_client")
        assert result is not None, "Required property 'user_pool_client' is missing"
        return typing.cast(_IUserPoolClient_4cdf19bd, result)

    @builtins.property
    def authorizer_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the authorizer.

        :default: 'UserPoolAuthorizer'

        :stability: experimental
        '''
        result = self._values.get("authorizer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_source(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The identity source for which authorization is requested.

        :default: ['$request.header.Authorization']

        :stability: experimental
        '''
        result = self._values.get("identity_source")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_pool_region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS region in which the user pool is present.

        :default: - same region as the Route the authorizer is attached to.

        :stability: experimental
        '''
        result = self._values.get("user_pool_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolAuthorizerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HttpJwtAuthorizer",
    "HttpJwtAuthorizerProps",
    "HttpUserPoolAuthorizer",
    "UserPoolAuthorizerProps",
]

publication.publish()
