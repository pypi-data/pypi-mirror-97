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
from .. import (
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IResolvable as _IResolvable_a771d0ef,
    IResolveContext as _IResolveContext_e363e2cb,
    Reference as _Reference_a96c80b4,
)
from ..aws_cloudformation import (
    CustomResourceProviderConfig as _CustomResourceProviderConfig_6579f796,
    ICustomResourceProvider as _ICustomResourceProvider_7c9ae4a2,
)
from ..aws_ec2 import (
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_iam import (
    IGrantable as _IGrantable_4c5a91d1,
    IPrincipal as _IPrincipal_93b48231,
    IRole as _IRole_59af6f50,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_logs import RetentionDays as _RetentionDays_6c560d31


@jsii.implements(_IGrantable_4c5a91d1)
class AwsCustomResource(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.custom_resources.AwsCustomResource",
):
    '''(experimental) Defines a custom resource that is materialized using specific AWS API calls.

    Use this to bridge any gap that might exist in the CloudFormation Coverage.
    You can specify exactly which calls are invoked for the 'CREATE', 'UPDATE' and 'DELETE' life cycle events.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        policy: "AwsCustomResourcePolicy",
        function_name: typing.Optional[builtins.str] = None,
        install_latest_aws_sdk: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        on_create: typing.Optional["AwsSdkCall"] = None,
        on_delete: typing.Optional["AwsSdkCall"] = None,
        on_update: typing.Optional["AwsSdkCall"] = None,
        resource_type: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param policy: (experimental) The policy that will be added to the execution role of the Lambda function implementing this custom resource provider. The custom resource also implements ``iam.IGrantable``, making it possible to use the ``grantXxx()`` methods. As this custom resource uses a singleton Lambda function, it's important to note the that function's role will eventually accumulate the permissions/grants from all resources.
        :param function_name: (experimental) A name for the Lambda function implementing this custom resource. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param install_latest_aws_sdk: (experimental) Whether to install the latest AWS SDK v2. Allows to use the latest API calls documented at https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html. The installation takes around 60 seconds. Default: true
        :param log_retention: (experimental) The number of days log events of the Lambda function implementing this custom resource are kept in CloudWatch Logs. Default: logs.RetentionDays.INFINITE
        :param on_create: (experimental) The AWS SDK call to make when the resource is created. Default: - the call when the resource is updated
        :param on_delete: (experimental) The AWS SDK call to make when the resource is deleted. Default: - no call
        :param on_update: (experimental) The AWS SDK call to make when the resource is updated. Default: - no call
        :param resource_type: (experimental) Cloudformation Resource type. Default: - Custom::AWS
        :param role: (experimental) The execution role for the Lambda function implementing this custom resource provider. This role will apply to all ``AwsCustomResource`` instances in the stack. The role must be assumable by the ``lambda.amazonaws.com`` service principal. Default: - a new role is created
        :param timeout: (experimental) The timeout for the Lambda function implementing this custom resource. Default: Duration.minutes(2)

        :stability: experimental
        '''
        props = AwsCustomResourceProps(
            policy=policy,
            function_name=function_name,
            install_latest_aws_sdk=install_latest_aws_sdk,
            log_retention=log_retention,
            on_create=on_create,
            on_delete=on_delete,
            on_update=on_update,
            resource_type=resource_type,
            role=role,
            timeout=timeout,
        )

        jsii.create(AwsCustomResource, self, [scope, id, props])

    @jsii.member(jsii_name="getResponseField")
    def get_response_field(self, data_path: builtins.str) -> builtins.str:
        '''(experimental) Returns response data for the AWS SDK call as string.

        Example for S3 / listBucket : 'Buckets.0.Name'

        Note that you cannot use this method if ``ignoreErrorCodesMatching``
        is configured for any of the SDK calls. This is because in such a case,
        the response data might not exist, and will cause a CloudFormation deploy time error.

        :param data_path: the path to the data.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "getResponseField", [data_path]))

    @jsii.member(jsii_name="getResponseFieldReference")
    def get_response_field_reference(
        self,
        data_path: builtins.str,
    ) -> _Reference_a96c80b4:
        '''(experimental) Returns response data for the AWS SDK call.

        Example for S3 / listBucket : 'Buckets.0.Name'

        Use ``Token.asXxx`` to encode the returned ``Reference`` as a specific type or
        use the convenience ``getDataString`` for string attributes.

        Note that you cannot use this method if ``ignoreErrorCodesMatching``
        is configured for any of the SDK calls. This is because in such a case,
        the response data might not exist, and will cause a CloudFormation deploy time error.

        :param data_path: the path to the data.

        :stability: experimental
        '''
        return typing.cast(_Reference_a96c80b4, jsii.invoke(self, "getResponseFieldReference", [data_path]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_93b48231:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(_IPrincipal_93b48231, jsii.get(self, "grantPrincipal"))


class AwsCustomResourcePolicy(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.custom_resources.AwsCustomResourcePolicy",
):
    '''(experimental) The IAM Policy that will be applied to the different calls.

    :stability: experimental
    '''

    @jsii.member(jsii_name="fromSdkCalls") # type: ignore[misc]
    @builtins.classmethod
    def from_sdk_calls(
        cls,
        *,
        resources: typing.List[builtins.str],
    ) -> "AwsCustomResourcePolicy":
        '''(experimental) Generate IAM Policy Statements from the configured SDK calls.

        Each SDK call with be translated to an IAM Policy Statement in the form of: ``call.service:call.action`` (e.g ``s3:PutObject``).

        :param resources: (experimental) The resources that the calls will have access to. It is best to use specific resource ARN's when possible. However, you can also use ``AwsCustomResourcePolicy.ANY_RESOURCE`` to allow access to all resources. For example, when ``onCreate`` is used to create a resource which you don't know the physical name of in advance. Note that will apply to ALL SDK calls.

        :stability: experimental
        '''
        options = SdkCallsPolicyOptions(resources=resources)

        return typing.cast("AwsCustomResourcePolicy", jsii.sinvoke(cls, "fromSdkCalls", [options]))

    @jsii.member(jsii_name="fromStatements") # type: ignore[misc]
    @builtins.classmethod
    def from_statements(
        cls,
        statements: typing.List[_PolicyStatement_296fe8a3],
    ) -> "AwsCustomResourcePolicy":
        '''(experimental) Explicit IAM Policy Statements.

        :param statements: the statements to propagate to the SDK calls.

        :stability: experimental
        '''
        return typing.cast("AwsCustomResourcePolicy", jsii.sinvoke(cls, "fromStatements", [statements]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="ANY_RESOURCE")
    def ANY_RESOURCE(cls) -> typing.List[builtins.str]:
        '''(experimental) Use this constant to configure access to any resource.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "ANY_RESOURCE"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="statements")
    def statements(self) -> typing.List[_PolicyStatement_296fe8a3]:
        '''(experimental) statements for explicit policy.

        :stability: experimental
        '''
        return typing.cast(typing.List[_PolicyStatement_296fe8a3], jsii.get(self, "statements"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) resources for auto-generated from SDK calls.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resources"))


@jsii.data_type(
    jsii_type="monocdk.custom_resources.AwsCustomResourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "function_name": "functionName",
        "install_latest_aws_sdk": "installLatestAwsSdk",
        "log_retention": "logRetention",
        "on_create": "onCreate",
        "on_delete": "onDelete",
        "on_update": "onUpdate",
        "resource_type": "resourceType",
        "role": "role",
        "timeout": "timeout",
    },
)
class AwsCustomResourceProps:
    def __init__(
        self,
        *,
        policy: AwsCustomResourcePolicy,
        function_name: typing.Optional[builtins.str] = None,
        install_latest_aws_sdk: typing.Optional[builtins.bool] = None,
        log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        on_create: typing.Optional["AwsSdkCall"] = None,
        on_delete: typing.Optional["AwsSdkCall"] = None,
        on_update: typing.Optional["AwsSdkCall"] = None,
        resource_type: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''(experimental) Properties for AwsCustomResource.

        Note that at least onCreate, onUpdate or onDelete must be specified.

        :param policy: (experimental) The policy that will be added to the execution role of the Lambda function implementing this custom resource provider. The custom resource also implements ``iam.IGrantable``, making it possible to use the ``grantXxx()`` methods. As this custom resource uses a singleton Lambda function, it's important to note the that function's role will eventually accumulate the permissions/grants from all resources.
        :param function_name: (experimental) A name for the Lambda function implementing this custom resource. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param install_latest_aws_sdk: (experimental) Whether to install the latest AWS SDK v2. Allows to use the latest API calls documented at https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html. The installation takes around 60 seconds. Default: true
        :param log_retention: (experimental) The number of days log events of the Lambda function implementing this custom resource are kept in CloudWatch Logs. Default: logs.RetentionDays.INFINITE
        :param on_create: (experimental) The AWS SDK call to make when the resource is created. Default: - the call when the resource is updated
        :param on_delete: (experimental) The AWS SDK call to make when the resource is deleted. Default: - no call
        :param on_update: (experimental) The AWS SDK call to make when the resource is updated. Default: - no call
        :param resource_type: (experimental) Cloudformation Resource type. Default: - Custom::AWS
        :param role: (experimental) The execution role for the Lambda function implementing this custom resource provider. This role will apply to all ``AwsCustomResource`` instances in the stack. The role must be assumable by the ``lambda.amazonaws.com`` service principal. Default: - a new role is created
        :param timeout: (experimental) The timeout for the Lambda function implementing this custom resource. Default: Duration.minutes(2)

        :stability: experimental
        '''
        if isinstance(on_create, dict):
            on_create = AwsSdkCall(**on_create)
        if isinstance(on_delete, dict):
            on_delete = AwsSdkCall(**on_delete)
        if isinstance(on_update, dict):
            on_update = AwsSdkCall(**on_update)
        self._values: typing.Dict[str, typing.Any] = {
            "policy": policy,
        }
        if function_name is not None:
            self._values["function_name"] = function_name
        if install_latest_aws_sdk is not None:
            self._values["install_latest_aws_sdk"] = install_latest_aws_sdk
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if on_create is not None:
            self._values["on_create"] = on_create
        if on_delete is not None:
            self._values["on_delete"] = on_delete
        if on_update is not None:
            self._values["on_update"] = on_update
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if role is not None:
            self._values["role"] = role
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def policy(self) -> AwsCustomResourcePolicy:
        '''(experimental) The policy that will be added to the execution role of the Lambda function implementing this custom resource provider.

        The custom resource also implements ``iam.IGrantable``, making it possible
        to use the ``grantXxx()`` methods.

        As this custom resource uses a singleton Lambda function, it's important
        to note the that function's role will eventually accumulate the
        permissions/grants from all resources.

        :see: Policy.fromSdkCalls
        :stability: experimental
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(AwsCustomResourcePolicy, result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the Lambda function implementing this custom resource.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
        ID for the function's name. For more information, see Name Type.

        :stability: experimental
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_latest_aws_sdk(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to install the latest AWS SDK v2. Allows to use the latest API calls documented at https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html.

        The installation takes around 60 seconds.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("install_latest_aws_sdk")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_6c560d31]:
        '''(experimental) The number of days log events of the Lambda function implementing this custom resource are kept in CloudWatch Logs.

        :default: logs.RetentionDays.INFINITE

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_RetentionDays_6c560d31], result)

    @builtins.property
    def on_create(self) -> typing.Optional["AwsSdkCall"]:
        '''(experimental) The AWS SDK call to make when the resource is created.

        :default: - the call when the resource is updated

        :stability: experimental
        '''
        result = self._values.get("on_create")
        return typing.cast(typing.Optional["AwsSdkCall"], result)

    @builtins.property
    def on_delete(self) -> typing.Optional["AwsSdkCall"]:
        '''(experimental) The AWS SDK call to make when the resource is deleted.

        :default: - no call

        :stability: experimental
        '''
        result = self._values.get("on_delete")
        return typing.cast(typing.Optional["AwsSdkCall"], result)

    @builtins.property
    def on_update(self) -> typing.Optional["AwsSdkCall"]:
        '''(experimental) The AWS SDK call to make when the resource is updated.

        :default: - no call

        :stability: experimental
        '''
        result = self._values.get("on_update")
        return typing.cast(typing.Optional["AwsSdkCall"], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Cloudformation Resource type.

        :default: - Custom::AWS

        :stability: experimental
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The execution role for the Lambda function implementing this custom resource provider.

        This role will apply to all ``AwsCustomResource``
        instances in the stack. The role must be assumable by the
        ``lambda.amazonaws.com`` service principal.

        :default: - a new role is created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The timeout for the Lambda function implementing this custom resource.

        :default: Duration.minutes(2)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCustomResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.custom_resources.AwsSdkCall",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "service": "service",
        "api_version": "apiVersion",
        "ignore_error_codes_matching": "ignoreErrorCodesMatching",
        "output_path": "outputPath",
        "parameters": "parameters",
        "physical_resource_id": "physicalResourceId",
        "region": "region",
    },
)
class AwsSdkCall:
    def __init__(
        self,
        *,
        action: builtins.str,
        service: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        ignore_error_codes_matching: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
        physical_resource_id: typing.Optional["PhysicalResourceId"] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) An AWS SDK call.

        :param action: (experimental) The service action to call.
        :param service: (experimental) The service to call.
        :param api_version: (experimental) API version to use for the service. Default: - use latest available API version
        :param ignore_error_codes_matching: (experimental) The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param output_path: (experimental) Restrict the data returned by the custom resource to a specific path in the API response. Use this to limit the data returned by the custom resource if working with API calls that could potentially result in custom response objects exceeding the hard limit of 4096 bytes. Example for ECS / updateService: 'service.deploymentConfiguration.maximumPercent' Default: - return all data
        :param parameters: (experimental) The parameters for the service action. Default: - no parameters
        :param physical_resource_id: (experimental) The physical resource id of the custom resource for this call. Mandatory for onCreate or onUpdate calls. Default: - no physical resource id
        :param region: (experimental) The region to send service requests to. **Note: Cross-region operations are generally considered an anti-pattern.** **Consider first deploying a stack in that region.** Default: - the region where this custom resource is deployed

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "service": service,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if ignore_error_codes_matching is not None:
            self._values["ignore_error_codes_matching"] = ignore_error_codes_matching
        if output_path is not None:
            self._values["output_path"] = output_path
        if parameters is not None:
            self._values["parameters"] = parameters
        if physical_resource_id is not None:
            self._values["physical_resource_id"] = physical_resource_id
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def action(self) -> builtins.str:
        '''(experimental) The service action to call.

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''(experimental) The service to call.

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) API version to use for the service.

        :default: - use latest available API version

        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
        :stability: experimental
        '''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_error_codes_matching(self) -> typing.Optional[builtins.str]:
        '''(experimental) The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        :default: - do not catch errors

        :stability: experimental
        '''
        result = self._values.get("ignore_error_codes_matching")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Restrict the data returned by the custom resource to a specific path in the API response.

        Use this to limit the data returned by the custom
        resource if working with API calls that could potentially result in custom
        response objects exceeding the hard limit of 4096 bytes.

        Example for ECS / updateService: 'service.deploymentConfiguration.maximumPercent'

        :default: - return all data

        :stability: experimental
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''(experimental) The parameters for the service action.

        :default: - no parameters

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def physical_resource_id(self) -> typing.Optional["PhysicalResourceId"]:
        '''(experimental) The physical resource id of the custom resource for this call.

        Mandatory for onCreate or onUpdate calls.

        :default: - no physical resource id

        :stability: experimental
        '''
        result = self._values.get("physical_resource_id")
        return typing.cast(typing.Optional["PhysicalResourceId"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region to send service requests to.

        **Note: Cross-region operations are generally considered an anti-pattern.**
        **Consider first deploying a stack in that region.**

        :default: - the region where this custom resource is deployed

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsSdkCall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PhysicalResourceId(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.custom_resources.PhysicalResourceId",
):
    '''(experimental) Physical ID of the custom resource.

    :stability: experimental
    '''

    @jsii.member(jsii_name="fromResponse") # type: ignore[misc]
    @builtins.classmethod
    def from_response(cls, response_path: builtins.str) -> "PhysicalResourceId":
        '''(experimental) Extract the physical resource id from the path (dot notation) to the data in the API call response.

        :param response_path: -

        :stability: experimental
        '''
        return typing.cast("PhysicalResourceId", jsii.sinvoke(cls, "fromResponse", [response_path]))

    @jsii.member(jsii_name="of") # type: ignore[misc]
    @builtins.classmethod
    def of(cls, id: builtins.str) -> "PhysicalResourceId":
        '''(experimental) Explicit physical resource id.

        :param id: -

        :stability: experimental
        '''
        return typing.cast("PhysicalResourceId", jsii.sinvoke(cls, "of", [id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Literal string to be used as the physical id.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="responsePath")
    def response_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to a response data element to be used as the physical id.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responsePath"))


@jsii.implements(_IResolvable_a771d0ef)
class PhysicalResourceIdReference(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.custom_resources.PhysicalResourceIdReference",
):
    '''(experimental) Reference to the physical resource id that can be passed to the AWS operation as a parameter.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(PhysicalResourceIdReference, self, [])

    @jsii.member(jsii_name="resolve")
    def resolve(self, _: _IResolveContext_e363e2cb) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param _: -

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [_]))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> builtins.str:
        '''(experimental) toJSON serialization to replace ``PhysicalResourceIdReference`` with a magic string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this resolvable object.

        Returns a reversible string representation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        This may return an array with a single informational element indicating how
        to get this property populated, if it was skipped for performance reasons.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))


@jsii.implements(_ICustomResourceProvider_7c9ae4a2)
class Provider(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.custom_resources.Provider",
):
    '''(experimental) Defines an AWS CloudFormation custom resource provider.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        on_event_handler: _IFunction_6e14f09e,
        is_complete_handler: typing.Optional[_IFunction_6e14f09e] = None,
        log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        query_interval: typing.Optional[_Duration_070aa057] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        total_timeout: typing.Optional[_Duration_070aa057] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param on_event_handler: (experimental) The AWS Lambda function to invoke for all resource lifecycle operations (CREATE/UPDATE/DELETE). This function is responsible to begin the requested resource operation (CREATE/UPDATE/DELETE) and return any additional properties to add to the event, which will later be passed to ``isComplete``. The ``PhysicalResourceId`` property must be included in the response.
        :param is_complete_handler: (experimental) The AWS Lambda function to invoke in order to determine if the operation is complete. This function will be called immediately after ``onEvent`` and then periodically based on the configured query interval as long as it returns ``false``. If the function still returns ``false`` and the alloted timeout has passed, the operation will fail. Default: - provider is synchronous. This means that the ``onEvent`` handler is expected to finish all lifecycle operations within the initial invocation.
        :param log_retention: (experimental) The number of days framework log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param query_interval: (experimental) Time between calls to the ``isComplete`` handler which determines if the resource has been stabilized. The first ``isComplete`` will be called immediately after ``handler`` and then every ``queryInterval`` seconds, and until ``timeout`` has been reached or until ``isComplete`` returns ``true``. Default: Duration.seconds(5)
        :param security_groups: (experimental) Security groups to attach to the provider functions. Only used if 'vpc' is supplied Default: - If ``vpc`` is not supplied, no security groups are attached. Otherwise, a dedicated security group is created for each function.
        :param total_timeout: (experimental) Total timeout for the entire operation. The maximum timeout is 2 hours (yes, it can exceed the AWS Lambda 15 minutes) Default: Duration.minutes(30)
        :param vpc: (experimental) The vpc to provision the lambda functions in. Default: - functions are not provisioned inside a vpc.
        :param vpc_subnets: (experimental) Which subnets from the VPC to place the lambda functions in. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified

        :stability: experimental
        '''
        props = ProviderProps(
            on_event_handler=on_event_handler,
            is_complete_handler=is_complete_handler,
            log_retention=log_retention,
            query_interval=query_interval,
            security_groups=security_groups,
            total_timeout=total_timeout,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(Provider, self, [scope, id, props])

    @jsii.member(jsii_name="bind")
    def bind(self, _: _Construct_e78e779f) -> _CustomResourceProviderConfig_6579f796:
        '''(deprecated) Called by ``CustomResource`` which uses this provider.

        :param _: -

        :deprecated: use ``provider.serviceToken`` instead

        :stability: deprecated
        '''
        return typing.cast(_CustomResourceProviderConfig_6579f796, jsii.invoke(self, "bind", [_]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="onEventHandler")
    def on_event_handler(self) -> _IFunction_6e14f09e:
        '''(experimental) The user-defined AWS Lambda function which is invoked for all resource lifecycle operations (CREATE/UPDATE/DELETE).

        :stability: experimental
        '''
        return typing.cast(_IFunction_6e14f09e, jsii.get(self, "onEventHandler"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> builtins.str:
        '''(experimental) The service token to use in order to define custom resources that are backed by this provider.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceToken"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="isCompleteHandler")
    def is_complete_handler(self) -> typing.Optional[_IFunction_6e14f09e]:
        '''(experimental) The user-defined AWS Lambda function which is invoked asynchronously in order to determine if the operation is complete.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IFunction_6e14f09e], jsii.get(self, "isCompleteHandler"))


@jsii.data_type(
    jsii_type="monocdk.custom_resources.ProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "on_event_handler": "onEventHandler",
        "is_complete_handler": "isCompleteHandler",
        "log_retention": "logRetention",
        "query_interval": "queryInterval",
        "security_groups": "securityGroups",
        "total_timeout": "totalTimeout",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class ProviderProps:
    def __init__(
        self,
        *,
        on_event_handler: _IFunction_6e14f09e,
        is_complete_handler: typing.Optional[_IFunction_6e14f09e] = None,
        log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        query_interval: typing.Optional[_Duration_070aa057] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        total_timeout: typing.Optional[_Duration_070aa057] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        '''(experimental) Initialization properties for the ``Provider`` construct.

        :param on_event_handler: (experimental) The AWS Lambda function to invoke for all resource lifecycle operations (CREATE/UPDATE/DELETE). This function is responsible to begin the requested resource operation (CREATE/UPDATE/DELETE) and return any additional properties to add to the event, which will later be passed to ``isComplete``. The ``PhysicalResourceId`` property must be included in the response.
        :param is_complete_handler: (experimental) The AWS Lambda function to invoke in order to determine if the operation is complete. This function will be called immediately after ``onEvent`` and then periodically based on the configured query interval as long as it returns ``false``. If the function still returns ``false`` and the alloted timeout has passed, the operation will fail. Default: - provider is synchronous. This means that the ``onEvent`` handler is expected to finish all lifecycle operations within the initial invocation.
        :param log_retention: (experimental) The number of days framework log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param query_interval: (experimental) Time between calls to the ``isComplete`` handler which determines if the resource has been stabilized. The first ``isComplete`` will be called immediately after ``handler`` and then every ``queryInterval`` seconds, and until ``timeout`` has been reached or until ``isComplete`` returns ``true``. Default: Duration.seconds(5)
        :param security_groups: (experimental) Security groups to attach to the provider functions. Only used if 'vpc' is supplied Default: - If ``vpc`` is not supplied, no security groups are attached. Otherwise, a dedicated security group is created for each function.
        :param total_timeout: (experimental) Total timeout for the entire operation. The maximum timeout is 2 hours (yes, it can exceed the AWS Lambda 15 minutes) Default: Duration.minutes(30)
        :param vpc: (experimental) The vpc to provision the lambda functions in. Default: - functions are not provisioned inside a vpc.
        :param vpc_subnets: (experimental) Which subnets from the VPC to place the lambda functions in. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "on_event_handler": on_event_handler,
        }
        if is_complete_handler is not None:
            self._values["is_complete_handler"] = is_complete_handler
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if query_interval is not None:
            self._values["query_interval"] = query_interval
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if total_timeout is not None:
            self._values["total_timeout"] = total_timeout
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def on_event_handler(self) -> _IFunction_6e14f09e:
        '''(experimental) The AWS Lambda function to invoke for all resource lifecycle operations (CREATE/UPDATE/DELETE).

        This function is responsible to begin the requested resource operation
        (CREATE/UPDATE/DELETE) and return any additional properties to add to the
        event, which will later be passed to ``isComplete``. The ``PhysicalResourceId``
        property must be included in the response.

        :stability: experimental
        '''
        result = self._values.get("on_event_handler")
        assert result is not None, "Required property 'on_event_handler' is missing"
        return typing.cast(_IFunction_6e14f09e, result)

    @builtins.property
    def is_complete_handler(self) -> typing.Optional[_IFunction_6e14f09e]:
        '''(experimental) The AWS Lambda function to invoke in order to determine if the operation is complete.

        This function will be called immediately after ``onEvent`` and then
        periodically based on the configured query interval as long as it returns
        ``false``. If the function still returns ``false`` and the alloted timeout has
        passed, the operation will fail.

        :default:

        - provider is synchronous. This means that the ``onEvent`` handler
        is expected to finish all lifecycle operations within the initial invocation.

        :stability: experimental
        '''
        result = self._values.get("is_complete_handler")
        return typing.cast(typing.Optional[_IFunction_6e14f09e], result)

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_6c560d31]:
        '''(experimental) The number of days framework log events are kept in CloudWatch Logs.

        When
        updating this property, unsetting it doesn't remove the log retention policy.
        To remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.INFINITE

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_RetentionDays_6c560d31], result)

    @builtins.property
    def query_interval(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Time between calls to the ``isComplete`` handler which determines if the resource has been stabilized.

        The first ``isComplete`` will be called immediately after ``handler`` and then
        every ``queryInterval`` seconds, and until ``timeout`` has been reached or until
        ``isComplete`` returns ``true``.

        :default: Duration.seconds(5)

        :stability: experimental
        '''
        result = self._values.get("query_interval")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) Security groups to attach to the provider functions.

        Only used if 'vpc' is supplied

        :default:

        - If ``vpc`` is not supplied, no security groups are attached. Otherwise, a dedicated security
        group is created for each function.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], result)

    @builtins.property
    def total_timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Total timeout for the entire operation.

        The maximum timeout is 2 hours (yes, it can exceed the AWS Lambda 15 minutes)

        :default: Duration.minutes(30)

        :stability: experimental
        '''
        result = self._values.get("total_timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The vpc to provision the lambda functions in.

        :default: - functions are not provisioned inside a vpc.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets from the VPC to place the lambda functions in.

        Only used if 'vpc' is supplied. Note: internet access for Lambdas
        requires a NAT gateway, so picking Public subnets is not allowed.

        :default: - the Vpc default strategy if not specified

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.custom_resources.SdkCallsPolicyOptions",
    jsii_struct_bases=[],
    name_mapping={"resources": "resources"},
)
class SdkCallsPolicyOptions:
    def __init__(self, *, resources: typing.List[builtins.str]) -> None:
        '''(experimental) Options for the auto-generation of policies based on the configured SDK calls.

        :param resources: (experimental) The resources that the calls will have access to. It is best to use specific resource ARN's when possible. However, you can also use ``AwsCustomResourcePolicy.ANY_RESOURCE`` to allow access to all resources. For example, when ``onCreate`` is used to create a resource which you don't know the physical name of in advance. Note that will apply to ALL SDK calls.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "resources": resources,
        }

    @builtins.property
    def resources(self) -> typing.List[builtins.str]:
        '''(experimental) The resources that the calls will have access to.

        It is best to use specific resource ARN's when possible. However, you can also use ``AwsCustomResourcePolicy.ANY_RESOURCE``
        to allow access to all resources. For example, when ``onCreate`` is used to create a resource which you don't
        know the physical name of in advance.

        Note that will apply to ALL SDK calls.

        :stability: experimental
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SdkCallsPolicyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsCustomResource",
    "AwsCustomResourcePolicy",
    "AwsCustomResourceProps",
    "AwsSdkCall",
    "PhysicalResourceId",
    "PhysicalResourceIdReference",
    "Provider",
    "ProviderProps",
    "SdkCallsPolicyOptions",
]

publication.publish()
