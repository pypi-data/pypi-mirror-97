'''
# AWS APIGatewayv2 Authorizers

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Table of Contents

* [HTTP APIs](#http-apis)
* [JWT Authorizers](#jwt-authorizers)

  * [User Pool Authorizer](#user-pool-authorizer)

## HTTP APIs

API Gateway supports multiple mechanisms for controlling and managing access to your HTTP API. They are mainly
classified into Lambda Authorizers, JWT authorizers and standard AWS IAM roles and policies. More information is
available at [Controlling and managing access to an HTTP
API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-access-control.html).

## JWT Authorizers

JWT authorizers allow the use of JSON Web Tokens (JWTs) as part of [OpenID Connect](https://openid.net/specs/openid-connect-core-1_0.html) and [OAuth 2.0](https://oauth.net/2/) frameworks to allow and restrict clients from accessing HTTP APIs.

When configured on a route, the API Gateway service validates the JWTs submitted by the client, and allows or denies access based on its content.

API gateway uses the `identitySource` to determine where to look for the token. By default it checks the http `Authorization` header. However it also [supports a number of other options](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html#http-api-lambda-authorizer.identity-sources). It then decodes the JWT and validates the signature and claims, against the options defined in the authorizer and route (scopes). For more information check the [JWT Authorizer documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
authorizer = HttpJwtAuthorizer(
    jwt_audience=["3131231"],
    jwt_issuer="https://test.us.auth0.com"
)

api = HttpApi(stack, "HttpApi")

api.add_routes(
    integration=HttpProxyIntegration(
        url="https://get-books-proxy.myproxy.internal"
    ),
    path="/books",
    authorizer=authorizer
)
```

### User Pool Authorizer

User Pool Authorizer is a type of JWT Authorizer that uses a Cognito user pool and app client to control who can access your Api. After a successful authorization from the app client, the generated access token will be used as the JWT.

Clients accessing an API that uses a user pool authorizer must first sign in to a user pool and obtain an identity or access token.
They must then use this token in the `Authorization` header of the API call. More information is available at [using Amazon Cognito user
pools as authorizer](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-integrate-with-cognito.html).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
user_pool = UserPool(stack, "UserPool")
user_pool_client = user_pool.add_client("UserPoolClient")

authorizer = HttpUserPoolAuthorizer(
    user_pool=user_pool,
    user_pool_client=user_pool_client
)

api = HttpApi(stack, "HttpApi")

api.add_routes(
    integration=HttpProxyIntegration(
        url="https://get-books-proxy.myproxy.internal"
    ),
    path="/books",
    authorizer=authorizer
)
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_apigatewayv2
import aws_cdk.aws_cognito
import constructs


@jsii.implements(aws_cdk.aws_apigatewayv2.IHttpRouteAuthorizer)
class HttpJwtAuthorizer(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-authorizers.HttpJwtAuthorizer",
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
        route: aws_cdk.aws_apigatewayv2.IHttpRoute,
        scope: constructs.Construct,
    ) -> aws_cdk.aws_apigatewayv2.HttpRouteAuthorizerConfig:
        '''(experimental) (experimental) Bind this authorizer to a specified Http route.

        :param route: (experimental) The route to which the authorizer is being bound.
        :param scope: (experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        '''
        options = aws_cdk.aws_apigatewayv2.HttpRouteAuthorizerBindOptions(
            route=route, scope=scope
        )

        return typing.cast(aws_cdk.aws_apigatewayv2.HttpRouteAuthorizerConfig, jsii.invoke(self, "bind", [options]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-authorizers.HttpJwtAuthorizerProps",
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


@jsii.implements(aws_cdk.aws_apigatewayv2.IHttpRouteAuthorizer)
class HttpUserPoolAuthorizer(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-authorizers.HttpUserPoolAuthorizer",
):
    '''(experimental) Authorize Http Api routes on whether the requester is registered as part of an AWS Cognito user pool.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        user_pool: aws_cdk.aws_cognito.IUserPool,
        user_pool_client: aws_cdk.aws_cognito.IUserPoolClient,
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
        route: aws_cdk.aws_apigatewayv2.IHttpRoute,
        scope: constructs.Construct,
    ) -> aws_cdk.aws_apigatewayv2.HttpRouteAuthorizerConfig:
        '''(experimental) (experimental) Bind this authorizer to a specified Http route.

        :param route: (experimental) The route to which the authorizer is being bound.
        :param scope: (experimental) The scope for any constructs created as part of the bind.

        :stability: experimental
        '''
        options = aws_cdk.aws_apigatewayv2.HttpRouteAuthorizerBindOptions(
            route=route, scope=scope
        )

        return typing.cast(aws_cdk.aws_apigatewayv2.HttpRouteAuthorizerConfig, jsii.invoke(self, "bind", [options]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-authorizers.UserPoolAuthorizerProps",
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
        user_pool: aws_cdk.aws_cognito.IUserPool,
        user_pool_client: aws_cdk.aws_cognito.IUserPoolClient,
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
    def user_pool(self) -> aws_cdk.aws_cognito.IUserPool:
        '''(experimental) The associated user pool.

        :stability: experimental
        '''
        result = self._values.get("user_pool")
        assert result is not None, "Required property 'user_pool' is missing"
        return typing.cast(aws_cdk.aws_cognito.IUserPool, result)

    @builtins.property
    def user_pool_client(self) -> aws_cdk.aws_cognito.IUserPoolClient:
        '''(experimental) The user pool client that should be used to authorize requests with the user pool.

        :stability: experimental
        '''
        result = self._values.get("user_pool_client")
        assert result is not None, "Required property 'user_pool_client' is missing"
        return typing.cast(aws_cdk.aws_cognito.IUserPoolClient, result)

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
