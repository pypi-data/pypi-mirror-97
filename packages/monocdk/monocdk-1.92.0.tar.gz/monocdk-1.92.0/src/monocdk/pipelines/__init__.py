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
    CfnOutput as _CfnOutput_a4d857a8,
    Construct as _Construct_e78e779f,
    Stage as _Stage_9729985a,
)
from ..aws_codebuild import (
    BuildEnvironment as _BuildEnvironment_77bc5f50,
    BuildEnvironmentVariable as _BuildEnvironmentVariable_00095c97,
    IProject as _IProject_6da8803e,
)
from ..aws_codepipeline import (
    ActionBindOptions as _ActionBindOptions_20e0a317,
    ActionConfig as _ActionConfig_0c698b52,
    ActionProperties as _ActionProperties_c7760ac6,
    Artifact as _Artifact_9905eec2,
    ArtifactPath as _ArtifactPath_a5b79113,
    IAction as _IAction_ecd54a08,
    IStage as _IStage_5a7e7342,
    Pipeline as _Pipeline_7744fe74,
)
from ..aws_ec2 import (
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
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
    IGrantable as _IGrantable_4c5a91d1,
    IPrincipal as _IPrincipal_93b48231,
    IRole as _IRole_59af6f50,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_s3 import IBucket as _IBucket_73486e29
from ..cx_api import (
    CloudFormationStackArtifact as _CloudFormationStackArtifact_45074b84
)


@jsii.data_type(
    jsii_type="monocdk.pipelines.AddManualApprovalOptions",
    jsii_struct_bases=[],
    name_mapping={"action_name": "actionName", "run_order": "runOrder"},
)
class AddManualApprovalOptions:
    def __init__(
        self,
        *,
        action_name: typing.Optional[builtins.str] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Options for addManualApproval.

        :param action_name: (experimental) The name of the manual approval action. Default: 'ManualApproval' with a rolling counter
        :param run_order: (experimental) The runOrder for this action. Default: - The next sequential runOrder

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if action_name is not None:
            self._values["action_name"] = action_name
        if run_order is not None:
            self._values["run_order"] = run_order

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the manual approval action.

        :default: 'ManualApproval' with a rolling counter

        :stability: experimental
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The runOrder for this action.

        :default: - The next sequential runOrder

        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddManualApprovalOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.AddStackOptions",
    jsii_struct_bases=[],
    name_mapping={"execute_run_order": "executeRunOrder", "run_order": "runOrder"},
)
class AddStackOptions:
    def __init__(
        self,
        *,
        execute_run_order: typing.Optional[jsii.Number] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Additional options for adding a stack deployment.

        :param execute_run_order: (experimental) Base runorder. Default: - runOrder + 1
        :param run_order: (experimental) Base runorder. Default: - Next sequential runorder

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if run_order is not None:
            self._values["run_order"] = run_order

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Base runorder.

        :default: - runOrder + 1

        :stability: experimental
        '''
        result = self._values.get("execute_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Base runorder.

        :default: - Next sequential runorder

        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddStackOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.AddStageOptions",
    jsii_struct_bases=[],
    name_mapping={
        "extra_run_order_space": "extraRunOrderSpace",
        "manual_approvals": "manualApprovals",
    },
)
class AddStageOptions:
    def __init__(
        self,
        *,
        extra_run_order_space: typing.Optional[jsii.Number] = None,
        manual_approvals: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for adding an application stage to a pipeline.

        :param extra_run_order_space: (experimental) Add room for extra actions. You can use this to make extra room in the runOrder sequence between the changeset 'prepare' and 'execute' actions and insert your own actions there. Default: 0
        :param manual_approvals: (experimental) Add manual approvals before executing change sets. This gives humans the opportunity to confirm the change set looks alright before deploying it. Default: false

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if extra_run_order_space is not None:
            self._values["extra_run_order_space"] = extra_run_order_space
        if manual_approvals is not None:
            self._values["manual_approvals"] = manual_approvals

    @builtins.property
    def extra_run_order_space(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Add room for extra actions.

        You can use this to make extra room in the runOrder sequence between the
        changeset 'prepare' and 'execute' actions and insert your own actions there.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("extra_run_order_space")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def manual_approvals(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add manual approvals before executing change sets.

        This gives humans the opportunity to confirm the change set looks alright
        before deploying it.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("manual_approvals")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddStageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.AdditionalArtifact",
    jsii_struct_bases=[],
    name_mapping={"artifact": "artifact", "directory": "directory"},
)
class AdditionalArtifact:
    def __init__(
        self,
        *,
        artifact: _Artifact_9905eec2,
        directory: builtins.str,
    ) -> None:
        '''(experimental) Specification of an additional artifact to generate.

        :param artifact: (experimental) Artifact to represent the build directory in the pipeline.
        :param directory: (experimental) Directory to be packaged.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "artifact": artifact,
            "directory": directory,
        }

    @builtins.property
    def artifact(self) -> _Artifact_9905eec2:
        '''(experimental) Artifact to represent the build directory in the pipeline.

        :stability: experimental
        '''
        result = self._values.get("artifact")
        assert result is not None, "Required property 'artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def directory(self) -> builtins.str:
        '''(experimental) Directory to be packaged.

        :stability: experimental
        '''
        result = self._values.get("directory")
        assert result is not None, "Required property 'directory' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdditionalArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.AssetPublishingCommand",
    jsii_struct_bases=[],
    name_mapping={
        "asset_id": "assetId",
        "asset_manifest_path": "assetManifestPath",
        "asset_selector": "assetSelector",
        "asset_type": "assetType",
    },
)
class AssetPublishingCommand:
    def __init__(
        self,
        *,
        asset_id: builtins.str,
        asset_manifest_path: builtins.str,
        asset_selector: builtins.str,
        asset_type: "AssetType",
    ) -> None:
        '''(experimental) Instructions to publish certain assets.

        :param asset_id: (experimental) Asset identifier.
        :param asset_manifest_path: (experimental) Asset manifest path.
        :param asset_selector: (experimental) Asset selector to pass to ``cdk-assets``.
        :param asset_type: (experimental) Type of asset to publish.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "asset_id": asset_id,
            "asset_manifest_path": asset_manifest_path,
            "asset_selector": asset_selector,
            "asset_type": asset_type,
        }

    @builtins.property
    def asset_id(self) -> builtins.str:
        '''(experimental) Asset identifier.

        :stability: experimental
        '''
        result = self._values.get("asset_id")
        assert result is not None, "Required property 'asset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_manifest_path(self) -> builtins.str:
        '''(experimental) Asset manifest path.

        :stability: experimental
        '''
        result = self._values.get("asset_manifest_path")
        assert result is not None, "Required property 'asset_manifest_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_selector(self) -> builtins.str:
        '''(experimental) Asset selector to pass to ``cdk-assets``.

        :stability: experimental
        '''
        result = self._values.get("asset_selector")
        assert result is not None, "Required property 'asset_selector' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_type(self) -> "AssetType":
        '''(experimental) Type of asset to publish.

        :stability: experimental
        '''
        result = self._values.get("asset_type")
        assert result is not None, "Required property 'asset_type' is missing"
        return typing.cast("AssetType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetPublishingCommand(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.pipelines.AssetType")
class AssetType(enum.Enum):
    '''(experimental) Type of the asset that is being published.

    :stability: experimental
    '''

    FILE = "FILE"
    '''(experimental) A file.

    :stability: experimental
    '''
    DOCKER_IMAGE = "DOCKER_IMAGE"
    '''(experimental) A Docker image.

    :stability: experimental
    '''


class CdkPipeline(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.CdkPipeline",
):
    '''(experimental) A Pipeline to deploy CDK apps.

    Defines an AWS CodePipeline-based Pipeline to deploy CDK applications.

    Automatically manages the following:

    - Stack dependency order.
    - Asset publishing.
    - Keeping the pipeline up-to-date as the CDK apps change.
    - Using stack outputs later on in the pipeline.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        code_pipeline: typing.Optional[_Pipeline_7744fe74] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        self_mutating: typing.Optional[builtins.bool] = None,
        source_action: typing.Optional[_IAction_ecd54a08] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        synth_action: typing.Optional[_IAction_ecd54a08] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cloud_assembly_artifact: (experimental) The artifact you have defined to be the artifact to hold the cloudAssemblyArtifact for the synth action.
        :param cdk_cli_version: (experimental) CDK CLI version to use in pipeline. Some Actions in the pipeline will download and run a version of the CDK CLI. Specify the version here. Default: - Latest version
        :param code_pipeline: (experimental) Existing CodePipeline to add deployment stages to. Use this if you want more control over the CodePipeline that gets created. You can choose to not pass this value, in which case a new CodePipeline is created with default settings. If you pass an existing CodePipeline, it should should have been created with ``restartExecutionOnUpdate: true``. [disable-awslint:ref-via-interface] Default: - A new CodePipeline is automatically generated
        :param cross_account_keys: (experimental) Create KMS keys for cross-account deployments. This controls whether the pipeline is enabled for cross-account deployments. Can only be set if ``codePipeline`` is not set. By default cross-account deployments are enabled, but this feature requires that KMS Customer Master Keys are created which have a cost of $1/month. If you do not need cross-account deployments, you can set this to ``false`` to not create those keys and save on that cost (the artifact bucket will be encrypted with an AWS-managed key). However, cross-account deployments will no longer be possible. Default: true
        :param pipeline_name: (experimental) Name of the pipeline. Can only be set if ``codePipeline`` is not set. Default: - A name is automatically generated
        :param self_mutating: (experimental) Whether the pipeline will update itself. This needs to be set to ``true`` to allow the pipeline to reconfigure itself when assets or stages are being added to it, and ``true`` is the recommended setting. You can temporarily set this to ``false`` while you are iterating on the pipeline itself and prefer to deploy changes using ``cdk deploy``. Default: true
        :param source_action: (experimental) The CodePipeline action used to retrieve the CDK app's source. Default: - Required unless ``codePipeline`` is given
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param synth_action: (experimental) The CodePipeline action build and synthesis step of the CDK app. Default: - Required unless ``codePipeline`` or ``sourceAction`` is given
        :param vpc: (experimental) The VPC where to execute the CdkPipeline actions. Default: - No VPC

        :stability: experimental
        '''
        props = CdkPipelineProps(
            cloud_assembly_artifact=cloud_assembly_artifact,
            cdk_cli_version=cdk_cli_version,
            code_pipeline=code_pipeline,
            cross_account_keys=cross_account_keys,
            pipeline_name=pipeline_name,
            self_mutating=self_mutating,
            source_action=source_action,
            subnet_selection=subnet_selection,
            synth_action=synth_action,
            vpc=vpc,
        )

        jsii.create(CdkPipeline, self, [scope, id, props])

    @jsii.member(jsii_name="addApplicationStage")
    def add_application_stage(
        self,
        app_stage: _Stage_9729985a,
        *,
        extra_run_order_space: typing.Optional[jsii.Number] = None,
        manual_approvals: typing.Optional[builtins.bool] = None,
    ) -> "CdkStage":
        '''(experimental) Add pipeline stage that will deploy the given application stage.

        The application construct should subclass ``Stage`` and can contain any
        number of ``Stacks`` inside it that may have dependency relationships
        on one another.

        All stacks in the application will be deployed in the appropriate order,
        and all assets found in the application will be added to the asset
        publishing stage.

        :param app_stage: -
        :param extra_run_order_space: (experimental) Add room for extra actions. You can use this to make extra room in the runOrder sequence between the changeset 'prepare' and 'execute' actions and insert your own actions there. Default: 0
        :param manual_approvals: (experimental) Add manual approvals before executing change sets. This gives humans the opportunity to confirm the change set looks alright before deploying it. Default: false

        :stability: experimental
        '''
        options = AddStageOptions(
            extra_run_order_space=extra_run_order_space,
            manual_approvals=manual_approvals,
        )

        return typing.cast("CdkStage", jsii.invoke(self, "addApplicationStage", [app_stage, options]))

    @jsii.member(jsii_name="addStage")
    def add_stage(self, stage_name: builtins.str) -> "CdkStage":
        '''(experimental) Add a new, empty stage to the pipeline.

        Prefer to use ``addApplicationStage`` if you are intended to deploy a CDK
        application, but you can use this method if you want to add other kinds of
        Actions to a pipeline.

        :param stage_name: -

        :stability: experimental
        '''
        return typing.cast("CdkStage", jsii.invoke(self, "addStage", [stage_name]))

    @jsii.member(jsii_name="stackOutput")
    def stack_output(self, cfn_output: _CfnOutput_a4d857a8) -> "StackOutput":
        '''(experimental) Get the StackOutput object that holds this CfnOutput's value in this pipeline.

        ``StackOutput`` can be used in validation actions later in the pipeline.

        :param cfn_output: -

        :stability: experimental
        '''
        return typing.cast("StackOutput", jsii.invoke(self, "stackOutput", [cfn_output]))

    @jsii.member(jsii_name="stage")
    def stage(self, stage_name: builtins.str) -> _IStage_5a7e7342:
        '''(experimental) Access one of the pipeline's stages by stage name.

        You can use this to add more Actions to a stage.

        :param stage_name: -

        :stability: experimental
        '''
        return typing.cast(_IStage_5a7e7342, jsii.invoke(self, "stage", [stage_name]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate that we don't have any stacks violating dependency order in the pipeline.

        Our own convenience methods will never generate a pipeline that does that (although
        this is a nice verification), but a user can also add the stacks by hand.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="codePipeline")
    def code_pipeline(self) -> _Pipeline_7744fe74:
        '''(experimental) The underlying CodePipeline object.

        You can use this to add more Stages to the pipeline, or Actions
        to Stages.

        :stability: experimental
        '''
        return typing.cast(_Pipeline_7744fe74, jsii.get(self, "codePipeline"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.CdkPipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "cdk_cli_version": "cdkCliVersion",
        "code_pipeline": "codePipeline",
        "cross_account_keys": "crossAccountKeys",
        "pipeline_name": "pipelineName",
        "self_mutating": "selfMutating",
        "source_action": "sourceAction",
        "subnet_selection": "subnetSelection",
        "synth_action": "synthAction",
        "vpc": "vpc",
    },
)
class CdkPipelineProps:
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        code_pipeline: typing.Optional[_Pipeline_7744fe74] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        self_mutating: typing.Optional[builtins.bool] = None,
        source_action: typing.Optional[_IAction_ecd54a08] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        synth_action: typing.Optional[_IAction_ecd54a08] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''(experimental) Properties for a CdkPipeline.

        :param cloud_assembly_artifact: (experimental) The artifact you have defined to be the artifact to hold the cloudAssemblyArtifact for the synth action.
        :param cdk_cli_version: (experimental) CDK CLI version to use in pipeline. Some Actions in the pipeline will download and run a version of the CDK CLI. Specify the version here. Default: - Latest version
        :param code_pipeline: (experimental) Existing CodePipeline to add deployment stages to. Use this if you want more control over the CodePipeline that gets created. You can choose to not pass this value, in which case a new CodePipeline is created with default settings. If you pass an existing CodePipeline, it should should have been created with ``restartExecutionOnUpdate: true``. [disable-awslint:ref-via-interface] Default: - A new CodePipeline is automatically generated
        :param cross_account_keys: (experimental) Create KMS keys for cross-account deployments. This controls whether the pipeline is enabled for cross-account deployments. Can only be set if ``codePipeline`` is not set. By default cross-account deployments are enabled, but this feature requires that KMS Customer Master Keys are created which have a cost of $1/month. If you do not need cross-account deployments, you can set this to ``false`` to not create those keys and save on that cost (the artifact bucket will be encrypted with an AWS-managed key). However, cross-account deployments will no longer be possible. Default: true
        :param pipeline_name: (experimental) Name of the pipeline. Can only be set if ``codePipeline`` is not set. Default: - A name is automatically generated
        :param self_mutating: (experimental) Whether the pipeline will update itself. This needs to be set to ``true`` to allow the pipeline to reconfigure itself when assets or stages are being added to it, and ``true`` is the recommended setting. You can temporarily set this to ``false`` while you are iterating on the pipeline itself and prefer to deploy changes using ``cdk deploy``. Default: true
        :param source_action: (experimental) The CodePipeline action used to retrieve the CDK app's source. Default: - Required unless ``codePipeline`` is given
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param synth_action: (experimental) The CodePipeline action build and synthesis step of the CDK app. Default: - Required unless ``codePipeline`` or ``sourceAction`` is given
        :param vpc: (experimental) The VPC where to execute the CdkPipeline actions. Default: - No VPC

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
        }
        if cdk_cli_version is not None:
            self._values["cdk_cli_version"] = cdk_cli_version
        if code_pipeline is not None:
            self._values["code_pipeline"] = code_pipeline
        if cross_account_keys is not None:
            self._values["cross_account_keys"] = cross_account_keys
        if pipeline_name is not None:
            self._values["pipeline_name"] = pipeline_name
        if self_mutating is not None:
            self._values["self_mutating"] = self_mutating
        if source_action is not None:
            self._values["source_action"] = source_action
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if synth_action is not None:
            self._values["synth_action"] = synth_action
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_9905eec2:
        '''(experimental) The artifact you have defined to be the artifact to hold the cloudAssemblyArtifact for the synth action.

        :stability: experimental
        '''
        result = self._values.get("cloud_assembly_artifact")
        assert result is not None, "Required property 'cloud_assembly_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def cdk_cli_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) CDK CLI version to use in pipeline.

        Some Actions in the pipeline will download and run a version of the CDK
        CLI. Specify the version here.

        :default: - Latest version

        :stability: experimental
        '''
        result = self._values.get("cdk_cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_pipeline(self) -> typing.Optional[_Pipeline_7744fe74]:
        '''(experimental) Existing CodePipeline to add deployment stages to.

        Use this if you want more control over the CodePipeline that gets created.
        You can choose to not pass this value, in which case a new CodePipeline is
        created with default settings.

        If you pass an existing CodePipeline, it should should have been created
        with ``restartExecutionOnUpdate: true``.

        [disable-awslint:ref-via-interface]

        :default: - A new CodePipeline is automatically generated

        :stability: experimental
        '''
        result = self._values.get("code_pipeline")
        return typing.cast(typing.Optional[_Pipeline_7744fe74], result)

    @builtins.property
    def cross_account_keys(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Create KMS keys for cross-account deployments.

        This controls whether the pipeline is enabled for cross-account deployments.

        Can only be set if ``codePipeline`` is not set.

        By default cross-account deployments are enabled, but this feature requires
        that KMS Customer Master Keys are created which have a cost of $1/month.

        If you do not need cross-account deployments, you can set this to ``false`` to
        not create those keys and save on that cost (the artifact bucket will be
        encrypted with an AWS-managed key). However, cross-account deployments will
        no longer be possible.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("cross_account_keys")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pipeline_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the pipeline.

        Can only be set if ``codePipeline`` is not set.

        :default: - A name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("pipeline_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def self_mutating(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the pipeline will update itself.

        This needs to be set to ``true`` to allow the pipeline to reconfigure
        itself when assets or stages are being added to it, and ``true`` is the
        recommended setting.

        You can temporarily set this to ``false`` while you are iterating
        on the pipeline itself and prefer to deploy changes using ``cdk deploy``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("self_mutating")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source_action(self) -> typing.Optional[_IAction_ecd54a08]:
        '''(experimental) The CodePipeline action used to retrieve the CDK app's source.

        :default: - Required unless ``codePipeline`` is given

        :stability: experimental
        '''
        result = self._values.get("source_action")
        return typing.cast(typing.Optional[_IAction_ecd54a08], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def synth_action(self) -> typing.Optional[_IAction_ecd54a08]:
        '''(experimental) The CodePipeline action build and synthesis step of the CDK app.

        :default: - Required unless ``codePipeline`` or ``sourceAction`` is given

        :stability: experimental
        '''
        result = self._values.get("synth_action")
        return typing.cast(typing.Optional[_IAction_ecd54a08], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The VPC where to execute the CdkPipeline actions.

        :default: - No VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkPipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdkStage(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.CdkStage",
):
    '''(experimental) Stage in a CdkPipeline.

    You don't need to instantiate this class directly. Use
    ``cdkPipeline.addStage()`` instead.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        host: "IStageHost",
        pipeline_stage: _IStage_5a7e7342,
        stage_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cloud_assembly_artifact: (experimental) The CodePipeline Artifact with the Cloud Assembly.
        :param host: (experimental) Features the Stage needs from its environment.
        :param pipeline_stage: (experimental) The underlying Pipeline Stage associated with thisCdkStage.
        :param stage_name: (experimental) Name of the stage that should be created.

        :stability: experimental
        '''
        props = CdkStageProps(
            cloud_assembly_artifact=cloud_assembly_artifact,
            host=host,
            pipeline_stage=pipeline_stage,
            stage_name=stage_name,
        )

        jsii.create(CdkStage, self, [scope, id, props])

    @jsii.member(jsii_name="addActions")
    def add_actions(self, *actions: _IAction_ecd54a08) -> None:
        '''(experimental) Add one or more CodePipeline Actions.

        You need to make sure it is created with the right runOrder. Call ``nextSequentialRunOrder()``
        for every action to get actions to execute in sequence.

        :param actions: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addActions", [*actions]))

    @jsii.member(jsii_name="addApplication")
    def add_application(
        self,
        app_stage: _Stage_9729985a,
        *,
        extra_run_order_space: typing.Optional[jsii.Number] = None,
        manual_approvals: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Add all stacks in the application Stage to this stage.

        The application construct should subclass ``Stage`` and can contain any
        number of ``Stacks`` inside it that may have dependency relationships
        on one another.

        All stacks in the application will be deployed in the appropriate order,
        and all assets found in the application will be added to the asset
        publishing stage.

        :param app_stage: -
        :param extra_run_order_space: (experimental) Add room for extra actions. You can use this to make extra room in the runOrder sequence between the changeset 'prepare' and 'execute' actions and insert your own actions there. Default: 0
        :param manual_approvals: (experimental) Add manual approvals before executing change sets. This gives humans the opportunity to confirm the change set looks alright before deploying it. Default: false

        :stability: experimental
        '''
        options = AddStageOptions(
            extra_run_order_space=extra_run_order_space,
            manual_approvals=manual_approvals,
        )

        return typing.cast(None, jsii.invoke(self, "addApplication", [app_stage, options]))

    @jsii.member(jsii_name="addManualApprovalAction")
    def add_manual_approval_action(
        self,
        *,
        action_name: typing.Optional[builtins.str] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Add a manual approval action.

        If you need more flexibility than what this method offers,
        use ``addAction`` with a ``ManualApprovalAction``.

        :param action_name: (experimental) The name of the manual approval action. Default: 'ManualApproval' with a rolling counter
        :param run_order: (experimental) The runOrder for this action. Default: - The next sequential runOrder

        :stability: experimental
        '''
        options = AddManualApprovalOptions(
            action_name=action_name, run_order=run_order
        )

        return typing.cast(None, jsii.invoke(self, "addManualApprovalAction", [options]))

    @jsii.member(jsii_name="addStackArtifactDeployment")
    def add_stack_artifact_deployment(
        self,
        stack_artifact: _CloudFormationStackArtifact_45074b84,
        *,
        execute_run_order: typing.Optional[jsii.Number] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Add a deployment action based on a stack artifact.

        :param stack_artifact: -
        :param execute_run_order: (experimental) Base runorder. Default: - runOrder + 1
        :param run_order: (experimental) Base runorder. Default: - Next sequential runorder

        :stability: experimental
        '''
        options = AddStackOptions(
            execute_run_order=execute_run_order, run_order=run_order
        )

        return typing.cast(None, jsii.invoke(self, "addStackArtifactDeployment", [stack_artifact, options]))

    @jsii.member(jsii_name="deploysStack")
    def deploys_stack(self, artifact_id: builtins.str) -> builtins.bool:
        '''(experimental) Whether this Stage contains an action to deploy the given stack, identified by its artifact ID.

        :param artifact_id: -

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "deploysStack", [artifact_id]))

    @jsii.member(jsii_name="nextSequentialRunOrder")
    def next_sequential_run_order(
        self,
        count: typing.Optional[jsii.Number] = None,
    ) -> jsii.Number:
        '''(experimental) Return the runOrder number necessary to run the next Action in sequence with the rest.

        FIXME: This is here because Actions are immutable and can't be reordered
        after creation, nor is there a way to specify relative priorities, which
        is a limitation that we should take away in the base library.

        :param count: -

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "nextSequentialRunOrder", [count]))


@jsii.data_type(
    jsii_type="monocdk.pipelines.CdkStageProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "host": "host",
        "pipeline_stage": "pipelineStage",
        "stage_name": "stageName",
    },
)
class CdkStageProps:
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        host: "IStageHost",
        pipeline_stage: _IStage_5a7e7342,
        stage_name: builtins.str,
    ) -> None:
        '''(experimental) Construction properties for a CdkStage.

        :param cloud_assembly_artifact: (experimental) The CodePipeline Artifact with the Cloud Assembly.
        :param host: (experimental) Features the Stage needs from its environment.
        :param pipeline_stage: (experimental) The underlying Pipeline Stage associated with thisCdkStage.
        :param stage_name: (experimental) Name of the stage that should be created.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "host": host,
            "pipeline_stage": pipeline_stage,
            "stage_name": stage_name,
        }

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_9905eec2:
        '''(experimental) The CodePipeline Artifact with the Cloud Assembly.

        :stability: experimental
        '''
        result = self._values.get("cloud_assembly_artifact")
        assert result is not None, "Required property 'cloud_assembly_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def host(self) -> "IStageHost":
        '''(experimental) Features the Stage needs from its environment.

        :stability: experimental
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast("IStageHost", result)

    @builtins.property
    def pipeline_stage(self) -> _IStage_5a7e7342:
        '''(experimental) The underlying Pipeline Stage associated with thisCdkStage.

        :stability: experimental
        '''
        result = self._values.get("pipeline_stage")
        assert result is not None, "Required property 'pipeline_stage' is missing"
        return typing.cast(_IStage_5a7e7342, result)

    @builtins.property
    def stage_name(self) -> builtins.str:
        '''(experimental) Name of the stage that should be created.

        :stability: experimental
        '''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkStageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_ecd54a08)
class DeployCdkStackAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.DeployCdkStackAction",
):
    '''(experimental) Action to deploy a CDK Stack.

    Adds two CodePipeline Actions to the pipeline: one to create a ChangeSet
    and one to execute it.

    You do not need to instantiate this action yourself -- it will automatically
    be added by the pipeline when you add stack artifacts or entire stages.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        action_role: _IRole_59af6f50,
        stack_name: builtins.str,
        template_path: builtins.str,
        cloud_formation_execution_role: typing.Optional[_IRole_59af6f50] = None,
        dependency_stack_artifact_ids: typing.Optional[typing.List[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        stack_artifact_id: typing.Optional[builtins.str] = None,
        template_configuration_path: typing.Optional[builtins.str] = None,
        cloud_assembly_input: _Artifact_9905eec2,
        base_action_name: typing.Optional[builtins.str] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action_role: (experimental) Role for the action to assume. This controls the account to deploy into
        :param stack_name: (experimental) The name of the stack that should be created/updated.
        :param template_path: (experimental) Relative path of template in the input artifact.
        :param cloud_formation_execution_role: (experimental) Role to execute CloudFormation under. Default: - Execute CloudFormation using the action role
        :param dependency_stack_artifact_ids: (experimental) Artifact ID for the stacks this stack depends on. Used for pipeline order checking. Default: - No dependencies
        :param region: (experimental) Region to deploy into. Default: - Same region as pipeline
        :param stack_artifact_id: (experimental) Artifact ID for the stack deployed here. Used for pipeline order checking. Default: - Order will not be checked
        :param template_configuration_path: (experimental) Template configuration path relative to the input artifact. Default: - No template configuration
        :param cloud_assembly_input: (experimental) The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: (experimental) Base name of the action. Default: stackName
        :param change_set_name: (experimental) Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: (experimental) Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: (experimental) Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: (experimental) Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: (experimental) Run order for the Prepare action. Default: 1

        :stability: experimental
        '''
        props = DeployCdkStackActionProps(
            action_role=action_role,
            stack_name=stack_name,
            template_path=template_path,
            cloud_formation_execution_role=cloud_formation_execution_role,
            dependency_stack_artifact_ids=dependency_stack_artifact_ids,
            region=region,
            stack_artifact_id=stack_artifact_id,
            template_configuration_path=template_configuration_path,
            cloud_assembly_input=cloud_assembly_input,
            base_action_name=base_action_name,
            change_set_name=change_set_name,
            execute_run_order=execute_run_order,
            output=output,
            output_file_name=output_file_name,
            prepare_run_order=prepare_run_order,
        )

        jsii.create(DeployCdkStackAction, self, [props])

    @jsii.member(jsii_name="fromStackArtifact") # type: ignore[misc]
    @builtins.classmethod
    def from_stack_artifact(
        cls,
        scope: constructs.Construct,
        artifact: _CloudFormationStackArtifact_45074b84,
        *,
        stack_name: typing.Optional[builtins.str] = None,
        cloud_assembly_input: _Artifact_9905eec2,
        base_action_name: typing.Optional[builtins.str] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
    ) -> "DeployCdkStackAction":
        '''(experimental) Construct a DeployCdkStackAction from a Stack artifact.

        :param scope: -
        :param artifact: -
        :param stack_name: (experimental) The name of the stack that should be created/updated. Default: - Same as stack artifact
        :param cloud_assembly_input: (experimental) The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: (experimental) Base name of the action. Default: stackName
        :param change_set_name: (experimental) Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: (experimental) Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: (experimental) Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: (experimental) Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: (experimental) Run order for the Prepare action. Default: 1

        :stability: experimental
        '''
        options = CdkStackActionFromArtifactOptions(
            stack_name=stack_name,
            cloud_assembly_input=cloud_assembly_input,
            base_action_name=base_action_name,
            change_set_name=change_set_name,
            execute_run_order=execute_run_order,
            output=output,
            output_file_name=output_file_name,
            prepare_run_order=prepare_run_order,
        )

        return typing.cast("DeployCdkStackAction", jsii.sinvoke(cls, "fromStackArtifact", [scope, artifact, options]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) Exists to implement IAction.

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
        '''(experimental) Exists to implement IAction.

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
        '''(experimental) Exists to implement IAction.

        :stability: experimental
        '''
        return typing.cast(_ActionProperties_c7760ac6, jsii.get(self, "actionProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dependencyStackArtifactIds")
    def dependency_stack_artifact_ids(self) -> typing.List[builtins.str]:
        '''(experimental) Artifact ids of the artifact this stack artifact depends on.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dependencyStackArtifactIds"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="executeRunOrder")
    def execute_run_order(self) -> jsii.Number:
        '''(experimental) The runorder for the execute action.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "executeRunOrder"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="prepareRunOrder")
    def prepare_run_order(self) -> jsii.Number:
        '''(experimental) The runorder for the prepare action.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "prepareRunOrder"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        '''(experimental) Name of the deployed stack.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stackArtifactId")
    def stack_artifact_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Artifact id of the artifact this action was based on.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stackArtifactId"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.DeployCdkStackActionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "base_action_name": "baseActionName",
        "change_set_name": "changeSetName",
        "execute_run_order": "executeRunOrder",
        "output": "output",
        "output_file_name": "outputFileName",
        "prepare_run_order": "prepareRunOrder",
    },
)
class DeployCdkStackActionOptions:
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_9905eec2,
        base_action_name: typing.Optional[builtins.str] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Customization options for a DeployCdkStackAction.

        :param cloud_assembly_input: (experimental) The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: (experimental) Base name of the action. Default: stackName
        :param change_set_name: (experimental) Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: (experimental) Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: (experimental) Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: (experimental) Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: (experimental) Run order for the Prepare action. Default: 1

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cloud_assembly_input": cloud_assembly_input,
        }
        if base_action_name is not None:
            self._values["base_action_name"] = base_action_name
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if prepare_run_order is not None:
            self._values["prepare_run_order"] = prepare_run_order

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_9905eec2:
        '''(experimental) The CodePipeline artifact that holds the Cloud Assembly.

        :stability: experimental
        '''
        result = self._values.get("cloud_assembly_input")
        assert result is not None, "Required property 'cloud_assembly_input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def base_action_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Base name of the action.

        :default: stackName

        :stability: experimental
        '''
        result = self._values.get("base_action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def change_set_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the change set to create and deploy.

        :default: 'PipelineChange'

        :stability: experimental
        '''
        result = self._values.get("change_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Run order for the Execute action.

        :default: - prepareRunOrder + 1

        :stability: experimental
        '''
        result = self._values.get("execute_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) Artifact to write Stack Outputs to.

        :default: - No outputs

        :stability: experimental
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def output_file_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Filename in output to write Stack outputs to.

        :default: - Required when 'output' is set

        :stability: experimental
        '''
        result = self._values.get("output_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prepare_run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Run order for the Prepare action.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("prepare_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeployCdkStackActionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.DeployCdkStackActionProps",
    jsii_struct_bases=[DeployCdkStackActionOptions],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "base_action_name": "baseActionName",
        "change_set_name": "changeSetName",
        "execute_run_order": "executeRunOrder",
        "output": "output",
        "output_file_name": "outputFileName",
        "prepare_run_order": "prepareRunOrder",
        "action_role": "actionRole",
        "stack_name": "stackName",
        "template_path": "templatePath",
        "cloud_formation_execution_role": "cloudFormationExecutionRole",
        "dependency_stack_artifact_ids": "dependencyStackArtifactIds",
        "region": "region",
        "stack_artifact_id": "stackArtifactId",
        "template_configuration_path": "templateConfigurationPath",
    },
)
class DeployCdkStackActionProps(DeployCdkStackActionOptions):
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_9905eec2,
        base_action_name: typing.Optional[builtins.str] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
        action_role: _IRole_59af6f50,
        stack_name: builtins.str,
        template_path: builtins.str,
        cloud_formation_execution_role: typing.Optional[_IRole_59af6f50] = None,
        dependency_stack_artifact_ids: typing.Optional[typing.List[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        stack_artifact_id: typing.Optional[builtins.str] = None,
        template_configuration_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a DeployCdkStackAction.

        :param cloud_assembly_input: (experimental) The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: (experimental) Base name of the action. Default: stackName
        :param change_set_name: (experimental) Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: (experimental) Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: (experimental) Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: (experimental) Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: (experimental) Run order for the Prepare action. Default: 1
        :param action_role: (experimental) Role for the action to assume. This controls the account to deploy into
        :param stack_name: (experimental) The name of the stack that should be created/updated.
        :param template_path: (experimental) Relative path of template in the input artifact.
        :param cloud_formation_execution_role: (experimental) Role to execute CloudFormation under. Default: - Execute CloudFormation using the action role
        :param dependency_stack_artifact_ids: (experimental) Artifact ID for the stacks this stack depends on. Used for pipeline order checking. Default: - No dependencies
        :param region: (experimental) Region to deploy into. Default: - Same region as pipeline
        :param stack_artifact_id: (experimental) Artifact ID for the stack deployed here. Used for pipeline order checking. Default: - Order will not be checked
        :param template_configuration_path: (experimental) Template configuration path relative to the input artifact. Default: - No template configuration

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cloud_assembly_input": cloud_assembly_input,
            "action_role": action_role,
            "stack_name": stack_name,
            "template_path": template_path,
        }
        if base_action_name is not None:
            self._values["base_action_name"] = base_action_name
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if prepare_run_order is not None:
            self._values["prepare_run_order"] = prepare_run_order
        if cloud_formation_execution_role is not None:
            self._values["cloud_formation_execution_role"] = cloud_formation_execution_role
        if dependency_stack_artifact_ids is not None:
            self._values["dependency_stack_artifact_ids"] = dependency_stack_artifact_ids
        if region is not None:
            self._values["region"] = region
        if stack_artifact_id is not None:
            self._values["stack_artifact_id"] = stack_artifact_id
        if template_configuration_path is not None:
            self._values["template_configuration_path"] = template_configuration_path

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_9905eec2:
        '''(experimental) The CodePipeline artifact that holds the Cloud Assembly.

        :stability: experimental
        '''
        result = self._values.get("cloud_assembly_input")
        assert result is not None, "Required property 'cloud_assembly_input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def base_action_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Base name of the action.

        :default: stackName

        :stability: experimental
        '''
        result = self._values.get("base_action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def change_set_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the change set to create and deploy.

        :default: 'PipelineChange'

        :stability: experimental
        '''
        result = self._values.get("change_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Run order for the Execute action.

        :default: - prepareRunOrder + 1

        :stability: experimental
        '''
        result = self._values.get("execute_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) Artifact to write Stack Outputs to.

        :default: - No outputs

        :stability: experimental
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def output_file_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Filename in output to write Stack outputs to.

        :default: - Required when 'output' is set

        :stability: experimental
        '''
        result = self._values.get("output_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prepare_run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Run order for the Prepare action.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("prepare_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def action_role(self) -> _IRole_59af6f50:
        '''(experimental) Role for the action to assume.

        This controls the account to deploy into

        :stability: experimental
        '''
        result = self._values.get("action_role")
        assert result is not None, "Required property 'action_role' is missing"
        return typing.cast(_IRole_59af6f50, result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''(experimental) The name of the stack that should be created/updated.

        :stability: experimental
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_path(self) -> builtins.str:
        '''(experimental) Relative path of template in the input artifact.

        :stability: experimental
        '''
        result = self._values.get("template_path")
        assert result is not None, "Required property 'template_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_formation_execution_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Role to execute CloudFormation under.

        :default: - Execute CloudFormation using the action role

        :stability: experimental
        '''
        result = self._values.get("cloud_formation_execution_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def dependency_stack_artifact_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Artifact ID for the stacks this stack depends on.

        Used for pipeline order checking.

        :default: - No dependencies

        :stability: experimental
        '''
        result = self._values.get("dependency_stack_artifact_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Region to deploy into.

        :default: - Same region as pipeline

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_artifact_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Artifact ID for the stack deployed here.

        Used for pipeline order checking.

        :default: - Order will not be checked

        :stability: experimental
        '''
        result = self._values.get("stack_artifact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_configuration_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Template configuration path relative to the input artifact.

        :default: - No template configuration

        :stability: experimental
        '''
        result = self._values.get("template_configuration_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeployCdkStackActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.FromStackArtifactOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "execute_run_order": "executeRunOrder",
        "output": "output",
        "output_file_name": "outputFileName",
        "prepare_run_order": "prepareRunOrder",
    },
)
class FromStackArtifactOptions:
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_9905eec2,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Options for CdkDeployAction.fromStackArtifact.

        :param cloud_assembly_input: (experimental) The CodePipeline artifact that holds the Cloud Assembly.
        :param execute_run_order: (experimental) Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: (experimental) Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: (experimental) Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: (experimental) Run order for the 2 actions that will be created. Default: 1

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cloud_assembly_input": cloud_assembly_input,
        }
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if prepare_run_order is not None:
            self._values["prepare_run_order"] = prepare_run_order

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_9905eec2:
        '''(experimental) The CodePipeline artifact that holds the Cloud Assembly.

        :stability: experimental
        '''
        result = self._values.get("cloud_assembly_input")
        assert result is not None, "Required property 'cloud_assembly_input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Run order for the Execute action.

        :default: - prepareRunOrder + 1

        :stability: experimental
        '''
        result = self._values.get("execute_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) Artifact to write Stack Outputs to.

        :default: - No outputs

        :stability: experimental
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def output_file_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Filename in output to write Stack outputs to.

        :default: - Required when 'output' is set

        :stability: experimental
        '''
        result = self._values.get("output_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prepare_run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Run order for the 2 actions that will be created.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("prepare_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FromStackArtifactOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.pipelines.IStageHost")
class IStageHost(typing_extensions.Protocol):
    '''(experimental) Features that the Stage needs from its environment.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IStageHostProxy"]:
        return _IStageHostProxy

    @jsii.member(jsii_name="publishAsset")
    def publish_asset(
        self,
        *,
        asset_id: builtins.str,
        asset_manifest_path: builtins.str,
        asset_selector: builtins.str,
        asset_type: AssetType,
    ) -> None:
        '''(experimental) Make sure all the assets from the given manifest are published.

        :param asset_id: (experimental) Asset identifier.
        :param asset_manifest_path: (experimental) Asset manifest path.
        :param asset_selector: (experimental) Asset selector to pass to ``cdk-assets``.
        :param asset_type: (experimental) Type of asset to publish.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="stackOutputArtifact")
    def stack_output_artifact(
        self,
        stack_artifact_id: builtins.str,
    ) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) Return the Artifact the given stack has to emit its outputs into, if any.

        :param stack_artifact_id: -

        :stability: experimental
        '''
        ...


class _IStageHostProxy:
    '''(experimental) Features that the Stage needs from its environment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.pipelines.IStageHost"

    @jsii.member(jsii_name="publishAsset")
    def publish_asset(
        self,
        *,
        asset_id: builtins.str,
        asset_manifest_path: builtins.str,
        asset_selector: builtins.str,
        asset_type: AssetType,
    ) -> None:
        '''(experimental) Make sure all the assets from the given manifest are published.

        :param asset_id: (experimental) Asset identifier.
        :param asset_manifest_path: (experimental) Asset manifest path.
        :param asset_selector: (experimental) Asset selector to pass to ``cdk-assets``.
        :param asset_type: (experimental) Type of asset to publish.

        :stability: experimental
        '''
        command = AssetPublishingCommand(
            asset_id=asset_id,
            asset_manifest_path=asset_manifest_path,
            asset_selector=asset_selector,
            asset_type=asset_type,
        )

        return typing.cast(None, jsii.invoke(self, "publishAsset", [command]))

    @jsii.member(jsii_name="stackOutputArtifact")
    def stack_output_artifact(
        self,
        stack_artifact_id: builtins.str,
    ) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) Return the Artifact the given stack has to emit its outputs into, if any.

        :param stack_artifact_id: -

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_Artifact_9905eec2], jsii.invoke(self, "stackOutputArtifact", [stack_artifact_id]))


@jsii.implements(_IAction_ecd54a08)
class PublishAssetsAction(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.PublishAssetsAction",
):
    '''(experimental) Action to publish an asset in the pipeline.

    Creates a CodeBuild project which will use the CDK CLI
    to prepare and publish the asset.

    You do not need to instantiate this action -- it will automatically
    be added by the pipeline when you add stacks that use assets.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        action_name: builtins.str,
        asset_type: AssetType,
        cloud_assembly_input: _Artifact_9905eec2,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param action_name: (experimental) Name of publishing action.
        :param asset_type: (experimental) AssetType we're publishing.
        :param cloud_assembly_input: (experimental) The CodePipeline artifact that holds the Cloud Assembly.
        :param cdk_cli_version: (experimental) Version of CDK CLI to 'npm install'. Default: - Latest version
        :param project_name: (experimental) Name of the CodeBuild project. Default: - Automatically generated
        :param role: (experimental) Role to use for CodePipeline and CodeBuild to build and publish the assets. Default: - Automatically generated
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (experimental) The VPC where to execute the PublishAssetsAction. Default: - No VPC

        :stability: experimental
        '''
        props = PublishAssetsActionProps(
            action_name=action_name,
            asset_type=asset_type,
            cloud_assembly_input=cloud_assembly_input,
            cdk_cli_version=cdk_cli_version,
            project_name=project_name,
            role=role,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(PublishAssetsAction, self, [scope, id, props])

    @jsii.member(jsii_name="addPublishCommand")
    def add_publish_command(
        self,
        relative_manifest_path: builtins.str,
        asset_selector: builtins.str,
    ) -> None:
        '''(experimental) Add a single publishing command.

        Manifest path should be relative to the root Cloud Assembly.

        :param relative_manifest_path: -
        :param asset_selector: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addPublishCommand", [relative_manifest_path, asset_selector]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) Exists to implement IAction.

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
        '''(experimental) Exists to implement IAction.

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
        '''(experimental) Exists to implement IAction.

        :stability: experimental
        '''
        return typing.cast(_ActionProperties_c7760ac6, jsii.get(self, "actionProperties"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.PublishAssetsActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_name": "actionName",
        "asset_type": "assetType",
        "cloud_assembly_input": "cloudAssemblyInput",
        "cdk_cli_version": "cdkCliVersion",
        "project_name": "projectName",
        "role": "role",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class PublishAssetsActionProps:
    def __init__(
        self,
        *,
        action_name: builtins.str,
        asset_type: AssetType,
        cloud_assembly_input: _Artifact_9905eec2,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''(experimental) Props for a PublishAssetsAction.

        :param action_name: (experimental) Name of publishing action.
        :param asset_type: (experimental) AssetType we're publishing.
        :param cloud_assembly_input: (experimental) The CodePipeline artifact that holds the Cloud Assembly.
        :param cdk_cli_version: (experimental) Version of CDK CLI to 'npm install'. Default: - Latest version
        :param project_name: (experimental) Name of the CodeBuild project. Default: - Automatically generated
        :param role: (experimental) Role to use for CodePipeline and CodeBuild to build and publish the assets. Default: - Automatically generated
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (experimental) The VPC where to execute the PublishAssetsAction. Default: - No VPC

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "asset_type": asset_type,
            "cloud_assembly_input": cloud_assembly_input,
        }
        if cdk_cli_version is not None:
            self._values["cdk_cli_version"] = cdk_cli_version
        if project_name is not None:
            self._values["project_name"] = project_name
        if role is not None:
            self._values["role"] = role
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) Name of publishing action.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_type(self) -> AssetType:
        '''(experimental) AssetType we're publishing.

        :stability: experimental
        '''
        result = self._values.get("asset_type")
        assert result is not None, "Required property 'asset_type' is missing"
        return typing.cast(AssetType, result)

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_9905eec2:
        '''(experimental) The CodePipeline artifact that holds the Cloud Assembly.

        :stability: experimental
        '''
        result = self._values.get("cloud_assembly_input")
        assert result is not None, "Required property 'cloud_assembly_input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def cdk_cli_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version of CDK CLI to 'npm install'.

        :default: - Latest version

        :stability: experimental
        '''
        result = self._values.get("cdk_cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the CodeBuild project.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Role to use for CodePipeline and CodeBuild to build and publish the assets.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The VPC where to execute the PublishAssetsAction.

        :default: - No VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PublishAssetsActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_ecd54a08, _IGrantable_4c5a91d1)
class ShellScriptAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.ShellScriptAction",
):
    '''(experimental) Validate a revision using shell commands.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        action_name: builtins.str,
        commands: typing.List[builtins.str],
        additional_artifacts: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        bash_options: typing.Optional[builtins.str] = None,
        environment: typing.Optional[_BuildEnvironment_77bc5f50] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        run_order: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        use_outputs: typing.Optional[typing.Mapping[builtins.str, "StackOutput"]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''
        :param action_name: (experimental) Name of the validation action in the pipeline.
        :param commands: (experimental) Commands to run.
        :param additional_artifacts: (experimental) Additional artifacts to use as input for the CodeBuild project. You can use these files to load more complex test sets into the shellscript build environment. The files artifact given here will be unpacked into the current working directory, the other ones will be unpacked into directories which are available through the environment variables $CODEBUILD_SRC_DIR_. The CodeBuild job must have at least one input artifact, so you must provide either at least one additional artifact here or one stack output using ``useOutput``. Default: - No additional artifacts
        :param bash_options: (experimental) Bash options to set at the start of the script. Default: '-eu' (errexit and nounset)
        :param environment: (experimental) The CodeBuild environment where scripts are executed. Default: LinuxBuildImage.STANDARD_4_0
        :param environment_variables: (experimental) Environment variables to send into build. Default: - No additional environment variables
        :param role_policy_statements: (experimental) Additional policy statements to add to the execution role. Default: - No policy statements
        :param run_order: (experimental) RunOrder for this action. Use this to sequence the shell script after the deployments. The default value is 100 so you don't have to supply the value if you just want to run this after the application stacks have been deployed, and you don't have more than 100 stacks. Default: 100
        :param security_groups: (experimental) Which security group to associate with the script's project network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param use_outputs: (experimental) Stack outputs to make available as environment variables. Default: - No outputs used
        :param vpc: (experimental) The VPC where to execute the specified script. Default: - No VPC

        :stability: experimental
        '''
        props = ShellScriptActionProps(
            action_name=action_name,
            commands=commands,
            additional_artifacts=additional_artifacts,
            bash_options=bash_options,
            environment=environment,
            environment_variables=environment_variables,
            role_policy_statements=role_policy_statements,
            run_order=run_order,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            use_outputs=use_outputs,
            vpc=vpc,
        )

        jsii.create(ShellScriptAction, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) Exists to implement IAction.

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
        '''(experimental) Exists to implement IAction.

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
        '''(experimental) Exists to implement IAction.

        :stability: experimental
        '''
        return typing.cast(_ActionProperties_c7760ac6, jsii.get(self, "actionProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_93b48231:
        '''(experimental) The CodeBuild Project's principal.

        :stability: experimental
        '''
        return typing.cast(_IPrincipal_93b48231, jsii.get(self, "grantPrincipal"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="project")
    def project(self) -> _IProject_6da8803e:
        '''(experimental) Project generated to run the shell script in.

        :stability: experimental
        '''
        return typing.cast(_IProject_6da8803e, jsii.get(self, "project"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.ShellScriptActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_name": "actionName",
        "commands": "commands",
        "additional_artifacts": "additionalArtifacts",
        "bash_options": "bashOptions",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "role_policy_statements": "rolePolicyStatements",
        "run_order": "runOrder",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "use_outputs": "useOutputs",
        "vpc": "vpc",
    },
)
class ShellScriptActionProps:
    def __init__(
        self,
        *,
        action_name: builtins.str,
        commands: typing.List[builtins.str],
        additional_artifacts: typing.Optional[typing.List[_Artifact_9905eec2]] = None,
        bash_options: typing.Optional[builtins.str] = None,
        environment: typing.Optional[_BuildEnvironment_77bc5f50] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        run_order: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        use_outputs: typing.Optional[typing.Mapping[builtins.str, "StackOutput"]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''(experimental) Properties for ShellScriptAction.

        :param action_name: (experimental) Name of the validation action in the pipeline.
        :param commands: (experimental) Commands to run.
        :param additional_artifacts: (experimental) Additional artifacts to use as input for the CodeBuild project. You can use these files to load more complex test sets into the shellscript build environment. The files artifact given here will be unpacked into the current working directory, the other ones will be unpacked into directories which are available through the environment variables $CODEBUILD_SRC_DIR_. The CodeBuild job must have at least one input artifact, so you must provide either at least one additional artifact here or one stack output using ``useOutput``. Default: - No additional artifacts
        :param bash_options: (experimental) Bash options to set at the start of the script. Default: '-eu' (errexit and nounset)
        :param environment: (experimental) The CodeBuild environment where scripts are executed. Default: LinuxBuildImage.STANDARD_4_0
        :param environment_variables: (experimental) Environment variables to send into build. Default: - No additional environment variables
        :param role_policy_statements: (experimental) Additional policy statements to add to the execution role. Default: - No policy statements
        :param run_order: (experimental) RunOrder for this action. Use this to sequence the shell script after the deployments. The default value is 100 so you don't have to supply the value if you just want to run this after the application stacks have been deployed, and you don't have more than 100 stacks. Default: 100
        :param security_groups: (experimental) Which security group to associate with the script's project network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param use_outputs: (experimental) Stack outputs to make available as environment variables. Default: - No outputs used
        :param vpc: (experimental) The VPC where to execute the specified script. Default: - No VPC

        :stability: experimental
        '''
        if isinstance(environment, dict):
            environment = _BuildEnvironment_77bc5f50(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "commands": commands,
        }
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if bash_options is not None:
            self._values["bash_options"] = bash_options
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if run_order is not None:
            self._values["run_order"] = run_order
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if use_outputs is not None:
            self._values["use_outputs"] = use_outputs
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) Name of the validation action in the pipeline.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commands(self) -> typing.List[builtins.str]:
        '''(experimental) Commands to run.

        :stability: experimental
        '''
        result = self._values.get("commands")
        assert result is not None, "Required property 'commands' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[_Artifact_9905eec2]]:
        '''(experimental) Additional artifacts to use as input for the CodeBuild project.

        You can use these files to load more complex test sets into the
        shellscript build environment.

        The files artifact given here will be unpacked into the current
        working directory, the other ones will be unpacked into directories
        which are available through the environment variables
        $CODEBUILD_SRC_DIR_.

        The CodeBuild job must have at least one input artifact, so you
        must provide either at least one additional artifact here or one
        stack output using ``useOutput``.

        :default: - No additional artifacts

        :stability: experimental
        '''
        result = self._values.get("additional_artifacts")
        return typing.cast(typing.Optional[typing.List[_Artifact_9905eec2]], result)

    @builtins.property
    def bash_options(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bash options to set at the start of the script.

        :default: '-eu' (errexit and nounset)

        :stability: experimental
        '''
        result = self._values.get("bash_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(experimental) The CodeBuild environment where scripts are executed.

        :default: LinuxBuildImage.STANDARD_4_0

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]]:
        '''(experimental) Environment variables to send into build.

        :default: - No additional environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]], result)

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Additional policy statements to add to the execution role.

        :default: - No policy statements

        :stability: experimental
        '''
        result = self._values.get("role_policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) RunOrder for this action.

        Use this to sequence the shell script after the deployments.

        The default value is 100 so you don't have to supply the value if you just
        want to run this after the application stacks have been deployed, and you
        don't have more than 100 stacks.

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) Which security group to associate with the script's project network interfaces.

        If no security group is identified, one will be created automatically.

        Only used if 'vpc' is supplied.

        :default: - Security group will be automatically created.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def use_outputs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "StackOutput"]]:
        '''(experimental) Stack outputs to make available as environment variables.

        :default: - No outputs used

        :stability: experimental
        '''
        result = self._values.get("use_outputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "StackOutput"]], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The VPC where to execute the specified script.

        :default: - No VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ShellScriptActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_ecd54a08, _IGrantable_4c5a91d1)
class SimpleSynthAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.SimpleSynthAction",
):
    '''(experimental) A standard synth with a generated buildspec.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        synth_command: builtins.str,
        build_command: typing.Optional[builtins.str] = None,
        build_commands: typing.Optional[typing.List[builtins.str]] = None,
        install_command: typing.Optional[builtins.str] = None,
        install_commands: typing.Optional[typing.List[builtins.str]] = None,
        test_commands: typing.Optional[typing.List[builtins.str]] = None,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.List[AdditionalArtifact]] = None,
        copy_environment_variables: typing.Optional[typing.List[builtins.str]] = None,
        environment: typing.Optional[_BuildEnvironment_77bc5f50] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''
        :param synth_command: (experimental) The synth command.
        :param build_command: (deprecated) The build command. If your programming language requires a compilation step, put the compilation command here. Default: - No build required
        :param build_commands: (experimental) The build commands. If your programming language requires a compilation step, put the compilation command here. Default: - No build required
        :param install_command: (deprecated) The install command. If not provided by the build image or another dependency management tool, at least install the CDK CLI here using ``npm install -g aws-cdk``. Default: - No install required
        :param install_commands: (experimental) Install commands. If not provided by the build image or another dependency management tool, at least install the CDK CLI here using ``npm install -g aws-cdk``. Default: - No install required
        :param test_commands: (experimental) Test commands. These commands are run after the build commands but before the synth command. Default: - No test commands
        :param cloud_assembly_artifact: (experimental) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (experimental) The source artifact of the CodePipeline.
        :param action_name: (experimental) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (experimental) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: (experimental) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (experimental) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: (experimental) Environment variables to send into build. Default: - No additional environment variables
        :param project_name: (experimental) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (experimental) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (experimental) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (experimental) The VPC where to execute the SimpleSynth. Default: - No VPC

        :stability: experimental
        '''
        props = SimpleSynthActionProps(
            synth_command=synth_command,
            build_command=build_command,
            build_commands=build_commands,
            install_command=install_command,
            install_commands=install_commands,
            test_commands=test_commands,
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_artifact=source_artifact,
            action_name=action_name,
            additional_artifacts=additional_artifacts,
            copy_environment_variables=copy_environment_variables,
            environment=environment,
            environment_variables=environment_variables,
            project_name=project_name,
            role_policy_statements=role_policy_statements,
            subdirectory=subdirectory,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(SimpleSynthAction, self, [props])

    @jsii.member(jsii_name="standardNpmSynth") # type: ignore[misc]
    @builtins.classmethod
    def standard_npm_synth(
        cls,
        *,
        build_command: typing.Optional[builtins.str] = None,
        install_command: typing.Optional[builtins.str] = None,
        synth_command: typing.Optional[builtins.str] = None,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.List[AdditionalArtifact]] = None,
        copy_environment_variables: typing.Optional[typing.List[builtins.str]] = None,
        environment: typing.Optional[_BuildEnvironment_77bc5f50] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> "SimpleSynthAction":
        '''(experimental) Create a standard NPM synth action.

        Uses ``npm ci`` to install dependencies and ``npx cdk synth`` to synthesize.

        If you need a build step, add ``buildCommand: 'npm run build'``.

        :param build_command: (experimental) The build command. By default, we assume NPM projects are either written in JavaScript or are using ``ts-node``, so don't need a build command. Otherwise, put the build command here, for example ``npm run build``. Default: - No build required
        :param install_command: (experimental) The install command. Default: 'npm ci'
        :param synth_command: (experimental) The synth command. Default: 'npx cdk synth'
        :param cloud_assembly_artifact: (experimental) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (experimental) The source artifact of the CodePipeline.
        :param action_name: (experimental) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (experimental) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: (experimental) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (experimental) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: (experimental) Environment variables to send into build. Default: - No additional environment variables
        :param project_name: (experimental) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (experimental) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (experimental) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (experimental) The VPC where to execute the SimpleSynth. Default: - No VPC

        :stability: experimental
        '''
        options = StandardNpmSynthOptions(
            build_command=build_command,
            install_command=install_command,
            synth_command=synth_command,
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_artifact=source_artifact,
            action_name=action_name,
            additional_artifacts=additional_artifacts,
            copy_environment_variables=copy_environment_variables,
            environment=environment,
            environment_variables=environment_variables,
            project_name=project_name,
            role_policy_statements=role_policy_statements,
            subdirectory=subdirectory,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        return typing.cast("SimpleSynthAction", jsii.sinvoke(cls, "standardNpmSynth", [options]))

    @jsii.member(jsii_name="standardYarnSynth") # type: ignore[misc]
    @builtins.classmethod
    def standard_yarn_synth(
        cls,
        *,
        build_command: typing.Optional[builtins.str] = None,
        install_command: typing.Optional[builtins.str] = None,
        synth_command: typing.Optional[builtins.str] = None,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.List[AdditionalArtifact]] = None,
        copy_environment_variables: typing.Optional[typing.List[builtins.str]] = None,
        environment: typing.Optional[_BuildEnvironment_77bc5f50] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> "SimpleSynthAction":
        '''(experimental) Create a standard Yarn synth action.

        Uses ``yarn install --frozen-lockfile`` to install dependencies and ``npx cdk synth`` to synthesize.

        If you need a build step, add ``buildCommand: 'yarn build'``.

        :param build_command: (experimental) The build command. By default, we assume NPM projects are either written in JavaScript or are using ``ts-node``, so don't need a build command. Otherwise, put the build command here, for example ``npm run build``. Default: - No build required
        :param install_command: (experimental) The install command. Default: 'yarn install --frozen-lockfile'
        :param synth_command: (experimental) The synth command. Default: 'npx cdk synth'
        :param cloud_assembly_artifact: (experimental) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (experimental) The source artifact of the CodePipeline.
        :param action_name: (experimental) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (experimental) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: (experimental) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (experimental) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: (experimental) Environment variables to send into build. Default: - No additional environment variables
        :param project_name: (experimental) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (experimental) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (experimental) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (experimental) The VPC where to execute the SimpleSynth. Default: - No VPC

        :stability: experimental
        '''
        options = StandardYarnSynthOptions(
            build_command=build_command,
            install_command=install_command,
            synth_command=synth_command,
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_artifact=source_artifact,
            action_name=action_name,
            additional_artifacts=additional_artifacts,
            copy_environment_variables=copy_environment_variables,
            environment=environment,
            environment_variables=environment_variables,
            project_name=project_name,
            role_policy_statements=role_policy_statements,
            subdirectory=subdirectory,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        return typing.cast("SimpleSynthAction", jsii.sinvoke(cls, "standardYarnSynth", [options]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) Exists to implement IAction.

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
        '''(experimental) Exists to implement IAction.

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
        '''(experimental) Exists to implement IAction.

        :stability: experimental
        '''
        return typing.cast(_ActionProperties_c7760ac6, jsii.get(self, "actionProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_93b48231:
        '''(experimental) The CodeBuild Project's principal.

        :stability: experimental
        '''
        return typing.cast(_IPrincipal_93b48231, jsii.get(self, "grantPrincipal"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="project")
    def project(self) -> _IProject_6da8803e:
        '''(experimental) Project generated to run the synth command.

        :stability: experimental
        '''
        return typing.cast(_IProject_6da8803e, jsii.get(self, "project"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.SimpleSynthOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "source_artifact": "sourceArtifact",
        "action_name": "actionName",
        "additional_artifacts": "additionalArtifacts",
        "copy_environment_variables": "copyEnvironmentVariables",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
        "role_policy_statements": "rolePolicyStatements",
        "subdirectory": "subdirectory",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class SimpleSynthOptions:
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.List[AdditionalArtifact]] = None,
        copy_environment_variables: typing.Optional[typing.List[builtins.str]] = None,
        environment: typing.Optional[_BuildEnvironment_77bc5f50] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''(experimental) Configuration options for a SimpleSynth.

        :param cloud_assembly_artifact: (experimental) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (experimental) The source artifact of the CodePipeline.
        :param action_name: (experimental) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (experimental) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: (experimental) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (experimental) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: (experimental) Environment variables to send into build. Default: - No additional environment variables
        :param project_name: (experimental) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (experimental) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (experimental) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (experimental) The VPC where to execute the SimpleSynth. Default: - No VPC

        :stability: experimental
        '''
        if isinstance(environment, dict):
            environment = _BuildEnvironment_77bc5f50(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "source_artifact": source_artifact,
        }
        if action_name is not None:
            self._values["action_name"] = action_name
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if copy_environment_variables is not None:
            self._values["copy_environment_variables"] = copy_environment_variables
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_9905eec2:
        '''(experimental) The artifact where the CloudAssembly should be emitted.

        :stability: experimental
        '''
        result = self._values.get("cloud_assembly_artifact")
        assert result is not None, "Required property 'cloud_assembly_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def source_artifact(self) -> _Artifact_9905eec2:
        '''(experimental) The source artifact of the CodePipeline.

        :stability: experimental
        '''
        result = self._values.get("source_artifact")
        assert result is not None, "Required property 'source_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the build action.

        :default: 'Synth'

        :stability: experimental
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[AdditionalArtifact]]:
        '''(experimental) Produce additional output artifacts after the build based on the given directories.

        Can be used to produce additional artifacts during the build step,
        separate from the cloud assembly, which can be used further on in the
        pipeline.

        Directories are evaluated with respect to ``subdirectory``.

        :default: - No additional artifacts generated

        :stability: experimental
        '''
        result = self._values.get("additional_artifacts")
        return typing.cast(typing.Optional[typing.List[AdditionalArtifact]], result)

    @builtins.property
    def copy_environment_variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Environment variables to copy over from parent env.

        These are environment variables that are being used by the build.

        :default: - No environment variables copied

        :stability: experimental
        '''
        result = self._values.get("copy_environment_variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(experimental) Build environment to use for CodeBuild job.

        :default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]]:
        '''(experimental) Environment variables to send into build.

        :default: - No additional environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the CodeBuild project.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        :default: - No policy statements added to CodeBuild Project Role

        :stability: experimental
        '''
        result = self._values.get("role_policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Directory inside the source where package.json and cdk.json are located.

        :default: - Repository root

        :stability: experimental
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The VPC where to execute the SimpleSynth.

        :default: - No VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SimpleSynthOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackOutput(metaclass=jsii.JSIIMeta, jsii_type="monocdk.pipelines.StackOutput"):
    '''(experimental) A single output of a Stack.

    :stability: experimental
    '''

    def __init__(
        self,
        artifact_file: _ArtifactPath_a5b79113,
        output_name: builtins.str,
    ) -> None:
        '''(experimental) Build a StackOutput from a known artifact and an output name.

        :param artifact_file: -
        :param output_name: -

        :stability: experimental
        '''
        jsii.create(StackOutput, self, [artifact_file, output_name])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="artifactFile")
    def artifact_file(self) -> _ArtifactPath_a5b79113:
        '''(experimental) The artifact and file the output is stored in.

        :stability: experimental
        '''
        return typing.cast(_ArtifactPath_a5b79113, jsii.get(self, "artifactFile"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="outputName")
    def output_name(self) -> builtins.str:
        '''(experimental) The name of the output in the JSON object in the file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "outputName"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.StandardNpmSynthOptions",
    jsii_struct_bases=[SimpleSynthOptions],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "source_artifact": "sourceArtifact",
        "action_name": "actionName",
        "additional_artifacts": "additionalArtifacts",
        "copy_environment_variables": "copyEnvironmentVariables",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
        "role_policy_statements": "rolePolicyStatements",
        "subdirectory": "subdirectory",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "build_command": "buildCommand",
        "install_command": "installCommand",
        "synth_command": "synthCommand",
    },
)
class StandardNpmSynthOptions(SimpleSynthOptions):
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.List[AdditionalArtifact]] = None,
        copy_environment_variables: typing.Optional[typing.List[builtins.str]] = None,
        environment: typing.Optional[_BuildEnvironment_77bc5f50] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        build_command: typing.Optional[builtins.str] = None,
        install_command: typing.Optional[builtins.str] = None,
        synth_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for a convention-based synth using NPM.

        :param cloud_assembly_artifact: (experimental) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (experimental) The source artifact of the CodePipeline.
        :param action_name: (experimental) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (experimental) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: (experimental) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (experimental) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: (experimental) Environment variables to send into build. Default: - No additional environment variables
        :param project_name: (experimental) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (experimental) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (experimental) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (experimental) The VPC where to execute the SimpleSynth. Default: - No VPC
        :param build_command: (experimental) The build command. By default, we assume NPM projects are either written in JavaScript or are using ``ts-node``, so don't need a build command. Otherwise, put the build command here, for example ``npm run build``. Default: - No build required
        :param install_command: (experimental) The install command. Default: 'npm ci'
        :param synth_command: (experimental) The synth command. Default: 'npx cdk synth'

        :stability: experimental
        '''
        if isinstance(environment, dict):
            environment = _BuildEnvironment_77bc5f50(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "source_artifact": source_artifact,
        }
        if action_name is not None:
            self._values["action_name"] = action_name
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if copy_environment_variables is not None:
            self._values["copy_environment_variables"] = copy_environment_variables
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc
        if build_command is not None:
            self._values["build_command"] = build_command
        if install_command is not None:
            self._values["install_command"] = install_command
        if synth_command is not None:
            self._values["synth_command"] = synth_command

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_9905eec2:
        '''(experimental) The artifact where the CloudAssembly should be emitted.

        :stability: experimental
        '''
        result = self._values.get("cloud_assembly_artifact")
        assert result is not None, "Required property 'cloud_assembly_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def source_artifact(self) -> _Artifact_9905eec2:
        '''(experimental) The source artifact of the CodePipeline.

        :stability: experimental
        '''
        result = self._values.get("source_artifact")
        assert result is not None, "Required property 'source_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the build action.

        :default: 'Synth'

        :stability: experimental
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[AdditionalArtifact]]:
        '''(experimental) Produce additional output artifacts after the build based on the given directories.

        Can be used to produce additional artifacts during the build step,
        separate from the cloud assembly, which can be used further on in the
        pipeline.

        Directories are evaluated with respect to ``subdirectory``.

        :default: - No additional artifacts generated

        :stability: experimental
        '''
        result = self._values.get("additional_artifacts")
        return typing.cast(typing.Optional[typing.List[AdditionalArtifact]], result)

    @builtins.property
    def copy_environment_variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Environment variables to copy over from parent env.

        These are environment variables that are being used by the build.

        :default: - No environment variables copied

        :stability: experimental
        '''
        result = self._values.get("copy_environment_variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(experimental) Build environment to use for CodeBuild job.

        :default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]]:
        '''(experimental) Environment variables to send into build.

        :default: - No additional environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the CodeBuild project.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        :default: - No policy statements added to CodeBuild Project Role

        :stability: experimental
        '''
        result = self._values.get("role_policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Directory inside the source where package.json and cdk.json are located.

        :default: - Repository root

        :stability: experimental
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The VPC where to execute the SimpleSynth.

        :default: - No VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The build command.

        By default, we assume NPM projects are either written in JavaScript or are
        using ``ts-node``, so don't need a build command.

        Otherwise, put the build command here, for example ``npm run build``.

        :default: - No build required

        :stability: experimental
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The install command.

        :default: 'npm ci'

        :stability: experimental
        '''
        result = self._values.get("install_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synth_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The synth command.

        :default: 'npx cdk synth'

        :stability: experimental
        '''
        result = self._values.get("synth_command")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StandardNpmSynthOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.StandardYarnSynthOptions",
    jsii_struct_bases=[SimpleSynthOptions],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "source_artifact": "sourceArtifact",
        "action_name": "actionName",
        "additional_artifacts": "additionalArtifacts",
        "copy_environment_variables": "copyEnvironmentVariables",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
        "role_policy_statements": "rolePolicyStatements",
        "subdirectory": "subdirectory",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "build_command": "buildCommand",
        "install_command": "installCommand",
        "synth_command": "synthCommand",
    },
)
class StandardYarnSynthOptions(SimpleSynthOptions):
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.List[AdditionalArtifact]] = None,
        copy_environment_variables: typing.Optional[typing.List[builtins.str]] = None,
        environment: typing.Optional[_BuildEnvironment_77bc5f50] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        build_command: typing.Optional[builtins.str] = None,
        install_command: typing.Optional[builtins.str] = None,
        synth_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for a convention-based synth using Yarn.

        :param cloud_assembly_artifact: (experimental) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (experimental) The source artifact of the CodePipeline.
        :param action_name: (experimental) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (experimental) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: (experimental) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (experimental) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: (experimental) Environment variables to send into build. Default: - No additional environment variables
        :param project_name: (experimental) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (experimental) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (experimental) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (experimental) The VPC where to execute the SimpleSynth. Default: - No VPC
        :param build_command: (experimental) The build command. By default, we assume NPM projects are either written in JavaScript or are using ``ts-node``, so don't need a build command. Otherwise, put the build command here, for example ``npm run build``. Default: - No build required
        :param install_command: (experimental) The install command. Default: 'yarn install --frozen-lockfile'
        :param synth_command: (experimental) The synth command. Default: 'npx cdk synth'

        :stability: experimental
        '''
        if isinstance(environment, dict):
            environment = _BuildEnvironment_77bc5f50(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "source_artifact": source_artifact,
        }
        if action_name is not None:
            self._values["action_name"] = action_name
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if copy_environment_variables is not None:
            self._values["copy_environment_variables"] = copy_environment_variables
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc
        if build_command is not None:
            self._values["build_command"] = build_command
        if install_command is not None:
            self._values["install_command"] = install_command
        if synth_command is not None:
            self._values["synth_command"] = synth_command

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_9905eec2:
        '''(experimental) The artifact where the CloudAssembly should be emitted.

        :stability: experimental
        '''
        result = self._values.get("cloud_assembly_artifact")
        assert result is not None, "Required property 'cloud_assembly_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def source_artifact(self) -> _Artifact_9905eec2:
        '''(experimental) The source artifact of the CodePipeline.

        :stability: experimental
        '''
        result = self._values.get("source_artifact")
        assert result is not None, "Required property 'source_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the build action.

        :default: 'Synth'

        :stability: experimental
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[AdditionalArtifact]]:
        '''(experimental) Produce additional output artifacts after the build based on the given directories.

        Can be used to produce additional artifacts during the build step,
        separate from the cloud assembly, which can be used further on in the
        pipeline.

        Directories are evaluated with respect to ``subdirectory``.

        :default: - No additional artifacts generated

        :stability: experimental
        '''
        result = self._values.get("additional_artifacts")
        return typing.cast(typing.Optional[typing.List[AdditionalArtifact]], result)

    @builtins.property
    def copy_environment_variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Environment variables to copy over from parent env.

        These are environment variables that are being used by the build.

        :default: - No environment variables copied

        :stability: experimental
        '''
        result = self._values.get("copy_environment_variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(experimental) Build environment to use for CodeBuild job.

        :default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]]:
        '''(experimental) Environment variables to send into build.

        :default: - No additional environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the CodeBuild project.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        :default: - No policy statements added to CodeBuild Project Role

        :stability: experimental
        '''
        result = self._values.get("role_policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Directory inside the source where package.json and cdk.json are located.

        :default: - Repository root

        :stability: experimental
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The VPC where to execute the SimpleSynth.

        :default: - No VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The build command.

        By default, we assume NPM projects are either written in JavaScript or are
        using ``ts-node``, so don't need a build command.

        Otherwise, put the build command here, for example ``npm run build``.

        :default: - No build required

        :stability: experimental
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The install command.

        :default: 'yarn install --frozen-lockfile'

        :stability: experimental
        '''
        result = self._values.get("install_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synth_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The synth command.

        :default: 'npx cdk synth'

        :stability: experimental
        '''
        result = self._values.get("synth_command")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StandardYarnSynthOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_ecd54a08)
class UpdatePipelineAction(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.UpdatePipelineAction",
):
    '''(experimental) Action to self-mutate the pipeline.

    Creates a CodeBuild project which will use the CDK CLI
    to deploy the pipeline stack.

    You do not need to instantiate this action -- it will automatically
    be added by the pipeline.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cloud_assembly_input: _Artifact_9905eec2,
        pipeline_stack_name: builtins.str,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cloud_assembly_input: (experimental) The CodePipeline artifact that holds the Cloud Assembly.
        :param pipeline_stack_name: (experimental) Name of the pipeline stack.
        :param cdk_cli_version: (experimental) Version of CDK CLI to 'npm install'. Default: - Latest version
        :param project_name: (experimental) Name of the CodeBuild project. Default: - Automatically generated

        :stability: experimental
        '''
        props = UpdatePipelineActionProps(
            cloud_assembly_input=cloud_assembly_input,
            pipeline_stack_name=pipeline_stack_name,
            cdk_cli_version=cdk_cli_version,
            project_name=project_name,
        )

        jsii.create(UpdatePipelineAction, self, [scope, id, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(experimental) Exists to implement IAction.

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
        '''(experimental) Exists to implement IAction.

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
        '''(experimental) Exists to implement IAction.

        :stability: experimental
        '''
        return typing.cast(_ActionProperties_c7760ac6, jsii.get(self, "actionProperties"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.UpdatePipelineActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "pipeline_stack_name": "pipelineStackName",
        "cdk_cli_version": "cdkCliVersion",
        "project_name": "projectName",
    },
)
class UpdatePipelineActionProps:
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_9905eec2,
        pipeline_stack_name: builtins.str,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Props for the UpdatePipelineAction.

        :param cloud_assembly_input: (experimental) The CodePipeline artifact that holds the Cloud Assembly.
        :param pipeline_stack_name: (experimental) Name of the pipeline stack.
        :param cdk_cli_version: (experimental) Version of CDK CLI to 'npm install'. Default: - Latest version
        :param project_name: (experimental) Name of the CodeBuild project. Default: - Automatically generated

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cloud_assembly_input": cloud_assembly_input,
            "pipeline_stack_name": pipeline_stack_name,
        }
        if cdk_cli_version is not None:
            self._values["cdk_cli_version"] = cdk_cli_version
        if project_name is not None:
            self._values["project_name"] = project_name

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_9905eec2:
        '''(experimental) The CodePipeline artifact that holds the Cloud Assembly.

        :stability: experimental
        '''
        result = self._values.get("cloud_assembly_input")
        assert result is not None, "Required property 'cloud_assembly_input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def pipeline_stack_name(self) -> builtins.str:
        '''(experimental) Name of the pipeline stack.

        :stability: experimental
        '''
        result = self._values.get("pipeline_stack_name")
        assert result is not None, "Required property 'pipeline_stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cdk_cli_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version of CDK CLI to 'npm install'.

        :default: - Latest version

        :stability: experimental
        '''
        result = self._values.get("cdk_cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the CodeBuild project.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UpdatePipelineActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.CdkStackActionFromArtifactOptions",
    jsii_struct_bases=[DeployCdkStackActionOptions],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "base_action_name": "baseActionName",
        "change_set_name": "changeSetName",
        "execute_run_order": "executeRunOrder",
        "output": "output",
        "output_file_name": "outputFileName",
        "prepare_run_order": "prepareRunOrder",
        "stack_name": "stackName",
    },
)
class CdkStackActionFromArtifactOptions(DeployCdkStackActionOptions):
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_9905eec2,
        base_action_name: typing.Optional[builtins.str] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
        stack_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for the 'fromStackArtifact' operation.

        :param cloud_assembly_input: (experimental) The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: (experimental) Base name of the action. Default: stackName
        :param change_set_name: (experimental) Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: (experimental) Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: (experimental) Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: (experimental) Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: (experimental) Run order for the Prepare action. Default: 1
        :param stack_name: (experimental) The name of the stack that should be created/updated. Default: - Same as stack artifact

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cloud_assembly_input": cloud_assembly_input,
        }
        if base_action_name is not None:
            self._values["base_action_name"] = base_action_name
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if prepare_run_order is not None:
            self._values["prepare_run_order"] = prepare_run_order
        if stack_name is not None:
            self._values["stack_name"] = stack_name

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_9905eec2:
        '''(experimental) The CodePipeline artifact that holds the Cloud Assembly.

        :stability: experimental
        '''
        result = self._values.get("cloud_assembly_input")
        assert result is not None, "Required property 'cloud_assembly_input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def base_action_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Base name of the action.

        :default: stackName

        :stability: experimental
        '''
        result = self._values.get("base_action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def change_set_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the change set to create and deploy.

        :default: 'PipelineChange'

        :stability: experimental
        '''
        result = self._values.get("change_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Run order for the Execute action.

        :default: - prepareRunOrder + 1

        :stability: experimental
        '''
        result = self._values.get("execute_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) Artifact to write Stack Outputs to.

        :default: - No outputs

        :stability: experimental
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def output_file_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Filename in output to write Stack outputs to.

        :default: - Required when 'output' is set

        :stability: experimental
        '''
        result = self._values.get("output_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prepare_run_order(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Run order for the Prepare action.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("prepare_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the stack that should be created/updated.

        :default: - Same as stack artifact

        :stability: experimental
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkStackActionFromArtifactOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.SimpleSynthActionProps",
    jsii_struct_bases=[SimpleSynthOptions],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "source_artifact": "sourceArtifact",
        "action_name": "actionName",
        "additional_artifacts": "additionalArtifacts",
        "copy_environment_variables": "copyEnvironmentVariables",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
        "role_policy_statements": "rolePolicyStatements",
        "subdirectory": "subdirectory",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "synth_command": "synthCommand",
        "build_command": "buildCommand",
        "build_commands": "buildCommands",
        "install_command": "installCommand",
        "install_commands": "installCommands",
        "test_commands": "testCommands",
    },
)
class SimpleSynthActionProps(SimpleSynthOptions):
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.List[AdditionalArtifact]] = None,
        copy_environment_variables: typing.Optional[typing.List[builtins.str]] = None,
        environment: typing.Optional[_BuildEnvironment_77bc5f50] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[_SubnetSelection_1284e62c] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        synth_command: builtins.str,
        build_command: typing.Optional[builtins.str] = None,
        build_commands: typing.Optional[typing.List[builtins.str]] = None,
        install_command: typing.Optional[builtins.str] = None,
        install_commands: typing.Optional[typing.List[builtins.str]] = None,
        test_commands: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''(experimental) Construction props for SimpleSynthAction.

        :param cloud_assembly_artifact: (experimental) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (experimental) The source artifact of the CodePipeline.
        :param action_name: (experimental) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (experimental) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: (experimental) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (experimental) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: (experimental) Environment variables to send into build. Default: - No additional environment variables
        :param project_name: (experimental) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (experimental) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (experimental) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (experimental) The VPC where to execute the SimpleSynth. Default: - No VPC
        :param synth_command: (experimental) The synth command.
        :param build_command: (deprecated) The build command. If your programming language requires a compilation step, put the compilation command here. Default: - No build required
        :param build_commands: (experimental) The build commands. If your programming language requires a compilation step, put the compilation command here. Default: - No build required
        :param install_command: (deprecated) The install command. If not provided by the build image or another dependency management tool, at least install the CDK CLI here using ``npm install -g aws-cdk``. Default: - No install required
        :param install_commands: (experimental) Install commands. If not provided by the build image or another dependency management tool, at least install the CDK CLI here using ``npm install -g aws-cdk``. Default: - No install required
        :param test_commands: (experimental) Test commands. These commands are run after the build commands but before the synth command. Default: - No test commands

        :stability: experimental
        '''
        if isinstance(environment, dict):
            environment = _BuildEnvironment_77bc5f50(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "source_artifact": source_artifact,
            "synth_command": synth_command,
        }
        if action_name is not None:
            self._values["action_name"] = action_name
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if copy_environment_variables is not None:
            self._values["copy_environment_variables"] = copy_environment_variables
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc
        if build_command is not None:
            self._values["build_command"] = build_command
        if build_commands is not None:
            self._values["build_commands"] = build_commands
        if install_command is not None:
            self._values["install_command"] = install_command
        if install_commands is not None:
            self._values["install_commands"] = install_commands
        if test_commands is not None:
            self._values["test_commands"] = test_commands

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_9905eec2:
        '''(experimental) The artifact where the CloudAssembly should be emitted.

        :stability: experimental
        '''
        result = self._values.get("cloud_assembly_artifact")
        assert result is not None, "Required property 'cloud_assembly_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def source_artifact(self) -> _Artifact_9905eec2:
        '''(experimental) The source artifact of the CodePipeline.

        :stability: experimental
        '''
        result = self._values.get("source_artifact")
        assert result is not None, "Required property 'source_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the build action.

        :default: 'Synth'

        :stability: experimental
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[AdditionalArtifact]]:
        '''(experimental) Produce additional output artifacts after the build based on the given directories.

        Can be used to produce additional artifacts during the build step,
        separate from the cloud assembly, which can be used further on in the
        pipeline.

        Directories are evaluated with respect to ``subdirectory``.

        :default: - No additional artifacts generated

        :stability: experimental
        '''
        result = self._values.get("additional_artifacts")
        return typing.cast(typing.Optional[typing.List[AdditionalArtifact]], result)

    @builtins.property
    def copy_environment_variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Environment variables to copy over from parent env.

        These are environment variables that are being used by the build.

        :default: - No environment variables copied

        :stability: experimental
        '''
        result = self._values.get("copy_environment_variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(experimental) Build environment to use for CodeBuild job.

        :default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]]:
        '''(experimental) Environment variables to send into build.

        :default: - No additional environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the CodeBuild project.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        :default: - No policy statements added to CodeBuild Project Role

        :stability: experimental
        '''
        result = self._values.get("role_policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''(experimental) Directory inside the source where package.json and cdk.json are located.

        :default: - Repository root

        :stability: experimental
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The VPC where to execute the SimpleSynth.

        :default: - No VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def synth_command(self) -> builtins.str:
        '''(experimental) The synth command.

        :stability: experimental
        '''
        result = self._values.get("synth_command")
        assert result is not None, "Required property 'synth_command' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The build command.

        If your programming language requires a compilation step, put the
        compilation command here.

        :default: - No build required

        :deprecated: Use ``buildCommands`` instead

        :stability: deprecated
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The build commands.

        If your programming language requires a compilation step, put the
        compilation command here.

        :default: - No build required

        :stability: experimental
        '''
        result = self._values.get("build_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def install_command(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The install command.

        If not provided by the build image or another dependency
        management tool, at least install the CDK CLI here using
        ``npm install -g aws-cdk``.

        :default: - No install required

        :deprecated: Use ``installCommands`` instead

        :stability: deprecated
        '''
        result = self._values.get("install_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Install commands.

        If not provided by the build image or another dependency
        management tool, at least install the CDK CLI here using
        ``npm install -g aws-cdk``.

        :default: - No install required

        :stability: experimental
        '''
        result = self._values.get("install_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def test_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Test commands.

        These commands are run after the build commands but before the
        synth command.

        :default: - No test commands

        :stability: experimental
        '''
        result = self._values.get("test_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SimpleSynthActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddManualApprovalOptions",
    "AddStackOptions",
    "AddStageOptions",
    "AdditionalArtifact",
    "AssetPublishingCommand",
    "AssetType",
    "CdkPipeline",
    "CdkPipelineProps",
    "CdkStackActionFromArtifactOptions",
    "CdkStage",
    "CdkStageProps",
    "DeployCdkStackAction",
    "DeployCdkStackActionOptions",
    "DeployCdkStackActionProps",
    "FromStackArtifactOptions",
    "IStageHost",
    "PublishAssetsAction",
    "PublishAssetsActionProps",
    "ShellScriptAction",
    "ShellScriptActionProps",
    "SimpleSynthAction",
    "SimpleSynthActionProps",
    "SimpleSynthOptions",
    "StackOutput",
    "StandardNpmSynthOptions",
    "StandardYarnSynthOptions",
    "UpdatePipelineAction",
    "UpdatePipelineActionProps",
]

publication.publish()
