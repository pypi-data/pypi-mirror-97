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
    CfnCapabilities as _CfnCapabilities_6e018757,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IConstruct as _IConstruct_5a0f9c5e,
    IResource as _IResource_8c1dbbbd,
    SecretValue as _SecretValue_c18506ef,
)
from ..aws_cloudformation import (
    CloudFormationCapabilities as _CloudFormationCapabilities_149b400e
)
from ..aws_codebuild import (
    BuildEnvironmentVariable as _BuildEnvironmentVariable_00095c97,
    IProject as _IProject_6da8803e,
)
from ..aws_codecommit import IRepository as _IRepository_cdb2a3c0
from ..aws_codedeploy import (
    IEcsDeploymentGroup as _IEcsDeploymentGroup_538bcae2,
    IServerDeploymentGroup as _IServerDeploymentGroup_9bf302e3,
)
from ..aws_codepipeline import (
    ActionArtifactBounds as _ActionArtifactBounds_77337cd6,
    ActionBindOptions as _ActionBindOptions_20e0a317,
    ActionCategory as _ActionCategory_338d31b4,
    ActionConfig as _ActionConfig_0c698b52,
    ActionProperties as _ActionProperties_c7760ac6,
    Artifact as _Artifact_9905eec2,
    ArtifactPath as _ArtifactPath_a5b79113,
    CommonActionProps as _CommonActionProps_4f0e79c2,
    CommonAwsActionProps as _CommonAwsActionProps_1494edc0,
    IAction as _IAction_ecd54a08,
    IStage as _IStage_5a7e7342,
)
from ..aws_ecr import IRepository as _IRepository_8b4d2894
from ..aws_ecs import IBaseService as _IBaseService_f1507c0b
from ..aws_events import (
    EventPattern as _EventPattern_a23fbf37,
    IEventBus as _IEventBus_2ca38c95,
    IRuleTarget as _IRuleTarget_d45ec729,
    Rule as _Rule_6cfff189,
    RuleProps as _RuleProps_32051f01,
    Schedule as _Schedule_297d3fad,
)
from ..aws_iam import (
    IRole as _IRole_59af6f50, PolicyStatement as _PolicyStatement_296fe8a3
)
from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_s3 import (
    BucketAccessControl as _BucketAccessControl_a8cb5bce, IBucket as _IBucket_73486e29
)
from ..aws_sns import ITopic as _ITopic_465e36b9
from ..aws_stepfunctions import IStateMachine as _IStateMachine_269a89c4


@jsii.implements(_IAction_ecd54a08)
class Action(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_codepipeline_actions.Action",
):
    '''(experimental) Low-level class for generic CodePipeline Actions.

    WARNING: this class should not be externally exposed, but is currently visible
    because of a limitation of jsii (https://github.com/aws/jsii/issues/524).

    This class will disappear in a future release and should not be used.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ActionProxy"]:
        return _ActionProxy

    def __init__(
        self,
        *,
        action_name: builtins.str,
        artifact_bounds: _ActionArtifactBounds_77337cd6,
        category: _ActionCategory_338d31b4,
        provider: builtins.str,
        account: typing.Optional[builtins.str] = None,
        inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        outputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        owner: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        resource: typing.Optional[_IResource_8c1dbbbd] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action_name: 
        :param artifact_bounds: 
        :param category: (experimental) The category of the action. The category defines which action type the owner (the entity that performs the action) performs.
        :param provider: (experimental) The service provider that the action calls.
        :param account: (experimental) The account the Action is supposed to live in. For Actions backed by resources, this is inferred from the Stack {@link resource} is part of. However, some Actions, like the CloudFormation ones, are not backed by any resource, and they still might want to be cross-account. In general, a concrete Action class should specify either {@link resource}, or {@link account} - but not both.
        :param inputs: 
        :param outputs: 
        :param owner: 
        :param region: (experimental) The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param resource: (experimental) The optional resource that is backing this Action. This is used for automatically handling Actions backed by resources from a different account and/or region.
        :param role: 
        :param run_order: (experimental) The order in which AWS CodePipeline runs this action. For more information, see the AWS CodePipeline User Guide. https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#action-requirements
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names
        :param version: 

        :stability: experimental
        '''
        action_properties = _ActionProperties_c7760ac6(
            action_name=action_name,
            artifact_bounds=artifact_bounds,
            category=category,
            provider=provider,
            account=account,
            inputs=inputs,
            outputs=outputs,
            owner=owner,
            region=region,
            resource=resource,
            role=role,
            run_order=run_order,
            variables_namespace=variables_namespace,
            version=version,
        )

        jsii.create(Action, self, [action_properties])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''
        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bind", [scope, stage, options]))

    @jsii.member(jsii_name="bound") # type: ignore[misc]
    @abc.abstractmethod
    def _bound(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: builtins.str,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[_IEventBus_2ca38c95] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[_Schedule_297d3fad] = None,
        targets: typing.Optional[typing.List[_IRuleTarget_d45ec729]] = None,
    ) -> _Rule_6cfff189:
        '''
        :param name: -
        :param target: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description.
        :param enabled: (experimental) Indicates whether the rule is enabled. Default: true
        :param event_bus: (experimental) The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: (experimental) Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: (experimental) A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: (experimental) The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: (experimental) Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        :stability: experimental
        '''
        options = _RuleProps_32051f01(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onStateChange", [name, target, options]))

    @jsii.member(jsii_name="variableExpression")
    def _variable_expression(self, variable_name: builtins.str) -> builtins.str:
        '''
        :param variable_name: -

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "variableExpression", [variable_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_c7760ac6:
        '''
        :stability: experimental
        '''
        return typing.cast(_ActionProperties_c7760ac6, jsii.get(self, "actionProperties"))


class _ActionProxy(Action):
    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [scope, stage, options]))


class AlexaSkillDeployAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.AlexaSkillDeployAction",
):
    '''(experimental) Deploys the skill to Alexa.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: _SecretValue_c18506ef,
        input: _Artifact_9905eec2,
        refresh_token: _SecretValue_c18506ef,
        skill_id: builtins.str,
        parameter_overrides_artifact: typing.Optional[_Artifact_9905eec2] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: (experimental) The client id of the developer console token.
        :param client_secret: (experimental) The client secret of the developer console token.
        :param input: (experimental) The source artifact containing the voice model and skill manifest.
        :param refresh_token: (experimental) The refresh token of the developer console token.
        :param skill_id: (experimental) The Alexa skill id.
        :param parameter_overrides_artifact: (experimental) An optional artifact containing overrides for the skill manifest.
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = AlexaSkillDeployActionProps(
            client_id=client_id,
            client_secret=client_secret,
            input=input,
            refresh_token=refresh_token,
            skill_id=skill_id,
            parameter_overrides_artifact=parameter_overrides_artifact,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(AlexaSkillDeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        _scope: _Construct_e78e779f,
        _stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        _options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [_scope, _stage, _options]))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.AlexaSkillDeployActionProps",
    jsii_struct_bases=[_CommonActionProps_4f0e79c2],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "input": "input",
        "refresh_token": "refreshToken",
        "skill_id": "skillId",
        "parameter_overrides_artifact": "parameterOverridesArtifact",
    },
)
class AlexaSkillDeployActionProps(_CommonActionProps_4f0e79c2):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        client_id: builtins.str,
        client_secret: _SecretValue_c18506ef,
        input: _Artifact_9905eec2,
        refresh_token: _SecretValue_c18506ef,
        skill_id: builtins.str,
        parameter_overrides_artifact: typing.Optional[_Artifact_9905eec2] = None,
    ) -> None:
        '''(experimental) Construction properties of the {@link AlexaSkillDeployAction Alexa deploy Action}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param client_id: (experimental) The client id of the developer console token.
        :param client_secret: (experimental) The client secret of the developer console token.
        :param input: (experimental) The source artifact containing the voice model and skill manifest.
        :param refresh_token: (experimental) The refresh token of the developer console token.
        :param skill_id: (experimental) The Alexa skill id.
        :param parameter_overrides_artifact: (experimental) An optional artifact containing overrides for the skill manifest.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "client_id": client_id,
            "client_secret": client_secret,
            "input": input,
            "refresh_token": refresh_token,
            "skill_id": skill_id,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if parameter_overrides_artifact is not None:
            self._values["parameter_overrides_artifact"] = parameter_overrides_artifact

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''(experimental) The client id of the developer console token.

        :stability: experimental
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> _SecretValue_c18506ef:
        '''(experimental) The client secret of the developer console token.

        :stability: experimental
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(_SecretValue_c18506ef, result)

    @builtins.property
    def input(self) -> _Artifact_9905eec2:
        '''(experimental) The source artifact containing the voice model and skill manifest.

        :stability: experimental
        '''
        result = self._values.get("input")
        assert result is not None, "Required property 'input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def refresh_token(self) -> _SecretValue_c18506ef:
        '''(experimental) The refresh token of the developer console token.

        :stability: experimental
        '''
        result = self._values.get("refresh_token")
        assert result is not None, "Required property 'refresh_token' is missing"
        return typing.cast(_SecretValue_c18506ef, result)

    @builtins.property
    def skill_id(self) -> builtins.str:
        '''(experimental) The Alexa skill id.

        :stability: experimental
        '''
        result = self._values.get("skill_id")
        assert result is not None, "Required property 'skill_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameter_overrides_artifact(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) An optional artifact containing overrides for the skill manifest.

        :stability: experimental
        '''
        result = self._values.get("parameter_overrides_artifact")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlexaSkillDeployActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BitBucketSourceAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.BitBucketSourceAction",
):
    '''(experimental) A CodePipeline source action for BitBucket.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        connection_arn: builtins.str,
        output: _Artifact_9905eec2,
        owner: builtins.str,
        repo: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        code_build_clone_output: typing.Optional[builtins.bool] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection_arn: (experimental) The ARN of the CodeStar Connection created in the AWS console that has permissions to access this BitBucket repository.
        :param output: (experimental) The output artifact that this action produces. Can be used as input for further pipeline actions.
        :param owner: (experimental) The owning user or organization of the repository.
        :param repo: (experimental) The name of the repository.
        :param branch: (experimental) The branch to build. Default: 'master'
        :param code_build_clone_output: (experimental) Whether the output should be the contents of the repository (which is the default), or a link that allows CodeBuild to clone the repository before building. **Note**: if this option is true, then only CodeBuild actions can use the resulting {@link output}. Default: false
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = BitBucketSourceActionProps(
            connection_arn=connection_arn,
            output=output,
            owner=owner,
            repo=repo,
            branch=branch,
            code_build_clone_output=code_build_clone_output,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(BitBucketSourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        _scope: _Construct_e78e779f,
        _stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [_scope, _stage, options]))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.BitBucketSourceActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "connection_arn": "connectionArn",
        "output": "output",
        "owner": "owner",
        "repo": "repo",
        "branch": "branch",
        "code_build_clone_output": "codeBuildCloneOutput",
    },
)
class BitBucketSourceActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        connection_arn: builtins.str,
        output: _Artifact_9905eec2,
        owner: builtins.str,
        repo: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        code_build_clone_output: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Construction properties for {@link BitBucketSourceAction}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param connection_arn: (experimental) The ARN of the CodeStar Connection created in the AWS console that has permissions to access this BitBucket repository.
        :param output: (experimental) The output artifact that this action produces. Can be used as input for further pipeline actions.
        :param owner: (experimental) The owning user or organization of the repository.
        :param repo: (experimental) The name of the repository.
        :param branch: (experimental) The branch to build. Default: 'master'
        :param code_build_clone_output: (experimental) Whether the output should be the contents of the repository (which is the default), or a link that allows CodeBuild to clone the repository before building. **Note**: if this option is true, then only CodeBuild actions can use the resulting {@link output}. Default: false

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "connection_arn": connection_arn,
            "output": output,
            "owner": owner,
            "repo": repo,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if branch is not None:
            self._values["branch"] = branch
        if code_build_clone_output is not None:
            self._values["code_build_clone_output"] = code_build_clone_output

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def connection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the CodeStar Connection created in the AWS console that has permissions to access this BitBucket repository.

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/connections-create.html
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "arn:aws:codestar-connections:us-east-1:123456789012:connection/12345678-abcd-12ab-34cdef5678gh"
        '''
        result = self._values.get("connection_arn")
        assert result is not None, "Required property 'connection_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output(self) -> _Artifact_9905eec2:
        '''(experimental) The output artifact that this action produces.

        Can be used as input for further pipeline actions.

        :stability: experimental
        '''
        result = self._values.get("output")
        assert result is not None, "Required property 'output' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) The owning user or organization of the repository.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "aws"
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo(self) -> builtins.str:
        '''(experimental) The name of the repository.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "aws-cdk"
        '''
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The branch to build.

        :default: 'master'

        :stability: experimental
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_build_clone_output(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the output should be the contents of the repository (which is the default), or a link that allows CodeBuild to clone the repository before building.

        **Note**: if this option is true,
        then only CodeBuild actions can use the resulting {@link output}.

        :default: false

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CodestarConnectionSource.html#action-reference-CodestarConnectionSource-config
        :stability: experimental
        '''
        result = self._values.get("code_build_clone_output")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BitBucketSourceActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CacheControl(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.CacheControl",
):
    '''(experimental) Used for HTTP cache-control header, which influences downstream caches.

    Use the provided static factory methods to construct instances of this class.
    Used in the {@link S3DeployActionProps.cacheControl} property.

    :see: https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.9
    :stability: experimental
    '''

    @jsii.member(jsii_name="fromString") # type: ignore[misc]
    @builtins.classmethod
    def from_string(cls, s: builtins.str) -> "CacheControl":
        '''(experimental) Allows you to create an arbitrary cache control directive, in case our support is missing a method for a particular directive.

        :param s: -

        :stability: experimental
        '''
        return typing.cast("CacheControl", jsii.sinvoke(cls, "fromString", [s]))

    @jsii.member(jsii_name="maxAge") # type: ignore[misc]
    @builtins.classmethod
    def max_age(cls, t: _Duration_070aa057) -> "CacheControl":
        '''(experimental) The 'max-age' cache control directive.

        :param t: -

        :stability: experimental
        '''
        return typing.cast("CacheControl", jsii.sinvoke(cls, "maxAge", [t]))

    @jsii.member(jsii_name="mustRevalidate") # type: ignore[misc]
    @builtins.classmethod
    def must_revalidate(cls) -> "CacheControl":
        '''(experimental) The 'must-revalidate' cache control directive.

        :stability: experimental
        '''
        return typing.cast("CacheControl", jsii.sinvoke(cls, "mustRevalidate", []))

    @jsii.member(jsii_name="noCache") # type: ignore[misc]
    @builtins.classmethod
    def no_cache(cls) -> "CacheControl":
        '''(experimental) The 'no-cache' cache control directive.

        :stability: experimental
        '''
        return typing.cast("CacheControl", jsii.sinvoke(cls, "noCache", []))

    @jsii.member(jsii_name="noTransform") # type: ignore[misc]
    @builtins.classmethod
    def no_transform(cls) -> "CacheControl":
        '''(experimental) The 'no-transform' cache control directive.

        :stability: experimental
        '''
        return typing.cast("CacheControl", jsii.sinvoke(cls, "noTransform", []))

    @jsii.member(jsii_name="proxyRevalidate") # type: ignore[misc]
    @builtins.classmethod
    def proxy_revalidate(cls) -> "CacheControl":
        '''(experimental) The 'proxy-revalidate' cache control directive.

        :stability: experimental
        '''
        return typing.cast("CacheControl", jsii.sinvoke(cls, "proxyRevalidate", []))

    @jsii.member(jsii_name="setPrivate") # type: ignore[misc]
    @builtins.classmethod
    def set_private(cls) -> "CacheControl":
        '''(experimental) The 'private' cache control directive.

        :stability: experimental
        '''
        return typing.cast("CacheControl", jsii.sinvoke(cls, "setPrivate", []))

    @jsii.member(jsii_name="setPublic") # type: ignore[misc]
    @builtins.classmethod
    def set_public(cls) -> "CacheControl":
        '''(experimental) The 'public' cache control directive.

        :stability: experimental
        '''
        return typing.cast("CacheControl", jsii.sinvoke(cls, "setPublic", []))

    @jsii.member(jsii_name="sMaxAge") # type: ignore[misc]
    @builtins.classmethod
    def s_max_age(cls, t: _Duration_070aa057) -> "CacheControl":
        '''(experimental) The 's-max-age' cache control directive.

        :param t: -

        :stability: experimental
        '''
        return typing.cast("CacheControl", jsii.sinvoke(cls, "sMaxAge", [t]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''(experimental) the actual text value of the created directive.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        jsii.set(self, "value", value)


class CloudFormationCreateReplaceChangeSetAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.CloudFormationCreateReplaceChangeSetAction",
):
    '''(experimental) CodePipeline action to prepare a change set.

    Creates the change set if it doesn't exist based on the stack name and template that you submit.
    If the change set exists, AWS CloudFormation deletes it, and then creates a new one.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        admin_permissions: builtins.bool,
        change_set_name: builtins.str,
        stack_name: builtins.str,
        template_path: _ArtifactPath_a5b79113,
        account: typing.Optional[builtins.str] = None,
        capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]] = None,
        cfn_capabilities: typing.Optional[typing.List[_CfnCapabilities_6e018757]] = None,
        deployment_role: typing.Optional[_IRole_59af6f50] = None,
        extra_inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        parameter_overrides: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        region: typing.Optional[builtins.str] = None,
        template_configuration: typing.Optional[_ArtifactPath_a5b79113] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_permissions: (experimental) Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param change_set_name: (experimental) Name of the change set to create or update.
        :param stack_name: (experimental) The name of the stack to apply this action to.
        :param template_path: (experimental) Input artifact with the ChangeSet's CloudFormation template.
        :param account: (experimental) The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: (deprecated) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param cfn_capabilities: (experimental) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement is required that AWS CloudFormation might create or update those resources. For example, you must specify ``ANONYMOUS_IAM`` or ``NAMED_IAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information, see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: (experimental) IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: (experimental) The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have: parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: (experimental) The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: (experimental) A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: (experimental) Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: (experimental) The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param template_configuration: (experimental) Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = CloudFormationCreateReplaceChangeSetActionProps(
            admin_permissions=admin_permissions,
            change_set_name=change_set_name,
            stack_name=stack_name,
            template_path=template_path,
            account=account,
            capabilities=capabilities,
            cfn_capabilities=cfn_capabilities,
            deployment_role=deployment_role,
            extra_inputs=extra_inputs,
            output=output,
            output_file_name=output_file_name,
            parameter_overrides=parameter_overrides,
            region=region,
            template_configuration=template_configuration,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(CloudFormationCreateReplaceChangeSetAction, self, [props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> builtins.bool:
        '''(experimental) Add statement to the service role assumed by CloudFormation while executing this action.

        :param statement: -

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "addToDeploymentRolePolicy", [statement]))

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [scope, stage, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> _IRole_59af6f50:
        '''
        :stability: experimental
        '''
        return typing.cast(_IRole_59af6f50, jsii.get(self, "deploymentRole"))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.CloudFormationCreateReplaceChangeSetActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "admin_permissions": "adminPermissions",
        "change_set_name": "changeSetName",
        "stack_name": "stackName",
        "template_path": "templatePath",
        "account": "account",
        "capabilities": "capabilities",
        "cfn_capabilities": "cfnCapabilities",
        "deployment_role": "deploymentRole",
        "extra_inputs": "extraInputs",
        "output": "output",
        "output_file_name": "outputFileName",
        "parameter_overrides": "parameterOverrides",
        "region": "region",
        "template_configuration": "templateConfiguration",
    },
)
class CloudFormationCreateReplaceChangeSetActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        admin_permissions: builtins.bool,
        change_set_name: builtins.str,
        stack_name: builtins.str,
        template_path: _ArtifactPath_a5b79113,
        account: typing.Optional[builtins.str] = None,
        capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]] = None,
        cfn_capabilities: typing.Optional[typing.List[_CfnCapabilities_6e018757]] = None,
        deployment_role: typing.Optional[_IRole_59af6f50] = None,
        extra_inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        parameter_overrides: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        region: typing.Optional[builtins.str] = None,
        template_configuration: typing.Optional[_ArtifactPath_a5b79113] = None,
    ) -> None:
        '''(experimental) Properties for the CloudFormationCreateReplaceChangeSetAction.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param admin_permissions: (experimental) Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param change_set_name: (experimental) Name of the change set to create or update.
        :param stack_name: (experimental) The name of the stack to apply this action to.
        :param template_path: (experimental) Input artifact with the ChangeSet's CloudFormation template.
        :param account: (experimental) The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: (deprecated) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param cfn_capabilities: (experimental) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement is required that AWS CloudFormation might create or update those resources. For example, you must specify ``ANONYMOUS_IAM`` or ``NAMED_IAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information, see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: (experimental) IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: (experimental) The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have: parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: (experimental) The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: (experimental) A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: (experimental) Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: (experimental) The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param template_configuration: (experimental) Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "admin_permissions": admin_permissions,
            "change_set_name": change_set_name,
            "stack_name": stack_name,
            "template_path": template_path,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if account is not None:
            self._values["account"] = account
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if cfn_capabilities is not None:
            self._values["cfn_capabilities"] = cfn_capabilities
        if deployment_role is not None:
            self._values["deployment_role"] = deployment_role
        if extra_inputs is not None:
            self._values["extra_inputs"] = extra_inputs
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if parameter_overrides is not None:
            self._values["parameter_overrides"] = parameter_overrides
        if region is not None:
            self._values["region"] = region
        if template_configuration is not None:
            self._values["template_configuration"] = template_configuration

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def admin_permissions(self) -> builtins.bool:
        '''(experimental) Whether to grant full permissions to CloudFormation while deploying this template.

        Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you
        don't specify any alternatives.

        The default role that will be created for you will have full (i.e., ``*``)
        permissions on all resources, and the deployment will have named IAM
        capabilities (i.e., able to create all IAM resources).

        This is a shorthand that you can use if you fully trust the templates that
        are deployed in this pipeline. If you want more fine-grained permissions,
        use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation
        deployment is allowed to do.

        :stability: experimental
        '''
        result = self._values.get("admin_permissions")
        assert result is not None, "Required property 'admin_permissions' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def change_set_name(self) -> builtins.str:
        '''(experimental) Name of the change set to create or update.

        :stability: experimental
        '''
        result = self._values.get("change_set_name")
        assert result is not None, "Required property 'change_set_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''(experimental) The name of the stack to apply this action to.

        :stability: experimental
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_path(self) -> _ArtifactPath_a5b79113:
        '''(experimental) Input artifact with the ChangeSet's CloudFormation template.

        :stability: experimental
        '''
        result = self._values.get("template_path")
        assert result is not None, "Required property 'template_path' is missing"
        return typing.cast(_ArtifactPath_a5b79113, result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account this Action is supposed to operate in.

        **Note**: if you specify the ``role`` property,
        this is ignored - the action will operate in the same region the passed role does.

        :default: - action resides in the same account as the pipeline

        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capabilities(
        self,
    ) -> typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]]:
        '''(deprecated) Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation
        might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM``
        if your stack template contains AWS Identity and Access Management (IAM) resources. For more
        information see the link below.

        :default: None, unless ``adminPermissions`` is true

        :deprecated: use {@link cfnCapabilities} instead

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        :stability: deprecated
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]], result)

    @builtins.property
    def cfn_capabilities(
        self,
    ) -> typing.Optional[typing.List[_CfnCapabilities_6e018757]]:
        '''(experimental) Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources,
        explicit acknowledgement is required that AWS CloudFormation might create or update those resources.
        For example, you must specify ``ANONYMOUS_IAM`` or ``NAMED_IAM`` if your stack template contains AWS
        Identity and Access Management (IAM) resources.
        For more information, see the link below.

        :default: None, unless ``adminPermissions`` is true

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        :stability: experimental
        '''
        result = self._values.get("cfn_capabilities")
        return typing.cast(typing.Optional[typing.List[_CfnCapabilities_6e018757]], result)

    @builtins.property
    def deployment_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) IAM role to assume when deploying changes.

        If not specified, a fresh role is created. The role is created with zero
        permissions unless ``adminPermissions`` is true, in which case the role will have
        full permissions.

        :default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).

        :stability: experimental
        '''
        result = self._values.get("deployment_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def extra_inputs(self) -> typing.Optional[typing.List[_Artifact_9905eec2]]:
        '''(experimental) The list of additional input Artifacts for this Action.

        This is especially useful when used in conjunction with the ``parameterOverrides`` property.
        For example, if you have:

        parameterOverrides: {
        'Param1': action1.outputArtifact.bucketName,
        'Param2': action2.outputArtifact.objectKey,
        }

        , if the output Artifacts of ``action1`` and ``action2`` were not used to
        set either the ``templateConfiguration`` or the ``templatePath`` properties,
        you need to make sure to include them in the ``extraInputs`` -
        otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.

        :stability: experimental
        '''
        result = self._values.get("extra_inputs")
        return typing.cast(typing.Optional[typing.List[_Artifact_9905eec2]], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) The name of the output artifact to generate.

        Only applied if ``outputFileName`` is set as well.

        :default: Automatically generated artifact name.

        :stability: experimental
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def output_file_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the filename in the output artifact to store the AWS CloudFormation call's result.

        The file will contain the result of the call to AWS CloudFormation (for example
        the call to UpdateStack or CreateChangeSet).

        AWS CodePipeline adds the file to the output artifact after performing
        the specified action.

        :default: No output artifact generated

        :stability: experimental
        '''
        result = self._values.get("output_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional template parameters.

        Template parameters specified here take precedence over template parameters
        found in the artifact specified by the ``templateConfiguration`` property.

        We recommend that you use the template configuration file to specify
        most of your parameter values. Use parameter overrides to specify only
        dynamic parameter values (values that are unknown until you run the
        pipeline).

        All parameter names must be present in the stack template.

        Note: the entire object cannot be more than 1kB.

        :default: No overrides

        :stability: experimental
        '''
        result = self._values.get("parameter_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS region the given Action resides in.

        Note that a cross-region Pipeline requires replication buckets to function correctly.
        You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property.
        If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets,
        that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        :default: the Action resides in the same region as the Pipeline

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_configuration(self) -> typing.Optional[_ArtifactPath_a5b79113]:
        '''(experimental) Input artifact to use for template parameters values and stack policy.

        The template configuration file should contain a JSON object that should look like this:
        ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information,
        see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_.

        Note that if you include sensitive information, such as passwords, restrict access to this
        file.

        :default: No template configuration based on input artifacts

        :stability: experimental
        '''
        result = self._values.get("template_configuration")
        return typing.cast(typing.Optional[_ArtifactPath_a5b79113], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFormationCreateReplaceChangeSetActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudFormationCreateUpdateStackAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.CloudFormationCreateUpdateStackAction",
):
    '''(experimental) CodePipeline action to deploy a stack.

    Creates the stack if the specified stack doesn't exist. If the stack exists,
    AWS CloudFormation updates the stack. Use this action to update existing
    stacks.

    AWS CodePipeline won't replace the stack, and will fail deployment if the
    stack is in a failed state. Use ``ReplaceOnFailure`` for an action that
    will delete and recreate the stack to try and recover from failed states.

    Use this action to automatically replace failed stacks without recovering or
    troubleshooting them. You would typically choose this mode for testing.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        admin_permissions: builtins.bool,
        stack_name: builtins.str,
        template_path: _ArtifactPath_a5b79113,
        account: typing.Optional[builtins.str] = None,
        capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]] = None,
        cfn_capabilities: typing.Optional[typing.List[_CfnCapabilities_6e018757]] = None,
        deployment_role: typing.Optional[_IRole_59af6f50] = None,
        extra_inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        parameter_overrides: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        region: typing.Optional[builtins.str] = None,
        replace_on_failure: typing.Optional[builtins.bool] = None,
        template_configuration: typing.Optional[_ArtifactPath_a5b79113] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_permissions: (experimental) Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param stack_name: (experimental) The name of the stack to apply this action to.
        :param template_path: (experimental) Input artifact with the CloudFormation template to deploy.
        :param account: (experimental) The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: (deprecated) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param cfn_capabilities: (experimental) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement is required that AWS CloudFormation might create or update those resources. For example, you must specify ``ANONYMOUS_IAM`` or ``NAMED_IAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information, see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: (experimental) IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: (experimental) The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have: parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: (experimental) The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: (experimental) A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: (experimental) Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: (experimental) The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param replace_on_failure: (experimental) Replace the stack if it's in a failed state. If this is set to true and the stack is in a failed state (one of ROLLBACK_COMPLETE, ROLLBACK_FAILED, CREATE_FAILED, DELETE_FAILED, or UPDATE_ROLLBACK_FAILED), AWS CloudFormation deletes the stack and then creates a new stack. If this is not set to true and the stack is in a failed state, the deployment fails. Default: false
        :param template_configuration: (experimental) Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = CloudFormationCreateUpdateStackActionProps(
            admin_permissions=admin_permissions,
            stack_name=stack_name,
            template_path=template_path,
            account=account,
            capabilities=capabilities,
            cfn_capabilities=cfn_capabilities,
            deployment_role=deployment_role,
            extra_inputs=extra_inputs,
            output=output,
            output_file_name=output_file_name,
            parameter_overrides=parameter_overrides,
            region=region,
            replace_on_failure=replace_on_failure,
            template_configuration=template_configuration,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(CloudFormationCreateUpdateStackAction, self, [props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> builtins.bool:
        '''(experimental) Add statement to the service role assumed by CloudFormation while executing this action.

        :param statement: -

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "addToDeploymentRolePolicy", [statement]))

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [scope, stage, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> _IRole_59af6f50:
        '''
        :stability: experimental
        '''
        return typing.cast(_IRole_59af6f50, jsii.get(self, "deploymentRole"))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.CloudFormationCreateUpdateStackActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "admin_permissions": "adminPermissions",
        "stack_name": "stackName",
        "template_path": "templatePath",
        "account": "account",
        "capabilities": "capabilities",
        "cfn_capabilities": "cfnCapabilities",
        "deployment_role": "deploymentRole",
        "extra_inputs": "extraInputs",
        "output": "output",
        "output_file_name": "outputFileName",
        "parameter_overrides": "parameterOverrides",
        "region": "region",
        "replace_on_failure": "replaceOnFailure",
        "template_configuration": "templateConfiguration",
    },
)
class CloudFormationCreateUpdateStackActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        admin_permissions: builtins.bool,
        stack_name: builtins.str,
        template_path: _ArtifactPath_a5b79113,
        account: typing.Optional[builtins.str] = None,
        capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]] = None,
        cfn_capabilities: typing.Optional[typing.List[_CfnCapabilities_6e018757]] = None,
        deployment_role: typing.Optional[_IRole_59af6f50] = None,
        extra_inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        parameter_overrides: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        region: typing.Optional[builtins.str] = None,
        replace_on_failure: typing.Optional[builtins.bool] = None,
        template_configuration: typing.Optional[_ArtifactPath_a5b79113] = None,
    ) -> None:
        '''(experimental) Properties for the CloudFormationCreateUpdateStackAction.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param admin_permissions: (experimental) Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param stack_name: (experimental) The name of the stack to apply this action to.
        :param template_path: (experimental) Input artifact with the CloudFormation template to deploy.
        :param account: (experimental) The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: (deprecated) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param cfn_capabilities: (experimental) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement is required that AWS CloudFormation might create or update those resources. For example, you must specify ``ANONYMOUS_IAM`` or ``NAMED_IAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information, see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: (experimental) IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: (experimental) The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have: parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: (experimental) The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: (experimental) A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: (experimental) Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: (experimental) The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param replace_on_failure: (experimental) Replace the stack if it's in a failed state. If this is set to true and the stack is in a failed state (one of ROLLBACK_COMPLETE, ROLLBACK_FAILED, CREATE_FAILED, DELETE_FAILED, or UPDATE_ROLLBACK_FAILED), AWS CloudFormation deletes the stack and then creates a new stack. If this is not set to true and the stack is in a failed state, the deployment fails. Default: false
        :param template_configuration: (experimental) Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "admin_permissions": admin_permissions,
            "stack_name": stack_name,
            "template_path": template_path,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if account is not None:
            self._values["account"] = account
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if cfn_capabilities is not None:
            self._values["cfn_capabilities"] = cfn_capabilities
        if deployment_role is not None:
            self._values["deployment_role"] = deployment_role
        if extra_inputs is not None:
            self._values["extra_inputs"] = extra_inputs
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if parameter_overrides is not None:
            self._values["parameter_overrides"] = parameter_overrides
        if region is not None:
            self._values["region"] = region
        if replace_on_failure is not None:
            self._values["replace_on_failure"] = replace_on_failure
        if template_configuration is not None:
            self._values["template_configuration"] = template_configuration

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def admin_permissions(self) -> builtins.bool:
        '''(experimental) Whether to grant full permissions to CloudFormation while deploying this template.

        Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you
        don't specify any alternatives.

        The default role that will be created for you will have full (i.e., ``*``)
        permissions on all resources, and the deployment will have named IAM
        capabilities (i.e., able to create all IAM resources).

        This is a shorthand that you can use if you fully trust the templates that
        are deployed in this pipeline. If you want more fine-grained permissions,
        use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation
        deployment is allowed to do.

        :stability: experimental
        '''
        result = self._values.get("admin_permissions")
        assert result is not None, "Required property 'admin_permissions' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''(experimental) The name of the stack to apply this action to.

        :stability: experimental
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_path(self) -> _ArtifactPath_a5b79113:
        '''(experimental) Input artifact with the CloudFormation template to deploy.

        :stability: experimental
        '''
        result = self._values.get("template_path")
        assert result is not None, "Required property 'template_path' is missing"
        return typing.cast(_ArtifactPath_a5b79113, result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account this Action is supposed to operate in.

        **Note**: if you specify the ``role`` property,
        this is ignored - the action will operate in the same region the passed role does.

        :default: - action resides in the same account as the pipeline

        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capabilities(
        self,
    ) -> typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]]:
        '''(deprecated) Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation
        might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM``
        if your stack template contains AWS Identity and Access Management (IAM) resources. For more
        information see the link below.

        :default: None, unless ``adminPermissions`` is true

        :deprecated: use {@link cfnCapabilities} instead

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        :stability: deprecated
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]], result)

    @builtins.property
    def cfn_capabilities(
        self,
    ) -> typing.Optional[typing.List[_CfnCapabilities_6e018757]]:
        '''(experimental) Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources,
        explicit acknowledgement is required that AWS CloudFormation might create or update those resources.
        For example, you must specify ``ANONYMOUS_IAM`` or ``NAMED_IAM`` if your stack template contains AWS
        Identity and Access Management (IAM) resources.
        For more information, see the link below.

        :default: None, unless ``adminPermissions`` is true

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        :stability: experimental
        '''
        result = self._values.get("cfn_capabilities")
        return typing.cast(typing.Optional[typing.List[_CfnCapabilities_6e018757]], result)

    @builtins.property
    def deployment_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) IAM role to assume when deploying changes.

        If not specified, a fresh role is created. The role is created with zero
        permissions unless ``adminPermissions`` is true, in which case the role will have
        full permissions.

        :default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).

        :stability: experimental
        '''
        result = self._values.get("deployment_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def extra_inputs(self) -> typing.Optional[typing.List[_Artifact_9905eec2]]:
        '''(experimental) The list of additional input Artifacts for this Action.

        This is especially useful when used in conjunction with the ``parameterOverrides`` property.
        For example, if you have:

        parameterOverrides: {
        'Param1': action1.outputArtifact.bucketName,
        'Param2': action2.outputArtifact.objectKey,
        }

        , if the output Artifacts of ``action1`` and ``action2`` were not used to
        set either the ``templateConfiguration`` or the ``templatePath`` properties,
        you need to make sure to include them in the ``extraInputs`` -
        otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.

        :stability: experimental
        '''
        result = self._values.get("extra_inputs")
        return typing.cast(typing.Optional[typing.List[_Artifact_9905eec2]], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) The name of the output artifact to generate.

        Only applied if ``outputFileName`` is set as well.

        :default: Automatically generated artifact name.

        :stability: experimental
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def output_file_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the filename in the output artifact to store the AWS CloudFormation call's result.

        The file will contain the result of the call to AWS CloudFormation (for example
        the call to UpdateStack or CreateChangeSet).

        AWS CodePipeline adds the file to the output artifact after performing
        the specified action.

        :default: No output artifact generated

        :stability: experimental
        '''
        result = self._values.get("output_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional template parameters.

        Template parameters specified here take precedence over template parameters
        found in the artifact specified by the ``templateConfiguration`` property.

        We recommend that you use the template configuration file to specify
        most of your parameter values. Use parameter overrides to specify only
        dynamic parameter values (values that are unknown until you run the
        pipeline).

        All parameter names must be present in the stack template.

        Note: the entire object cannot be more than 1kB.

        :default: No overrides

        :stability: experimental
        '''
        result = self._values.get("parameter_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS region the given Action resides in.

        Note that a cross-region Pipeline requires replication buckets to function correctly.
        You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property.
        If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets,
        that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        :default: the Action resides in the same region as the Pipeline

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replace_on_failure(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Replace the stack if it's in a failed state.

        If this is set to true and the stack is in a failed state (one of
        ROLLBACK_COMPLETE, ROLLBACK_FAILED, CREATE_FAILED, DELETE_FAILED, or
        UPDATE_ROLLBACK_FAILED), AWS CloudFormation deletes the stack and then
        creates a new stack.

        If this is not set to true and the stack is in a failed state,
        the deployment fails.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("replace_on_failure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def template_configuration(self) -> typing.Optional[_ArtifactPath_a5b79113]:
        '''(experimental) Input artifact to use for template parameters values and stack policy.

        The template configuration file should contain a JSON object that should look like this:
        ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information,
        see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_.

        Note that if you include sensitive information, such as passwords, restrict access to this
        file.

        :default: No template configuration based on input artifacts

        :stability: experimental
        '''
        result = self._values.get("template_configuration")
        return typing.cast(typing.Optional[_ArtifactPath_a5b79113], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFormationCreateUpdateStackActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudFormationDeleteStackAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.CloudFormationDeleteStackAction",
):
    '''(experimental) CodePipeline action to delete a stack.

    Deletes a stack. If you specify a stack that doesn't exist, the action completes successfully
    without deleting a stack.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        admin_permissions: builtins.bool,
        stack_name: builtins.str,
        account: typing.Optional[builtins.str] = None,
        capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]] = None,
        cfn_capabilities: typing.Optional[typing.List[_CfnCapabilities_6e018757]] = None,
        deployment_role: typing.Optional[_IRole_59af6f50] = None,
        extra_inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        parameter_overrides: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        region: typing.Optional[builtins.str] = None,
        template_configuration: typing.Optional[_ArtifactPath_a5b79113] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param admin_permissions: (experimental) Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param stack_name: (experimental) The name of the stack to apply this action to.
        :param account: (experimental) The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: (deprecated) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param cfn_capabilities: (experimental) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement is required that AWS CloudFormation might create or update those resources. For example, you must specify ``ANONYMOUS_IAM`` or ``NAMED_IAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information, see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: (experimental) IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: (experimental) The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have: parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: (experimental) The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: (experimental) A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: (experimental) Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: (experimental) The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param template_configuration: (experimental) Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = CloudFormationDeleteStackActionProps(
            admin_permissions=admin_permissions,
            stack_name=stack_name,
            account=account,
            capabilities=capabilities,
            cfn_capabilities=cfn_capabilities,
            deployment_role=deployment_role,
            extra_inputs=extra_inputs,
            output=output,
            output_file_name=output_file_name,
            parameter_overrides=parameter_overrides,
            region=region,
            template_configuration=template_configuration,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(CloudFormationDeleteStackAction, self, [props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> builtins.bool:
        '''(experimental) Add statement to the service role assumed by CloudFormation while executing this action.

        :param statement: -

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "addToDeploymentRolePolicy", [statement]))

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [scope, stage, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> _IRole_59af6f50:
        '''
        :stability: experimental
        '''
        return typing.cast(_IRole_59af6f50, jsii.get(self, "deploymentRole"))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.CloudFormationDeleteStackActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "admin_permissions": "adminPermissions",
        "stack_name": "stackName",
        "account": "account",
        "capabilities": "capabilities",
        "cfn_capabilities": "cfnCapabilities",
        "deployment_role": "deploymentRole",
        "extra_inputs": "extraInputs",
        "output": "output",
        "output_file_name": "outputFileName",
        "parameter_overrides": "parameterOverrides",
        "region": "region",
        "template_configuration": "templateConfiguration",
    },
)
class CloudFormationDeleteStackActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        admin_permissions: builtins.bool,
        stack_name: builtins.str,
        account: typing.Optional[builtins.str] = None,
        capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]] = None,
        cfn_capabilities: typing.Optional[typing.List[_CfnCapabilities_6e018757]] = None,
        deployment_role: typing.Optional[_IRole_59af6f50] = None,
        extra_inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        parameter_overrides: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        region: typing.Optional[builtins.str] = None,
        template_configuration: typing.Optional[_ArtifactPath_a5b79113] = None,
    ) -> None:
        '''(experimental) Properties for the CloudFormationDeleteStackAction.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param admin_permissions: (experimental) Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param stack_name: (experimental) The name of the stack to apply this action to.
        :param account: (experimental) The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: (deprecated) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param cfn_capabilities: (experimental) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement is required that AWS CloudFormation might create or update those resources. For example, you must specify ``ANONYMOUS_IAM`` or ``NAMED_IAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information, see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: (experimental) IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: (experimental) The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have: parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: (experimental) The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: (experimental) A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: (experimental) Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: (experimental) The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param template_configuration: (experimental) Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "admin_permissions": admin_permissions,
            "stack_name": stack_name,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if account is not None:
            self._values["account"] = account
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if cfn_capabilities is not None:
            self._values["cfn_capabilities"] = cfn_capabilities
        if deployment_role is not None:
            self._values["deployment_role"] = deployment_role
        if extra_inputs is not None:
            self._values["extra_inputs"] = extra_inputs
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if parameter_overrides is not None:
            self._values["parameter_overrides"] = parameter_overrides
        if region is not None:
            self._values["region"] = region
        if template_configuration is not None:
            self._values["template_configuration"] = template_configuration

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def admin_permissions(self) -> builtins.bool:
        '''(experimental) Whether to grant full permissions to CloudFormation while deploying this template.

        Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you
        don't specify any alternatives.

        The default role that will be created for you will have full (i.e., ``*``)
        permissions on all resources, and the deployment will have named IAM
        capabilities (i.e., able to create all IAM resources).

        This is a shorthand that you can use if you fully trust the templates that
        are deployed in this pipeline. If you want more fine-grained permissions,
        use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation
        deployment is allowed to do.

        :stability: experimental
        '''
        result = self._values.get("admin_permissions")
        assert result is not None, "Required property 'admin_permissions' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''(experimental) The name of the stack to apply this action to.

        :stability: experimental
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account this Action is supposed to operate in.

        **Note**: if you specify the ``role`` property,
        this is ignored - the action will operate in the same region the passed role does.

        :default: - action resides in the same account as the pipeline

        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capabilities(
        self,
    ) -> typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]]:
        '''(deprecated) Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation
        might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM``
        if your stack template contains AWS Identity and Access Management (IAM) resources. For more
        information see the link below.

        :default: None, unless ``adminPermissions`` is true

        :deprecated: use {@link cfnCapabilities} instead

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        :stability: deprecated
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]], result)

    @builtins.property
    def cfn_capabilities(
        self,
    ) -> typing.Optional[typing.List[_CfnCapabilities_6e018757]]:
        '''(experimental) Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources,
        explicit acknowledgement is required that AWS CloudFormation might create or update those resources.
        For example, you must specify ``ANONYMOUS_IAM`` or ``NAMED_IAM`` if your stack template contains AWS
        Identity and Access Management (IAM) resources.
        For more information, see the link below.

        :default: None, unless ``adminPermissions`` is true

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        :stability: experimental
        '''
        result = self._values.get("cfn_capabilities")
        return typing.cast(typing.Optional[typing.List[_CfnCapabilities_6e018757]], result)

    @builtins.property
    def deployment_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) IAM role to assume when deploying changes.

        If not specified, a fresh role is created. The role is created with zero
        permissions unless ``adminPermissions`` is true, in which case the role will have
        full permissions.

        :default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).

        :stability: experimental
        '''
        result = self._values.get("deployment_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def extra_inputs(self) -> typing.Optional[typing.List[_Artifact_9905eec2]]:
        '''(experimental) The list of additional input Artifacts for this Action.

        This is especially useful when used in conjunction with the ``parameterOverrides`` property.
        For example, if you have:

        parameterOverrides: {
        'Param1': action1.outputArtifact.bucketName,
        'Param2': action2.outputArtifact.objectKey,
        }

        , if the output Artifacts of ``action1`` and ``action2`` were not used to
        set either the ``templateConfiguration`` or the ``templatePath`` properties,
        you need to make sure to include them in the ``extraInputs`` -
        otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.

        :stability: experimental
        '''
        result = self._values.get("extra_inputs")
        return typing.cast(typing.Optional[typing.List[_Artifact_9905eec2]], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) The name of the output artifact to generate.

        Only applied if ``outputFileName`` is set as well.

        :default: Automatically generated artifact name.

        :stability: experimental
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def output_file_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the filename in the output artifact to store the AWS CloudFormation call's result.

        The file will contain the result of the call to AWS CloudFormation (for example
        the call to UpdateStack or CreateChangeSet).

        AWS CodePipeline adds the file to the output artifact after performing
        the specified action.

        :default: No output artifact generated

        :stability: experimental
        '''
        result = self._values.get("output_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_overrides(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional template parameters.

        Template parameters specified here take precedence over template parameters
        found in the artifact specified by the ``templateConfiguration`` property.

        We recommend that you use the template configuration file to specify
        most of your parameter values. Use parameter overrides to specify only
        dynamic parameter values (values that are unknown until you run the
        pipeline).

        All parameter names must be present in the stack template.

        Note: the entire object cannot be more than 1kB.

        :default: No overrides

        :stability: experimental
        '''
        result = self._values.get("parameter_overrides")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS region the given Action resides in.

        Note that a cross-region Pipeline requires replication buckets to function correctly.
        You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property.
        If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets,
        that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        :default: the Action resides in the same region as the Pipeline

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_configuration(self) -> typing.Optional[_ArtifactPath_a5b79113]:
        '''(experimental) Input artifact to use for template parameters values and stack policy.

        The template configuration file should contain a JSON object that should look like this:
        ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information,
        see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_.

        Note that if you include sensitive information, such as passwords, restrict access to this
        file.

        :default: No template configuration based on input artifacts

        :stability: experimental
        '''
        result = self._values.get("template_configuration")
        return typing.cast(typing.Optional[_ArtifactPath_a5b79113], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFormationDeleteStackActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudFormationExecuteChangeSetAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.CloudFormationExecuteChangeSetAction",
):
    '''(experimental) CodePipeline action to execute a prepared change set.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        change_set_name: builtins.str,
        stack_name: builtins.str,
        account: typing.Optional[builtins.str] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param change_set_name: (experimental) Name of the change set to execute.
        :param stack_name: (experimental) The name of the stack to apply this action to.
        :param account: (experimental) The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param output: (experimental) The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: (experimental) A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param region: (experimental) The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = CloudFormationExecuteChangeSetActionProps(
            change_set_name=change_set_name,
            stack_name=stack_name,
            account=account,
            output=output,
            output_file_name=output_file_name,
            region=region,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(CloudFormationExecuteChangeSetAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [scope, stage, options]))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.CloudFormationExecuteChangeSetActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "change_set_name": "changeSetName",
        "stack_name": "stackName",
        "account": "account",
        "output": "output",
        "output_file_name": "outputFileName",
        "region": "region",
    },
)
class CloudFormationExecuteChangeSetActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        change_set_name: builtins.str,
        stack_name: builtins.str,
        account: typing.Optional[builtins.str] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for the CloudFormationExecuteChangeSetAction.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param change_set_name: (experimental) Name of the change set to execute.
        :param stack_name: (experimental) The name of the stack to apply this action to.
        :param account: (experimental) The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param output: (experimental) The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: (experimental) A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param region: (experimental) The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "change_set_name": change_set_name,
            "stack_name": stack_name,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if account is not None:
            self._values["account"] = account
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def change_set_name(self) -> builtins.str:
        '''(experimental) Name of the change set to execute.

        :stability: experimental
        '''
        result = self._values.get("change_set_name")
        assert result is not None, "Required property 'change_set_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''(experimental) The name of the stack to apply this action to.

        :stability: experimental
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account this Action is supposed to operate in.

        **Note**: if you specify the ``role`` property,
        this is ignored - the action will operate in the same region the passed role does.

        :default: - action resides in the same account as the pipeline

        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) The name of the output artifact to generate.

        Only applied if ``outputFileName`` is set as well.

        :default: Automatically generated artifact name.

        :stability: experimental
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def output_file_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the filename in the output artifact to store the AWS CloudFormation call's result.

        The file will contain the result of the call to AWS CloudFormation (for example
        the call to UpdateStack or CreateChangeSet).

        AWS CodePipeline adds the file to the output artifact after performing
        the specified action.

        :default: No output artifact generated

        :stability: experimental
        '''
        result = self._values.get("output_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS region the given Action resides in.

        Note that a cross-region Pipeline requires replication buckets to function correctly.
        You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property.
        If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets,
        that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        :default: the Action resides in the same region as the Pipeline

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFormationExecuteChangeSetActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodeBuildAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.CodeBuildAction",
):
    '''(experimental) CodePipeline build action that uses AWS CodeBuild.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        input: _Artifact_9905eec2,
        project: _IProject_6da8803e,
        check_secrets_in_plain_text_env_variables: typing.Optional[builtins.bool] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]] = None,
        execute_batch_build: typing.Optional[builtins.bool] = None,
        extra_inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        outputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        type: typing.Optional["CodeBuildActionType"] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input: (experimental) The source to use as input for this action.
        :param project: (experimental) The action's Project.
        :param check_secrets_in_plain_text_env_variables: (experimental) Whether to check for the presence of any secrets in the environment variables of the default type, BuildEnvironmentVariableType.PLAINTEXT. Since using a secret for the value of that kind of variable would result in it being displayed in plain text in the AWS Console, the construct will throw an exception if it detects a secret was passed there. Pass this property as false if you want to skip this validation, and keep using a secret in a plain text environment variable. Default: true
        :param environment_variables: (experimental) The environment variables to pass to the CodeBuild project when this action executes. If a variable with the same name was set both on the project level, and here, this value will take precedence. Default: - No additional environment variables are specified.
        :param execute_batch_build: (experimental) Trigger a batch build. Enabling this will enable batch builds on the CodeBuild project. Default: false
        :param extra_inputs: (experimental) The list of additional input Artifacts for this action. The directories the additional inputs will be available at are available during the project's build in the CODEBUILD_SRC_DIR_ environment variables. The project's build always starts in the directory with the primary input artifact checked out, the one pointed to by the {@link input} property. For more information, see https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html .
        :param outputs: (experimental) The list of output Artifacts for this action. **Note**: if you specify more than one output Artifact here, you cannot use the primary 'artifacts' section of the buildspec; you have to use the 'secondary-artifacts' section instead. See https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html for details. Default: the action will not have any outputs
        :param type: (experimental) The type of the action that determines its CodePipeline Category - Build, or Test. Default: CodeBuildActionType.BUILD
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = CodeBuildActionProps(
            input=input,
            project=project,
            check_secrets_in_plain_text_env_variables=check_secrets_in_plain_text_env_variables,
            environment_variables=environment_variables,
            execute_batch_build=execute_batch_build,
            extra_inputs=extra_inputs,
            outputs=outputs,
            type=type,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(CodeBuildAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        scope: _Construct_e78e779f,
        _stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [scope, _stage, options]))

    @jsii.member(jsii_name="variable")
    def variable(self, variable_name: builtins.str) -> builtins.str:
        '''(experimental) Reference a CodePipeline variable defined by the CodeBuild project this action points to.

        Variables in CodeBuild actions are defined using the 'exported-variables' subsection of the 'env'
        section of the buildspec.

        :param variable_name: the name of the variable to reference. A variable by this name must be present in the 'exported-variables' section of the buildspec

        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-syntax
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "variable", [variable_name]))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.CodeBuildActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "input": "input",
        "project": "project",
        "check_secrets_in_plain_text_env_variables": "checkSecretsInPlainTextEnvVariables",
        "environment_variables": "environmentVariables",
        "execute_batch_build": "executeBatchBuild",
        "extra_inputs": "extraInputs",
        "outputs": "outputs",
        "type": "type",
    },
)
class CodeBuildActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        input: _Artifact_9905eec2,
        project: _IProject_6da8803e,
        check_secrets_in_plain_text_env_variables: typing.Optional[builtins.bool] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]] = None,
        execute_batch_build: typing.Optional[builtins.bool] = None,
        extra_inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        outputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        type: typing.Optional["CodeBuildActionType"] = None,
    ) -> None:
        '''(experimental) Construction properties of the {@link CodeBuildAction CodeBuild build CodePipeline action}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param input: (experimental) The source to use as input for this action.
        :param project: (experimental) The action's Project.
        :param check_secrets_in_plain_text_env_variables: (experimental) Whether to check for the presence of any secrets in the environment variables of the default type, BuildEnvironmentVariableType.PLAINTEXT. Since using a secret for the value of that kind of variable would result in it being displayed in plain text in the AWS Console, the construct will throw an exception if it detects a secret was passed there. Pass this property as false if you want to skip this validation, and keep using a secret in a plain text environment variable. Default: true
        :param environment_variables: (experimental) The environment variables to pass to the CodeBuild project when this action executes. If a variable with the same name was set both on the project level, and here, this value will take precedence. Default: - No additional environment variables are specified.
        :param execute_batch_build: (experimental) Trigger a batch build. Enabling this will enable batch builds on the CodeBuild project. Default: false
        :param extra_inputs: (experimental) The list of additional input Artifacts for this action. The directories the additional inputs will be available at are available during the project's build in the CODEBUILD_SRC_DIR_ environment variables. The project's build always starts in the directory with the primary input artifact checked out, the one pointed to by the {@link input} property. For more information, see https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html .
        :param outputs: (experimental) The list of output Artifacts for this action. **Note**: if you specify more than one output Artifact here, you cannot use the primary 'artifacts' section of the buildspec; you have to use the 'secondary-artifacts' section instead. See https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html for details. Default: the action will not have any outputs
        :param type: (experimental) The type of the action that determines its CodePipeline Category - Build, or Test. Default: CodeBuildActionType.BUILD

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "input": input,
            "project": project,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if check_secrets_in_plain_text_env_variables is not None:
            self._values["check_secrets_in_plain_text_env_variables"] = check_secrets_in_plain_text_env_variables
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if execute_batch_build is not None:
            self._values["execute_batch_build"] = execute_batch_build
        if extra_inputs is not None:
            self._values["extra_inputs"] = extra_inputs
        if outputs is not None:
            self._values["outputs"] = outputs
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def input(self) -> _Artifact_9905eec2:
        '''(experimental) The source to use as input for this action.

        :stability: experimental
        '''
        result = self._values.get("input")
        assert result is not None, "Required property 'input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def project(self) -> _IProject_6da8803e:
        '''(experimental) The action's Project.

        :stability: experimental
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(_IProject_6da8803e, result)

    @builtins.property
    def check_secrets_in_plain_text_env_variables(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to check for the presence of any secrets in the environment variables of the default type, BuildEnvironmentVariableType.PLAINTEXT. Since using a secret for the value of that kind of variable would result in it being displayed in plain text in the AWS Console, the construct will throw an exception if it detects a secret was passed there. Pass this property as false if you want to skip this validation, and keep using a secret in a plain text environment variable.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("check_secrets_in_plain_text_env_variables")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]]:
        '''(experimental) The environment variables to pass to the CodeBuild project when this action executes.

        If a variable with the same name was set both on the project level, and here,
        this value will take precedence.

        :default: - No additional environment variables are specified.

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]], result)

    @builtins.property
    def execute_batch_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Trigger a batch build.

        Enabling this will enable batch builds on the CodeBuild project.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("execute_batch_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def extra_inputs(self) -> typing.Optional[typing.List[_Artifact_9905eec2]]:
        '''(experimental) The list of additional input Artifacts for this action.

        The directories the additional inputs will be available at are available
        during the project's build in the CODEBUILD_SRC_DIR_ environment variables.
        The project's build always starts in the directory with the primary input artifact checked out,
        the one pointed to by the {@link input} property.
        For more information,
        see https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html .

        :stability: experimental
        '''
        result = self._values.get("extra_inputs")
        return typing.cast(typing.Optional[typing.List[_Artifact_9905eec2]], result)

    @builtins.property
    def outputs(self) -> typing.Optional[typing.List[_Artifact_9905eec2]]:
        '''(experimental) The list of output Artifacts for this action.

        **Note**: if you specify more than one output Artifact here,
        you cannot use the primary 'artifacts' section of the buildspec;
        you have to use the 'secondary-artifacts' section instead.
        See https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html
        for details.

        :default: the action will not have any outputs

        :stability: experimental
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.List[_Artifact_9905eec2]], result)

    @builtins.property
    def type(self) -> typing.Optional["CodeBuildActionType"]:
        '''(experimental) The type of the action that determines its CodePipeline Category - Build, or Test.

        :default: CodeBuildActionType.BUILD

        :stability: experimental
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["CodeBuildActionType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeBuildActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_codepipeline_actions.CodeBuildActionType")
class CodeBuildActionType(enum.Enum):
    '''(experimental) The type of the CodeBuild action that determines its CodePipeline Category - Build, or Test.

    The default is Build.

    :stability: experimental
    '''

    BUILD = "BUILD"
    '''(experimental) The action will have the Build Category.

    This is the default.

    :stability: experimental
    '''
    TEST = "TEST"
    '''(experimental) The action will have the Test Category.

    :stability: experimental
    '''


class CodeCommitSourceAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.CodeCommitSourceAction",
):
    '''(experimental) CodePipeline Source that is provided by an AWS CodeCommit repository.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        output: _Artifact_9905eec2,
        repository: _IRepository_cdb2a3c0,
        branch: typing.Optional[builtins.str] = None,
        code_build_clone_output: typing.Optional[builtins.bool] = None,
        event_role: typing.Optional[_IRole_59af6f50] = None,
        trigger: typing.Optional["CodeCommitTrigger"] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param output: 
        :param repository: (experimental) The CodeCommit repository.
        :param branch: Default: 'master'
        :param code_build_clone_output: (experimental) Whether the output should be the contents of the repository (which is the default), or a link that allows CodeBuild to clone the repository before building. **Note**: if this option is true, then only CodeBuild actions can use the resulting {@link output}. Default: false
        :param event_role: (experimental) Role to be used by on commit event rule. Used only when trigger value is CodeCommitTrigger.EVENTS. Default: a new role will be created.
        :param trigger: (experimental) How should CodePipeline detect source changes for this Action. Default: CodeCommitTrigger.EVENTS
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = CodeCommitSourceActionProps(
            output=output,
            repository=repository,
            branch=branch,
            code_build_clone_output=code_build_clone_output,
            event_role=event_role,
            trigger=trigger,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(CodeCommitSourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        _scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [_scope, stage, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variables")
    def variables(self) -> "CodeCommitSourceVariables":
        '''(experimental) The variables emitted by this action.

        :stability: experimental
        '''
        return typing.cast("CodeCommitSourceVariables", jsii.get(self, "variables"))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.CodeCommitSourceActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "output": "output",
        "repository": "repository",
        "branch": "branch",
        "code_build_clone_output": "codeBuildCloneOutput",
        "event_role": "eventRole",
        "trigger": "trigger",
    },
)
class CodeCommitSourceActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        output: _Artifact_9905eec2,
        repository: _IRepository_cdb2a3c0,
        branch: typing.Optional[builtins.str] = None,
        code_build_clone_output: typing.Optional[builtins.bool] = None,
        event_role: typing.Optional[_IRole_59af6f50] = None,
        trigger: typing.Optional["CodeCommitTrigger"] = None,
    ) -> None:
        '''(experimental) Construction properties of the {@link CodeCommitSourceAction CodeCommit source CodePipeline Action}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param output: 
        :param repository: (experimental) The CodeCommit repository.
        :param branch: Default: 'master'
        :param code_build_clone_output: (experimental) Whether the output should be the contents of the repository (which is the default), or a link that allows CodeBuild to clone the repository before building. **Note**: if this option is true, then only CodeBuild actions can use the resulting {@link output}. Default: false
        :param event_role: (experimental) Role to be used by on commit event rule. Used only when trigger value is CodeCommitTrigger.EVENTS. Default: a new role will be created.
        :param trigger: (experimental) How should CodePipeline detect source changes for this Action. Default: CodeCommitTrigger.EVENTS

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "output": output,
            "repository": repository,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if branch is not None:
            self._values["branch"] = branch
        if code_build_clone_output is not None:
            self._values["code_build_clone_output"] = code_build_clone_output
        if event_role is not None:
            self._values["event_role"] = event_role
        if trigger is not None:
            self._values["trigger"] = trigger

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def output(self) -> _Artifact_9905eec2:
        '''
        :stability: experimental
        '''
        result = self._values.get("output")
        assert result is not None, "Required property 'output' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def repository(self) -> _IRepository_cdb2a3c0:
        '''(experimental) The CodeCommit repository.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(_IRepository_cdb2a3c0, result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''
        :default: 'master'

        :stability: experimental
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_build_clone_output(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the output should be the contents of the repository (which is the default), or a link that allows CodeBuild to clone the repository before building.

        **Note**: if this option is true,
        then only CodeBuild actions can use the resulting {@link output}.

        :default: false

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CodeCommit.html
        :stability: experimental
        '''
        result = self._values.get("code_build_clone_output")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def event_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Role to be used by on commit event rule.

        Used only when trigger value is CodeCommitTrigger.EVENTS.

        :default: a new role will be created.

        :stability: experimental
        '''
        result = self._values.get("event_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def trigger(self) -> typing.Optional["CodeCommitTrigger"]:
        '''(experimental) How should CodePipeline detect source changes for this Action.

        :default: CodeCommitTrigger.EVENTS

        :stability: experimental
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional["CodeCommitTrigger"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeCommitSourceActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.CodeCommitSourceVariables",
    jsii_struct_bases=[],
    name_mapping={
        "author_date": "authorDate",
        "branch_name": "branchName",
        "commit_id": "commitId",
        "commit_message": "commitMessage",
        "committer_date": "committerDate",
        "repository_name": "repositoryName",
    },
)
class CodeCommitSourceVariables:
    def __init__(
        self,
        *,
        author_date: builtins.str,
        branch_name: builtins.str,
        commit_id: builtins.str,
        commit_message: builtins.str,
        committer_date: builtins.str,
        repository_name: builtins.str,
    ) -> None:
        '''(experimental) The CodePipeline variables emitted by the CodeCommit source Action.

        :param author_date: (experimental) The date the currently last commit on the tracked branch was authored, in ISO-8601 format.
        :param branch_name: (experimental) The name of the branch this action tracks.
        :param commit_id: (experimental) The SHA1 hash of the currently last commit on the tracked branch.
        :param commit_message: (experimental) The message of the currently last commit on the tracked branch.
        :param committer_date: (experimental) The date the currently last commit on the tracked branch was committed, in ISO-8601 format.
        :param repository_name: (experimental) The name of the repository this action points to.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "author_date": author_date,
            "branch_name": branch_name,
            "commit_id": commit_id,
            "commit_message": commit_message,
            "committer_date": committer_date,
            "repository_name": repository_name,
        }

    @builtins.property
    def author_date(self) -> builtins.str:
        '''(experimental) The date the currently last commit on the tracked branch was authored, in ISO-8601 format.

        :stability: experimental
        '''
        result = self._values.get("author_date")
        assert result is not None, "Required property 'author_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch_name(self) -> builtins.str:
        '''(experimental) The name of the branch this action tracks.

        :stability: experimental
        '''
        result = self._values.get("branch_name")
        assert result is not None, "Required property 'branch_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_id(self) -> builtins.str:
        '''(experimental) The SHA1 hash of the currently last commit on the tracked branch.

        :stability: experimental
        '''
        result = self._values.get("commit_id")
        assert result is not None, "Required property 'commit_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_message(self) -> builtins.str:
        '''(experimental) The message of the currently last commit on the tracked branch.

        :stability: experimental
        '''
        result = self._values.get("commit_message")
        assert result is not None, "Required property 'commit_message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def committer_date(self) -> builtins.str:
        '''(experimental) The date the currently last commit on the tracked branch was committed, in ISO-8601 format.

        :stability: experimental
        '''
        result = self._values.get("committer_date")
        assert result is not None, "Required property 'committer_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''(experimental) The name of the repository this action points to.

        :stability: experimental
        '''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeCommitSourceVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_codepipeline_actions.CodeCommitTrigger")
class CodeCommitTrigger(enum.Enum):
    '''(experimental) How should the CodeCommit Action detect changes.

    This is the type of the {@link CodeCommitSourceAction.trigger} property.

    :stability: experimental
    '''

    NONE = "NONE"
    '''(experimental) The Action will never detect changes - the Pipeline it's part of will only begin a run when explicitly started.

    :stability: experimental
    '''
    POLL = "POLL"
    '''(experimental) CodePipeline will poll the repository to detect changes.

    :stability: experimental
    '''
    EVENTS = "EVENTS"
    '''(experimental) CodePipeline will use CloudWatch Events to be notified of changes.

    This is the default method of detecting changes.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.CodeDeployEcsContainerImageInput",
    jsii_struct_bases=[],
    name_mapping={
        "input": "input",
        "task_definition_placeholder": "taskDefinitionPlaceholder",
    },
)
class CodeDeployEcsContainerImageInput:
    def __init__(
        self,
        *,
        input: _Artifact_9905eec2,
        task_definition_placeholder: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration for replacing a placeholder string in the ECS task definition template file with an image URI.

        :param input: (experimental) The artifact that contains an ``imageDetails.json`` file with the image URI. The artifact's ``imageDetails.json`` file must be a JSON file containing an ``ImageURI`` property. For example: ``{ "ImageURI": "ACCOUNTID.dkr.ecr.us-west-2.amazonaws.com/dk-image-repo@sha256:example3" }``
        :param task_definition_placeholder: (experimental) The placeholder string in the ECS task definition template file that will be replaced with the image URI. The placeholder string must be surrounded by angle brackets in the template file. For example, if the task definition template file contains a placeholder like ``"image": "<PLACEHOLDER>"``, then the ``taskDefinitionPlaceholder`` value should be ``PLACEHOLDER``. Default: IMAGE

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "input": input,
        }
        if task_definition_placeholder is not None:
            self._values["task_definition_placeholder"] = task_definition_placeholder

    @builtins.property
    def input(self) -> _Artifact_9905eec2:
        '''(experimental) The artifact that contains an ``imageDetails.json`` file with the image URI.

        The artifact's ``imageDetails.json`` file must be a JSON file containing an
        ``ImageURI`` property.  For example:
        ``{ "ImageURI": "ACCOUNTID.dkr.ecr.us-west-2.amazonaws.com/dk-image-repo@sha256:example3" }``

        :stability: experimental
        '''
        result = self._values.get("input")
        assert result is not None, "Required property 'input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def task_definition_placeholder(self) -> typing.Optional[builtins.str]:
        '''(experimental) The placeholder string in the ECS task definition template file that will be replaced with the image URI.

        The placeholder string must be surrounded by angle brackets in the template file.
        For example, if the task definition template file contains a placeholder like
        ``"image": "<PLACEHOLDER>"``, then the ``taskDefinitionPlaceholder`` value should
        be ``PLACEHOLDER``.

        :default: IMAGE

        :stability: experimental
        '''
        result = self._values.get("task_definition_placeholder")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeDeployEcsContainerImageInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodeDeployEcsDeployAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.CodeDeployEcsDeployAction",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        *,
        deployment_group: _IEcsDeploymentGroup_538bcae2,
        app_spec_template_file: typing.Optional[_ArtifactPath_a5b79113] = None,
        app_spec_template_input: typing.Optional[_Artifact_9905eec2] = None,
        container_image_inputs: typing.Optional[typing.List[CodeDeployEcsContainerImageInput]] = None,
        task_definition_template_file: typing.Optional[_ArtifactPath_a5b79113] = None,
        task_definition_template_input: typing.Optional[_Artifact_9905eec2] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment_group: (experimental) The CodeDeploy ECS Deployment Group to deploy to.
        :param app_spec_template_file: (experimental) The name of the CodeDeploy AppSpec file. During deployment, a new task definition will be registered with ECS, and the new task definition ID will be inserted into the CodeDeploy AppSpec file. The AppSpec file contents will be provided to CodeDeploy for the deployment. Use this property if you want to use a different name for this file than the default 'appspec.yaml'. If you use this property, you don't need to specify the ``appSpecTemplateInput`` property. Default: - one of this property, or ``appSpecTemplateInput``, is required
        :param app_spec_template_input: (experimental) The artifact containing the CodeDeploy AppSpec file. During deployment, a new task definition will be registered with ECS, and the new task definition ID will be inserted into the CodeDeploy AppSpec file. The AppSpec file contents will be provided to CodeDeploy for the deployment. If you use this property, it's assumed the file is called 'appspec.yaml'. If your AppSpec file uses a different filename, leave this property empty, and use the ``appSpecTemplateFile`` property instead. Default: - one of this property, or ``appSpecTemplateFile``, is required
        :param container_image_inputs: (experimental) Configuration for dynamically updated images in the task definition. Provide pairs of an image details input artifact and a placeholder string that will be used to dynamically update the ECS task definition template file prior to deployment. A maximum of 4 images can be given.
        :param task_definition_template_file: (experimental) The name of the ECS task definition template file. During deployment, the task definition template file contents will be registered with ECS. Use this property if you want to use a different name for this file than the default 'taskdef.json'. If you use this property, you don't need to specify the ``taskDefinitionTemplateInput`` property. Default: - one of this property, or ``taskDefinitionTemplateInput``, is required
        :param task_definition_template_input: (experimental) The artifact containing the ECS task definition template file. During deployment, the task definition template file contents will be registered with ECS. If you use this property, it's assumed the file is called 'taskdef.json'. If your task definition template uses a different filename, leave this property empty, and use the ``taskDefinitionTemplateFile`` property instead. Default: - one of this property, or ``taskDefinitionTemplateFile``, is required
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = CodeDeployEcsDeployActionProps(
            deployment_group=deployment_group,
            app_spec_template_file=app_spec_template_file,
            app_spec_template_input=app_spec_template_input,
            container_image_inputs=container_image_inputs,
            task_definition_template_file=task_definition_template_file,
            task_definition_template_input=task_definition_template_input,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(CodeDeployEcsDeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        _scope: _Construct_e78e779f,
        _stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [_scope, _stage, options]))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.CodeDeployEcsDeployActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "deployment_group": "deploymentGroup",
        "app_spec_template_file": "appSpecTemplateFile",
        "app_spec_template_input": "appSpecTemplateInput",
        "container_image_inputs": "containerImageInputs",
        "task_definition_template_file": "taskDefinitionTemplateFile",
        "task_definition_template_input": "taskDefinitionTemplateInput",
    },
)
class CodeDeployEcsDeployActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        deployment_group: _IEcsDeploymentGroup_538bcae2,
        app_spec_template_file: typing.Optional[_ArtifactPath_a5b79113] = None,
        app_spec_template_input: typing.Optional[_Artifact_9905eec2] = None,
        container_image_inputs: typing.Optional[typing.List[CodeDeployEcsContainerImageInput]] = None,
        task_definition_template_file: typing.Optional[_ArtifactPath_a5b79113] = None,
        task_definition_template_input: typing.Optional[_Artifact_9905eec2] = None,
    ) -> None:
        '''(experimental) Construction properties of the {@link CodeDeployEcsDeployAction CodeDeploy ECS deploy CodePipeline Action}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param deployment_group: (experimental) The CodeDeploy ECS Deployment Group to deploy to.
        :param app_spec_template_file: (experimental) The name of the CodeDeploy AppSpec file. During deployment, a new task definition will be registered with ECS, and the new task definition ID will be inserted into the CodeDeploy AppSpec file. The AppSpec file contents will be provided to CodeDeploy for the deployment. Use this property if you want to use a different name for this file than the default 'appspec.yaml'. If you use this property, you don't need to specify the ``appSpecTemplateInput`` property. Default: - one of this property, or ``appSpecTemplateInput``, is required
        :param app_spec_template_input: (experimental) The artifact containing the CodeDeploy AppSpec file. During deployment, a new task definition will be registered with ECS, and the new task definition ID will be inserted into the CodeDeploy AppSpec file. The AppSpec file contents will be provided to CodeDeploy for the deployment. If you use this property, it's assumed the file is called 'appspec.yaml'. If your AppSpec file uses a different filename, leave this property empty, and use the ``appSpecTemplateFile`` property instead. Default: - one of this property, or ``appSpecTemplateFile``, is required
        :param container_image_inputs: (experimental) Configuration for dynamically updated images in the task definition. Provide pairs of an image details input artifact and a placeholder string that will be used to dynamically update the ECS task definition template file prior to deployment. A maximum of 4 images can be given.
        :param task_definition_template_file: (experimental) The name of the ECS task definition template file. During deployment, the task definition template file contents will be registered with ECS. Use this property if you want to use a different name for this file than the default 'taskdef.json'. If you use this property, you don't need to specify the ``taskDefinitionTemplateInput`` property. Default: - one of this property, or ``taskDefinitionTemplateInput``, is required
        :param task_definition_template_input: (experimental) The artifact containing the ECS task definition template file. During deployment, the task definition template file contents will be registered with ECS. If you use this property, it's assumed the file is called 'taskdef.json'. If your task definition template uses a different filename, leave this property empty, and use the ``taskDefinitionTemplateFile`` property instead. Default: - one of this property, or ``taskDefinitionTemplateFile``, is required

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "deployment_group": deployment_group,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if app_spec_template_file is not None:
            self._values["app_spec_template_file"] = app_spec_template_file
        if app_spec_template_input is not None:
            self._values["app_spec_template_input"] = app_spec_template_input
        if container_image_inputs is not None:
            self._values["container_image_inputs"] = container_image_inputs
        if task_definition_template_file is not None:
            self._values["task_definition_template_file"] = task_definition_template_file
        if task_definition_template_input is not None:
            self._values["task_definition_template_input"] = task_definition_template_input

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def deployment_group(self) -> _IEcsDeploymentGroup_538bcae2:
        '''(experimental) The CodeDeploy ECS Deployment Group to deploy to.

        :stability: experimental
        '''
        result = self._values.get("deployment_group")
        assert result is not None, "Required property 'deployment_group' is missing"
        return typing.cast(_IEcsDeploymentGroup_538bcae2, result)

    @builtins.property
    def app_spec_template_file(self) -> typing.Optional[_ArtifactPath_a5b79113]:
        '''(experimental) The name of the CodeDeploy AppSpec file.

        During deployment, a new task definition will be registered
        with ECS, and the new task definition ID will be inserted into
        the CodeDeploy AppSpec file.  The AppSpec file contents will be
        provided to CodeDeploy for the deployment.

        Use this property if you want to use a different name for this file than the default 'appspec.yaml'.
        If you use this property, you don't need to specify the ``appSpecTemplateInput`` property.

        :default: - one of this property, or ``appSpecTemplateInput``, is required

        :stability: experimental
        '''
        result = self._values.get("app_spec_template_file")
        return typing.cast(typing.Optional[_ArtifactPath_a5b79113], result)

    @builtins.property
    def app_spec_template_input(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) The artifact containing the CodeDeploy AppSpec file.

        During deployment, a new task definition will be registered
        with ECS, and the new task definition ID will be inserted into
        the CodeDeploy AppSpec file.  The AppSpec file contents will be
        provided to CodeDeploy for the deployment.

        If you use this property, it's assumed the file is called 'appspec.yaml'.
        If your AppSpec file uses a different filename, leave this property empty,
        and use the ``appSpecTemplateFile`` property instead.

        :default: - one of this property, or ``appSpecTemplateFile``, is required

        :stability: experimental
        '''
        result = self._values.get("app_spec_template_input")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def container_image_inputs(
        self,
    ) -> typing.Optional[typing.List[CodeDeployEcsContainerImageInput]]:
        '''(experimental) Configuration for dynamically updated images in the task definition.

        Provide pairs of an image details input artifact and a placeholder string
        that will be used to dynamically update the ECS task definition template
        file prior to deployment. A maximum of 4 images can be given.

        :stability: experimental
        '''
        result = self._values.get("container_image_inputs")
        return typing.cast(typing.Optional[typing.List[CodeDeployEcsContainerImageInput]], result)

    @builtins.property
    def task_definition_template_file(self) -> typing.Optional[_ArtifactPath_a5b79113]:
        '''(experimental) The name of the ECS task definition template file.

        During deployment, the task definition template file contents
        will be registered with ECS.

        Use this property if you want to use a different name for this file than the default 'taskdef.json'.
        If you use this property, you don't need to specify the ``taskDefinitionTemplateInput`` property.

        :default: - one of this property, or ``taskDefinitionTemplateInput``, is required

        :stability: experimental
        '''
        result = self._values.get("task_definition_template_file")
        return typing.cast(typing.Optional[_ArtifactPath_a5b79113], result)

    @builtins.property
    def task_definition_template_input(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) The artifact containing the ECS task definition template file.

        During deployment, the task definition template file contents
        will be registered with ECS.

        If you use this property, it's assumed the file is called 'taskdef.json'.
        If your task definition template uses a different filename, leave this property empty,
        and use the ``taskDefinitionTemplateFile`` property instead.

        :default: - one of this property, or ``taskDefinitionTemplateFile``, is required

        :stability: experimental
        '''
        result = self._values.get("task_definition_template_input")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeDeployEcsDeployActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodeDeployServerDeployAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.CodeDeployServerDeployAction",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        *,
        deployment_group: _IServerDeploymentGroup_9bf302e3,
        input: _Artifact_9905eec2,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deployment_group: (experimental) The CodeDeploy server Deployment Group to deploy to.
        :param input: (experimental) The source to use as input for deployment.
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = CodeDeployServerDeployActionProps(
            deployment_group=deployment_group,
            input=input,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(CodeDeployServerDeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        _scope: _Construct_e78e779f,
        _stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [_scope, _stage, options]))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.CodeDeployServerDeployActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "deployment_group": "deploymentGroup",
        "input": "input",
    },
)
class CodeDeployServerDeployActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        deployment_group: _IServerDeploymentGroup_9bf302e3,
        input: _Artifact_9905eec2,
    ) -> None:
        '''(experimental) Construction properties of the {@link CodeDeployServerDeployAction CodeDeploy server deploy CodePipeline Action}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param deployment_group: (experimental) The CodeDeploy server Deployment Group to deploy to.
        :param input: (experimental) The source to use as input for deployment.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "deployment_group": deployment_group,
            "input": input,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def deployment_group(self) -> _IServerDeploymentGroup_9bf302e3:
        '''(experimental) The CodeDeploy server Deployment Group to deploy to.

        :stability: experimental
        '''
        result = self._values.get("deployment_group")
        assert result is not None, "Required property 'deployment_group' is missing"
        return typing.cast(_IServerDeploymentGroup_9bf302e3, result)

    @builtins.property
    def input(self) -> _Artifact_9905eec2:
        '''(experimental) The source to use as input for deployment.

        :stability: experimental
        '''
        result = self._values.get("input")
        assert result is not None, "Required property 'input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeDeployServerDeployActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcrSourceAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.EcrSourceAction",
):
    '''(experimental) The ECR Repository source CodePipeline Action.

    Will trigger the pipeline as soon as the target tag in the repository
    changes, but only if there is a CloudTrail Trail in the account that
    captures the ECR event.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        output: _Artifact_9905eec2,
        repository: _IRepository_8b4d2894,
        image_tag: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param output: 
        :param repository: (experimental) The repository that will be watched for changes.
        :param image_tag: (experimental) The image tag that will be checked for changes. Default: 'latest'
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = EcrSourceActionProps(
            output=output,
            repository=repository,
            image_tag=image_tag,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(EcrSourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        _scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [_scope, stage, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variables")
    def variables(self) -> "EcrSourceVariables":
        '''(experimental) The variables emitted by this action.

        :stability: experimental
        '''
        return typing.cast("EcrSourceVariables", jsii.get(self, "variables"))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.EcrSourceActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "output": "output",
        "repository": "repository",
        "image_tag": "imageTag",
    },
)
class EcrSourceActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        output: _Artifact_9905eec2,
        repository: _IRepository_8b4d2894,
        image_tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construction properties of {@link EcrSourceAction}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param output: 
        :param repository: (experimental) The repository that will be watched for changes.
        :param image_tag: (experimental) The image tag that will be checked for changes. Default: 'latest'

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "output": output,
            "repository": repository,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if image_tag is not None:
            self._values["image_tag"] = image_tag

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def output(self) -> _Artifact_9905eec2:
        '''
        :stability: experimental
        '''
        result = self._values.get("output")
        assert result is not None, "Required property 'output' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def repository(self) -> _IRepository_8b4d2894:
        '''(experimental) The repository that will be watched for changes.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(_IRepository_8b4d2894, result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        '''(experimental) The image tag that will be checked for changes.

        :default: 'latest'

        :stability: experimental
        '''
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcrSourceActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.EcrSourceVariables",
    jsii_struct_bases=[],
    name_mapping={
        "image_digest": "imageDigest",
        "image_tag": "imageTag",
        "image_uri": "imageUri",
        "registry_id": "registryId",
        "repository_name": "repositoryName",
    },
)
class EcrSourceVariables:
    def __init__(
        self,
        *,
        image_digest: builtins.str,
        image_tag: builtins.str,
        image_uri: builtins.str,
        registry_id: builtins.str,
        repository_name: builtins.str,
    ) -> None:
        '''(experimental) The CodePipeline variables emitted by the ECR source Action.

        :param image_digest: (experimental) The digest of the current image, in the form ':'.
        :param image_tag: (experimental) The Docker tag of the current image.
        :param image_uri: (experimental) The full ECR Docker URI of the current image.
        :param registry_id: (experimental) The identifier of the registry. In ECR, this is usually the ID of the AWS account owning it.
        :param repository_name: (experimental) The physical name of the repository that this action tracks.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "image_digest": image_digest,
            "image_tag": image_tag,
            "image_uri": image_uri,
            "registry_id": registry_id,
            "repository_name": repository_name,
        }

    @builtins.property
    def image_digest(self) -> builtins.str:
        '''(experimental) The digest of the current image, in the form ':'.

        :stability: experimental
        '''
        result = self._values.get("image_digest")
        assert result is not None, "Required property 'image_digest' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_tag(self) -> builtins.str:
        '''(experimental) The Docker tag of the current image.

        :stability: experimental
        '''
        result = self._values.get("image_tag")
        assert result is not None, "Required property 'image_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_uri(self) -> builtins.str:
        '''(experimental) The full ECR Docker URI of the current image.

        :stability: experimental
        '''
        result = self._values.get("image_uri")
        assert result is not None, "Required property 'image_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def registry_id(self) -> builtins.str:
        '''(experimental) The identifier of the registry.

        In ECR, this is usually the ID of the AWS account owning it.

        :stability: experimental
        '''
        result = self._values.get("registry_id")
        assert result is not None, "Required property 'registry_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''(experimental) The physical name of the repository that this action tracks.

        :stability: experimental
        '''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcrSourceVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsDeployAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.EcsDeployAction",
):
    '''(experimental) CodePipeline Action to deploy an ECS Service.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        service: _IBaseService_f1507c0b,
        deployment_timeout: typing.Optional[_Duration_070aa057] = None,
        image_file: typing.Optional[_ArtifactPath_a5b79113] = None,
        input: typing.Optional[_Artifact_9905eec2] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: (experimental) The ECS Service to deploy.
        :param deployment_timeout: (experimental) Timeout for the ECS deployment in minutes. Value must be between 1-60. Default: - 60 minutes
        :param image_file: (experimental) The name of the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. Use this property if you want to use a different name for this file than the default 'imagedefinitions.json'. If you use this property, you don't need to specify the ``input`` property. Default: - one of this property, or ``input``, is required
        :param input: (experimental) The input artifact that contains the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. If you use this property, it's assumed the file is called 'imagedefinitions.json'. If your build uses a different file, leave this property empty, and use the ``imageFile`` property instead. Default: - one of this property, or ``imageFile``, is required
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = EcsDeployActionProps(
            service=service,
            deployment_timeout=deployment_timeout,
            image_file=image_file,
            input=input,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(EcsDeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        _scope: _Construct_e78e779f,
        _stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [_scope, _stage, options]))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.EcsDeployActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "service": "service",
        "deployment_timeout": "deploymentTimeout",
        "image_file": "imageFile",
        "input": "input",
    },
)
class EcsDeployActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        service: _IBaseService_f1507c0b,
        deployment_timeout: typing.Optional[_Duration_070aa057] = None,
        image_file: typing.Optional[_ArtifactPath_a5b79113] = None,
        input: typing.Optional[_Artifact_9905eec2] = None,
    ) -> None:
        '''(experimental) Construction properties of {@link EcsDeployAction}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param service: (experimental) The ECS Service to deploy.
        :param deployment_timeout: (experimental) Timeout for the ECS deployment in minutes. Value must be between 1-60. Default: - 60 minutes
        :param image_file: (experimental) The name of the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. Use this property if you want to use a different name for this file than the default 'imagedefinitions.json'. If you use this property, you don't need to specify the ``input`` property. Default: - one of this property, or ``input``, is required
        :param input: (experimental) The input artifact that contains the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. If you use this property, it's assumed the file is called 'imagedefinitions.json'. If your build uses a different file, leave this property empty, and use the ``imageFile`` property instead. Default: - one of this property, or ``imageFile``, is required

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "service": service,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if deployment_timeout is not None:
            self._values["deployment_timeout"] = deployment_timeout
        if image_file is not None:
            self._values["image_file"] = image_file
        if input is not None:
            self._values["input"] = input

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def service(self) -> _IBaseService_f1507c0b:
        '''(experimental) The ECS Service to deploy.

        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(_IBaseService_f1507c0b, result)

    @builtins.property
    def deployment_timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Timeout for the ECS deployment in minutes.

        Value must be between 1-60.

        :default: - 60 minutes

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-ECS.html
        :stability: experimental
        '''
        result = self._values.get("deployment_timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def image_file(self) -> typing.Optional[_ArtifactPath_a5b79113]:
        '''(experimental) The name of the JSON image definitions file to use for deployments.

        The JSON file is a list of objects,
        each with 2 keys: ``name`` is the name of the container in the Task Definition,
        and ``imageUri`` is the Docker image URI you want to update your service with.
        Use this property if you want to use a different name for this file than the default 'imagedefinitions.json'.
        If you use this property, you don't need to specify the ``input`` property.

        :default: - one of this property, or ``input``, is required

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-create.html#pipelines-create-image-definitions
        :stability: experimental
        '''
        result = self._values.get("image_file")
        return typing.cast(typing.Optional[_ArtifactPath_a5b79113], result)

    @builtins.property
    def input(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) The input artifact that contains the JSON image definitions file to use for deployments.

        The JSON file is a list of objects,
        each with 2 keys: ``name`` is the name of the container in the Task Definition,
        and ``imageUri`` is the Docker image URI you want to update your service with.
        If you use this property, it's assumed the file is called 'imagedefinitions.json'.
        If your build uses a different file, leave this property empty,
        and use the ``imageFile`` property instead.

        :default: - one of this property, or ``imageFile``, is required

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-create.html#pipelines-create-image-definitions
        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsDeployActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubSourceAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.GitHubSourceAction",
):
    '''(experimental) Source that is provided by a GitHub repository.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        oauth_token: _SecretValue_c18506ef,
        output: _Artifact_9905eec2,
        owner: builtins.str,
        repo: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        trigger: typing.Optional["GitHubTrigger"] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param oauth_token: (experimental) A GitHub OAuth token to use for authentication. It is recommended to use a Secrets Manager ``Secret`` to obtain the token: const oauth = cdk.SecretValue.secretsManager('my-github-token'); new GitHubSource(this, 'GitHubAction', { oauthToken: oauth, ... }); The GitHub Personal Access Token should have these scopes: - **repo** - to read the repository - **admin:repo_hook** - if you plan to use webhooks (true by default)
        :param output: 
        :param owner: (experimental) The GitHub account/user that owns the repo.
        :param repo: (experimental) The name of the repo, without the username.
        :param branch: (experimental) The branch to use. Default: "master"
        :param trigger: (experimental) How AWS CodePipeline should be triggered. With the default value "WEBHOOK", a webhook is created in GitHub that triggers the action With "POLL", CodePipeline periodically checks the source for changes With "None", the action is not triggered through changes in the source To use ``WEBHOOK``, your GitHub Personal Access Token should have **admin:repo_hook** scope (in addition to the regular **repo** scope). Default: GitHubTrigger.WEBHOOK
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = GitHubSourceActionProps(
            oauth_token=oauth_token,
            output=output,
            owner=owner,
            repo=repo,
            branch=branch,
            trigger=trigger,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(GitHubSourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        _options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [scope, stage, _options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variables")
    def variables(self) -> "GitHubSourceVariables":
        '''(experimental) The variables emitted by this action.

        :stability: experimental
        '''
        return typing.cast("GitHubSourceVariables", jsii.get(self, "variables"))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.GitHubSourceActionProps",
    jsii_struct_bases=[_CommonActionProps_4f0e79c2],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "oauth_token": "oauthToken",
        "output": "output",
        "owner": "owner",
        "repo": "repo",
        "branch": "branch",
        "trigger": "trigger",
    },
)
class GitHubSourceActionProps(_CommonActionProps_4f0e79c2):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        oauth_token: _SecretValue_c18506ef,
        output: _Artifact_9905eec2,
        owner: builtins.str,
        repo: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        trigger: typing.Optional["GitHubTrigger"] = None,
    ) -> None:
        '''(experimental) Construction properties of the {@link GitHubSourceAction GitHub source action}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param oauth_token: (experimental) A GitHub OAuth token to use for authentication. It is recommended to use a Secrets Manager ``Secret`` to obtain the token: const oauth = cdk.SecretValue.secretsManager('my-github-token'); new GitHubSource(this, 'GitHubAction', { oauthToken: oauth, ... }); The GitHub Personal Access Token should have these scopes: - **repo** - to read the repository - **admin:repo_hook** - if you plan to use webhooks (true by default)
        :param output: 
        :param owner: (experimental) The GitHub account/user that owns the repo.
        :param repo: (experimental) The name of the repo, without the username.
        :param branch: (experimental) The branch to use. Default: "master"
        :param trigger: (experimental) How AWS CodePipeline should be triggered. With the default value "WEBHOOK", a webhook is created in GitHub that triggers the action With "POLL", CodePipeline periodically checks the source for changes With "None", the action is not triggered through changes in the source To use ``WEBHOOK``, your GitHub Personal Access Token should have **admin:repo_hook** scope (in addition to the regular **repo** scope). Default: GitHubTrigger.WEBHOOK

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "oauth_token": oauth_token,
            "output": output,
            "owner": owner,
            "repo": repo,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if branch is not None:
            self._values["branch"] = branch
        if trigger is not None:
            self._values["trigger"] = trigger

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_token(self) -> _SecretValue_c18506ef:
        '''(experimental) A GitHub OAuth token to use for authentication.

        It is recommended to use a Secrets Manager ``Secret`` to obtain the token:

        const oauth = cdk.SecretValue.secretsManager('my-github-token');
        new GitHubSource(this, 'GitHubAction', { oauthToken: oauth, ... });

        The GitHub Personal Access Token should have these scopes:

        - **repo** - to read the repository
        - **admin:repo_hook** - if you plan to use webhooks (true by default)

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/appendix-github-oauth.html#GitHub-create-personal-token-CLI
        :stability: experimental
        '''
        result = self._values.get("oauth_token")
        assert result is not None, "Required property 'oauth_token' is missing"
        return typing.cast(_SecretValue_c18506ef, result)

    @builtins.property
    def output(self) -> _Artifact_9905eec2:
        '''
        :stability: experimental
        '''
        result = self._values.get("output")
        assert result is not None, "Required property 'output' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) The GitHub account/user that owns the repo.

        :stability: experimental
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo(self) -> builtins.str:
        '''(experimental) The name of the repo, without the username.

        :stability: experimental
        '''
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The branch to use.

        :default: "master"

        :stability: experimental
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger(self) -> typing.Optional["GitHubTrigger"]:
        '''(experimental) How AWS CodePipeline should be triggered.

        With the default value "WEBHOOK", a webhook is created in GitHub that triggers the action
        With "POLL", CodePipeline periodically checks the source for changes
        With "None", the action is not triggered through changes in the source

        To use ``WEBHOOK``, your GitHub Personal Access Token should have
        **admin:repo_hook** scope (in addition to the regular **repo** scope).

        :default: GitHubTrigger.WEBHOOK

        :stability: experimental
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional["GitHubTrigger"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSourceActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.GitHubSourceVariables",
    jsii_struct_bases=[],
    name_mapping={
        "author_date": "authorDate",
        "branch_name": "branchName",
        "commit_id": "commitId",
        "commit_message": "commitMessage",
        "committer_date": "committerDate",
        "commit_url": "commitUrl",
        "repository_name": "repositoryName",
    },
)
class GitHubSourceVariables:
    def __init__(
        self,
        *,
        author_date: builtins.str,
        branch_name: builtins.str,
        commit_id: builtins.str,
        commit_message: builtins.str,
        committer_date: builtins.str,
        commit_url: builtins.str,
        repository_name: builtins.str,
    ) -> None:
        '''(experimental) The CodePipeline variables emitted by GitHub source Action.

        :param author_date: (experimental) The date the currently last commit on the tracked branch was authored, in ISO-8601 format.
        :param branch_name: (experimental) The name of the branch this action tracks.
        :param commit_id: (experimental) The SHA1 hash of the currently last commit on the tracked branch.
        :param commit_message: (experimental) The message of the currently last commit on the tracked branch.
        :param committer_date: (experimental) The date the currently last commit on the tracked branch was committed, in ISO-8601 format.
        :param commit_url: (experimental) The GitHub API URL of the currently last commit on the tracked branch.
        :param repository_name: (experimental) The name of the repository this action points to.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "author_date": author_date,
            "branch_name": branch_name,
            "commit_id": commit_id,
            "commit_message": commit_message,
            "committer_date": committer_date,
            "commit_url": commit_url,
            "repository_name": repository_name,
        }

    @builtins.property
    def author_date(self) -> builtins.str:
        '''(experimental) The date the currently last commit on the tracked branch was authored, in ISO-8601 format.

        :stability: experimental
        '''
        result = self._values.get("author_date")
        assert result is not None, "Required property 'author_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch_name(self) -> builtins.str:
        '''(experimental) The name of the branch this action tracks.

        :stability: experimental
        '''
        result = self._values.get("branch_name")
        assert result is not None, "Required property 'branch_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_id(self) -> builtins.str:
        '''(experimental) The SHA1 hash of the currently last commit on the tracked branch.

        :stability: experimental
        '''
        result = self._values.get("commit_id")
        assert result is not None, "Required property 'commit_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_message(self) -> builtins.str:
        '''(experimental) The message of the currently last commit on the tracked branch.

        :stability: experimental
        '''
        result = self._values.get("commit_message")
        assert result is not None, "Required property 'commit_message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def committer_date(self) -> builtins.str:
        '''(experimental) The date the currently last commit on the tracked branch was committed, in ISO-8601 format.

        :stability: experimental
        '''
        result = self._values.get("committer_date")
        assert result is not None, "Required property 'committer_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_url(self) -> builtins.str:
        '''(experimental) The GitHub API URL of the currently last commit on the tracked branch.

        :stability: experimental
        '''
        result = self._values.get("commit_url")
        assert result is not None, "Required property 'commit_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''(experimental) The name of the repository this action points to.

        :stability: experimental
        '''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSourceVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_codepipeline_actions.GitHubTrigger")
class GitHubTrigger(enum.Enum):
    '''(experimental) If and how the GitHub source action should be triggered.

    :stability: experimental
    '''

    NONE = "NONE"
    '''
    :stability: experimental
    '''
    POLL = "POLL"
    '''
    :stability: experimental
    '''
    WEBHOOK = "WEBHOOK"
    '''
    :stability: experimental
    '''


@jsii.interface(jsii_type="monocdk.aws_codepipeline_actions.IJenkinsProvider")
class IJenkinsProvider(_IConstruct_5a0f9c5e, typing_extensions.Protocol):
    '''(experimental) A Jenkins provider.

    If you want to create a new Jenkins provider managed alongside your CDK code,
    instantiate the {@link JenkinsProvider} class directly.

    If you want to reference an already registered provider,
    use the {@link JenkinsProvider#fromJenkinsProviderAttributes} method.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IJenkinsProviderProxy"]:
        return _IJenkinsProviderProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...


class _IJenkinsProviderProxy(
    jsii.proxy_for(_IConstruct_5a0f9c5e) # type: ignore[misc]
):
    '''(experimental) A Jenkins provider.

    If you want to create a new Jenkins provider managed alongside your CDK code,
    instantiate the {@link JenkinsProvider} class directly.

    If you want to reference an already registered provider,
    use the {@link JenkinsProvider#fromJenkinsProviderAttributes} method.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codepipeline_actions.IJenkinsProvider"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "providerName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serverUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))


class JenkinsAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.JenkinsAction",
):
    '''(experimental) Jenkins build CodePipeline Action.

    :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-four-stage-pipeline.html
    :stability: experimental
    '''

    def __init__(
        self,
        *,
        jenkins_provider: IJenkinsProvider,
        project_name: builtins.str,
        type: "JenkinsActionType",
        inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        outputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param jenkins_provider: (experimental) The Jenkins Provider for this Action.
        :param project_name: (experimental) The name of the project (sometimes also called job, or task) on your Jenkins installation that will be invoked by this Action.
        :param type: (experimental) The type of the Action - Build, or Test.
        :param inputs: (experimental) The source to use as input for this build.
        :param outputs: 
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = JenkinsActionProps(
            jenkins_provider=jenkins_provider,
            project_name=project_name,
            type=type,
            inputs=inputs,
            outputs=outputs,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(JenkinsAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        _scope: _Construct_e78e779f,
        _stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        _options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [_scope, _stage, _options]))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.JenkinsActionProps",
    jsii_struct_bases=[_CommonActionProps_4f0e79c2],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "jenkins_provider": "jenkinsProvider",
        "project_name": "projectName",
        "type": "type",
        "inputs": "inputs",
        "outputs": "outputs",
    },
)
class JenkinsActionProps(_CommonActionProps_4f0e79c2):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        jenkins_provider: IJenkinsProvider,
        project_name: builtins.str,
        type: "JenkinsActionType",
        inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        outputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
    ) -> None:
        '''(experimental) Construction properties of {@link JenkinsAction}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param jenkins_provider: (experimental) The Jenkins Provider for this Action.
        :param project_name: (experimental) The name of the project (sometimes also called job, or task) on your Jenkins installation that will be invoked by this Action.
        :param type: (experimental) The type of the Action - Build, or Test.
        :param inputs: (experimental) The source to use as input for this build.
        :param outputs: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "jenkins_provider": jenkins_provider,
            "project_name": project_name,
            "type": type,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if inputs is not None:
            self._values["inputs"] = inputs
        if outputs is not None:
            self._values["outputs"] = outputs

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jenkins_provider(self) -> IJenkinsProvider:
        '''(experimental) The Jenkins Provider for this Action.

        :stability: experimental
        '''
        result = self._values.get("jenkins_provider")
        assert result is not None, "Required property 'jenkins_provider' is missing"
        return typing.cast(IJenkinsProvider, result)

    @builtins.property
    def project_name(self) -> builtins.str:
        '''(experimental) The name of the project (sometimes also called job, or task) on your Jenkins installation that will be invoked by this Action.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "MyJob"
        '''
        result = self._values.get("project_name")
        assert result is not None, "Required property 'project_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "JenkinsActionType":
        '''(experimental) The type of the Action - Build, or Test.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("JenkinsActionType", result)

    @builtins.property
    def inputs(self) -> typing.Optional[typing.List[_Artifact_9905eec2]]:
        '''(experimental) The source to use as input for this build.

        :stability: experimental
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[typing.List[_Artifact_9905eec2]], result)

    @builtins.property
    def outputs(self) -> typing.Optional[typing.List[_Artifact_9905eec2]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.List[_Artifact_9905eec2]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JenkinsActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_codepipeline_actions.JenkinsActionType")
class JenkinsActionType(enum.Enum):
    '''(experimental) The type of the Jenkins Action that determines its CodePipeline Category - Build, or Test.

    Note that a Jenkins provider, even if it has the same name,
    must be separately registered for each type.

    :stability: experimental
    '''

    BUILD = "BUILD"
    '''(experimental) The Action will have the Build Category.

    :stability: experimental
    '''
    TEST = "TEST"
    '''(experimental) The Action will have the Test Category.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.JenkinsProviderAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "provider_name": "providerName",
        "server_url": "serverUrl",
        "version": "version",
    },
)
class JenkinsProviderAttributes:
    def __init__(
        self,
        *,
        provider_name: builtins.str,
        server_url: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for importing an existing Jenkins provider.

        :param provider_name: (experimental) The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.
        :param server_url: (experimental) The base URL of your Jenkins server.
        :param version: (experimental) The version of your provider. Default: '1'

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "provider_name": provider_name,
            "server_url": server_url,
        }
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def provider_name(self) -> builtins.str:
        '''(experimental) The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "MyJenkinsProvider"
        '''
        result = self._values.get("provider_name")
        assert result is not None, "Required property 'provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_url(self) -> builtins.str:
        '''(experimental) The base URL of your Jenkins server.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "http://myjenkins.com:8080"
        '''
        result = self._values.get("server_url")
        assert result is not None, "Required property 'server_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of your provider.

        :default: '1'

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JenkinsProviderAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.JenkinsProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "provider_name": "providerName",
        "server_url": "serverUrl",
        "for_build": "forBuild",
        "for_test": "forTest",
        "version": "version",
    },
)
class JenkinsProviderProps:
    def __init__(
        self,
        *,
        provider_name: builtins.str,
        server_url: builtins.str,
        for_build: typing.Optional[builtins.bool] = None,
        for_test: typing.Optional[builtins.bool] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param provider_name: (experimental) The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.
        :param server_url: (experimental) The base URL of your Jenkins server.
        :param for_build: (experimental) Whether to immediately register a Jenkins Provider for the build category. The Provider will always be registered if you create a {@link JenkinsAction}. Default: false
        :param for_test: (experimental) Whether to immediately register a Jenkins Provider for the test category. The Provider will always be registered if you create a {@link JenkinsTestAction}. Default: false
        :param version: (experimental) The version of your provider. Default: '1'

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "provider_name": provider_name,
            "server_url": server_url,
        }
        if for_build is not None:
            self._values["for_build"] = for_build
        if for_test is not None:
            self._values["for_test"] = for_test
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def provider_name(self) -> builtins.str:
        '''(experimental) The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "MyJenkinsProvider"
        '''
        result = self._values.get("provider_name")
        assert result is not None, "Required property 'provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_url(self) -> builtins.str:
        '''(experimental) The base URL of your Jenkins server.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "http://myjenkins.com:8080"
        '''
        result = self._values.get("server_url")
        assert result is not None, "Required property 'server_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def for_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to immediately register a Jenkins Provider for the build category.

        The Provider will always be registered if you create a {@link JenkinsAction}.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("for_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def for_test(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to immediately register a Jenkins Provider for the test category.

        The Provider will always be registered if you create a {@link JenkinsTestAction}.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("for_test")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of your provider.

        :default: '1'

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JenkinsProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaInvokeAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.LambdaInvokeAction",
):
    '''(experimental) CodePipeline invoke Action that is provided by an AWS Lambda function.

    :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-invoke-lambda-function.html
    :stability: experimental
    '''

    def __init__(
        self,
        *,
        lambda_: _IFunction_6e14f09e,
        inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        outputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        user_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lambda_: (experimental) The lambda function to invoke.
        :param inputs: (experimental) The optional input Artifacts of the Action. A Lambda Action can have up to 5 inputs. The inputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.inputArtifacts`` path. Default: the Action will not have any inputs
        :param outputs: (experimental) The optional names of the output Artifacts of the Action. A Lambda Action can have up to 5 outputs. The outputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.outputArtifacts`` path. It is the responsibility of the Lambda to upload ZIP files with the Artifact contents to the provided locations. Default: the Action will not have any outputs
        :param user_parameters: (experimental) A set of key-value pairs that will be accessible to the invoked Lambda inside the event that the Pipeline will call it with.
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = LambdaInvokeActionProps(
            lambda_=lambda_,
            inputs=inputs,
            outputs=outputs,
            user_parameters=user_parameters,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(LambdaInvokeAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        scope: _Construct_e78e779f,
        _stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [scope, _stage, options]))

    @jsii.member(jsii_name="variable")
    def variable(self, variable_name: builtins.str) -> builtins.str:
        '''(experimental) Reference a CodePipeline variable defined by the Lambda function this action points to.

        Variables in Lambda invoke actions are defined by calling the PutJobSuccessResult CodePipeline API call
        with the 'outputVariables' property filled.

        :param variable_name: the name of the variable to reference. A variable by this name must be present in the 'outputVariables' section of the PutJobSuccessResult request that the Lambda function calls when the action is invoked

        :see: https://docs.aws.amazon.com/codepipeline/latest/APIReference/API_PutJobSuccessResult.html
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "variable", [variable_name]))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.LambdaInvokeActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "lambda_": "lambda",
        "inputs": "inputs",
        "outputs": "outputs",
        "user_parameters": "userParameters",
    },
)
class LambdaInvokeActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        lambda_: _IFunction_6e14f09e,
        inputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        outputs: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        user_parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''(experimental) Construction properties of the {@link LambdaInvokeAction Lambda invoke CodePipeline Action}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param lambda_: (experimental) The lambda function to invoke.
        :param inputs: (experimental) The optional input Artifacts of the Action. A Lambda Action can have up to 5 inputs. The inputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.inputArtifacts`` path. Default: the Action will not have any inputs
        :param outputs: (experimental) The optional names of the output Artifacts of the Action. A Lambda Action can have up to 5 outputs. The outputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.outputArtifacts`` path. It is the responsibility of the Lambda to upload ZIP files with the Artifact contents to the provided locations. Default: the Action will not have any outputs
        :param user_parameters: (experimental) A set of key-value pairs that will be accessible to the invoked Lambda inside the event that the Pipeline will call it with.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "lambda_": lambda_,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if inputs is not None:
            self._values["inputs"] = inputs
        if outputs is not None:
            self._values["outputs"] = outputs
        if user_parameters is not None:
            self._values["user_parameters"] = user_parameters

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def lambda_(self) -> _IFunction_6e14f09e:
        '''(experimental) The lambda function to invoke.

        :stability: experimental
        '''
        result = self._values.get("lambda_")
        assert result is not None, "Required property 'lambda_' is missing"
        return typing.cast(_IFunction_6e14f09e, result)

    @builtins.property
    def inputs(self) -> typing.Optional[typing.List[_Artifact_9905eec2]]:
        '''(experimental) The optional input Artifacts of the Action.

        A Lambda Action can have up to 5 inputs.
        The inputs will appear in the event passed to the Lambda,
        under the ``'CodePipeline.job'.data.inputArtifacts`` path.

        :default: the Action will not have any inputs

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-invoke-lambda-function.html#actions-invoke-lambda-function-json-event-example
        :stability: experimental
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[typing.List[_Artifact_9905eec2]], result)

    @builtins.property
    def outputs(self) -> typing.Optional[typing.List[_Artifact_9905eec2]]:
        '''(experimental) The optional names of the output Artifacts of the Action.

        A Lambda Action can have up to 5 outputs.
        The outputs will appear in the event passed to the Lambda,
        under the ``'CodePipeline.job'.data.outputArtifacts`` path.
        It is the responsibility of the Lambda to upload ZIP files with the Artifact contents to the provided locations.

        :default: the Action will not have any outputs

        :stability: experimental
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.List[_Artifact_9905eec2]], result)

    @builtins.property
    def user_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) A set of key-value pairs that will be accessible to the invoked Lambda inside the event that the Pipeline will call it with.

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-invoke-lambda-function.html#actions-invoke-lambda-function-json-event-example
        :stability: experimental
        '''
        result = self._values.get("user_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaInvokeActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManualApprovalAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.ManualApprovalAction",
):
    '''(experimental) Manual approval action.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        additional_information: typing.Optional[builtins.str] = None,
        external_entity_link: typing.Optional[builtins.str] = None,
        notification_topic: typing.Optional[_ITopic_465e36b9] = None,
        notify_emails: typing.Optional[typing.List[builtins.str]] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_information: (experimental) Any additional information that you want to include in the notification email message.
        :param external_entity_link: (experimental) URL you want to provide to the reviewer as part of the approval request. Default: - the approval request will not have an external link
        :param notification_topic: (experimental) Optional SNS topic to send notifications to when an approval is pending.
        :param notify_emails: (experimental) A list of email addresses to subscribe to notifications when this Action is pending approval. If this has been provided, but not ``notificationTopic``, a new Topic will be created.
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = ManualApprovalActionProps(
            additional_information=additional_information,
            external_entity_link=external_entity_link,
            notification_topic=notification_topic,
            notify_emails=notify_emails,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(ManualApprovalAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        scope: _Construct_e78e779f,
        _stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [scope, _stage, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationTopic")
    def notification_topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_ITopic_465e36b9], jsii.get(self, "notificationTopic"))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.ManualApprovalActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "additional_information": "additionalInformation",
        "external_entity_link": "externalEntityLink",
        "notification_topic": "notificationTopic",
        "notify_emails": "notifyEmails",
    },
)
class ManualApprovalActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        additional_information: typing.Optional[builtins.str] = None,
        external_entity_link: typing.Optional[builtins.str] = None,
        notification_topic: typing.Optional[_ITopic_465e36b9] = None,
        notify_emails: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''(experimental) Construction properties of the {@link ManualApprovalAction}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param additional_information: (experimental) Any additional information that you want to include in the notification email message.
        :param external_entity_link: (experimental) URL you want to provide to the reviewer as part of the approval request. Default: - the approval request will not have an external link
        :param notification_topic: (experimental) Optional SNS topic to send notifications to when an approval is pending.
        :param notify_emails: (experimental) A list of email addresses to subscribe to notifications when this Action is pending approval. If this has been provided, but not ``notificationTopic``, a new Topic will be created.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if additional_information is not None:
            self._values["additional_information"] = additional_information
        if external_entity_link is not None:
            self._values["external_entity_link"] = external_entity_link
        if notification_topic is not None:
            self._values["notification_topic"] = notification_topic
        if notify_emails is not None:
            self._values["notify_emails"] = notify_emails

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def additional_information(self) -> typing.Optional[builtins.str]:
        '''(experimental) Any additional information that you want to include in the notification email message.

        :stability: experimental
        '''
        result = self._values.get("additional_information")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_entity_link(self) -> typing.Optional[builtins.str]:
        '''(experimental) URL you want to provide to the reviewer as part of the approval request.

        :default: - the approval request will not have an external link

        :stability: experimental
        '''
        result = self._values.get("external_entity_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''(experimental) Optional SNS topic to send notifications to when an approval is pending.

        :stability: experimental
        '''
        result = self._values.get("notification_topic")
        return typing.cast(typing.Optional[_ITopic_465e36b9], result)

    @builtins.property
    def notify_emails(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of email addresses to subscribe to notifications when this Action is pending approval.

        If this has been provided, but not ``notificationTopic``,
        a new Topic will be created.

        :stability: experimental
        '''
        result = self._values.get("notify_emails")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManualApprovalActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3DeployAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.S3DeployAction",
):
    '''(experimental) Deploys the sourceArtifact to Amazon S3.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        bucket: _IBucket_73486e29,
        input: _Artifact_9905eec2,
        access_control: typing.Optional[_BucketAccessControl_a8cb5bce] = None,
        cache_control: typing.Optional[typing.List[CacheControl]] = None,
        extract: typing.Optional[builtins.bool] = None,
        object_key: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: (experimental) The Amazon S3 bucket that is the deploy target.
        :param input: (experimental) The input Artifact to deploy to Amazon S3.
        :param access_control: (experimental) The specified canned ACL to objects deployed to Amazon S3. This overwrites any existing ACL that was applied to the object. Default: - the original object ACL
        :param cache_control: (experimental) The caching behavior for requests/responses for objects in the bucket. The final cache control property will be the result of joining all of the provided array elements with a comma (plus a space after the comma). Default: - none, decided by the HTTP client
        :param extract: (experimental) Should the deploy action extract the artifact before deploying to Amazon S3. Default: true
        :param object_key: (experimental) The key of the target object. This is required if extract is false.
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = S3DeployActionProps(
            bucket=bucket,
            input=input,
            access_control=access_control,
            cache_control=cache_control,
            extract=extract,
            object_key=object_key,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(S3DeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        _scope: _Construct_e78e779f,
        _stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [_scope, _stage, options]))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.S3DeployActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "bucket": "bucket",
        "input": "input",
        "access_control": "accessControl",
        "cache_control": "cacheControl",
        "extract": "extract",
        "object_key": "objectKey",
    },
)
class S3DeployActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        bucket: _IBucket_73486e29,
        input: _Artifact_9905eec2,
        access_control: typing.Optional[_BucketAccessControl_a8cb5bce] = None,
        cache_control: typing.Optional[typing.List[CacheControl]] = None,
        extract: typing.Optional[builtins.bool] = None,
        object_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construction properties of the {@link S3DeployAction S3 deploy Action}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param bucket: (experimental) The Amazon S3 bucket that is the deploy target.
        :param input: (experimental) The input Artifact to deploy to Amazon S3.
        :param access_control: (experimental) The specified canned ACL to objects deployed to Amazon S3. This overwrites any existing ACL that was applied to the object. Default: - the original object ACL
        :param cache_control: (experimental) The caching behavior for requests/responses for objects in the bucket. The final cache control property will be the result of joining all of the provided array elements with a comma (plus a space after the comma). Default: - none, decided by the HTTP client
        :param extract: (experimental) Should the deploy action extract the artifact before deploying to Amazon S3. Default: true
        :param object_key: (experimental) The key of the target object. This is required if extract is false.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "bucket": bucket,
            "input": input,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if access_control is not None:
            self._values["access_control"] = access_control
        if cache_control is not None:
            self._values["cache_control"] = cache_control
        if extract is not None:
            self._values["extract"] = extract
        if object_key is not None:
            self._values["object_key"] = object_key

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def bucket(self) -> _IBucket_73486e29:
        '''(experimental) The Amazon S3 bucket that is the deploy target.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_IBucket_73486e29, result)

    @builtins.property
    def input(self) -> _Artifact_9905eec2:
        '''(experimental) The input Artifact to deploy to Amazon S3.

        :stability: experimental
        '''
        result = self._values.get("input")
        assert result is not None, "Required property 'input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def access_control(self) -> typing.Optional[_BucketAccessControl_a8cb5bce]:
        '''(experimental) The specified canned ACL to objects deployed to Amazon S3.

        This overwrites any existing ACL that was applied to the object.

        :default: - the original object ACL

        :stability: experimental
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[_BucketAccessControl_a8cb5bce], result)

    @builtins.property
    def cache_control(self) -> typing.Optional[typing.List[CacheControl]]:
        '''(experimental) The caching behavior for requests/responses for objects in the bucket.

        The final cache control property will be the result of joining all of the provided array elements with a comma
        (plus a space after the comma).

        :default: - none, decided by the HTTP client

        :stability: experimental
        '''
        result = self._values.get("cache_control")
        return typing.cast(typing.Optional[typing.List[CacheControl]], result)

    @builtins.property
    def extract(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should the deploy action extract the artifact before deploying to Amazon S3.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("extract")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def object_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The key of the target object.

        This is required if extract is false.

        :stability: experimental
        '''
        result = self._values.get("object_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3DeployActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3SourceAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.S3SourceAction",
):
    '''(experimental) Source that is provided by a specific Amazon S3 object.

    Will trigger the pipeline as soon as the S3 object changes, but only if there is
    a CloudTrail Trail in the account that captures the S3 event.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        bucket: _IBucket_73486e29,
        bucket_key: builtins.str,
        output: _Artifact_9905eec2,
        trigger: typing.Optional["S3Trigger"] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: (experimental) The Amazon S3 bucket that stores the source code.
        :param bucket_key: (experimental) The key within the S3 bucket that stores the source code.
        :param output: 
        :param trigger: (experimental) How should CodePipeline detect source changes for this Action. Note that if this is S3Trigger.EVENTS, you need to make sure to include the source Bucket in a CloudTrail Trail, as otherwise the CloudWatch Events will not be emitted. Default: S3Trigger.POLL
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = S3SourceActionProps(
            bucket=bucket,
            bucket_key=bucket_key,
            output=output,
            trigger=trigger,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(S3SourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        _scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [_scope, stage, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variables")
    def variables(self) -> "S3SourceVariables":
        '''(experimental) The variables emitted by this action.

        :stability: experimental
        '''
        return typing.cast("S3SourceVariables", jsii.get(self, "variables"))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.S3SourceActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "bucket": "bucket",
        "bucket_key": "bucketKey",
        "output": "output",
        "trigger": "trigger",
    },
)
class S3SourceActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        bucket: _IBucket_73486e29,
        bucket_key: builtins.str,
        output: _Artifact_9905eec2,
        trigger: typing.Optional["S3Trigger"] = None,
    ) -> None:
        '''(experimental) Construction properties of the {@link S3SourceAction S3 source Action}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param bucket: (experimental) The Amazon S3 bucket that stores the source code.
        :param bucket_key: (experimental) The key within the S3 bucket that stores the source code.
        :param output: 
        :param trigger: (experimental) How should CodePipeline detect source changes for this Action. Note that if this is S3Trigger.EVENTS, you need to make sure to include the source Bucket in a CloudTrail Trail, as otherwise the CloudWatch Events will not be emitted. Default: S3Trigger.POLL

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "bucket": bucket,
            "bucket_key": bucket_key,
            "output": output,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if trigger is not None:
            self._values["trigger"] = trigger

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def bucket(self) -> _IBucket_73486e29:
        '''(experimental) The Amazon S3 bucket that stores the source code.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_IBucket_73486e29, result)

    @builtins.property
    def bucket_key(self) -> builtins.str:
        '''(experimental) The key within the S3 bucket that stores the source code.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "path/to/file.zip"
        '''
        result = self._values.get("bucket_key")
        assert result is not None, "Required property 'bucket_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output(self) -> _Artifact_9905eec2:
        '''
        :stability: experimental
        '''
        result = self._values.get("output")
        assert result is not None, "Required property 'output' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def trigger(self) -> typing.Optional["S3Trigger"]:
        '''(experimental) How should CodePipeline detect source changes for this Action.

        Note that if this is S3Trigger.EVENTS, you need to make sure to include the source Bucket in a CloudTrail Trail,
        as otherwise the CloudWatch Events will not be emitted.

        :default: S3Trigger.POLL

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/log-s3-data-events.html
        :stability: experimental
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional["S3Trigger"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3SourceActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.S3SourceVariables",
    jsii_struct_bases=[],
    name_mapping={"e_tag": "eTag", "version_id": "versionId"},
)
class S3SourceVariables:
    def __init__(self, *, e_tag: builtins.str, version_id: builtins.str) -> None:
        '''(experimental) The CodePipeline variables emitted by the S3 source Action.

        :param e_tag: (experimental) The e-tag of the S3 version of the object that triggered the build.
        :param version_id: (experimental) The identifier of the S3 version of the object that triggered the build.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "e_tag": e_tag,
            "version_id": version_id,
        }

    @builtins.property
    def e_tag(self) -> builtins.str:
        '''(experimental) The e-tag of the S3 version of the object that triggered the build.

        :stability: experimental
        '''
        result = self._values.get("e_tag")
        assert result is not None, "Required property 'e_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_id(self) -> builtins.str:
        '''(experimental) The identifier of the S3 version of the object that triggered the build.

        :stability: experimental
        '''
        result = self._values.get("version_id")
        assert result is not None, "Required property 'version_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3SourceVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_codepipeline_actions.S3Trigger")
class S3Trigger(enum.Enum):
    '''(experimental) How should the S3 Action detect changes.

    This is the type of the {@link S3SourceAction.trigger} property.

    :stability: experimental
    '''

    NONE = "NONE"
    '''(experimental) The Action will never detect changes - the Pipeline it's part of will only begin a run when explicitly started.

    :stability: experimental
    '''
    POLL = "POLL"
    '''(experimental) CodePipeline will poll S3 to detect changes.

    This is the default method of detecting changes.

    :stability: experimental
    '''
    EVENTS = "EVENTS"
    '''(experimental) CodePipeline will use CloudWatch Events to be notified of changes.

    Note that the Bucket that the Action uses needs to be part of a CloudTrail Trail
    for the events to be delivered.

    :stability: experimental
    '''


class ServiceCatalogDeployAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.ServiceCatalogDeployAction",
):
    '''(experimental) CodePipeline action to connect to an existing ServiceCatalog product.

    **Note**: this class is still experimental, and may have breaking changes in the future!

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        product_id: builtins.str,
        product_version_name: builtins.str,
        template_path: _ArtifactPath_a5b79113,
        product_version_description: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param product_id: (experimental) The identifier of the product in the Service Catalog. This product must already exist.
        :param product_version_name: (experimental) The name of the version of the Service Catalog product to be deployed.
        :param template_path: (experimental) The path to the cloudformation artifact.
        :param product_version_description: (experimental) The optional description of this version of the Service Catalog product. Default: ''
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = ServiceCatalogDeployActionProps(
            product_id=product_id,
            product_version_name=product_version_name,
            template_path=template_path,
            product_version_description=product_version_description,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(ServiceCatalogDeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        _scope: _Construct_e78e779f,
        _stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [_scope, _stage, options]))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.ServiceCatalogDeployActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "product_id": "productId",
        "product_version_name": "productVersionName",
        "template_path": "templatePath",
        "product_version_description": "productVersionDescription",
    },
)
class ServiceCatalogDeployActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        product_id: builtins.str,
        product_version_name: builtins.str,
        template_path: _ArtifactPath_a5b79113,
        product_version_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construction properties of the {@link ServiceCatalogDeployAction ServiceCatalog deploy CodePipeline Action}.

        **Note**: this API is still experimental, and may have breaking changes in the future!

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param product_id: (experimental) The identifier of the product in the Service Catalog. This product must already exist.
        :param product_version_name: (experimental) The name of the version of the Service Catalog product to be deployed.
        :param template_path: (experimental) The path to the cloudformation artifact.
        :param product_version_description: (experimental) The optional description of this version of the Service Catalog product. Default: ''

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "product_id": product_id,
            "product_version_name": product_version_name,
            "template_path": template_path,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if product_version_description is not None:
            self._values["product_version_description"] = product_version_description

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def product_id(self) -> builtins.str:
        '''(experimental) The identifier of the product in the Service Catalog.

        This product must already exist.

        :stability: experimental
        '''
        result = self._values.get("product_id")
        assert result is not None, "Required property 'product_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product_version_name(self) -> builtins.str:
        '''(experimental) The name of the version of the Service Catalog product to be deployed.

        :stability: experimental
        '''
        result = self._values.get("product_version_name")
        assert result is not None, "Required property 'product_version_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_path(self) -> _ArtifactPath_a5b79113:
        '''(experimental) The path to the cloudformation artifact.

        :stability: experimental
        '''
        result = self._values.get("template_path")
        assert result is not None, "Required property 'template_path' is missing"
        return typing.cast(_ArtifactPath_a5b79113, result)

    @builtins.property
    def product_version_description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The optional description of this version of the Service Catalog product.

        :default: ''

        :stability: experimental
        '''
        result = self._values.get("product_version_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceCatalogDeployActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StateMachineInput(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.StateMachineInput",
):
    '''(experimental) Represents the input for the StateMachine.

    :stability: experimental
    '''

    @jsii.member(jsii_name="filePath") # type: ignore[misc]
    @builtins.classmethod
    def file_path(cls, input_file: _ArtifactPath_a5b79113) -> "StateMachineInput":
        '''(experimental) When the input type is FilePath, input artifact and filepath must be specified.

        :param input_file: -

        :stability: experimental
        '''
        return typing.cast("StateMachineInput", jsii.sinvoke(cls, "filePath", [input_file]))

    @jsii.member(jsii_name="literal") # type: ignore[misc]
    @builtins.classmethod
    def literal(
        cls,
        object: typing.Mapping[typing.Any, typing.Any],
    ) -> "StateMachineInput":
        '''(experimental) When the input type is Literal, input value is passed directly to the state machine input.

        :param object: -

        :stability: experimental
        '''
        return typing.cast("StateMachineInput", jsii.sinvoke(cls, "literal", [object]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="input")
    def input(self) -> typing.Any:
        '''(experimental) When InputType is set to Literal (default), the Input field is used directly as the input for the state machine execution.

        Otherwise, the state machine is invoked with an empty JSON object {}.

        When InputType is set to FilePath, this field is required.
        An input artifact is also required when InputType is set to FilePath.

        :default: - none

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "input"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="inputArtifact")
    def input_artifact(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) The optional input Artifact of the Action.

        If InputType is set to FilePath, this artifact is required
        and is used to source the input for the state machine execution.

        :default: - the Action will not have any inputs

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-StepFunctions.html#action-reference-StepFunctions-example
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_Artifact_9905eec2], jsii.get(self, "inputArtifact"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="inputType")
    def input_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional StateMachine InputType InputType can be Literal or FilePath.

        :default: - Literal

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputType"))


class StepFunctionInvokeAction(
    Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.StepFunctionInvokeAction",
):
    '''(experimental) StepFunctionInvokeAction that is provided by an AWS CodePipeline.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        state_machine: _IStateMachine_269a89c4,
        execution_name_prefix: typing.Optional[builtins.str] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        state_machine_input: typing.Optional[StateMachineInput] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param state_machine: (experimental) The state machine to invoke.
        :param execution_name_prefix: (experimental) Prefix (optional). By default, the action execution ID is used as the state machine execution name. If a prefix is provided, it is prepended to the action execution ID with a hyphen and together used as the state machine execution name. Default: - action execution ID
        :param output: (experimental) The optional output Artifact of the Action. Default: the Action will not have any outputs
        :param state_machine_input: (experimental) Represents the input to the StateMachine. This includes input artifact, input type and the statemachine input. Default: - none
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set

        :stability: experimental
        '''
        props = StepFunctionsInvokeActionProps(
            state_machine=state_machine,
            execution_name_prefix=execution_name_prefix,
            output=output,
            state_machine_input=state_machine_input,
            role=role,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(StepFunctionInvokeAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        _scope: _Construct_e78e779f,
        _stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param bucket: 
        :param role: 

        :stability: experimental
        '''
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bound", [_scope, _stage, options]))


@jsii.data_type(
    jsii_type="monocdk.aws_codepipeline_actions.StepFunctionsInvokeActionProps",
    jsii_struct_bases=[_CommonAwsActionProps_1494edc0],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "role": "role",
        "state_machine": "stateMachine",
        "execution_name_prefix": "executionNamePrefix",
        "output": "output",
        "state_machine_input": "stateMachineInput",
    },
)
class StepFunctionsInvokeActionProps(_CommonAwsActionProps_1494edc0):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        state_machine: _IStateMachine_269a89c4,
        execution_name_prefix: typing.Optional[builtins.str] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        state_machine_input: typing.Optional[StateMachineInput] = None,
    ) -> None:
        '''(experimental) Construction properties of the {@link StepFunctionsInvokeAction StepFunction Invoke Action}.

        :param action_name: (experimental) The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: (experimental) The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: (experimental) The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param role: (experimental) The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param state_machine: (experimental) The state machine to invoke.
        :param execution_name_prefix: (experimental) Prefix (optional). By default, the action execution ID is used as the state machine execution name. If a prefix is provided, it is prepended to the action execution ID with a hyphen and together used as the state machine execution name. Default: - action execution ID
        :param output: (experimental) The optional output Artifact of the Action. Default: the Action will not have any outputs
        :param state_machine_input: (experimental) Represents the input to the StateMachine. This includes input artifact, input type and the statemachine input. Default: - none

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "state_machine": state_machine,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if role is not None:
            self._values["role"] = role
        if execution_name_prefix is not None:
            self._values["execution_name_prefix"] = execution_name_prefix
        if output is not None:
            self._values["output"] = output
        if state_machine_input is not None:
            self._values["state_machine_input"] = state_machine_input

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The Role in which context's this Action will be executing in.

        The Pipeline's Role will assume this Role
        (the required permissions for that will be granted automatically)
        right before executing this Action.
        This Action will be passed into your {@link IAction.bind}
        method in the {@link ActionBindOptions.role} property.

        :default: a new Role will be generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def state_machine(self) -> _IStateMachine_269a89c4:
        '''(experimental) The state machine to invoke.

        :stability: experimental
        '''
        result = self._values.get("state_machine")
        assert result is not None, "Required property 'state_machine' is missing"
        return typing.cast(_IStateMachine_269a89c4, result)

    @builtins.property
    def execution_name_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix (optional).

        By default, the action execution ID is used as the state machine execution name.
        If a prefix is provided, it is prepended to the action execution ID with a hyphen and
        together used as the state machine execution name.

        :default: - action execution ID

        :stability: experimental
        '''
        result = self._values.get("execution_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) The optional output Artifact of the Action.

        :default: the Action will not have any outputs

        :stability: experimental
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def state_machine_input(self) -> typing.Optional[StateMachineInput]:
        '''(experimental) Represents the input to the StateMachine.

        This includes input artifact, input type and the statemachine input.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("state_machine_input")
        return typing.cast(typing.Optional[StateMachineInput], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StepFunctionsInvokeActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IJenkinsProvider)
class BaseJenkinsProvider(
    _Construct_e78e779f,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_codepipeline_actions.BaseJenkinsProvider",
):
    '''
    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_BaseJenkinsProviderProxy"]:
        return _BaseJenkinsProviderProxy

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: -

        :stability: experimental
        '''
        jsii.create(BaseJenkinsProvider, self, [scope, id, version])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="providerName")
    @abc.abstractmethod
    def provider_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serverUrl")
    @abc.abstractmethod
    def server_url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))


class _BaseJenkinsProviderProxy(BaseJenkinsProvider):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "providerName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serverUrl"))


class JenkinsProvider(
    BaseJenkinsProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codepipeline_actions.JenkinsProvider",
):
    '''(experimental) A class representing Jenkins providers.

    :see: #import
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        provider_name: builtins.str,
        server_url: builtins.str,
        for_build: typing.Optional[builtins.bool] = None,
        for_test: typing.Optional[builtins.bool] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param provider_name: (experimental) The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.
        :param server_url: (experimental) The base URL of your Jenkins server.
        :param for_build: (experimental) Whether to immediately register a Jenkins Provider for the build category. The Provider will always be registered if you create a {@link JenkinsAction}. Default: false
        :param for_test: (experimental) Whether to immediately register a Jenkins Provider for the test category. The Provider will always be registered if you create a {@link JenkinsTestAction}. Default: false
        :param version: (experimental) The version of your provider. Default: '1'

        :stability: experimental
        '''
        props = JenkinsProviderProps(
            provider_name=provider_name,
            server_url=server_url,
            for_build=for_build,
            for_test=for_test,
            version=version,
        )

        jsii.create(JenkinsProvider, self, [scope, id, props])

    @jsii.member(jsii_name="fromJenkinsProviderAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_jenkins_provider_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        provider_name: builtins.str,
        server_url: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> IJenkinsProvider:
        '''(experimental) Import a Jenkins provider registered either outside the CDK, or in a different CDK Stack.

        :param scope: the parent Construct for the new provider.
        :param id: the identifier of the new provider Construct.
        :param provider_name: (experimental) The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.
        :param server_url: (experimental) The base URL of your Jenkins server.
        :param version: (experimental) The version of your provider. Default: '1'

        :return: a new Construct representing a reference to an existing Jenkins provider

        :stability: experimental
        '''
        attrs = JenkinsProviderAttributes(
            provider_name=provider_name, server_url=server_url, version=version
        )

        return typing.cast(IJenkinsProvider, jsii.sinvoke(cls, "fromJenkinsProviderAttributes", [scope, id, attrs]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "providerName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "serverUrl"))


__all__ = [
    "Action",
    "AlexaSkillDeployAction",
    "AlexaSkillDeployActionProps",
    "BaseJenkinsProvider",
    "BitBucketSourceAction",
    "BitBucketSourceActionProps",
    "CacheControl",
    "CloudFormationCreateReplaceChangeSetAction",
    "CloudFormationCreateReplaceChangeSetActionProps",
    "CloudFormationCreateUpdateStackAction",
    "CloudFormationCreateUpdateStackActionProps",
    "CloudFormationDeleteStackAction",
    "CloudFormationDeleteStackActionProps",
    "CloudFormationExecuteChangeSetAction",
    "CloudFormationExecuteChangeSetActionProps",
    "CodeBuildAction",
    "CodeBuildActionProps",
    "CodeBuildActionType",
    "CodeCommitSourceAction",
    "CodeCommitSourceActionProps",
    "CodeCommitSourceVariables",
    "CodeCommitTrigger",
    "CodeDeployEcsContainerImageInput",
    "CodeDeployEcsDeployAction",
    "CodeDeployEcsDeployActionProps",
    "CodeDeployServerDeployAction",
    "CodeDeployServerDeployActionProps",
    "EcrSourceAction",
    "EcrSourceActionProps",
    "EcrSourceVariables",
    "EcsDeployAction",
    "EcsDeployActionProps",
    "GitHubSourceAction",
    "GitHubSourceActionProps",
    "GitHubSourceVariables",
    "GitHubTrigger",
    "IJenkinsProvider",
    "JenkinsAction",
    "JenkinsActionProps",
    "JenkinsActionType",
    "JenkinsProvider",
    "JenkinsProviderAttributes",
    "JenkinsProviderProps",
    "LambdaInvokeAction",
    "LambdaInvokeActionProps",
    "ManualApprovalAction",
    "ManualApprovalActionProps",
    "S3DeployAction",
    "S3DeployActionProps",
    "S3SourceAction",
    "S3SourceActionProps",
    "S3SourceVariables",
    "S3Trigger",
    "ServiceCatalogDeployAction",
    "ServiceCatalogDeployActionProps",
    "StateMachineInput",
    "StepFunctionInvokeAction",
    "StepFunctionsInvokeActionProps",
]

publication.publish()
