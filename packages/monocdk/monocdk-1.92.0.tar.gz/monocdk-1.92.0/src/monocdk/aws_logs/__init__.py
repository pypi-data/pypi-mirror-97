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
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_cloudwatch import (
    Metric as _Metric_5b2b8e58,
    MetricOptions as _MetricOptions_1c185ae8,
    Unit as _Unit_113c79f9,
)
from ..aws_iam import (
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    IRole as _IRole_59af6f50,
    PolicyDocument as _PolicyDocument_b5de5177,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_kms import IKey as _IKey_36930160


@jsii.implements(_IInspectable_82c04a63)
class CfnDestination(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CfnDestination",
):
    '''A CloudFormation ``AWS::Logs::Destination``.

    :cloudformationResource: AWS::Logs::Destination
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        destination_name: builtins.str,
        destination_policy: builtins.str,
        role_arn: builtins.str,
        target_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Logs::Destination``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_name: ``AWS::Logs::Destination.DestinationName``.
        :param destination_policy: ``AWS::Logs::Destination.DestinationPolicy``.
        :param role_arn: ``AWS::Logs::Destination.RoleArn``.
        :param target_arn: ``AWS::Logs::Destination.TargetArn``.
        '''
        props = CfnDestinationProps(
            destination_name=destination_name,
            destination_policy=destination_policy,
            role_arn=role_arn,
            target_arn=target_arn,
        )

        jsii.create(CfnDestination, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="destinationName")
    def destination_name(self) -> builtins.str:
        '''``AWS::Logs::Destination.DestinationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationName"))

    @destination_name.setter
    def destination_name(self, value: builtins.str) -> None:
        jsii.set(self, "destinationName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="destinationPolicy")
    def destination_policy(self) -> builtins.str:
        '''``AWS::Logs::Destination.DestinationPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationpolicy
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationPolicy"))

    @destination_policy.setter
    def destination_policy(self, value: builtins.str) -> None:
        jsii.set(self, "destinationPolicy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''``AWS::Logs::Destination.RoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''``AWS::Logs::Destination.TargetArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-targetarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @target_arn.setter
    def target_arn(self, value: builtins.str) -> None:
        jsii.set(self, "targetArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CfnDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_name": "destinationName",
        "destination_policy": "destinationPolicy",
        "role_arn": "roleArn",
        "target_arn": "targetArn",
    },
)
class CfnDestinationProps:
    def __init__(
        self,
        *,
        destination_name: builtins.str,
        destination_policy: builtins.str,
        role_arn: builtins.str,
        target_arn: builtins.str,
    ) -> None:
        '''Properties for defining a ``AWS::Logs::Destination``.

        :param destination_name: ``AWS::Logs::Destination.DestinationName``.
        :param destination_policy: ``AWS::Logs::Destination.DestinationPolicy``.
        :param role_arn: ``AWS::Logs::Destination.RoleArn``.
        :param target_arn: ``AWS::Logs::Destination.TargetArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "destination_name": destination_name,
            "destination_policy": destination_policy,
            "role_arn": role_arn,
            "target_arn": target_arn,
        }

    @builtins.property
    def destination_name(self) -> builtins.str:
        '''``AWS::Logs::Destination.DestinationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationname
        '''
        result = self._values.get("destination_name")
        assert result is not None, "Required property 'destination_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_policy(self) -> builtins.str:
        '''``AWS::Logs::Destination.DestinationPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationpolicy
        '''
        result = self._values.get("destination_policy")
        assert result is not None, "Required property 'destination_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''``AWS::Logs::Destination.RoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''``AWS::Logs::Destination.TargetArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-targetarn
        '''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLogGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CfnLogGroup",
):
    '''A CloudFormation ``AWS::Logs::LogGroup``.

    :cloudformationResource: AWS::Logs::LogGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        retention_in_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::LogGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param kms_key_id: ``AWS::Logs::LogGroup.KmsKeyId``.
        :param log_group_name: ``AWS::Logs::LogGroup.LogGroupName``.
        :param retention_in_days: ``AWS::Logs::LogGroup.RetentionInDays``.
        '''
        props = CfnLogGroupProps(
            kms_key_id=kms_key_id,
            log_group_name=log_group_name,
            retention_in_days=retention_in_days,
        )

        jsii.create(CfnLogGroup, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::Logs::LogGroup.KmsKeyId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Logs::LogGroup.LogGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-loggroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "logGroupName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="retentionInDays")
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Logs::LogGroup.RetentionInDays``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-retentionindays
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionInDays"))

    @retention_in_days.setter
    def retention_in_days(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "retentionInDays", value)


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CfnLogGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_id": "kmsKeyId",
        "log_group_name": "logGroupName",
        "retention_in_days": "retentionInDays",
    },
)
class CfnLogGroupProps:
    def __init__(
        self,
        *,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        retention_in_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Logs::LogGroup``.

        :param kms_key_id: ``AWS::Logs::LogGroup.KmsKeyId``.
        :param log_group_name: ``AWS::Logs::LogGroup.LogGroupName``.
        :param retention_in_days: ``AWS::Logs::LogGroup.RetentionInDays``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if retention_in_days is not None:
            self._values["retention_in_days"] = retention_in_days

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::Logs::LogGroup.KmsKeyId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Logs::LogGroup.LogGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-loggroupname
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Logs::LogGroup.RetentionInDays``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-retentionindays
        '''
        result = self._values.get("retention_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLogGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLogStream(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CfnLogStream",
):
    '''A CloudFormation ``AWS::Logs::LogStream``.

    :cloudformationResource: AWS::Logs::LogStream
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        log_group_name: builtins.str,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::LogStream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param log_group_name: ``AWS::Logs::LogStream.LogGroupName``.
        :param log_stream_name: ``AWS::Logs::LogStream.LogStreamName``.
        '''
        props = CfnLogStreamProps(
            log_group_name=log_group_name, log_stream_name=log_stream_name
        )

        jsii.create(CfnLogStream, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''``AWS::Logs::LogStream.LogGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-loggroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "logGroupName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Logs::LogStream.LogStreamName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-logstreamname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamName"))

    @log_stream_name.setter
    def log_stream_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "logStreamName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CfnLogStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "log_stream_name": "logStreamName",
    },
)
class CfnLogStreamProps:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Logs::LogStream``.

        :param log_group_name: ``AWS::Logs::LogStream.LogGroupName``.
        :param log_stream_name: ``AWS::Logs::LogStream.LogStreamName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "log_group_name": log_group_name,
        }
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''``AWS::Logs::LogStream.LogGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-loggroupname
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Logs::LogStream.LogStreamName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-logstreamname
        '''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLogStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnMetricFilter(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CfnMetricFilter",
):
    '''A CloudFormation ``AWS::Logs::MetricFilter``.

    :cloudformationResource: AWS::Logs::MetricFilter
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        filter_pattern: builtins.str,
        log_group_name: builtins.str,
        metric_transformations: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricFilter.MetricTransformationProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        '''Create a new ``AWS::Logs::MetricFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param filter_pattern: ``AWS::Logs::MetricFilter.FilterPattern``.
        :param log_group_name: ``AWS::Logs::MetricFilter.LogGroupName``.
        :param metric_transformations: ``AWS::Logs::MetricFilter.MetricTransformations``.
        '''
        props = CfnMetricFilterProps(
            filter_pattern=filter_pattern,
            log_group_name=log_group_name,
            metric_transformations=metric_transformations,
        )

        jsii.create(CfnMetricFilter, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filterPattern")
    def filter_pattern(self) -> builtins.str:
        '''``AWS::Logs::MetricFilter.FilterPattern``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-filterpattern
        '''
        return typing.cast(builtins.str, jsii.get(self, "filterPattern"))

    @filter_pattern.setter
    def filter_pattern(self, value: builtins.str) -> None:
        jsii.set(self, "filterPattern", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''``AWS::Logs::MetricFilter.LogGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-loggroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "logGroupName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="metricTransformations")
    def metric_transformations(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricFilter.MetricTransformationProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::Logs::MetricFilter.MetricTransformations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-metrictransformations
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricFilter.MetricTransformationProperty", _IResolvable_a771d0ef]]], jsii.get(self, "metricTransformations"))

    @metric_transformations.setter
    def metric_transformations(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnMetricFilter.MetricTransformationProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "metricTransformations", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_logs.CfnMetricFilter.MetricTransformationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric_name": "metricName",
            "metric_namespace": "metricNamespace",
            "metric_value": "metricValue",
            "default_value": "defaultValue",
        },
    )
    class MetricTransformationProperty:
        def __init__(
            self,
            *,
            metric_name: builtins.str,
            metric_namespace: builtins.str,
            metric_value: builtins.str,
            default_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param metric_name: ``CfnMetricFilter.MetricTransformationProperty.MetricName``.
            :param metric_namespace: ``CfnMetricFilter.MetricTransformationProperty.MetricNamespace``.
            :param metric_value: ``CfnMetricFilter.MetricTransformationProperty.MetricValue``.
            :param default_value: ``CfnMetricFilter.MetricTransformationProperty.DefaultValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "metric_name": metric_name,
                "metric_namespace": metric_namespace,
                "metric_value": metric_value,
            }
            if default_value is not None:
                self._values["default_value"] = default_value

        @builtins.property
        def metric_name(self) -> builtins.str:
            '''``CfnMetricFilter.MetricTransformationProperty.MetricName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-cwl-metricfilter-metrictransformation-metricname
            '''
            result = self._values.get("metric_name")
            assert result is not None, "Required property 'metric_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def metric_namespace(self) -> builtins.str:
            '''``CfnMetricFilter.MetricTransformationProperty.MetricNamespace``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-cwl-metricfilter-metrictransformation-metricnamespace
            '''
            result = self._values.get("metric_namespace")
            assert result is not None, "Required property 'metric_namespace' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def metric_value(self) -> builtins.str:
            '''``CfnMetricFilter.MetricTransformationProperty.MetricValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-cwl-metricfilter-metrictransformation-metricvalue
            '''
            result = self._values.get("metric_value")
            assert result is not None, "Required property 'metric_value' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def default_value(self) -> typing.Optional[jsii.Number]:
            '''``CfnMetricFilter.MetricTransformationProperty.DefaultValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-cwl-metricfilter-metrictransformation-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricTransformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CfnMetricFilterProps",
    jsii_struct_bases=[],
    name_mapping={
        "filter_pattern": "filterPattern",
        "log_group_name": "logGroupName",
        "metric_transformations": "metricTransformations",
    },
)
class CfnMetricFilterProps:
    def __init__(
        self,
        *,
        filter_pattern: builtins.str,
        log_group_name: builtins.str,
        metric_transformations: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricFilter.MetricTransformationProperty, _IResolvable_a771d0ef]]],
    ) -> None:
        '''Properties for defining a ``AWS::Logs::MetricFilter``.

        :param filter_pattern: ``AWS::Logs::MetricFilter.FilterPattern``.
        :param log_group_name: ``AWS::Logs::MetricFilter.LogGroupName``.
        :param metric_transformations: ``AWS::Logs::MetricFilter.MetricTransformations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "filter_pattern": filter_pattern,
            "log_group_name": log_group_name,
            "metric_transformations": metric_transformations,
        }

    @builtins.property
    def filter_pattern(self) -> builtins.str:
        '''``AWS::Logs::MetricFilter.FilterPattern``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-filterpattern
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''``AWS::Logs::MetricFilter.LogGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-loggroupname
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_transformations(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricFilter.MetricTransformationProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::Logs::MetricFilter.MetricTransformations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-metrictransformations
        '''
        result = self._values.get("metric_transformations")
        assert result is not None, "Required property 'metric_transformations' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnMetricFilter.MetricTransformationProperty, _IResolvable_a771d0ef]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMetricFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSubscriptionFilter(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CfnSubscriptionFilter",
):
    '''A CloudFormation ``AWS::Logs::SubscriptionFilter``.

    :cloudformationResource: AWS::Logs::SubscriptionFilter
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        destination_arn: builtins.str,
        filter_pattern: builtins.str,
        log_group_name: builtins.str,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Logs::SubscriptionFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_arn: ``AWS::Logs::SubscriptionFilter.DestinationArn``.
        :param filter_pattern: ``AWS::Logs::SubscriptionFilter.FilterPattern``.
        :param log_group_name: ``AWS::Logs::SubscriptionFilter.LogGroupName``.
        :param role_arn: ``AWS::Logs::SubscriptionFilter.RoleArn``.
        '''
        props = CfnSubscriptionFilterProps(
            destination_arn=destination_arn,
            filter_pattern=filter_pattern,
            log_group_name=log_group_name,
            role_arn=role_arn,
        )

        jsii.create(CfnSubscriptionFilter, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        '''``AWS::Logs::SubscriptionFilter.DestinationArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-destinationarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: builtins.str) -> None:
        jsii.set(self, "destinationArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filterPattern")
    def filter_pattern(self) -> builtins.str:
        '''``AWS::Logs::SubscriptionFilter.FilterPattern``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-filterpattern
        '''
        return typing.cast(builtins.str, jsii.get(self, "filterPattern"))

    @filter_pattern.setter
    def filter_pattern(self, value: builtins.str) -> None:
        jsii.set(self, "filterPattern", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''``AWS::Logs::SubscriptionFilter.LogGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-loggroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "logGroupName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Logs::SubscriptionFilter.RoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CfnSubscriptionFilterProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_arn": "destinationArn",
        "filter_pattern": "filterPattern",
        "log_group_name": "logGroupName",
        "role_arn": "roleArn",
    },
)
class CfnSubscriptionFilterProps:
    def __init__(
        self,
        *,
        destination_arn: builtins.str,
        filter_pattern: builtins.str,
        log_group_name: builtins.str,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Logs::SubscriptionFilter``.

        :param destination_arn: ``AWS::Logs::SubscriptionFilter.DestinationArn``.
        :param filter_pattern: ``AWS::Logs::SubscriptionFilter.FilterPattern``.
        :param log_group_name: ``AWS::Logs::SubscriptionFilter.LogGroupName``.
        :param role_arn: ``AWS::Logs::SubscriptionFilter.RoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "destination_arn": destination_arn,
            "filter_pattern": filter_pattern,
            "log_group_name": log_group_name,
        }
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def destination_arn(self) -> builtins.str:
        '''``AWS::Logs::SubscriptionFilter.DestinationArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-destinationarn
        '''
        result = self._values.get("destination_arn")
        assert result is not None, "Required property 'destination_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_pattern(self) -> builtins.str:
        '''``AWS::Logs::SubscriptionFilter.FilterPattern``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-filterpattern
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''``AWS::Logs::SubscriptionFilter.LogGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-loggroupname
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Logs::SubscriptionFilter.RoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.ColumnRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "comparison": "comparison",
        "number_value": "numberValue",
        "string_value": "stringValue",
    },
)
class ColumnRestriction:
    def __init__(
        self,
        *,
        comparison: builtins.str,
        number_value: typing.Optional[jsii.Number] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparison: (experimental) Comparison operator to use.
        :param number_value: (experimental) Number value to compare to. Exactly one of 'stringValue' and 'numberValue' must be set.
        :param string_value: (experimental) String value to compare to. Exactly one of 'stringValue' and 'numberValue' must be set.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "comparison": comparison,
        }
        if number_value is not None:
            self._values["number_value"] = number_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def comparison(self) -> builtins.str:
        '''(experimental) Comparison operator to use.

        :stability: experimental
        '''
        result = self._values.get("comparison")
        assert result is not None, "Required property 'comparison' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def number_value(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number value to compare to.

        Exactly one of 'stringValue' and 'numberValue' must be set.

        :stability: experimental
        '''
        result = self._values.get("number_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''(experimental) String value to compare to.

        Exactly one of 'stringValue' and 'numberValue' must be set.

        :stability: experimental
        '''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ColumnRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.CrossAccountDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "role": "role",
        "target_arn": "targetArn",
        "destination_name": "destinationName",
    },
)
class CrossAccountDestinationProps:
    def __init__(
        self,
        *,
        role: _IRole_59af6f50,
        target_arn: builtins.str,
        destination_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a CrossAccountDestination.

        :param role: (experimental) The role to assume that grants permissions to write to 'target'. The role must be assumable by 'logs.{REGION}.amazonaws.com'.
        :param target_arn: (experimental) The log destination target's ARN.
        :param destination_name: (experimental) The name of the log destination. Default: Automatically generated

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "role": role,
            "target_arn": target_arn,
        }
        if destination_name is not None:
            self._values["destination_name"] = destination_name

    @builtins.property
    def role(self) -> _IRole_59af6f50:
        '''(experimental) The role to assume that grants permissions to write to 'target'.

        The role must be assumable by 'logs.{REGION}.amazonaws.com'.

        :stability: experimental
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(_IRole_59af6f50, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''(experimental) The log destination target's ARN.

        :stability: experimental
        '''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the log destination.

        :default: Automatically generated

        :stability: experimental
        '''
        result = self._values.get("destination_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrossAccountDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FilterPattern(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.FilterPattern",
):
    '''(experimental) A collection of static methods to generate appropriate ILogPatterns.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(FilterPattern, self, [])

    @jsii.member(jsii_name="all") # type: ignore[misc]
    @builtins.classmethod
    def all(cls, *patterns: "JsonPattern") -> "JsonPattern":
        '''(experimental) A JSON log pattern that matches if all given JSON log patterns match.

        :param patterns: -

        :stability: experimental
        '''
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "all", [*patterns]))

    @jsii.member(jsii_name="allEvents") # type: ignore[misc]
    @builtins.classmethod
    def all_events(cls) -> "IFilterPattern":
        '''(experimental) A log pattern that matches all events.

        :stability: experimental
        '''
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "allEvents", []))

    @jsii.member(jsii_name="allTerms") # type: ignore[misc]
    @builtins.classmethod
    def all_terms(cls, *terms: builtins.str) -> "IFilterPattern":
        '''(experimental) A log pattern that matches if all the strings given appear in the event.

        :param terms: The words to search for. All terms must match.

        :stability: experimental
        '''
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "allTerms", [*terms]))

    @jsii.member(jsii_name="any") # type: ignore[misc]
    @builtins.classmethod
    def any(cls, *patterns: "JsonPattern") -> "JsonPattern":
        '''(experimental) A JSON log pattern that matches if any of the given JSON log patterns match.

        :param patterns: -

        :stability: experimental
        '''
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "any", [*patterns]))

    @jsii.member(jsii_name="anyTerm") # type: ignore[misc]
    @builtins.classmethod
    def any_term(cls, *terms: builtins.str) -> "IFilterPattern":
        '''(experimental) A log pattern that matches if any of the strings given appear in the event.

        :param terms: The words to search for. Any terms must match.

        :stability: experimental
        '''
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "anyTerm", [*terms]))

    @jsii.member(jsii_name="anyTermGroup") # type: ignore[misc]
    @builtins.classmethod
    def any_term_group(
        cls,
        *term_groups: typing.List[builtins.str],
    ) -> "IFilterPattern":
        '''(experimental) A log pattern that matches if any of the given term groups matches the event.

        A term group matches an event if all the terms in it appear in the event string.

        :param term_groups: A list of term groups to search for. Any one of the clauses must match.

        :stability: experimental
        '''
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "anyTermGroup", [*term_groups]))

    @jsii.member(jsii_name="booleanValue") # type: ignore[misc]
    @builtins.classmethod
    def boolean_value(
        cls,
        json_field: builtins.str,
        value: builtins.bool,
    ) -> "JsonPattern":
        '''(experimental) A JSON log pattern that matches if the field exists and equals the boolean value.

        :param json_field: Field inside JSON. Example: "$.myField"
        :param value: The value to match.

        :stability: experimental
        '''
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "booleanValue", [json_field, value]))

    @jsii.member(jsii_name="exists") # type: ignore[misc]
    @builtins.classmethod
    def exists(cls, json_field: builtins.str) -> "JsonPattern":
        '''(experimental) A JSON log patter that matches if the field exists.

        This is a readable convenience wrapper over 'field = *'

        :param json_field: Field inside JSON. Example: "$.myField"

        :stability: experimental
        '''
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "exists", [json_field]))

    @jsii.member(jsii_name="isNull") # type: ignore[misc]
    @builtins.classmethod
    def is_null(cls, json_field: builtins.str) -> "JsonPattern":
        '''(experimental) A JSON log pattern that matches if the field exists and has the special value 'null'.

        :param json_field: Field inside JSON. Example: "$.myField"

        :stability: experimental
        '''
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "isNull", [json_field]))

    @jsii.member(jsii_name="literal") # type: ignore[misc]
    @builtins.classmethod
    def literal(cls, log_pattern_string: builtins.str) -> "IFilterPattern":
        '''(experimental) Use the given string as log pattern.

        See https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html
        for information on writing log patterns.

        :param log_pattern_string: The pattern string to use.

        :stability: experimental
        '''
        return typing.cast("IFilterPattern", jsii.sinvoke(cls, "literal", [log_pattern_string]))

    @jsii.member(jsii_name="notExists") # type: ignore[misc]
    @builtins.classmethod
    def not_exists(cls, json_field: builtins.str) -> "JsonPattern":
        '''(experimental) A JSON log pattern that matches if the field does not exist.

        :param json_field: Field inside JSON. Example: "$.myField"

        :stability: experimental
        '''
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "notExists", [json_field]))

    @jsii.member(jsii_name="numberValue") # type: ignore[misc]
    @builtins.classmethod
    def number_value(
        cls,
        json_field: builtins.str,
        comparison: builtins.str,
        value: jsii.Number,
    ) -> "JsonPattern":
        '''(experimental) A JSON log pattern that compares numerical values.

        This pattern only matches if the event is a JSON event, and the indicated field inside
        compares with the value in the indicated way.

        Use '$' to indicate the root of the JSON structure. The comparison operator can only
        compare equality or inequality. The '*' wildcard may appear in the value may at the
        start or at the end.

        For more information, see:

        https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html

        :param json_field: Field inside JSON. Example: "$.myField"
        :param comparison: Comparison to carry out. One of =, !=, <, <=, >, >=.
        :param value: The numerical value to compare to.

        :stability: experimental
        '''
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "numberValue", [json_field, comparison, value]))

    @jsii.member(jsii_name="spaceDelimited") # type: ignore[misc]
    @builtins.classmethod
    def space_delimited(cls, *columns: builtins.str) -> "SpaceDelimitedTextPattern":
        '''(experimental) A space delimited log pattern matcher.

        The log event is divided into space-delimited columns (optionally
        enclosed by "" or [] to capture spaces into column values), and names
        are given to each column.

        '...' may be specified once to match any number of columns.

        Afterwards, conditions may be added to individual columns.

        :param columns: The columns in the space-delimited log stream.

        :stability: experimental
        '''
        return typing.cast("SpaceDelimitedTextPattern", jsii.sinvoke(cls, "spaceDelimited", [*columns]))

    @jsii.member(jsii_name="stringValue") # type: ignore[misc]
    @builtins.classmethod
    def string_value(
        cls,
        json_field: builtins.str,
        comparison: builtins.str,
        value: builtins.str,
    ) -> "JsonPattern":
        '''(experimental) A JSON log pattern that compares string values.

        This pattern only matches if the event is a JSON event, and the indicated field inside
        compares with the string value.

        Use '$' to indicate the root of the JSON structure. The comparison operator can only
        compare equality or inequality. The '*' wildcard may appear in the value may at the
        start or at the end.

        For more information, see:

        https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html

        :param json_field: Field inside JSON. Example: "$.myField"
        :param comparison: Comparison to carry out. Either = or !=.
        :param value: The string value to compare to. May use '*' as wildcard at start or end of string.

        :stability: experimental
        '''
        return typing.cast("JsonPattern", jsii.sinvoke(cls, "stringValue", [json_field, comparison, value]))


@jsii.interface(jsii_type="monocdk.aws_logs.IFilterPattern")
class IFilterPattern(typing_extensions.Protocol):
    '''(experimental) Interface for objects that can render themselves to log patterns.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IFilterPatternProxy"]:
        return _IFilterPatternProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...


class _IFilterPatternProxy:
    '''(experimental) Interface for objects that can render themselves to log patterns.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_logs.IFilterPattern"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logPatternString"))


@jsii.interface(jsii_type="monocdk.aws_logs.ILogGroup")
class ILogGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ILogGroupProxy"]:
        return _ILogGroupProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of this log group, with ':*' appended.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''(experimental) The name of this log group.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(
        self,
        id: builtins.str,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> "MetricFilter":
        '''(experimental) Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: (experimental) Pattern to search for log events.
        :param metric_name: (experimental) The name of the metric to emit.
        :param metric_namespace: (experimental) The namespace of the metric to emit.
        :param default_value: (experimental) The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: (experimental) The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addStream")
    def add_stream(
        self,
        id: builtins.str,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> "LogStream":
        '''(experimental) Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: (experimental) The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(
        self,
        id: builtins.str,
        *,
        destination: "ILogSubscriptionDestination",
        filter_pattern: IFilterPattern,
    ) -> "SubscriptionFilter":
        '''(experimental) Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: (experimental) The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: (experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(
        self,
        json_field: builtins.str,
        metric_namespace: builtins.str,
        metric_name: builtins.str,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        :return: A Metric object representing the extracted metric

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Give permissions to write to create and write to streams in this log group.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _ILogGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_logs.ILogGroup"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of this log group, with ':*' appended.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''(experimental) The name of this log group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(
        self,
        id: builtins.str,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> "MetricFilter":
        '''(experimental) Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: (experimental) Pattern to search for log events.
        :param metric_name: (experimental) The name of the metric to emit.
        :param metric_namespace: (experimental) The namespace of the metric to emit.
        :param default_value: (experimental) The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: (experimental) The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        :stability: experimental
        '''
        props = MetricFilterOptions(
            filter_pattern=filter_pattern,
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            default_value=default_value,
            metric_value=metric_value,
        )

        return typing.cast("MetricFilter", jsii.invoke(self, "addMetricFilter", [id, props]))

    @jsii.member(jsii_name="addStream")
    def add_stream(
        self,
        id: builtins.str,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> "LogStream":
        '''(experimental) Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: (experimental) The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        :stability: experimental
        '''
        props = StreamOptions(log_stream_name=log_stream_name)

        return typing.cast("LogStream", jsii.invoke(self, "addStream", [id, props]))

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(
        self,
        id: builtins.str,
        *,
        destination: "ILogSubscriptionDestination",
        filter_pattern: IFilterPattern,
    ) -> "SubscriptionFilter":
        '''(experimental) Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: (experimental) The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: (experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        props = SubscriptionFilterOptions(
            destination=destination, filter_pattern=filter_pattern
        )

        return typing.cast("SubscriptionFilter", jsii.invoke(self, "addSubscriptionFilter", [id, props]))

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(
        self,
        json_field: builtins.str,
        metric_namespace: builtins.str,
        metric_name: builtins.str,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        :return: A Metric object representing the extracted metric

        :stability: experimental
        '''
        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "extractMetric", [json_field, metric_namespace, metric_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Give permissions to write to create and write to streams in this log group.

        :param grantee: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [grantee]))


@jsii.interface(jsii_type="monocdk.aws_logs.ILogStream")
class ILogStream(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ILogStreamProxy"]:
        return _ILogStreamProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        '''(experimental) The name of this log stream.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ILogStreamProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_logs.ILogStream"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        '''(experimental) The name of this log stream.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))


@jsii.interface(jsii_type="monocdk.aws_logs.ILogSubscriptionDestination")
class ILogSubscriptionDestination(typing_extensions.Protocol):
    '''(experimental) Interface for classes that can be the destination of a log Subscription.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ILogSubscriptionDestinationProxy"]:
        return _ILogSubscriptionDestinationProxy

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        source_log_group: ILogGroup,
    ) -> "LogSubscriptionDestinationConfig":
        '''(experimental) Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param source_log_group: -

        :stability: experimental
        '''
        ...


class _ILogSubscriptionDestinationProxy:
    '''(experimental) Interface for classes that can be the destination of a log Subscription.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_logs.ILogSubscriptionDestination"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        source_log_group: ILogGroup,
    ) -> "LogSubscriptionDestinationConfig":
        '''(experimental) Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param source_log_group: -

        :stability: experimental
        '''
        return typing.cast("LogSubscriptionDestinationConfig", jsii.invoke(self, "bind", [scope, source_log_group]))


@jsii.implements(IFilterPattern)
class JsonPattern(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_logs.JsonPattern",
):
    '''(experimental) Base class for patterns that only match JSON log events.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_JsonPatternProxy"]:
        return _JsonPatternProxy

    def __init__(self, json_pattern_string: builtins.str) -> None:
        '''
        :param json_pattern_string: -

        :stability: experimental
        '''
        jsii.create(JsonPattern, self, [json_pattern_string])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="jsonPatternString")
    def json_pattern_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jsonPatternString"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logPatternString"))


class _JsonPatternProxy(JsonPattern):
    pass


@jsii.implements(ILogGroup)
class LogGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.LogGroup",
):
    '''(experimental) Define a CloudWatch Log Group.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        retention: typing.Optional["RetentionDays"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param encryption_key: (experimental) The KMS Key to encrypt the log group with. Default: - log group is encrypted with the default master key
        :param log_group_name: (experimental) Name of the log group. Default: Automatically generated
        :param removal_policy: (experimental) Determine the removal policy of this log group. Normally you want to retain the log group so you can diagnose issues from logs even after a deployment that no longer includes the log group. In that case, use the normal date-based retention policy to age out your logs. Default: RemovalPolicy.Retain
        :param retention: (experimental) How long, in days, the log contents will be retained. To retain all logs, set this value to RetentionDays.INFINITE. Default: RetentionDays.TWO_YEARS

        :stability: experimental
        '''
        props = LogGroupProps(
            encryption_key=encryption_key,
            log_group_name=log_group_name,
            removal_policy=removal_policy,
            retention=retention,
        )

        jsii.create(LogGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromLogGroupArn") # type: ignore[misc]
    @builtins.classmethod
    def from_log_group_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        log_group_arn: builtins.str,
    ) -> ILogGroup:
        '''(experimental) Import an existing LogGroup given its ARN.

        :param scope: -
        :param id: -
        :param log_group_arn: -

        :stability: experimental
        '''
        return typing.cast(ILogGroup, jsii.sinvoke(cls, "fromLogGroupArn", [scope, id, log_group_arn]))

    @jsii.member(jsii_name="fromLogGroupName") # type: ignore[misc]
    @builtins.classmethod
    def from_log_group_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        log_group_name: builtins.str,
    ) -> ILogGroup:
        '''(experimental) Import an existing LogGroup given its name.

        :param scope: -
        :param id: -
        :param log_group_name: -

        :stability: experimental
        '''
        return typing.cast(ILogGroup, jsii.sinvoke(cls, "fromLogGroupName", [scope, id, log_group_name]))

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(
        self,
        id: builtins.str,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> "MetricFilter":
        '''(experimental) Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: (experimental) Pattern to search for log events.
        :param metric_name: (experimental) The name of the metric to emit.
        :param metric_namespace: (experimental) The namespace of the metric to emit.
        :param default_value: (experimental) The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: (experimental) The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        :stability: experimental
        '''
        props = MetricFilterOptions(
            filter_pattern=filter_pattern,
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            default_value=default_value,
            metric_value=metric_value,
        )

        return typing.cast("MetricFilter", jsii.invoke(self, "addMetricFilter", [id, props]))

    @jsii.member(jsii_name="addStream")
    def add_stream(
        self,
        id: builtins.str,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> "LogStream":
        '''(experimental) Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: (experimental) The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        :stability: experimental
        '''
        props = StreamOptions(log_stream_name=log_stream_name)

        return typing.cast("LogStream", jsii.invoke(self, "addStream", [id, props]))

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(
        self,
        id: builtins.str,
        *,
        destination: ILogSubscriptionDestination,
        filter_pattern: IFilterPattern,
    ) -> "SubscriptionFilter":
        '''(experimental) Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: (experimental) The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: (experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        props = SubscriptionFilterOptions(
            destination=destination, filter_pattern=filter_pattern
        )

        return typing.cast("SubscriptionFilter", jsii.invoke(self, "addSubscriptionFilter", [id, props]))

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(
        self,
        json_field: builtins.str,
        metric_namespace: builtins.str,
        metric_name: builtins.str,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        :return: A Metric object representing the extracted metric

        :stability: experimental
        '''
        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "extractMetric", [json_field, metric_namespace, metric_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Give permissions to create and write to streams in this log group.

        :param grantee: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [grantee]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of this log group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        '''(experimental) The name of this log group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.LogGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_key": "encryptionKey",
        "log_group_name": "logGroupName",
        "removal_policy": "removalPolicy",
        "retention": "retention",
    },
)
class LogGroupProps:
    def __init__(
        self,
        *,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        retention: typing.Optional["RetentionDays"] = None,
    ) -> None:
        '''(experimental) Properties for a LogGroup.

        :param encryption_key: (experimental) The KMS Key to encrypt the log group with. Default: - log group is encrypted with the default master key
        :param log_group_name: (experimental) Name of the log group. Default: Automatically generated
        :param removal_policy: (experimental) Determine the removal policy of this log group. Normally you want to retain the log group so you can diagnose issues from logs even after a deployment that no longer includes the log group. In that case, use the normal date-based retention policy to age out your logs. Default: RemovalPolicy.Retain
        :param retention: (experimental) How long, in days, the log contents will be retained. To retain all logs, set this value to RetentionDays.INFINITE. Default: RetentionDays.TWO_YEARS

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if retention is not None:
            self._values["retention"] = retention

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The KMS Key to encrypt the log group with.

        :default: - log group is encrypted with the default master key

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the log group.

        :default: Automatically generated

        :stability: experimental
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) Determine the removal policy of this log group.

        Normally you want to retain the log group so you can diagnose issues
        from logs even after a deployment that no longer includes the log group.
        In that case, use the normal date-based retention policy to age out your
        logs.

        :default: RemovalPolicy.Retain

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def retention(self) -> typing.Optional["RetentionDays"]:
        '''(experimental) How long, in days, the log contents will be retained.

        To retain all logs, set this value to RetentionDays.INFINITE.

        :default: RetentionDays.TWO_YEARS

        :stability: experimental
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional["RetentionDays"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogRetention(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.LogRetention",
):
    '''(experimental) Creates a custom resource to control the retention policy of a CloudWatch Logs log group.

    The log group is created if it doesn't already exist. The policy
    is removed when ``retentionDays`` is ``undefined`` or equal to ``Infinity``.
    Log group can be created in the region that is different from stack region by
    specifying ``logGroupRegion``

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        log_group_name: builtins.str,
        retention: "RetentionDays",
        log_group_region: typing.Optional[builtins.str] = None,
        log_retention_retry_options: typing.Optional["LogRetentionRetryOptions"] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group_name: (experimental) The log group name.
        :param retention: (experimental) The number of days log events are kept in CloudWatch Logs.
        :param log_group_region: (experimental) The region where the log group should be created. Default: - same region as the stack
        :param log_retention_retry_options: (experimental) Retry options for all AWS API calls. Default: - AWS SDK default retry options
        :param role: (experimental) The IAM role for the Lambda function associated with the custom resource. Default: - A new role is created

        :stability: experimental
        '''
        props = LogRetentionProps(
            log_group_name=log_group_name,
            retention=retention,
            log_group_region=log_group_region,
            log_retention_retry_options=log_retention_retry_options,
            role=role,
        )

        jsii.create(LogRetention, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of the LogGroup.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.LogRetentionProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "retention": "retention",
        "log_group_region": "logGroupRegion",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "role": "role",
    },
)
class LogRetentionProps:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        retention: "RetentionDays",
        log_group_region: typing.Optional[builtins.str] = None,
        log_retention_retry_options: typing.Optional["LogRetentionRetryOptions"] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) Construction properties for a LogRetention.

        :param log_group_name: (experimental) The log group name.
        :param retention: (experimental) The number of days log events are kept in CloudWatch Logs.
        :param log_group_region: (experimental) The region where the log group should be created. Default: - same region as the stack
        :param log_retention_retry_options: (experimental) Retry options for all AWS API calls. Default: - AWS SDK default retry options
        :param role: (experimental) The IAM role for the Lambda function associated with the custom resource. Default: - A new role is created

        :stability: experimental
        '''
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = LogRetentionRetryOptions(**log_retention_retry_options)
        self._values: typing.Dict[str, typing.Any] = {
            "log_group_name": log_group_name,
            "retention": retention,
        }
        if log_group_region is not None:
            self._values["log_group_region"] = log_group_region
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''(experimental) The log group name.

        :stability: experimental
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention(self) -> "RetentionDays":
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        :stability: experimental
        '''
        result = self._values.get("retention")
        assert result is not None, "Required property 'retention' is missing"
        return typing.cast("RetentionDays", result)

    @builtins.property
    def log_group_region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region where the log group should be created.

        :default: - same region as the stack

        :stability: experimental
        '''
        result = self._values.get("log_group_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional["LogRetentionRetryOptions"]:
        '''(experimental) Retry options for all AWS API calls.

        :default: - AWS SDK default retry options

        :stability: experimental
        '''
        result = self._values.get("log_retention_retry_options")
        return typing.cast(typing.Optional["LogRetentionRetryOptions"], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role for the Lambda function associated with the custom resource.

        :default: - A new role is created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogRetentionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.LogRetentionRetryOptions",
    jsii_struct_bases=[],
    name_mapping={"base": "base", "max_retries": "maxRetries"},
)
class LogRetentionRetryOptions:
    def __init__(
        self,
        *,
        base: typing.Optional[_Duration_070aa057] = None,
        max_retries: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Retry options for all AWS API calls.

        :param base: (experimental) The base duration to use in the exponential backoff for operation retries. Default: Duration.millis(100) (AWS SDK default)
        :param max_retries: (experimental) The maximum amount of retries. Default: 3 (AWS SDK default)

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if base is not None:
            self._values["base"] = base
        if max_retries is not None:
            self._values["max_retries"] = max_retries

    @builtins.property
    def base(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The base duration to use in the exponential backoff for operation retries.

        :default: Duration.millis(100) (AWS SDK default)

        :stability: experimental
        '''
        result = self._values.get("base")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum amount of retries.

        :default: 3 (AWS SDK default)

        :stability: experimental
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogRetentionRetryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILogStream)
class LogStream(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.LogStream",
):
    '''(experimental) Define a Log Stream in a Log Group.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        log_group: ILogGroup,
        log_stream_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group: (experimental) The log group to create a log stream for.
        :param log_stream_name: (experimental) The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        :param removal_policy: (experimental) Determine what happens when the log stream resource is removed from the app. Normally you want to retain the log stream so you can diagnose issues from logs even after a deployment that no longer includes the log stream. The date-based retention policy of your log group will age out the logs after a certain time. Default: RemovalPolicy.Retain

        :stability: experimental
        '''
        props = LogStreamProps(
            log_group=log_group,
            log_stream_name=log_stream_name,
            removal_policy=removal_policy,
        )

        jsii.create(LogStream, self, [scope, id, props])

    @jsii.member(jsii_name="fromLogStreamName") # type: ignore[misc]
    @builtins.classmethod
    def from_log_stream_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        log_stream_name: builtins.str,
    ) -> ILogStream:
        '''(experimental) Import an existing LogGroup.

        :param scope: -
        :param id: -
        :param log_stream_name: -

        :stability: experimental
        '''
        return typing.cast(ILogStream, jsii.sinvoke(cls, "fromLogStreamName", [scope, id, log_stream_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        '''(experimental) The name of this log stream.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.LogStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group": "logGroup",
        "log_stream_name": "logStreamName",
        "removal_policy": "removalPolicy",
    },
)
class LogStreamProps:
    def __init__(
        self,
        *,
        log_group: ILogGroup,
        log_stream_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''(experimental) Properties for a LogStream.

        :param log_group: (experimental) The log group to create a log stream for.
        :param log_stream_name: (experimental) The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        :param removal_policy: (experimental) Determine what happens when the log stream resource is removed from the app. Normally you want to retain the log stream so you can diagnose issues from logs even after a deployment that no longer includes the log stream. The date-based retention policy of your log group will age out the logs after a certain time. Default: RemovalPolicy.Retain

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "log_group": log_group,
        }
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def log_group(self) -> ILogGroup:
        '''(experimental) The log group to create a log stream for.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        assert result is not None, "Required property 'log_group' is missing"
        return typing.cast(ILogGroup, result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the log stream to create.

        The name must be unique within the log group.

        :default: Automatically generated

        :stability: experimental
        '''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) Determine what happens when the log stream resource is removed from the app.

        Normally you want to retain the log stream so you can diagnose issues from
        logs even after a deployment that no longer includes the log stream.

        The date-based retention policy of your log group will age out the logs
        after a certain time.

        :default: RemovalPolicy.Retain

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.LogSubscriptionDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "role": "role"},
)
class LogSubscriptionDestinationConfig:
    def __init__(
        self,
        *,
        arn: builtins.str,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) Properties returned by a Subscription destination.

        :param arn: (experimental) The ARN of the subscription's destination.
        :param role: (experimental) The role to assume to write log events to the destination. Default: No role assumed

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "arn": arn,
        }
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the subscription's destination.

        :stability: experimental
        '''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The role to assume to write log events to the destination.

        :default: No role assumed

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogSubscriptionDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetricFilter(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.MetricFilter",
):
    '''(experimental) A filter that extracts information from CloudWatch Logs and emits to CloudWatch Metrics.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        log_group: ILogGroup,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group: (experimental) The log group to create the filter on.
        :param filter_pattern: (experimental) Pattern to search for log events.
        :param metric_name: (experimental) The name of the metric to emit.
        :param metric_namespace: (experimental) The namespace of the metric to emit.
        :param default_value: (experimental) The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: (experimental) The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        :stability: experimental
        '''
        props = MetricFilterProps(
            log_group=log_group,
            filter_pattern=filter_pattern,
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            default_value=default_value,
            metric_value=metric_value,
        )

        jsii.create(MetricFilter, self, [scope, id, props])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this Metric Filter.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: avg over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [props]))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.MetricFilterOptions",
    jsii_struct_bases=[],
    name_mapping={
        "filter_pattern": "filterPattern",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "default_value": "defaultValue",
        "metric_value": "metricValue",
    },
)
class MetricFilterOptions:
    def __init__(
        self,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a MetricFilter created from a LogGroup.

        :param filter_pattern: (experimental) Pattern to search for log events.
        :param metric_name: (experimental) The name of the metric to emit.
        :param metric_namespace: (experimental) The namespace of the metric to emit.
        :param default_value: (experimental) The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: (experimental) The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "filter_pattern": filter_pattern,
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
        }
        if default_value is not None:
            self._values["default_value"] = default_value
        if metric_value is not None:
            self._values["metric_value"] = metric_value

    @builtins.property
    def filter_pattern(self) -> IFilterPattern:
        '''(experimental) Pattern to search for log events.

        :stability: experimental
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(IFilterPattern, result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''(experimental) The name of the metric to emit.

        :stability: experimental
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''(experimental) The namespace of the metric to emit.

        :stability: experimental
        '''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_value(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The value to emit if the pattern does not match a particular event.

        :default: No metric emitted.

        :stability: experimental
        '''
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metric_value(self) -> typing.Optional[builtins.str]:
        '''(experimental) The value to emit for the metric.

        Can either be a literal number (typically "1"), or the name of a field in the structure
        to take the value from the matched event. If you are using a field value, the field
        value must have been matched using the pattern.

        If you want to specify a field from a matched JSON structure, use '$.fieldName',
        and make sure the field is in the pattern (if only as '$.fieldName = *').

        If you want to specify a field from a matched space-delimited structure,
        use '$fieldName'.

        :default: "1"

        :stability: experimental
        '''
        result = self._values.get("metric_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.MetricFilterProps",
    jsii_struct_bases=[MetricFilterOptions],
    name_mapping={
        "filter_pattern": "filterPattern",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "default_value": "defaultValue",
        "metric_value": "metricValue",
        "log_group": "logGroup",
    },
)
class MetricFilterProps(MetricFilterOptions):
    def __init__(
        self,
        *,
        filter_pattern: IFilterPattern,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        default_value: typing.Optional[jsii.Number] = None,
        metric_value: typing.Optional[builtins.str] = None,
        log_group: ILogGroup,
    ) -> None:
        '''(experimental) Properties for a MetricFilter.

        :param filter_pattern: (experimental) Pattern to search for log events.
        :param metric_name: (experimental) The name of the metric to emit.
        :param metric_namespace: (experimental) The namespace of the metric to emit.
        :param default_value: (experimental) The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: (experimental) The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        :param log_group: (experimental) The log group to create the filter on.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "filter_pattern": filter_pattern,
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "log_group": log_group,
        }
        if default_value is not None:
            self._values["default_value"] = default_value
        if metric_value is not None:
            self._values["metric_value"] = metric_value

    @builtins.property
    def filter_pattern(self) -> IFilterPattern:
        '''(experimental) Pattern to search for log events.

        :stability: experimental
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(IFilterPattern, result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''(experimental) The name of the metric to emit.

        :stability: experimental
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''(experimental) The namespace of the metric to emit.

        :stability: experimental
        '''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_value(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The value to emit if the pattern does not match a particular event.

        :default: No metric emitted.

        :stability: experimental
        '''
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metric_value(self) -> typing.Optional[builtins.str]:
        '''(experimental) The value to emit for the metric.

        Can either be a literal number (typically "1"), or the name of a field in the structure
        to take the value from the matched event. If you are using a field value, the field
        value must have been matched using the pattern.

        If you want to specify a field from a matched JSON structure, use '$.fieldName',
        and make sure the field is in the pattern (if only as '$.fieldName = *').

        If you want to specify a field from a matched space-delimited structure,
        use '$fieldName'.

        :default: "1"

        :stability: experimental
        '''
        result = self._values.get("metric_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group(self) -> ILogGroup:
        '''(experimental) The log group to create the filter on.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        assert result is not None, "Required property 'log_group' is missing"
        return typing.cast(ILogGroup, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_logs.RetentionDays")
class RetentionDays(enum.Enum):
    '''(experimental) How long, in days, the log contents will be retained.

    :stability: experimental
    '''

    ONE_DAY = "ONE_DAY"
    '''(experimental) 1 day.

    :stability: experimental
    '''
    THREE_DAYS = "THREE_DAYS"
    '''(experimental) 3 days.

    :stability: experimental
    '''
    FIVE_DAYS = "FIVE_DAYS"
    '''(experimental) 5 days.

    :stability: experimental
    '''
    ONE_WEEK = "ONE_WEEK"
    '''(experimental) 1 week.

    :stability: experimental
    '''
    TWO_WEEKS = "TWO_WEEKS"
    '''(experimental) 2 weeks.

    :stability: experimental
    '''
    ONE_MONTH = "ONE_MONTH"
    '''(experimental) 1 month.

    :stability: experimental
    '''
    TWO_MONTHS = "TWO_MONTHS"
    '''(experimental) 2 months.

    :stability: experimental
    '''
    THREE_MONTHS = "THREE_MONTHS"
    '''(experimental) 3 months.

    :stability: experimental
    '''
    FOUR_MONTHS = "FOUR_MONTHS"
    '''(experimental) 4 months.

    :stability: experimental
    '''
    FIVE_MONTHS = "FIVE_MONTHS"
    '''(experimental) 5 months.

    :stability: experimental
    '''
    SIX_MONTHS = "SIX_MONTHS"
    '''(experimental) 6 months.

    :stability: experimental
    '''
    ONE_YEAR = "ONE_YEAR"
    '''(experimental) 1 year.

    :stability: experimental
    '''
    THIRTEEN_MONTHS = "THIRTEEN_MONTHS"
    '''(experimental) 13 months.

    :stability: experimental
    '''
    EIGHTEEN_MONTHS = "EIGHTEEN_MONTHS"
    '''(experimental) 18 months.

    :stability: experimental
    '''
    TWO_YEARS = "TWO_YEARS"
    '''(experimental) 2 years.

    :stability: experimental
    '''
    FIVE_YEARS = "FIVE_YEARS"
    '''(experimental) 5 years.

    :stability: experimental
    '''
    TEN_YEARS = "TEN_YEARS"
    '''(experimental) 10 years.

    :stability: experimental
    '''
    INFINITE = "INFINITE"
    '''(experimental) Retain logs forever.

    :stability: experimental
    '''


@jsii.implements(IFilterPattern)
class SpaceDelimitedTextPattern(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.SpaceDelimitedTextPattern",
):
    '''(experimental) Space delimited text pattern.

    :stability: experimental
    '''

    def __init__(
        self,
        columns: typing.List[builtins.str],
        restrictions: typing.Mapping[builtins.str, typing.List[ColumnRestriction]],
    ) -> None:
        '''
        :param columns: -
        :param restrictions: -

        :stability: experimental
        '''
        jsii.create(SpaceDelimitedTextPattern, self, [columns, restrictions])

    @jsii.member(jsii_name="construct") # type: ignore[misc]
    @builtins.classmethod
    def construct(
        cls,
        columns: typing.List[builtins.str],
    ) -> "SpaceDelimitedTextPattern":
        '''(experimental) Construct a new instance of a space delimited text pattern.

        Since this class must be public, we can't rely on the user only creating it through
        the ``LogPattern.spaceDelimited()`` factory function. We must therefore validate the
        argument in the constructor. Since we're returning a copy on every mutation, and we
        don't want to re-validate the same things on every construction, we provide a limited
        set of mutator functions and only validate the new data every time.

        :param columns: -

        :stability: experimental
        '''
        return typing.cast("SpaceDelimitedTextPattern", jsii.sinvoke(cls, "construct", [columns]))

    @jsii.member(jsii_name="whereNumber")
    def where_number(
        self,
        column_name: builtins.str,
        comparison: builtins.str,
        value: jsii.Number,
    ) -> "SpaceDelimitedTextPattern":
        '''(experimental) Restrict where the pattern applies.

        :param column_name: -
        :param comparison: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("SpaceDelimitedTextPattern", jsii.invoke(self, "whereNumber", [column_name, comparison, value]))

    @jsii.member(jsii_name="whereString")
    def where_string(
        self,
        column_name: builtins.str,
        comparison: builtins.str,
        value: builtins.str,
    ) -> "SpaceDelimitedTextPattern":
        '''(experimental) Restrict where the pattern applies.

        :param column_name: -
        :param comparison: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("SpaceDelimitedTextPattern", jsii.invoke(self, "whereString", [column_name, comparison, value]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "logPatternString"))


@jsii.data_type(
    jsii_type="monocdk.aws_logs.StreamOptions",
    jsii_struct_bases=[],
    name_mapping={"log_stream_name": "logStreamName"},
)
class StreamOptions:
    def __init__(
        self,
        *,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a new LogStream created from a LogGroup.

        :param log_stream_name: (experimental) The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the log stream to create.

        The name must be unique within the log group.

        :default: Automatically generated

        :stability: experimental
        '''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SubscriptionFilter(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.SubscriptionFilter",
):
    '''(experimental) A new Subscription on a CloudWatch log group.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        log_group: ILogGroup,
        destination: ILogSubscriptionDestination,
        filter_pattern: IFilterPattern,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group: (experimental) The log group to create the subscription on.
        :param destination: (experimental) The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: (experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        props = SubscriptionFilterProps(
            log_group=log_group, destination=destination, filter_pattern=filter_pattern
        )

        jsii.create(SubscriptionFilter, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_logs.SubscriptionFilterOptions",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination", "filter_pattern": "filterPattern"},
)
class SubscriptionFilterOptions:
    def __init__(
        self,
        *,
        destination: ILogSubscriptionDestination,
        filter_pattern: IFilterPattern,
    ) -> None:
        '''(experimental) Properties for a new SubscriptionFilter created from a LogGroup.

        :param destination: (experimental) The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: (experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "destination": destination,
            "filter_pattern": filter_pattern,
        }

    @builtins.property
    def destination(self) -> ILogSubscriptionDestination:
        '''(experimental) The destination to send the filtered events to.

        For example, a Kinesis stream or a Lambda function.

        :stability: experimental
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(ILogSubscriptionDestination, result)

    @builtins.property
    def filter_pattern(self) -> IFilterPattern:
        '''(experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(IFilterPattern, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_logs.SubscriptionFilterProps",
    jsii_struct_bases=[SubscriptionFilterOptions],
    name_mapping={
        "destination": "destination",
        "filter_pattern": "filterPattern",
        "log_group": "logGroup",
    },
)
class SubscriptionFilterProps(SubscriptionFilterOptions):
    def __init__(
        self,
        *,
        destination: ILogSubscriptionDestination,
        filter_pattern: IFilterPattern,
        log_group: ILogGroup,
    ) -> None:
        '''(experimental) Properties for a SubscriptionFilter.

        :param destination: (experimental) The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: (experimental) Log events matching this pattern will be sent to the destination.
        :param log_group: (experimental) The log group to create the subscription on.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "destination": destination,
            "filter_pattern": filter_pattern,
            "log_group": log_group,
        }

    @builtins.property
    def destination(self) -> ILogSubscriptionDestination:
        '''(experimental) The destination to send the filtered events to.

        For example, a Kinesis stream or a Lambda function.

        :stability: experimental
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(ILogSubscriptionDestination, result)

    @builtins.property
    def filter_pattern(self) -> IFilterPattern:
        '''(experimental) Log events matching this pattern will be sent to the destination.

        :stability: experimental
        '''
        result = self._values.get("filter_pattern")
        assert result is not None, "Required property 'filter_pattern' is missing"
        return typing.cast(IFilterPattern, result)

    @builtins.property
    def log_group(self) -> ILogGroup:
        '''(experimental) The log group to create the subscription on.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        assert result is not None, "Required property 'log_group' is missing"
        return typing.cast(ILogGroup, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILogSubscriptionDestination)
class CrossAccountDestination(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_logs.CrossAccountDestination",
):
    '''(experimental) A new CloudWatch Logs Destination for use in cross-account scenarios.

    CrossAccountDestinations are used to subscribe a Kinesis stream in a
    different account to a CloudWatch Subscription.

    Consumers will hardly ever need to use this class. Instead, directly
    subscribe a Kinesis stream using the integration class in the
    ``@aws-cdk/aws-logs-destinations`` package; if necessary, a
    ``CrossAccountDestination`` will be created automatically.

    :stability: experimental
    :resource: AWS::Logs::Destination
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        role: _IRole_59af6f50,
        target_arn: builtins.str,
        destination_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param role: (experimental) The role to assume that grants permissions to write to 'target'. The role must be assumable by 'logs.{REGION}.amazonaws.com'.
        :param target_arn: (experimental) The log destination target's ARN.
        :param destination_name: (experimental) The name of the log destination. Default: Automatically generated

        :stability: experimental
        '''
        props = CrossAccountDestinationProps(
            role=role, target_arn=target_arn, destination_name=destination_name
        )

        jsii.create(CrossAccountDestination, self, [scope, id, props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: _PolicyStatement_296fe8a3) -> None:
        '''
        :param statement: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _Construct_e78e779f,
        _source_log_group: ILogGroup,
    ) -> LogSubscriptionDestinationConfig:
        '''(experimental) Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param _scope: -
        :param _source_log_group: -

        :stability: experimental
        '''
        return typing.cast(LogSubscriptionDestinationConfig, jsii.invoke(self, "bind", [_scope, _source_log_group]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        '''(experimental) The ARN of this CrossAccountDestination object.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="destinationName")
    def destination_name(self) -> builtins.str:
        '''(experimental) The name of this CrossAccountDestination object.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> _PolicyDocument_b5de5177:
        '''(experimental) Policy object of this CrossAccountDestination object.

        :stability: experimental
        '''
        return typing.cast(_PolicyDocument_b5de5177, jsii.get(self, "policyDocument"))


__all__ = [
    "CfnDestination",
    "CfnDestinationProps",
    "CfnLogGroup",
    "CfnLogGroupProps",
    "CfnLogStream",
    "CfnLogStreamProps",
    "CfnMetricFilter",
    "CfnMetricFilterProps",
    "CfnSubscriptionFilter",
    "CfnSubscriptionFilterProps",
    "ColumnRestriction",
    "CrossAccountDestination",
    "CrossAccountDestinationProps",
    "FilterPattern",
    "IFilterPattern",
    "ILogGroup",
    "ILogStream",
    "ILogSubscriptionDestination",
    "JsonPattern",
    "LogGroup",
    "LogGroupProps",
    "LogRetention",
    "LogRetentionProps",
    "LogRetentionRetryOptions",
    "LogStream",
    "LogStreamProps",
    "LogSubscriptionDestinationConfig",
    "MetricFilter",
    "MetricFilterOptions",
    "MetricFilterProps",
    "RetentionDays",
    "SpaceDelimitedTextPattern",
    "StreamOptions",
    "SubscriptionFilter",
    "SubscriptionFilterOptions",
    "SubscriptionFilterProps",
]

publication.publish()
