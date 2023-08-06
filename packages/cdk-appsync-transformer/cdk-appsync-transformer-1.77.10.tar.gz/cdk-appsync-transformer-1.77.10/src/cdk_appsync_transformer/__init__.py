'''
# AppSync Transformer Construct for AWS CDK

![build](https://github.com/kcwinner/cdk-appsync-transformer/workflows/Build/badge.svg)
[![codecov](https://codecov.io/gh/kcwinner/cdk-appsync-transformer/branch/main/graph/badge.svg)](https://codecov.io/gh/kcwinner/cdk-appsync-transformer)
[![dependencies Status](https://david-dm.org/kcwinner/cdk-appsync-transformer/status.svg)](https://david-dm.org/kcwinner/cdk-appsync-transformer)
[![npm](https://img.shields.io/npm/dt/cdk-appsync-transformer)](https://www.npmjs.com/package/cdk-appsync-transformer)

[![npm version](https://badge.fury.io/js/cdk-appsync-transformer.svg)](https://badge.fury.io/js/cdk-appsync-transformer)
[![PyPI version](https://badge.fury.io/py/cdk-appsync-transformer.svg)](https://badge.fury.io/py/cdk-appsync-transformer)

## Notice

For CDK versions < 1.64.0 please use [aws-cdk-appsync-transformer](https://github.com/kcwinner/aws-cdk-appsync-transformer).

## Why This Package

In April 2020 I wrote a [blog post](https://www.trek10.com/blog/appsync-with-the-aws-cloud-development-kit) on using the AWS Cloud Development Kit with AppSync. I wrote my own transformer in order to emulate AWS Amplify's method of using GraphQL directives in order to template a lot of the Schema Definition Language.

This package is my attempt to convert all of that effort into a separate construct in order to clean up the process.

## How Do I Use It

### Example Usage

API With Default Values

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_appsync_transformer import AppSyncTransformer
AppSyncTransformer(self, "my-cool-api",
    schema_path="schema.graphql"
)
```

schema.graphql

```graphql
type Customer @model
    @auth(rules: [
        { allow: groups, groups: ["Admins"] },
        { allow: private, provider: iam, operations: [read, update] }
    ]) {
        id: ID!
        firstName: String!
        lastName: String!
        active: Boolean!
        address: String!
}

type Product @model
    @auth(rules: [
        { allow: groups, groups: ["Admins"] },
        { allow: public, provider: iam, operations: [read] }
    ]) {
        id: ID!
        name: String!
        description: String!
        price: String!
        active: Boolean!
        added: AWSDateTime!
        orders: [Order] @connection
}

type Order @model
    @key(fields: ["id", "productID"]) {
        id: ID!
        productID: ID!
        total: String!
        ordered: AWSDateTime!
}
```

### [Supported Amplify Directives](https://docs.amplify.aws/cli/graphql-transformer/directives)

Tested:

* [@model](https://docs.amplify.aws/cli/graphql-transformer/directives#model)
* [@auth](https://docs.amplify.aws/cli/graphql-transformer/directives#auth)
* [@connection](https://docs.amplify.aws/cli/graphql-transformer/directives#connection)
* [@key](https://docs.amplify.aws/cli/graphql-transformer/directives#key)
* [@function](https://docs.amplify.aws/cli/graphql-transformer/directives#function)

  * These work differently here than they do in Amplify - see [Functions](#functions) below

Experimental:

* [@versioned](https://docs.amplify.aws/cli/graphql-transformer/directives#versioned)
* [@http](https://docs.amplify.aws/cli/graphql-transformer/directives#http)
* [@ttl](https://github.com/flogy/graphql-ttl-transformer)

  * Community directive transformer

Not Yet Supported:

* [@searchable](https://docs.amplify.aws/cli/graphql-transformer/directives#searchable)
* [@predictions](https://docs.amplify.aws/cli/graphql-transformer/directives#predictions)

### Custom Transformers & Directives

*This is an advanced feature*

It is possible to add pre/post custom transformers that extend the Amplify ITransformer. To see a simple example please look at [mapped-transformer.ts](./test/mappedTransformer/mapped-transformer.ts) in the tests section.

This allows you to modify the data either before or after the [cdk-transformer](./src/transformer/cdk-transformer.ts) is run.

*Limitation:* Due to some limitations with `jsii` we are unable to export the ITransformer interface from `graphql-transformer-core` to ensure complete type safety. Instead, there is a validation method that will check for `name`, `directive` and `typeDefinitions` members in the transformers that are passed in.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from ..customTransformers import PreTransformer, PostTransformer
AppSyncTransformer(self, "my-cool-api",
    schema_path="schema.graphql",
    pre_cdk_transformers=[
        PreTransformer()
    ],
    post_cdk_transformers=[
        PostTransformer()
    ]
)
```

### Authentication

User Pool Authentication

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
user_pool = UserPool(self, "my-cool-user-pool", ...
)
user_pool_client = UserPoolClient(self, f"{id}-client",
    user_pool=self.user_pool, ...
)
AppSyncTransformer(self, "my-cool-api",
    schema_path="schema.graphql",
    authorization_config={
        "default_authorization": {
            "authorization_type": AuthorizationType.USER_POOL,
            "user_pool_config": {
                "user_pool": user_pool,
                "app_id_client_regex": user_pool_client.user_pool_client_id,
                "default_action": UserPoolDefaultAction.ALLOW
            }
        }
    }
)
```

#### IAM

Unauth Role: TODO

Auth Role: Unsupported. Authorized roles (Lambda Functions, EC2 roles, etc) are required to setup their own role permissions.

### Functions

There are two ways to add functions as data sources (and their resolvers)

#### Convenience Method

`addLambdaDataSourceAndResolvers` will do the same thing as the manual version below. However, if you want to customize mapping templates you will have to bypass this and set up the data source and resolvers yourself

#### Manually

Fields with the `@function` directive will be accessible via `appsyncTransformer.functionResolvers`. It will return a map like so:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
    "user-function"[{"type_name": "Query", "field_name": "listUsers"}, {"type_name": "Query", "field_name": "getUser"}, {"type_name": "Mutation", "field_name": "createUser"}, {"type_name": "Mutation", "field_name": "updateUser"}
    ]
```

You can grab your function resolvers via the map and assign them your own function(s). Example might be something like:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
user_function = Function(...)
user_function_data_source = appsync_transformer.appsync_aPI.add_lambda_data_source("some-id", user_function)

data_source_map = {
    "user-function": user_function_data_source
}

for [function_name, resolver] in Object.entries(appsync_transformer.function_resolvers):
    data_source = dataSourceMap[functionName]
    Resolver(self.nested_appsync_stack, f"{resolver.typeName}-{resolver.fieldName}-resolver",
        api=appsync_transformer.appsync_aPI,
        type_name=resolver.type_name,
        field_name=resolver.field_name,
        data_source=data_source,
        request_mapping_template=resolver.default_request_mapping_template,
        response_mapping_template=resolver.default_response_mapping_template
    )
```

### Table Name Map

Often you will need to access your table names in a lambda function or elsewhere. The cdk-appsync-transformer will return these values as a map of table names to cdk tokens. These tokens will be resolved at deploy time. They can be accessed via `appSyncTransformer.tableNameMap`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
CustomerTable: '${Token[TOKEN.1300]}',
      ProductTable"${Token[TOKEN.1346]}" , OrderTable"${Token[TOKEN.1392]}" , BlogTable"${Token[TOKEN.1442]}" , PostTable"${Token[TOKEN.1492]}" , CommentTable"${Token[TOKEN.1546]}" , UserTable"${Token[TOKEN.1596]}"
```

### DataStore Support

1. Pass `syncEnabled: true` to the `AppSyncTransformerProps`
2. Generate necessary exports (see [Code Generation](#code-generation) below)

### Cfn Outputs

* `appsyncGraphQLEndpointOutput` - the appsync graphql endpoint

### Code Generation

I've written some helpers to generate code similarly to how AWS Amplify generates statements and types. You can find the code [here](https://github.com/kcwinner/advocacy/tree/master/cdk-amplify-appsync-helpers).

## Versioning

I will *attempt* to align the major and minor version of this package with [AWS CDK], but always check the release descriptions for compatibility.

I currently support [![GitHub package.json dependency version (prod)](https://img.shields.io/github/package-json/dependency-version/kcwinner/cdk-appsync-transformer/@aws-cdk/core)](https://github.com/aws/aws-cdk)

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details

## License

Distributed under [Apache License, Version 2.0](LICENSE)

## References

* [aws cdk](https://aws.amazon.com/cdk)
* [amplify-cli](https://github.com/aws-amplify/amplify-cli)
* [Amplify Directives](https://docs.amplify.aws/cli/graphql-transformer/directives)
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

import aws_cdk.aws_appsync
import aws_cdk.aws_lambda
import aws_cdk.core


class AppSyncTransformer(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-appsync-transformer.AppSyncTransformer",
):
    '''(experimental) AppSyncTransformer Construct.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        schema_path: builtins.str,
        api_name: typing.Optional[builtins.str] = None,
        authorization_config: typing.Optional[aws_cdk.aws_appsync.AuthorizationConfig] = None,
        enable_dynamo_point_in_time_recovery: typing.Optional[builtins.bool] = None,
        field_log_level: typing.Optional[aws_cdk.aws_appsync.FieldLogLevel] = None,
        post_cdk_transformers: typing.Optional[typing.List[typing.Any]] = None,
        pre_cdk_transformers: typing.Optional[typing.List[typing.Any]] = None,
        sync_enabled: typing.Optional[builtins.bool] = None,
        xray_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param schema_path: (experimental) Relative path where schema.graphql exists.
        :param api_name: (experimental) String value representing the api name. Default: ``${id}-api``
        :param authorization_config: (experimental) Optional. {@link AuthorizationConfig} type defining authorization for AppSync GraphqlApi. Defaults to API_KEY Default: API_KEY authorization config
        :param enable_dynamo_point_in_time_recovery: (experimental) Whether to enable dynamo Point In Time Recovery. Default to false for backwards compatibility Default: false
        :param field_log_level: (experimental) Optional. {@link FieldLogLevel} type for AppSync GraphqlApi log level Default: FieldLogLevel.NONE
        :param post_cdk_transformers: (experimental) Optional. Additonal custom transformers to run after the CDK resource generations. Mostly useful for deep level customization of the generated CDK CloudFormation resources. These should extend Transformer class from graphql-transformer-core Default: undefined
        :param pre_cdk_transformers: (experimental) Optional. Additonal custom transformers to run prior to the CDK resource generations. Particularly useful for custom directives. These should extend Transformer class from graphql-transformer-core Default: undefined
        :param sync_enabled: (experimental) Whether to enable Amplify DataStore and Sync Tables. Default: false
        :param xray_enabled: (experimental) Determines whether xray should be enabled on the AppSync API. Default: false

        :stability: experimental
        '''
        props = AppSyncTransformerProps(
            schema_path=schema_path,
            api_name=api_name,
            authorization_config=authorization_config,
            enable_dynamo_point_in_time_recovery=enable_dynamo_point_in_time_recovery,
            field_log_level=field_log_level,
            post_cdk_transformers=post_cdk_transformers,
            pre_cdk_transformers=pre_cdk_transformers,
            sync_enabled=sync_enabled,
            xray_enabled=xray_enabled,
        )

        jsii.create(AppSyncTransformer, self, [scope, id, props])

    @jsii.member(jsii_name="addLambdaDataSourceAndResolvers")
    def add_lambda_data_source_and_resolvers(
        self,
        function_name: builtins.str,
        id: builtins.str,
        lambda_function: aws_cdk.aws_lambda.IFunction,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_appsync.LambdaDataSource:
        '''(experimental) Adds the function as a lambdaDataSource to the AppSync api Adds all of the functions resolvers to the AppSync api.

        :param function_name: The function name specified in the.
        :param id: The id to give.
        :param lambda_function: The lambda function to attach.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        :function: directive of the schema
        '''
        options = aws_cdk.aws_appsync.DataSourceOptions(
            description=description, name=name
        )

        return typing.cast(aws_cdk.aws_appsync.LambdaDataSource, jsii.invoke(self, "addLambdaDataSourceAndResolvers", [function_name, id, lambda_function, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="appsyncAPI")
    def appsync_api(self) -> aws_cdk.aws_appsync.GraphqlApi:
        '''(experimental) The cdk GraphqlApi construct.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_appsync.GraphqlApi, jsii.get(self, "appsyncAPI"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="functionResolvers")
    def function_resolvers(
        self,
    ) -> typing.Mapping[builtins.str, typing.List["CdkTransformerFunctionResolver"]]:
        '''(experimental) The Lambda Function resolvers designated by the function directive https://github.com/kcwinner/cdk-appsync-transformer#functions.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.List["CdkTransformerFunctionResolver"]], jsii.get(self, "functionResolvers"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpResolvers")
    def http_resolvers(
        self,
    ) -> typing.Mapping[builtins.str, typing.List["CdkTransformerHttpResolver"]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.List["CdkTransformerHttpResolver"]], jsii.get(self, "httpResolvers"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nestedAppsyncStack")
    def nested_appsync_stack(self) -> aws_cdk.core.NestedStack:
        '''(experimental) The NestedStack that contains the AppSync resources.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.core.NestedStack, jsii.get(self, "nestedAppsyncStack"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "SchemaTransformerOutputs":
        '''(experimental) The outputs from the SchemaTransformer.

        :stability: experimental
        '''
        return typing.cast("SchemaTransformerOutputs", jsii.get(self, "outputs"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="resolvers")
    def resolvers(self) -> typing.Any:
        '''(experimental) The AppSync resolvers from the transformer minus any function resolvers.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "resolvers"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tableNameMap")
    def table_name_map(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Map of cdk table tokens to table names.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "tableNameMap"))


@jsii.data_type(
    jsii_type="cdk-appsync-transformer.AppSyncTransformerProps",
    jsii_struct_bases=[],
    name_mapping={
        "schema_path": "schemaPath",
        "api_name": "apiName",
        "authorization_config": "authorizationConfig",
        "enable_dynamo_point_in_time_recovery": "enableDynamoPointInTimeRecovery",
        "field_log_level": "fieldLogLevel",
        "post_cdk_transformers": "postCdkTransformers",
        "pre_cdk_transformers": "preCdkTransformers",
        "sync_enabled": "syncEnabled",
        "xray_enabled": "xrayEnabled",
    },
)
class AppSyncTransformerProps:
    def __init__(
        self,
        *,
        schema_path: builtins.str,
        api_name: typing.Optional[builtins.str] = None,
        authorization_config: typing.Optional[aws_cdk.aws_appsync.AuthorizationConfig] = None,
        enable_dynamo_point_in_time_recovery: typing.Optional[builtins.bool] = None,
        field_log_level: typing.Optional[aws_cdk.aws_appsync.FieldLogLevel] = None,
        post_cdk_transformers: typing.Optional[typing.List[typing.Any]] = None,
        pre_cdk_transformers: typing.Optional[typing.List[typing.Any]] = None,
        sync_enabled: typing.Optional[builtins.bool] = None,
        xray_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param schema_path: (experimental) Relative path where schema.graphql exists.
        :param api_name: (experimental) String value representing the api name. Default: ``${id}-api``
        :param authorization_config: (experimental) Optional. {@link AuthorizationConfig} type defining authorization for AppSync GraphqlApi. Defaults to API_KEY Default: API_KEY authorization config
        :param enable_dynamo_point_in_time_recovery: (experimental) Whether to enable dynamo Point In Time Recovery. Default to false for backwards compatibility Default: false
        :param field_log_level: (experimental) Optional. {@link FieldLogLevel} type for AppSync GraphqlApi log level Default: FieldLogLevel.NONE
        :param post_cdk_transformers: (experimental) Optional. Additonal custom transformers to run after the CDK resource generations. Mostly useful for deep level customization of the generated CDK CloudFormation resources. These should extend Transformer class from graphql-transformer-core Default: undefined
        :param pre_cdk_transformers: (experimental) Optional. Additonal custom transformers to run prior to the CDK resource generations. Particularly useful for custom directives. These should extend Transformer class from graphql-transformer-core Default: undefined
        :param sync_enabled: (experimental) Whether to enable Amplify DataStore and Sync Tables. Default: false
        :param xray_enabled: (experimental) Determines whether xray should be enabled on the AppSync API. Default: false

        :stability: experimental
        '''
        if isinstance(authorization_config, dict):
            authorization_config = aws_cdk.aws_appsync.AuthorizationConfig(**authorization_config)
        self._values: typing.Dict[str, typing.Any] = {
            "schema_path": schema_path,
        }
        if api_name is not None:
            self._values["api_name"] = api_name
        if authorization_config is not None:
            self._values["authorization_config"] = authorization_config
        if enable_dynamo_point_in_time_recovery is not None:
            self._values["enable_dynamo_point_in_time_recovery"] = enable_dynamo_point_in_time_recovery
        if field_log_level is not None:
            self._values["field_log_level"] = field_log_level
        if post_cdk_transformers is not None:
            self._values["post_cdk_transformers"] = post_cdk_transformers
        if pre_cdk_transformers is not None:
            self._values["pre_cdk_transformers"] = pre_cdk_transformers
        if sync_enabled is not None:
            self._values["sync_enabled"] = sync_enabled
        if xray_enabled is not None:
            self._values["xray_enabled"] = xray_enabled

    @builtins.property
    def schema_path(self) -> builtins.str:
        '''(experimental) Relative path where schema.graphql exists.

        :stability: experimental
        '''
        result = self._values.get("schema_path")
        assert result is not None, "Required property 'schema_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) String value representing the api name.

        :default: ``${id}-api``

        :stability: experimental
        '''
        result = self._values.get("api_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorization_config(
        self,
    ) -> typing.Optional[aws_cdk.aws_appsync.AuthorizationConfig]:
        '''(experimental) Optional.

        {@link AuthorizationConfig} type defining authorization for AppSync GraphqlApi. Defaults to API_KEY

        :default: API_KEY authorization config

        :stability: experimental
        '''
        result = self._values.get("authorization_config")
        return typing.cast(typing.Optional[aws_cdk.aws_appsync.AuthorizationConfig], result)

    @builtins.property
    def enable_dynamo_point_in_time_recovery(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable dynamo Point In Time Recovery.

        Default to false for backwards compatibility

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_dynamo_point_in_time_recovery")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def field_log_level(self) -> typing.Optional[aws_cdk.aws_appsync.FieldLogLevel]:
        '''(experimental) Optional.

        {@link FieldLogLevel} type for AppSync GraphqlApi log level

        :default: FieldLogLevel.NONE

        :stability: experimental
        '''
        result = self._values.get("field_log_level")
        return typing.cast(typing.Optional[aws_cdk.aws_appsync.FieldLogLevel], result)

    @builtins.property
    def post_cdk_transformers(self) -> typing.Optional[typing.List[typing.Any]]:
        '''(experimental) Optional.

        Additonal custom transformers to run after the CDK resource generations.
        Mostly useful for deep level customization of the generated CDK CloudFormation resources.
        These should extend Transformer class from graphql-transformer-core

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("post_cdk_transformers")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def pre_cdk_transformers(self) -> typing.Optional[typing.List[typing.Any]]:
        '''(experimental) Optional.

        Additonal custom transformers to run prior to the CDK resource generations.
        Particularly useful for custom directives.
        These should extend Transformer class from graphql-transformer-core

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("pre_cdk_transformers")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def sync_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable Amplify DataStore and Sync Tables.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("sync_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def xray_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Determines whether xray should be enabled on the AppSync API.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("xray_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppSyncTransformerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-appsync-transformer.CdkTransformerGlobalSecondaryIndex",
    jsii_struct_bases=[],
    name_mapping={
        "index_name": "indexName",
        "partition_key": "partitionKey",
        "projection": "projection",
        "sort_key": "sortKey",
    },
)
class CdkTransformerGlobalSecondaryIndex:
    def __init__(
        self,
        *,
        index_name: builtins.str,
        partition_key: "CdkTransformerTableKey",
        projection: typing.Any,
        sort_key: "CdkTransformerTableKey",
    ) -> None:
        '''
        :param index_name: 
        :param partition_key: 
        :param projection: 
        :param sort_key: 

        :stability: experimental
        '''
        if isinstance(partition_key, dict):
            partition_key = CdkTransformerTableKey(**partition_key)
        if isinstance(sort_key, dict):
            sort_key = CdkTransformerTableKey(**sort_key)
        self._values: typing.Dict[str, typing.Any] = {
            "index_name": index_name,
            "partition_key": partition_key,
            "projection": projection,
            "sort_key": sort_key,
        }

    @builtins.property
    def index_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("index_name")
        assert result is not None, "Required property 'index_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partition_key(self) -> "CdkTransformerTableKey":
        '''
        :stability: experimental
        '''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast("CdkTransformerTableKey", result)

    @builtins.property
    def projection(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        result = self._values.get("projection")
        assert result is not None, "Required property 'projection' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def sort_key(self) -> "CdkTransformerTableKey":
        '''
        :stability: experimental
        '''
        result = self._values.get("sort_key")
        assert result is not None, "Required property 'sort_key' is missing"
        return typing.cast("CdkTransformerTableKey", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkTransformerGlobalSecondaryIndex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-appsync-transformer.CdkTransformerResolver",
    jsii_struct_bases=[],
    name_mapping={"field_name": "fieldName", "type_name": "typeName"},
)
class CdkTransformerResolver:
    def __init__(self, *, field_name: builtins.str, type_name: builtins.str) -> None:
        '''
        :param field_name: 
        :param type_name: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "field_name": field_name,
            "type_name": type_name,
        }

    @builtins.property
    def field_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("field_name")
        assert result is not None, "Required property 'field_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("type_name")
        assert result is not None, "Required property 'type_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkTransformerResolver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-appsync-transformer.CdkTransformerTable",
    jsii_struct_bases=[],
    name_mapping={
        "global_secondary_indexes": "globalSecondaryIndexes",
        "gsi_resolvers": "gsiResolvers",
        "partition_key": "partitionKey",
        "resolvers": "resolvers",
        "table_name": "tableName",
        "sort_key": "sortKey",
        "ttl": "ttl",
    },
)
class CdkTransformerTable:
    def __init__(
        self,
        *,
        global_secondary_indexes: typing.List[CdkTransformerGlobalSecondaryIndex],
        gsi_resolvers: typing.List[builtins.str],
        partition_key: "CdkTransformerTableKey",
        resolvers: typing.List[builtins.str],
        table_name: builtins.str,
        sort_key: typing.Optional["CdkTransformerTableKey"] = None,
        ttl: typing.Optional["CdkTransformerTableTtl"] = None,
    ) -> None:
        '''
        :param global_secondary_indexes: 
        :param gsi_resolvers: 
        :param partition_key: 
        :param resolvers: 
        :param table_name: 
        :param sort_key: 
        :param ttl: 

        :stability: experimental
        '''
        if isinstance(partition_key, dict):
            partition_key = CdkTransformerTableKey(**partition_key)
        if isinstance(sort_key, dict):
            sort_key = CdkTransformerTableKey(**sort_key)
        if isinstance(ttl, dict):
            ttl = CdkTransformerTableTtl(**ttl)
        self._values: typing.Dict[str, typing.Any] = {
            "global_secondary_indexes": global_secondary_indexes,
            "gsi_resolvers": gsi_resolvers,
            "partition_key": partition_key,
            "resolvers": resolvers,
            "table_name": table_name,
        }
        if sort_key is not None:
            self._values["sort_key"] = sort_key
        if ttl is not None:
            self._values["ttl"] = ttl

    @builtins.property
    def global_secondary_indexes(
        self,
    ) -> typing.List[CdkTransformerGlobalSecondaryIndex]:
        '''
        :stability: experimental
        '''
        result = self._values.get("global_secondary_indexes")
        assert result is not None, "Required property 'global_secondary_indexes' is missing"
        return typing.cast(typing.List[CdkTransformerGlobalSecondaryIndex], result)

    @builtins.property
    def gsi_resolvers(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("gsi_resolvers")
        assert result is not None, "Required property 'gsi_resolvers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def partition_key(self) -> "CdkTransformerTableKey":
        '''
        :stability: experimental
        '''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast("CdkTransformerTableKey", result)

    @builtins.property
    def resolvers(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("resolvers")
        assert result is not None, "Required property 'resolvers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sort_key(self) -> typing.Optional["CdkTransformerTableKey"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("sort_key")
        return typing.cast(typing.Optional["CdkTransformerTableKey"], result)

    @builtins.property
    def ttl(self) -> typing.Optional["CdkTransformerTableTtl"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional["CdkTransformerTableTtl"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkTransformerTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-appsync-transformer.CdkTransformerTableKey",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class CdkTransformerTableKey:
    def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
        '''
        :param name: 
        :param type: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkTransformerTableKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-appsync-transformer.CdkTransformerTableTtl",
    jsii_struct_bases=[],
    name_mapping={"attribute_name": "attributeName", "enabled": "enabled"},
)
class CdkTransformerTableTtl:
    def __init__(self, *, attribute_name: builtins.str, enabled: builtins.bool) -> None:
        '''
        :param attribute_name: 
        :param enabled: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "attribute_name": attribute_name,
            "enabled": enabled,
        }

    @builtins.property
    def attribute_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("attribute_name")
        assert result is not None, "Required property 'attribute_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''
        :stability: experimental
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkTransformerTableTtl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-appsync-transformer.SchemaTransformerOutputs",
    jsii_struct_bases=[],
    name_mapping={
        "cdk_tables": "cdkTables",
        "function_resolvers": "functionResolvers",
        "http_resolvers": "httpResolvers",
        "mutations": "mutations",
        "none_resolvers": "noneResolvers",
        "queries": "queries",
        "subscriptions": "subscriptions",
    },
)
class SchemaTransformerOutputs:
    def __init__(
        self,
        *,
        cdk_tables: typing.Optional[typing.Mapping[builtins.str, CdkTransformerTable]] = None,
        function_resolvers: typing.Optional[typing.Mapping[builtins.str, typing.List["CdkTransformerFunctionResolver"]]] = None,
        http_resolvers: typing.Optional[typing.Mapping[builtins.str, typing.List["CdkTransformerHttpResolver"]]] = None,
        mutations: typing.Optional[typing.Mapping[builtins.str, CdkTransformerResolver]] = None,
        none_resolvers: typing.Optional[typing.Mapping[builtins.str, CdkTransformerResolver]] = None,
        queries: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        subscriptions: typing.Optional[typing.Mapping[builtins.str, CdkTransformerResolver]] = None,
    ) -> None:
        '''
        :param cdk_tables: 
        :param function_resolvers: 
        :param http_resolvers: 
        :param mutations: 
        :param none_resolvers: 
        :param queries: 
        :param subscriptions: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if cdk_tables is not None:
            self._values["cdk_tables"] = cdk_tables
        if function_resolvers is not None:
            self._values["function_resolvers"] = function_resolvers
        if http_resolvers is not None:
            self._values["http_resolvers"] = http_resolvers
        if mutations is not None:
            self._values["mutations"] = mutations
        if none_resolvers is not None:
            self._values["none_resolvers"] = none_resolvers
        if queries is not None:
            self._values["queries"] = queries
        if subscriptions is not None:
            self._values["subscriptions"] = subscriptions

    @builtins.property
    def cdk_tables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, CdkTransformerTable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cdk_tables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, CdkTransformerTable]], result)

    @builtins.property
    def function_resolvers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List["CdkTransformerFunctionResolver"]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("function_resolvers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List["CdkTransformerFunctionResolver"]]], result)

    @builtins.property
    def http_resolvers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List["CdkTransformerHttpResolver"]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("http_resolvers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List["CdkTransformerHttpResolver"]]], result)

    @builtins.property
    def mutations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, CdkTransformerResolver]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("mutations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, CdkTransformerResolver]], result)

    @builtins.property
    def none_resolvers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, CdkTransformerResolver]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("none_resolvers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, CdkTransformerResolver]], result)

    @builtins.property
    def queries(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("queries")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def subscriptions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, CdkTransformerResolver]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("subscriptions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, CdkTransformerResolver]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaTransformerOutputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-appsync-transformer.CdkTransformerFunctionResolver",
    jsii_struct_bases=[CdkTransformerResolver],
    name_mapping={
        "field_name": "fieldName",
        "type_name": "typeName",
        "default_request_mapping_template": "defaultRequestMappingTemplate",
        "default_response_mapping_template": "defaultResponseMappingTemplate",
    },
)
class CdkTransformerFunctionResolver(CdkTransformerResolver):
    def __init__(
        self,
        *,
        field_name: builtins.str,
        type_name: builtins.str,
        default_request_mapping_template: builtins.str,
        default_response_mapping_template: builtins.str,
    ) -> None:
        '''
        :param field_name: 
        :param type_name: 
        :param default_request_mapping_template: 
        :param default_response_mapping_template: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "field_name": field_name,
            "type_name": type_name,
            "default_request_mapping_template": default_request_mapping_template,
            "default_response_mapping_template": default_response_mapping_template,
        }

    @builtins.property
    def field_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("field_name")
        assert result is not None, "Required property 'field_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("type_name")
        assert result is not None, "Required property 'type_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_request_mapping_template(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("default_request_mapping_template")
        assert result is not None, "Required property 'default_request_mapping_template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_response_mapping_template(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("default_response_mapping_template")
        assert result is not None, "Required property 'default_response_mapping_template' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkTransformerFunctionResolver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-appsync-transformer.CdkTransformerHttpResolver",
    jsii_struct_bases=[CdkTransformerResolver],
    name_mapping={
        "field_name": "fieldName",
        "type_name": "typeName",
        "default_request_mapping_template": "defaultRequestMappingTemplate",
        "default_response_mapping_template": "defaultResponseMappingTemplate",
        "http_config": "httpConfig",
    },
)
class CdkTransformerHttpResolver(CdkTransformerResolver):
    def __init__(
        self,
        *,
        field_name: builtins.str,
        type_name: builtins.str,
        default_request_mapping_template: builtins.str,
        default_response_mapping_template: builtins.str,
        http_config: typing.Any,
    ) -> None:
        '''
        :param field_name: 
        :param type_name: 
        :param default_request_mapping_template: 
        :param default_response_mapping_template: 
        :param http_config: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "field_name": field_name,
            "type_name": type_name,
            "default_request_mapping_template": default_request_mapping_template,
            "default_response_mapping_template": default_response_mapping_template,
            "http_config": http_config,
        }

    @builtins.property
    def field_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("field_name")
        assert result is not None, "Required property 'field_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("type_name")
        assert result is not None, "Required property 'type_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_request_mapping_template(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("default_request_mapping_template")
        assert result is not None, "Required property 'default_request_mapping_template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_response_mapping_template(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("default_response_mapping_template")
        assert result is not None, "Required property 'default_response_mapping_template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_config(self) -> typing.Any:
        '''
        :stability: experimental
        '''
        result = self._values.get("http_config")
        assert result is not None, "Required property 'http_config' is missing"
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkTransformerHttpResolver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AppSyncTransformer",
    "AppSyncTransformerProps",
    "CdkTransformerFunctionResolver",
    "CdkTransformerGlobalSecondaryIndex",
    "CdkTransformerHttpResolver",
    "CdkTransformerResolver",
    "CdkTransformerTable",
    "CdkTransformerTableKey",
    "CdkTransformerTableTtl",
    "SchemaTransformerOutputs",
]

publication.publish()
