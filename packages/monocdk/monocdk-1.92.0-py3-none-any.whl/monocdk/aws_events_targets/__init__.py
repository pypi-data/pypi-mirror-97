import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from ..aws_batch import (
    IJobDefinition as _IJobDefinition_62e31f75, IJobQueue as _IJobQueue_1a4ac619
)
from ..aws_codebuild import IProject as _IProject_6da8803e
from ..aws_codepipeline import IPipeline as _IPipeline_1647b414
from ..aws_ec2 import (
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_ecs import (
    FargatePlatformVersion as _FargatePlatformVersion_8169c79a,
    ICluster as _ICluster_42c4ec1a,
    ITaskDefinition as _ITaskDefinition_ee0d1862,
)
from ..aws_events import (
    IEventBus as _IEventBus_2ca38c95,
    IRule as _IRule_af97620d,
    IRuleTarget as _IRuleTarget_d45ec729,
    RuleTargetConfig as _RuleTargetConfig_8b3a5e58,
    RuleTargetInput as _RuleTargetInput_d925a0d7,
)
from ..aws_iam import (
    IRole as _IRole_59af6f50, PolicyStatement as _PolicyStatement_296fe8a3
)
from ..aws_kinesis import IStream as _IStream_14c6ec7f
from ..aws_kinesisfirehose import CfnDeliveryStream as _CfnDeliveryStream_9c3c087d
from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_logs import ILogGroup as _ILogGroup_846e17a0
from ..aws_sns import ITopic as _ITopic_465e36b9
from ..aws_sqs import IQueue as _IQueue_45a01ab4
from ..aws_stepfunctions import IStateMachine as _IStateMachine_269a89c4


@jsii.implements(_IRuleTarget_d45ec729)
class AwsApi(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_events_targets.AwsApi"):
    '''(experimental) Use an AWS Lambda function that makes API calls as an event rule target.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        policy_statement: typing.Optional[_PolicyStatement_296fe8a3] = None,
        action: builtins.str,
        service: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        catch_error_pattern: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
    ) -> None:
        '''
        :param policy_statement: (experimental) The IAM policy statement to allow the API call. Use only if resource restriction is needed. Default: - extract the permission from the API call
        :param action: (experimental) The service action to call.
        :param service: (experimental) The service to call.
        :param api_version: (experimental) API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: (experimental) The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: (experimental) The parameters for the service action. Default: - no parameters

        :stability: experimental
        '''
        props = AwsApiProps(
            policy_statement=policy_statement,
            action=action,
            service=service,
            api_version=api_version,
            catch_error_pattern=catch_error_pattern,
            parameters=parameters,
        )

        jsii.create(AwsApi, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _IRule_af97620d,
        id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Returns a RuleTarget that can be used to trigger this AwsApi as a result from an EventBridge event.

        :param rule: -
        :param id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [rule, id]))


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.AwsApiInput",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "service": "service",
        "api_version": "apiVersion",
        "catch_error_pattern": "catchErrorPattern",
        "parameters": "parameters",
    },
)
class AwsApiInput:
    def __init__(
        self,
        *,
        action: builtins.str,
        service: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        catch_error_pattern: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
    ) -> None:
        '''(experimental) Rule target input for an AwsApi target.

        :param action: (experimental) The service action to call.
        :param service: (experimental) The service to call.
        :param api_version: (experimental) API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: (experimental) The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: (experimental) The parameters for the service action. Default: - no parameters

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "service": service,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if catch_error_pattern is not None:
            self._values["catch_error_pattern"] = catch_error_pattern
        if parameters is not None:
            self._values["parameters"] = parameters

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
    def catch_error_pattern(self) -> typing.Optional[builtins.str]:
        '''(experimental) The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        :default: - do not catch errors

        :stability: experimental
        '''
        result = self._values.get("catch_error_pattern")
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

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.AwsApiProps",
    jsii_struct_bases=[AwsApiInput],
    name_mapping={
        "action": "action",
        "service": "service",
        "api_version": "apiVersion",
        "catch_error_pattern": "catchErrorPattern",
        "parameters": "parameters",
        "policy_statement": "policyStatement",
    },
)
class AwsApiProps(AwsApiInput):
    def __init__(
        self,
        *,
        action: builtins.str,
        service: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        catch_error_pattern: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
        policy_statement: typing.Optional[_PolicyStatement_296fe8a3] = None,
    ) -> None:
        '''(experimental) Properties for an AwsApi target.

        :param action: (experimental) The service action to call.
        :param service: (experimental) The service to call.
        :param api_version: (experimental) API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: (experimental) The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: (experimental) The parameters for the service action. Default: - no parameters
        :param policy_statement: (experimental) The IAM policy statement to allow the API call. Use only if resource restriction is needed. Default: - extract the permission from the API call

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "service": service,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if catch_error_pattern is not None:
            self._values["catch_error_pattern"] = catch_error_pattern
        if parameters is not None:
            self._values["parameters"] = parameters
        if policy_statement is not None:
            self._values["policy_statement"] = policy_statement

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
    def catch_error_pattern(self) -> typing.Optional[builtins.str]:
        '''(experimental) The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        :default: - do not catch errors

        :stability: experimental
        '''
        result = self._values.get("catch_error_pattern")
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
    def policy_statement(self) -> typing.Optional[_PolicyStatement_296fe8a3]:
        '''(experimental) The IAM policy statement to allow the API call.

        Use only if
        resource restriction is needed.

        :default: - extract the permission from the API call

        :stability: experimental
        '''
        result = self._values.get("policy_statement")
        return typing.cast(typing.Optional[_PolicyStatement_296fe8a3], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_d45ec729)
class BatchJob(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events_targets.BatchJob",
):
    '''(experimental) Use an AWS Batch Job / Queue as an event rule target.

    :stability: experimental
    '''

    def __init__(
        self,
        job_queue: _IJobQueue_1a4ac619,
        job_definition: _IJobDefinition_62e31f75,
        *,
        attempts: typing.Optional[jsii.Number] = None,
        event: typing.Optional[_RuleTargetInput_d925a0d7] = None,
        job_name: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param job_queue: -
        :param job_definition: -
        :param attempts: (experimental) The number of times to attempt to retry, if the job fails. Valid values are 1–10. Default: no retryStrategy is set
        :param event: (experimental) The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        :param job_name: (experimental) The name of the submitted job. Default: - Automatically generated
        :param size: (experimental) The size of the array, if this is an array batch job. Valid values are integers between 2 and 10,000. Default: no arrayProperties are set

        :stability: experimental
        '''
        props = BatchJobProps(
            attempts=attempts, event=event, job_name=job_name, size=size
        )

        jsii.create(BatchJob, self, [job_queue, job_definition, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _IRule_af97620d,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Returns a RuleTarget that can be used to trigger queue this batch job as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [rule, _id]))


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.BatchJobProps",
    jsii_struct_bases=[],
    name_mapping={
        "attempts": "attempts",
        "event": "event",
        "job_name": "jobName",
        "size": "size",
    },
)
class BatchJobProps:
    def __init__(
        self,
        *,
        attempts: typing.Optional[jsii.Number] = None,
        event: typing.Optional[_RuleTargetInput_d925a0d7] = None,
        job_name: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Customize the Batch Job Event Target.

        :param attempts: (experimental) The number of times to attempt to retry, if the job fails. Valid values are 1–10. Default: no retryStrategy is set
        :param event: (experimental) The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        :param job_name: (experimental) The name of the submitted job. Default: - Automatically generated
        :param size: (experimental) The size of the array, if this is an array batch job. Valid values are integers between 2 and 10,000. Default: no arrayProperties are set

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if attempts is not None:
            self._values["attempts"] = attempts
        if event is not None:
            self._values["event"] = event
        if job_name is not None:
            self._values["job_name"] = job_name
        if size is not None:
            self._values["size"] = size

    @builtins.property
    def attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of times to attempt to retry, if the job fails.

        Valid values are 1–10.

        :default: no retryStrategy is set

        :stability: experimental
        '''
        result = self._values.get("attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def event(self) -> typing.Optional[_RuleTargetInput_d925a0d7]:
        '''(experimental) The event to send to the Lambda.

        This will be the payload sent to the Lambda Function.

        :default: the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[_RuleTargetInput_d925a0d7], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the submitted job.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the array, if this is an array batch job.

        Valid values are integers between 2 and 10,000.

        :default: no arrayProperties are set

        :stability: experimental
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_d45ec729)
class CloudWatchLogGroup(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events_targets.CloudWatchLogGroup",
):
    '''(experimental) Use an AWS CloudWatch LogGroup as an event rule target.

    :stability: experimental
    '''

    def __init__(
        self,
        log_group: _ILogGroup_846e17a0,
        *,
        event: typing.Optional[_RuleTargetInput_d925a0d7] = None,
    ) -> None:
        '''
        :param log_group: -
        :param event: (experimental) The event to send to the CloudWatch LogGroup. This will be the event logged into the CloudWatch LogGroup Default: - the entire EventBridge event

        :stability: experimental
        '''
        props = LogGroupProps(event=event)

        jsii.create(CloudWatchLogGroup, self, [log_group, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af97620d,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Returns a RuleTarget that can be used to log an event into a CloudWatch LogGroup.

        :param _rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [_rule, _id]))


@jsii.implements(_IRuleTarget_d45ec729)
class CodeBuildProject(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events_targets.CodeBuildProject",
):
    '''(experimental) Start a CodeBuild build when an Amazon EventBridge rule is triggered.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _IProject_6da8803e,
        *,
        event: typing.Optional[_RuleTargetInput_d925a0d7] = None,
        event_role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param project: -
        :param event: (experimental) The event to send to CodeBuild. This will be the payload for the StartBuild API. Default: - the entire EventBridge event
        :param event_role: (experimental) The role to assume before invoking the target (i.e., the codebuild) when the given rule is triggered. Default: - a new role will be created

        :stability: experimental
        '''
        props = CodeBuildProjectProps(event=event, event_role=event_role)

        jsii.create(CodeBuildProject, self, [project, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af97620d,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Allows using build projects as event rule targets.

        :param _rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [_rule, _id]))


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.CodeBuildProjectProps",
    jsii_struct_bases=[],
    name_mapping={"event": "event", "event_role": "eventRole"},
)
class CodeBuildProjectProps:
    def __init__(
        self,
        *,
        event: typing.Optional[_RuleTargetInput_d925a0d7] = None,
        event_role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) Customize the CodeBuild Event Target.

        :param event: (experimental) The event to send to CodeBuild. This will be the payload for the StartBuild API. Default: - the entire EventBridge event
        :param event_role: (experimental) The role to assume before invoking the target (i.e., the codebuild) when the given rule is triggered. Default: - a new role will be created

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if event is not None:
            self._values["event"] = event
        if event_role is not None:
            self._values["event_role"] = event_role

    @builtins.property
    def event(self) -> typing.Optional[_RuleTargetInput_d925a0d7]:
        '''(experimental) The event to send to CodeBuild.

        This will be the payload for the StartBuild API.

        :default: - the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[_RuleTargetInput_d925a0d7], result)

    @builtins.property
    def event_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The role to assume before invoking the target (i.e., the codebuild) when the given rule is triggered.

        :default: - a new role will be created

        :stability: experimental
        '''
        result = self._values.get("event_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeBuildProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_d45ec729)
class CodePipeline(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events_targets.CodePipeline",
):
    '''(experimental) Allows the pipeline to be used as an EventBridge rule target.

    :stability: experimental
    '''

    def __init__(
        self,
        pipeline: _IPipeline_1647b414,
        *,
        event_role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param pipeline: -
        :param event_role: (experimental) The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered. Default: - a new role will be created

        :stability: experimental
        '''
        options = CodePipelineTargetOptions(event_role=event_role)

        jsii.create(CodePipeline, self, [pipeline, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af97620d,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param _rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [_rule, _id]))


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.CodePipelineTargetOptions",
    jsii_struct_bases=[],
    name_mapping={"event_role": "eventRole"},
)
class CodePipelineTargetOptions:
    def __init__(self, *, event_role: typing.Optional[_IRole_59af6f50] = None) -> None:
        '''(experimental) Customization options when creating a {@link CodePipeline} event target.

        :param event_role: (experimental) The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered. Default: - a new role will be created

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if event_role is not None:
            self._values["event_role"] = event_role

    @builtins.property
    def event_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered.

        :default: - a new role will be created

        :stability: experimental
        '''
        result = self._values.get("event_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodePipelineTargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.ContainerOverride",
    jsii_struct_bases=[],
    name_mapping={
        "container_name": "containerName",
        "command": "command",
        "cpu": "cpu",
        "environment": "environment",
        "memory_limit": "memoryLimit",
        "memory_reservation": "memoryReservation",
    },
)
class ContainerOverride:
    def __init__(
        self,
        *,
        container_name: builtins.str,
        command: typing.Optional[typing.List[builtins.str]] = None,
        cpu: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.List["TaskEnvironmentVariable"]] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        memory_reservation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param container_name: (experimental) Name of the container inside the task definition.
        :param command: (experimental) Command to run inside the container. Default: Default command
        :param cpu: (experimental) The number of cpu units reserved for the container. Default: The default value from the task definition.
        :param environment: (experimental) Variables to set in the container's environment.
        :param memory_limit: (experimental) Hard memory limit on the container. Default: The default value from the task definition.
        :param memory_reservation: (experimental) Soft memory limit on the container. Default: The default value from the task definition.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "container_name": container_name,
        }
        if command is not None:
            self._values["command"] = command
        if cpu is not None:
            self._values["cpu"] = cpu
        if environment is not None:
            self._values["environment"] = environment
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit
        if memory_reservation is not None:
            self._values["memory_reservation"] = memory_reservation

    @builtins.property
    def container_name(self) -> builtins.str:
        '''(experimental) Name of the container inside the task definition.

        :stability: experimental
        '''
        result = self._values.get("container_name")
        assert result is not None, "Required property 'container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Command to run inside the container.

        :default: Default command

        :stability: experimental
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of cpu units reserved for the container.

        :default: The default value from the task definition.

        :stability: experimental
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(self) -> typing.Optional[typing.List["TaskEnvironmentVariable"]]:
        '''(experimental) Variables to set in the container's environment.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.List["TaskEnvironmentVariable"]], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Hard memory limit on the container.

        :default: The default value from the task definition.

        :stability: experimental
        '''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Soft memory limit on the container.

        :default: The default value from the task definition.

        :stability: experimental
        '''
        result = self._values.get("memory_reservation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_d45ec729)
class EcsTask(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_events_targets.EcsTask"):
    '''(experimental) Start a task on an ECS cluster.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        cluster: _ICluster_42c4ec1a,
        task_definition: _ITaskDefinition_ee0d1862,
        container_overrides: typing.Optional[typing.List[ContainerOverride]] = None,
        platform_version: typing.Optional[_FargatePlatformVersion_8169c79a] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        task_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cluster: (experimental) Cluster where service will be deployed.
        :param task_definition: (experimental) Task Definition of the task that should be started.
        :param container_overrides: (experimental) Container setting overrides. Key is the name of the container to override, value is the values you want to override.
        :param platform_version: (experimental) The platform version on which to run your task. Unless you have specific compatibility requirements, you don't need to specify this. Default: - ECS will set the Fargate platform version to 'LATEST'
        :param role: (experimental) Existing IAM role to run the ECS task. Default: A new IAM role is created
        :param security_group: (deprecated) Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param security_groups: (experimental) Existing security groups to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnet_selection: (experimental) In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param task_count: (experimental) How many tasks should be started when this event is triggered. Default: 1

        :stability: experimental
        '''
        props = EcsTaskProps(
            cluster=cluster,
            task_definition=task_definition,
            container_overrides=container_overrides,
            platform_version=platform_version,
            role=role,
            security_group=security_group,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            task_count=task_count,
        )

        jsii.create(EcsTask, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af97620d,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Allows using tasks as target of EventBridge events.

        :param _rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [_rule, _id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> typing.Optional[_ISecurityGroup_cdbba9d3]:
        '''(deprecated) The security group associated with the task.

        Only applicable with awsvpc network mode.

        :default: - A new security group is created.

        :deprecated: use securityGroups instead.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[_ISecurityGroup_cdbba9d3], jsii.get(self, "securityGroup"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) The security groups associated with the task.

        Only applicable with awsvpc network mode.

        :default: - A new security group is created.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], jsii.get(self, "securityGroups"))


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.EcsTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "task_definition": "taskDefinition",
        "container_overrides": "containerOverrides",
        "platform_version": "platformVersion",
        "role": "role",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "task_count": "taskCount",
    },
)
class EcsTaskProps:
    def __init__(
        self,
        *,
        cluster: _ICluster_42c4ec1a,
        task_definition: _ITaskDefinition_ee0d1862,
        container_overrides: typing.Optional[typing.List[ContainerOverride]] = None,
        platform_version: typing.Optional[_FargatePlatformVersion_8169c79a] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        task_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties to define an ECS Event Task.

        :param cluster: (experimental) Cluster where service will be deployed.
        :param task_definition: (experimental) Task Definition of the task that should be started.
        :param container_overrides: (experimental) Container setting overrides. Key is the name of the container to override, value is the values you want to override.
        :param platform_version: (experimental) The platform version on which to run your task. Unless you have specific compatibility requirements, you don't need to specify this. Default: - ECS will set the Fargate platform version to 'LATEST'
        :param role: (experimental) Existing IAM role to run the ECS task. Default: A new IAM role is created
        :param security_group: (deprecated) Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param security_groups: (experimental) Existing security groups to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnet_selection: (experimental) In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param task_count: (experimental) How many tasks should be started when this event is triggered. Default: 1

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "task_definition": task_definition,
        }
        if container_overrides is not None:
            self._values["container_overrides"] = container_overrides
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if task_count is not None:
            self._values["task_count"] = task_count

    @builtins.property
    def cluster(self) -> _ICluster_42c4ec1a:
        '''(experimental) Cluster where service will be deployed.

        :stability: experimental
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(_ICluster_42c4ec1a, result)

    @builtins.property
    def task_definition(self) -> _ITaskDefinition_ee0d1862:
        '''(experimental) Task Definition of the task that should be started.

        :stability: experimental
        '''
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast(_ITaskDefinition_ee0d1862, result)

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List[ContainerOverride]]:
        '''(experimental) Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.

        :stability: experimental
        '''
        result = self._values.get("container_overrides")
        return typing.cast(typing.Optional[typing.List[ContainerOverride]], result)

    @builtins.property
    def platform_version(self) -> typing.Optional[_FargatePlatformVersion_8169c79a]:
        '''(experimental) The platform version on which to run your task.

        Unless you have specific compatibility requirements, you don't need to specify this.

        :default: - ECS will set the Fargate platform version to 'LATEST'

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html
        :stability: experimental
        '''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[_FargatePlatformVersion_8169c79a], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Existing IAM role to run the ECS task.

        :default: A new IAM role is created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_cdbba9d3]:
        '''(deprecated) Existing security group to use for the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: A new security group is created

        :deprecated: use securityGroups instead

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_ISecurityGroup_cdbba9d3], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) Existing security groups to use for the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: A new security group is created

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) In what subnets to place the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: Private subnets

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def task_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) How many tasks should be started when this event is triggered.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_d45ec729)
class EventBus(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events_targets.EventBus",
):
    '''(experimental) Notify an existing Event Bus of an event.

    :stability: experimental
    '''

    def __init__(
        self,
        event_bus: _IEventBus_2ca38c95,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param event_bus: -
        :param role: (experimental) Role to be used to publish the event. Default: a new role is created.

        :stability: experimental
        '''
        props = EventBusProps(role=role)

        jsii.create(EventBus, self, [event_bus, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _IRule_af97620d,
        id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param rule: -
        :param id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [rule, id]))


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.EventBusProps",
    jsii_struct_bases=[],
    name_mapping={"role": "role"},
)
class EventBusProps:
    def __init__(self, *, role: typing.Optional[_IRole_59af6f50] = None) -> None:
        '''(experimental) Configuration properties of an Event Bus event.

        :param role: (experimental) Role to be used to publish the event. Default: a new role is created.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Role to be used to publish the event.

        :default: a new role is created.

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventBusProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_d45ec729)
class KinesisFirehoseStream(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events_targets.KinesisFirehoseStream",
):
    '''(experimental) Customize the Firehose Stream Event Target.

    :stability: experimental
    '''

    def __init__(
        self,
        stream: _CfnDeliveryStream_9c3c087d,
        *,
        message: typing.Optional[_RuleTargetInput_d925a0d7] = None,
    ) -> None:
        '''
        :param stream: -
        :param message: (experimental) The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire Event Bridge event

        :stability: experimental
        '''
        props = KinesisFirehoseStreamProps(message=message)

        jsii.create(KinesisFirehoseStream, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af97620d,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Returns a RuleTarget that can be used to trigger this Firehose Stream as a result from a Event Bridge event.

        :param _rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [_rule, _id]))


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.KinesisFirehoseStreamProps",
    jsii_struct_bases=[],
    name_mapping={"message": "message"},
)
class KinesisFirehoseStreamProps:
    def __init__(
        self,
        *,
        message: typing.Optional[_RuleTargetInput_d925a0d7] = None,
    ) -> None:
        '''(experimental) Customize the Firehose Stream Event Target.

        :param message: (experimental) The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire Event Bridge event

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def message(self) -> typing.Optional[_RuleTargetInput_d925a0d7]:
        '''(experimental) The message to send to the stream.

        Must be a valid JSON text passed to the target stream.

        :default: - the entire Event Bridge event

        :stability: experimental
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[_RuleTargetInput_d925a0d7], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_d45ec729)
class KinesisStream(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events_targets.KinesisStream",
):
    '''(experimental) Use a Kinesis Stream as a target for AWS CloudWatch event rules.

    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # put to a Kinesis stream every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.KinesisStream(stream))
    '''

    def __init__(
        self,
        stream: _IStream_14c6ec7f,
        *,
        message: typing.Optional[_RuleTargetInput_d925a0d7] = None,
        partition_key_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param stream: -
        :param message: (experimental) The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire CloudWatch event
        :param partition_key_path: (experimental) Partition Key Path for records sent to this stream. Default: - eventId as the partition key

        :stability: experimental
        '''
        props = KinesisStreamProps(
            message=message, partition_key_path=partition_key_path
        )

        jsii.create(KinesisStream, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af97620d,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Returns a RuleTarget that can be used to trigger this Kinesis Stream as a result from a CloudWatch event.

        :param _rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [_rule, _id]))


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.KinesisStreamProps",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "partition_key_path": "partitionKeyPath"},
)
class KinesisStreamProps:
    def __init__(
        self,
        *,
        message: typing.Optional[_RuleTargetInput_d925a0d7] = None,
        partition_key_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Customize the Kinesis Stream Event Target.

        :param message: (experimental) The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire CloudWatch event
        :param partition_key_path: (experimental) Partition Key Path for records sent to this stream. Default: - eventId as the partition key

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if partition_key_path is not None:
            self._values["partition_key_path"] = partition_key_path

    @builtins.property
    def message(self) -> typing.Optional[_RuleTargetInput_d925a0d7]:
        '''(experimental) The message to send to the stream.

        Must be a valid JSON text passed to the target stream.

        :default: - the entire CloudWatch event

        :stability: experimental
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[_RuleTargetInput_d925a0d7], result)

    @builtins.property
    def partition_key_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Partition Key Path for records sent to this stream.

        :default: - eventId as the partition key

        :stability: experimental
        '''
        result = self._values.get("partition_key_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_d45ec729)
class LambdaFunction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events_targets.LambdaFunction",
):
    '''(experimental) Use an AWS Lambda function as an event rule target.

    :stability: experimental
    '''

    def __init__(
        self,
        handler: _IFunction_6e14f09e,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        event: typing.Optional[_RuleTargetInput_d925a0d7] = None,
    ) -> None:
        '''
        :param handler: -
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param event: (experimental) The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event

        :stability: experimental
        '''
        props = LambdaFunctionProps(dead_letter_queue=dead_letter_queue, event=event)

        jsii.create(LambdaFunction, self, [handler, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _IRule_af97620d,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Returns a RuleTarget that can be used to trigger this Lambda as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [rule, _id]))


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.LambdaFunctionProps",
    jsii_struct_bases=[],
    name_mapping={"dead_letter_queue": "deadLetterQueue", "event": "event"},
)
class LambdaFunctionProps:
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        event: typing.Optional[_RuleTargetInput_d925a0d7] = None,
    ) -> None:
        '''(experimental) Customize the Lambda Event Target.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param event: (experimental) The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if event is not None:
            self._values["event"] = event

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def event(self) -> typing.Optional[_RuleTargetInput_d925a0d7]:
        '''(experimental) The event to send to the Lambda.

        This will be the payload sent to the Lambda Function.

        :default: the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[_RuleTargetInput_d925a0d7], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.LogGroupProps",
    jsii_struct_bases=[],
    name_mapping={"event": "event"},
)
class LogGroupProps:
    def __init__(
        self,
        *,
        event: typing.Optional[_RuleTargetInput_d925a0d7] = None,
    ) -> None:
        '''(experimental) Customize the CloudWatch LogGroup Event Target.

        :param event: (experimental) The event to send to the CloudWatch LogGroup. This will be the event logged into the CloudWatch LogGroup Default: - the entire EventBridge event

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if event is not None:
            self._values["event"] = event

    @builtins.property
    def event(self) -> typing.Optional[_RuleTargetInput_d925a0d7]:
        '''(experimental) The event to send to the CloudWatch LogGroup.

        This will be the event logged into the CloudWatch LogGroup

        :default: - the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[_RuleTargetInput_d925a0d7], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_d45ec729)
class SfnStateMachine(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events_targets.SfnStateMachine",
):
    '''(experimental) Use a StepFunctions state machine as a target for Amazon EventBridge rules.

    :stability: experimental
    '''

    def __init__(
        self,
        machine: _IStateMachine_269a89c4,
        *,
        input: typing.Optional[_RuleTargetInput_d925a0d7] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param machine: -
        :param input: (experimental) The input to the state machine execution. Default: the entire EventBridge event
        :param role: (experimental) The IAM role to be assumed to execute the State Machine. Default: - a new role will be created

        :stability: experimental
        '''
        props = SfnStateMachineProps(input=input, role=role)

        jsii.create(SfnStateMachine, self, [machine, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af97620d,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Returns a properties that are used in an Rule to trigger this State Machine.

        :param _rule: -
        :param _id: -

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sns-permissions
        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [_rule, _id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="machine")
    def machine(self) -> _IStateMachine_269a89c4:
        '''
        :stability: experimental
        '''
        return typing.cast(_IStateMachine_269a89c4, jsii.get(self, "machine"))


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.SfnStateMachineProps",
    jsii_struct_bases=[],
    name_mapping={"input": "input", "role": "role"},
)
class SfnStateMachineProps:
    def __init__(
        self,
        *,
        input: typing.Optional[_RuleTargetInput_d925a0d7] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) Customize the Step Functions State Machine target.

        :param input: (experimental) The input to the state machine execution. Default: the entire EventBridge event
        :param role: (experimental) The IAM role to be assumed to execute the State Machine. Default: - a new role will be created

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if input is not None:
            self._values["input"] = input
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def input(self) -> typing.Optional[_RuleTargetInput_d925a0d7]:
        '''(experimental) The input to the state machine execution.

        :default: the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_RuleTargetInput_d925a0d7], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role to be assumed to execute the State Machine.

        :default: - a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SfnStateMachineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_d45ec729)
class SnsTopic(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events_targets.SnsTopic",
):
    '''(experimental) Use an SNS topic as a target for Amazon EventBridge rules.

    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # publish to an SNS topic every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.SnsTopic(topic))
    '''

    def __init__(
        self,
        topic: _ITopic_465e36b9,
        *,
        message: typing.Optional[_RuleTargetInput_d925a0d7] = None,
    ) -> None:
        '''
        :param topic: -
        :param message: (experimental) The message to send to the topic. Default: the entire EventBridge event

        :stability: experimental
        '''
        props = SnsTopicProps(message=message)

        jsii.create(SnsTopic, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af97620d,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Returns a RuleTarget that can be used to trigger this SNS topic as a result from an EventBridge event.

        :param _rule: -
        :param _id: -

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sns-permissions
        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [_rule, _id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="topic")
    def topic(self) -> _ITopic_465e36b9:
        '''
        :stability: experimental
        '''
        return typing.cast(_ITopic_465e36b9, jsii.get(self, "topic"))


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.SnsTopicProps",
    jsii_struct_bases=[],
    name_mapping={"message": "message"},
)
class SnsTopicProps:
    def __init__(
        self,
        *,
        message: typing.Optional[_RuleTargetInput_d925a0d7] = None,
    ) -> None:
        '''(experimental) Customize the SNS Topic Event Target.

        :param message: (experimental) The message to send to the topic. Default: the entire EventBridge event

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def message(self) -> typing.Optional[_RuleTargetInput_d925a0d7]:
        '''(experimental) The message to send to the topic.

        :default: the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[_RuleTargetInput_d925a0d7], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsTopicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_d45ec729)
class SqsQueue(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_events_targets.SqsQueue",
):
    '''(experimental) Use an SQS Queue as a target for Amazon EventBridge rules.

    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # publish to an SQS queue every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.SqsQueue(queue))
    '''

    def __init__(
        self,
        queue: _IQueue_45a01ab4,
        *,
        message: typing.Optional[_RuleTargetInput_d925a0d7] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param queue: -
        :param message: (experimental) The message to send to the queue. Must be a valid JSON text passed to the target queue. Default: the entire EventBridge event
        :param message_group_id: (experimental) Message Group ID for messages sent to this queue. Required for FIFO queues, leave empty for regular queues. Default: - no message group ID (regular queue)

        :stability: experimental
        '''
        props = SqsQueueProps(message=message, message_group_id=message_group_id)

        jsii.create(SqsQueue, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _IRule_af97620d,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_8b3a5e58:
        '''(experimental) Returns a RuleTarget that can be used to trigger this SQS queue as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sqs-permissions
        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_8b3a5e58, jsii.invoke(self, "bind", [rule, _id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="queue")
    def queue(self) -> _IQueue_45a01ab4:
        '''
        :stability: experimental
        '''
        return typing.cast(_IQueue_45a01ab4, jsii.get(self, "queue"))


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.SqsQueueProps",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "message_group_id": "messageGroupId"},
)
class SqsQueueProps:
    def __init__(
        self,
        *,
        message: typing.Optional[_RuleTargetInput_d925a0d7] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Customize the SQS Queue Event Target.

        :param message: (experimental) The message to send to the queue. Must be a valid JSON text passed to the target queue. Default: the entire EventBridge event
        :param message_group_id: (experimental) Message Group ID for messages sent to this queue. Required for FIFO queues, leave empty for regular queues. Default: - no message group ID (regular queue)

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if message_group_id is not None:
            self._values["message_group_id"] = message_group_id

    @builtins.property
    def message(self) -> typing.Optional[_RuleTargetInput_d925a0d7]:
        '''(experimental) The message to send to the queue.

        Must be a valid JSON text passed to the target queue.

        :default: the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[_RuleTargetInput_d925a0d7], result)

    @builtins.property
    def message_group_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Message Group ID for messages sent to this queue.

        Required for FIFO queues, leave empty for regular queues.

        :default: - no message group ID (regular queue)

        :stability: experimental
        '''
        result = self._values.get("message_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_events_targets.TaskEnvironmentVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class TaskEnvironmentVariable:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) An environment variable to be set in the container run as a task.

        :param name: (experimental) Name for the environment variable. Exactly one of ``name`` and ``namePath`` must be specified.
        :param value: (experimental) Value of the environment variable. Exactly one of ``value`` and ``valuePath`` must be specified.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name for the environment variable.

        Exactly one of ``name`` and ``namePath`` must be specified.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) Value of the environment variable.

        Exactly one of ``value`` and ``valuePath`` must be specified.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskEnvironmentVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AwsApi",
    "AwsApiInput",
    "AwsApiProps",
    "BatchJob",
    "BatchJobProps",
    "CloudWatchLogGroup",
    "CodeBuildProject",
    "CodeBuildProjectProps",
    "CodePipeline",
    "CodePipelineTargetOptions",
    "ContainerOverride",
    "EcsTask",
    "EcsTaskProps",
    "EventBus",
    "EventBusProps",
    "KinesisFirehoseStream",
    "KinesisFirehoseStreamProps",
    "KinesisStream",
    "KinesisStreamProps",
    "LambdaFunction",
    "LambdaFunctionProps",
    "LogGroupProps",
    "SfnStateMachine",
    "SfnStateMachineProps",
    "SnsTopic",
    "SnsTopicProps",
    "SqsQueue",
    "SqsQueueProps",
    "TaskEnvironmentVariable",
]

publication.publish()
