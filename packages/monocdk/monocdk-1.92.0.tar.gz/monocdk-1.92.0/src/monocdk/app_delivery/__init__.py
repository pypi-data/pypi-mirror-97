import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import Construct as _Construct_e78e779f, Stack as _Stack_9f43e4a3
from ..aws_cloudformation import (
    CloudFormationCapabilities as _CloudFormationCapabilities_149b400e
)
from ..aws_codepipeline import (
    ActionBindOptions as _ActionBindOptions_20e0a317,
    ActionConfig as _ActionConfig_0c698b52,
    ActionProperties as _ActionProperties_c7760ac6,
    Artifact as _Artifact_9905eec2,
    IAction as _IAction_ecd54a08,
    IStage as _IStage_5a7e7342,
)
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
from ..aws_s3 import IBucket as _IBucket_73486e29


@jsii.implements(_IAction_ecd54a08)
class PipelineDeployStackAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.app_delivery.PipelineDeployStackAction",
):
    '''(experimental) A class to deploy a stack that is part of a CDK App, using CodePipeline.

    This composite Action takes care of preparing and executing a CloudFormation ChangeSet.

    It currently does *not* support stacks that make use of ``Asset``s, and
    requires the deployed stack is in the same account and region where the
    CodePipeline is hosted.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        admin_permissions: builtins.bool,
        input: _Artifact_9905eec2,
        stack: _Stack_9f43e4a3,
        capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        create_change_set_action_name: typing.Optional[builtins.str] = None,
        create_change_set_run_order: typing.Optional[jsii.Number] = None,
        execute_change_set_action_name: typing.Optional[builtins.str] = None,
        execute_change_set_run_order: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param admin_permissions: (experimental) Whether to grant admin permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have admin (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param input: (experimental) The CodePipeline artifact that holds the synthesized app, which is the contents of the ``<directory>`` when running ``cdk synth -o <directory>``.
        :param stack: (experimental) The CDK stack to be deployed.
        :param capabilities: (experimental) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify AnonymousIAM if your stack template contains AWS Identity and Access Management (IAM) resources. For more information Default: [AnonymousIAM, AutoExpand], unless ``adminPermissions`` is true
        :param change_set_name: (experimental) The name to use when creating a ChangeSet for the stack. Default: CDK-CodePipeline-ChangeSet
        :param create_change_set_action_name: (experimental) The name of the CodePipeline action creating the ChangeSet. Default: 'ChangeSet'
        :param create_change_set_run_order: (experimental) The runOrder for the CodePipeline action creating the ChangeSet. Default: 1
        :param execute_change_set_action_name: (experimental) The name of the CodePipeline action creating the ChangeSet. Default: 'Execute'
        :param execute_change_set_run_order: (experimental) The runOrder for the CodePipeline action executing the ChangeSet. Default: ``createChangeSetRunOrder + 1``
        :param role: (experimental) IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have admin permissions. Default: A fresh role with admin or no permissions (depending on the value of ``adminPermissions``).

        :stability: experimental
        '''
        props = PipelineDeployStackActionProps(
            admin_permissions=admin_permissions,
            input=input,
            stack=stack,
            capabilities=capabilities,
            change_set_name=change_set_name,
            create_change_set_action_name=create_change_set_action_name,
            create_change_set_run_order=create_change_set_run_order,
            execute_change_set_action_name=execute_change_set_action_name,
            execute_change_set_run_order=execute_change_set_run_order,
            role=role,
        )

        jsii.create(PipelineDeployStackAction, self, [props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> None:
        '''(experimental) Add policy statements to the role deploying the stack.

        This role is passed to CloudFormation and must have the IAM permissions
        necessary to deploy the stack or you can grant this role ``adminPermissions``
        by using that option during creation. If you do not grant
        ``adminPermissions`` you need to identify the proper statements to add to
        this role based on the CloudFormation Resources in your stack.

        :param statement: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addToDeploymentRolePolicy", [statement]))

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

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_c7760ac6:
        '''
        :stability: experimental
        '''
        return typing.cast(_ActionProperties_c7760ac6, jsii.get(self, "actionProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> _IRole_59af6f50:
        '''
        :stability: experimental
        '''
        return typing.cast(_IRole_59af6f50, jsii.get(self, "deploymentRole"))


@jsii.data_type(
    jsii_type="monocdk.app_delivery.PipelineDeployStackActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "admin_permissions": "adminPermissions",
        "input": "input",
        "stack": "stack",
        "capabilities": "capabilities",
        "change_set_name": "changeSetName",
        "create_change_set_action_name": "createChangeSetActionName",
        "create_change_set_run_order": "createChangeSetRunOrder",
        "execute_change_set_action_name": "executeChangeSetActionName",
        "execute_change_set_run_order": "executeChangeSetRunOrder",
        "role": "role",
    },
)
class PipelineDeployStackActionProps:
    def __init__(
        self,
        *,
        admin_permissions: builtins.bool,
        input: _Artifact_9905eec2,
        stack: _Stack_9f43e4a3,
        capabilities: typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        create_change_set_action_name: typing.Optional[builtins.str] = None,
        create_change_set_run_order: typing.Optional[jsii.Number] = None,
        execute_change_set_action_name: typing.Optional[builtins.str] = None,
        execute_change_set_run_order: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param admin_permissions: (experimental) Whether to grant admin permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have admin (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param input: (experimental) The CodePipeline artifact that holds the synthesized app, which is the contents of the ``<directory>`` when running ``cdk synth -o <directory>``.
        :param stack: (experimental) The CDK stack to be deployed.
        :param capabilities: (experimental) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify AnonymousIAM if your stack template contains AWS Identity and Access Management (IAM) resources. For more information Default: [AnonymousIAM, AutoExpand], unless ``adminPermissions`` is true
        :param change_set_name: (experimental) The name to use when creating a ChangeSet for the stack. Default: CDK-CodePipeline-ChangeSet
        :param create_change_set_action_name: (experimental) The name of the CodePipeline action creating the ChangeSet. Default: 'ChangeSet'
        :param create_change_set_run_order: (experimental) The runOrder for the CodePipeline action creating the ChangeSet. Default: 1
        :param execute_change_set_action_name: (experimental) The name of the CodePipeline action creating the ChangeSet. Default: 'Execute'
        :param execute_change_set_run_order: (experimental) The runOrder for the CodePipeline action executing the ChangeSet. Default: ``createChangeSetRunOrder + 1``
        :param role: (experimental) IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have admin permissions. Default: A fresh role with admin or no permissions (depending on the value of ``adminPermissions``).

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "admin_permissions": admin_permissions,
            "input": input,
            "stack": stack,
        }
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if create_change_set_action_name is not None:
            self._values["create_change_set_action_name"] = create_change_set_action_name
        if create_change_set_run_order is not None:
            self._values["create_change_set_run_order"] = create_change_set_run_order
        if execute_change_set_action_name is not None:
            self._values["execute_change_set_action_name"] = execute_change_set_action_name
        if execute_change_set_run_order is not None:
            self._values["execute_change_set_run_order"] = execute_change_set_run_order
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def admin_permissions(self) -> builtins.bool:
        '''(experimental) Whether to grant admin permissions to CloudFormation while deploying this template.

        Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you
        don't specify any alternatives.

        The default role that will be created for you will have admin (i.e., ``*``)
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
    def input(self) -> _Artifact_9905eec2:
        '''(experimental) The CodePipeline artifact that holds the synthesized app, which is the contents of the ``<directory>`` when running ``cdk synth -o <directory>``.

        :stability: experimental
        '''
        result = self._values.get("input")
        assert result is not None, "Required property 'input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def stack(self) -> _Stack_9f43e4a3:
        '''(experimental) The CDK stack to be deployed.

        :stability: experimental
        '''
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return typing.cast(_Stack_9f43e4a3, result)

    @builtins.property
    def capabilities(
        self,
    ) -> typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]]:
        '''(experimental) Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation
        might create or update those resources. For example, you must specify AnonymousIAM if your
        stack template contains AWS Identity and Access Management (IAM) resources. For more
        information

        :default: [AnonymousIAM, AutoExpand], unless ``adminPermissions`` is true

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        :stability: experimental
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[_CloudFormationCapabilities_149b400e]], result)

    @builtins.property
    def change_set_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name to use when creating a ChangeSet for the stack.

        :default: CDK-CodePipeline-ChangeSet

        :stability: experimental
        '''
        result = self._values.get("change_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_change_set_action_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the CodePipeline action creating the ChangeSet.

        :default: 'ChangeSet'

        :stability: experimental
        '''
        result = self._values.get("create_change_set_action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_change_set_run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder for the CodePipeline action creating the ChangeSet.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("create_change_set_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def execute_change_set_action_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the CodePipeline action creating the ChangeSet.

        :default: 'Execute'

        :stability: experimental
        '''
        result = self._values.get("execute_change_set_action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execute_change_set_run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder for the CodePipeline action executing the ChangeSet.

        :default: ``createChangeSetRunOrder + 1``

        :stability: experimental
        '''
        result = self._values.get("execute_change_set_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) IAM role to assume when deploying changes.

        If not specified, a fresh role is created. The role is created with zero
        permissions unless ``adminPermissions`` is true, in which case the role will have
        admin permissions.

        :default: A fresh role with admin or no permissions (depending on the value of ``adminPermissions``).

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineDeployStackActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PipelineDeployStackAction",
    "PipelineDeployStackActionProps",
]

publication.publish()
