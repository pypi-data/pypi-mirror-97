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
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ivs.CfnChannel",
):
    '''A CloudFormation ``AWS::IVS::Channel``.

    :cloudformationResource: AWS::IVS::Channel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        authorized: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        latency_mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        recording_configuration_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IVS::Channel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param authorized: ``AWS::IVS::Channel.Authorized``.
        :param latency_mode: ``AWS::IVS::Channel.LatencyMode``.
        :param name: ``AWS::IVS::Channel.Name``.
        :param recording_configuration_arn: ``AWS::IVS::Channel.RecordingConfigurationArn``.
        :param tags: ``AWS::IVS::Channel.Tags``.
        :param type: ``AWS::IVS::Channel.Type``.
        '''
        props = CfnChannelProps(
            authorized=authorized,
            latency_mode=latency_mode,
            name=name,
            recording_configuration_arn=recording_configuration_arn,
            tags=tags,
            type=type,
        )

        jsii.create(CfnChannel, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrIngestEndpoint")
    def attr_ingest_endpoint(self) -> builtins.str:
        '''
        :cloudformationAttribute: IngestEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrIngestEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrPlaybackUrl")
    def attr_playback_url(self) -> builtins.str:
        '''
        :cloudformationAttribute: PlaybackUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPlaybackUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::IVS::Channel.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="authorized")
    def authorized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::IVS::Channel.Authorized``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-authorized
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "authorized"))

    @authorized.setter
    def authorized(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "authorized", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="latencyMode")
    def latency_mode(self) -> typing.Optional[builtins.str]:
        '''``AWS::IVS::Channel.LatencyMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-latencymode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "latencyMode"))

    @latency_mode.setter
    def latency_mode(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "latencyMode", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::IVS::Channel.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="recordingConfigurationArn")
    def recording_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::IVS::Channel.RecordingConfigurationArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-recordingconfigurationarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordingConfigurationArn"))

    @recording_configuration_arn.setter
    def recording_configuration_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "recordingConfigurationArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''``AWS::IVS::Channel.Type``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="monocdk.aws_ivs.CfnChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorized": "authorized",
        "latency_mode": "latencyMode",
        "name": "name",
        "recording_configuration_arn": "recordingConfigurationArn",
        "tags": "tags",
        "type": "type",
    },
)
class CfnChannelProps:
    def __init__(
        self,
        *,
        authorized: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        latency_mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        recording_configuration_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::IVS::Channel``.

        :param authorized: ``AWS::IVS::Channel.Authorized``.
        :param latency_mode: ``AWS::IVS::Channel.LatencyMode``.
        :param name: ``AWS::IVS::Channel.Name``.
        :param recording_configuration_arn: ``AWS::IVS::Channel.RecordingConfigurationArn``.
        :param tags: ``AWS::IVS::Channel.Tags``.
        :param type: ``AWS::IVS::Channel.Type``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if authorized is not None:
            self._values["authorized"] = authorized
        if latency_mode is not None:
            self._values["latency_mode"] = latency_mode
        if name is not None:
            self._values["name"] = name
        if recording_configuration_arn is not None:
            self._values["recording_configuration_arn"] = recording_configuration_arn
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def authorized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::IVS::Channel.Authorized``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-authorized
        '''
        result = self._values.get("authorized")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def latency_mode(self) -> typing.Optional[builtins.str]:
        '''``AWS::IVS::Channel.LatencyMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-latencymode
        '''
        result = self._values.get("latency_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::IVS::Channel.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recording_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::IVS::Channel.RecordingConfigurationArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-recordingconfigurationarn
        '''
        result = self._values.get("recording_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::IVS::Channel.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''``AWS::IVS::Channel.Type``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPlaybackKeyPair(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ivs.CfnPlaybackKeyPair",
):
    '''A CloudFormation ``AWS::IVS::PlaybackKeyPair``.

    :cloudformationResource: AWS::IVS::PlaybackKeyPair
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        public_key_material: builtins.str,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::IVS::PlaybackKeyPair``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param public_key_material: ``AWS::IVS::PlaybackKeyPair.PublicKeyMaterial``.
        :param name: ``AWS::IVS::PlaybackKeyPair.Name``.
        :param tags: ``AWS::IVS::PlaybackKeyPair.Tags``.
        '''
        props = CfnPlaybackKeyPairProps(
            public_key_material=public_key_material, name=name, tags=tags
        )

        jsii.create(CfnPlaybackKeyPair, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrFingerprint")
    def attr_fingerprint(self) -> builtins.str:
        '''
        :cloudformationAttribute: Fingerprint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFingerprint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::IVS::PlaybackKeyPair.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="publicKeyMaterial")
    def public_key_material(self) -> builtins.str:
        '''``AWS::IVS::PlaybackKeyPair.PublicKeyMaterial``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-publickeymaterial
        '''
        return typing.cast(builtins.str, jsii.get(self, "publicKeyMaterial"))

    @public_key_material.setter
    def public_key_material(self, value: builtins.str) -> None:
        jsii.set(self, "publicKeyMaterial", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::IVS::PlaybackKeyPair.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_ivs.CfnPlaybackKeyPairProps",
    jsii_struct_bases=[],
    name_mapping={
        "public_key_material": "publicKeyMaterial",
        "name": "name",
        "tags": "tags",
    },
)
class CfnPlaybackKeyPairProps:
    def __init__(
        self,
        *,
        public_key_material: builtins.str,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::IVS::PlaybackKeyPair``.

        :param public_key_material: ``AWS::IVS::PlaybackKeyPair.PublicKeyMaterial``.
        :param name: ``AWS::IVS::PlaybackKeyPair.Name``.
        :param tags: ``AWS::IVS::PlaybackKeyPair.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "public_key_material": public_key_material,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def public_key_material(self) -> builtins.str:
        '''``AWS::IVS::PlaybackKeyPair.PublicKeyMaterial``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-publickeymaterial
        '''
        result = self._values.get("public_key_material")
        assert result is not None, "Required property 'public_key_material' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::IVS::PlaybackKeyPair.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::IVS::PlaybackKeyPair.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlaybackKeyPairProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnStreamKey(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ivs.CfnStreamKey",
):
    '''A CloudFormation ``AWS::IVS::StreamKey``.

    :cloudformationResource: AWS::IVS::StreamKey
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        channel_arn: builtins.str,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::IVS::StreamKey``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param channel_arn: ``AWS::IVS::StreamKey.ChannelArn``.
        :param tags: ``AWS::IVS::StreamKey.Tags``.
        '''
        props = CfnStreamKeyProps(channel_arn=channel_arn, tags=tags)

        jsii.create(CfnStreamKey, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrValue")
    def attr_value(self) -> builtins.str:
        '''
        :cloudformationAttribute: Value
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrValue"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::IVS::StreamKey.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html#cfn-ivs-streamkey-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="channelArn")
    def channel_arn(self) -> builtins.str:
        '''``AWS::IVS::StreamKey.ChannelArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html#cfn-ivs-streamkey-channelarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelArn"))

    @channel_arn.setter
    def channel_arn(self, value: builtins.str) -> None:
        jsii.set(self, "channelArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_ivs.CfnStreamKeyProps",
    jsii_struct_bases=[],
    name_mapping={"channel_arn": "channelArn", "tags": "tags"},
)
class CfnStreamKeyProps:
    def __init__(
        self,
        *,
        channel_arn: builtins.str,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::IVS::StreamKey``.

        :param channel_arn: ``AWS::IVS::StreamKey.ChannelArn``.
        :param tags: ``AWS::IVS::StreamKey.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "channel_arn": channel_arn,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def channel_arn(self) -> builtins.str:
        '''``AWS::IVS::StreamKey.ChannelArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html#cfn-ivs-streamkey-channelarn
        '''
        result = self._values.get("channel_arn")
        assert result is not None, "Required property 'channel_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::IVS::StreamKey.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html#cfn-ivs-streamkey-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_ivs.ChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorized": "authorized",
        "latency_mode": "latencyMode",
        "name": "name",
        "type": "type",
    },
)
class ChannelProps:
    def __init__(
        self,
        *,
        authorized: typing.Optional[builtins.bool] = None,
        latency_mode: typing.Optional["LatencyMode"] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional["ChannelType"] = None,
    ) -> None:
        '''(experimental) Properties for creating a new Channel.

        :param authorized: (experimental) Whether the channel is authorized. If you wish to make an authorized channel, you will need to ensure that a PlaybackKeyPair has been uploaded to your account as this is used to validate the signed JWT that is required for authorization Default: false
        :param latency_mode: (experimental) Channel latency mode. Default: LatencyMode.LOW
        :param name: (experimental) Channel name. Default: - None
        :param type: (experimental) The channel type, which determines the allowable resolution and bitrate. If you exceed the allowable resolution or bitrate, the stream will disconnect immediately Default: ChannelType.STANDARD

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if authorized is not None:
            self._values["authorized"] = authorized
        if latency_mode is not None:
            self._values["latency_mode"] = latency_mode
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def authorized(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the channel is authorized.

        If you wish to make an authorized channel, you will need to ensure that
        a PlaybackKeyPair has been uploaded to your account as this is used to
        validate the signed JWT that is required for authorization

        :default: false

        :stability: experimental
        '''
        result = self._values.get("authorized")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def latency_mode(self) -> typing.Optional["LatencyMode"]:
        '''(experimental) Channel latency mode.

        :default: LatencyMode.LOW

        :stability: experimental
        '''
        result = self._values.get("latency_mode")
        return typing.cast(typing.Optional["LatencyMode"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Channel name.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional["ChannelType"]:
        '''(experimental) The channel type, which determines the allowable resolution and bitrate.

        If you exceed the allowable resolution or bitrate, the stream will disconnect immediately

        :default: ChannelType.STANDARD

        :stability: experimental
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["ChannelType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_ivs.ChannelType")
class ChannelType(enum.Enum):
    '''(experimental) The channel type, which determines the allowable resolution and bitrate.

    If you exceed the allowable resolution or bitrate, the stream probably will disconnect immediately.

    :stability: experimental
    '''

    STANDARD = "STANDARD"
    '''(experimental) Multiple qualities are generated from the original input, to automatically give viewers the best experience for their devices and network conditions.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html
    :stability: experimental
    '''
    BASIC = "BASIC"
    '''(experimental) delivers the original input to viewers.

    The viewer’s video-quality choice is limited to the original input.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html
    :stability: experimental
    '''


@jsii.interface(jsii_type="monocdk.aws_ivs.IChannel")
class IChannel(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents an IVS Channel.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IChannelProxy"]:
        return _IChannelProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="channelArn")
    def channel_arn(self) -> builtins.str:
        '''(experimental) The channel ARN.

        For example: arn:aws:ivs:us-west-2:123456789012:channel/abcdABCDefgh

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addStreamKey")
    def add_stream_key(self, id: builtins.str) -> "StreamKey":
        '''(experimental) Adds a stream key for this IVS Channel.

        :param id: construct ID.

        :stability: experimental
        '''
        ...


class _IChannelProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) Represents an IVS Channel.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_ivs.IChannel"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="channelArn")
    def channel_arn(self) -> builtins.str:
        '''(experimental) The channel ARN.

        For example: arn:aws:ivs:us-west-2:123456789012:channel/abcdABCDefgh

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelArn"))

    @jsii.member(jsii_name="addStreamKey")
    def add_stream_key(self, id: builtins.str) -> "StreamKey":
        '''(experimental) Adds a stream key for this IVS Channel.

        :param id: construct ID.

        :stability: experimental
        '''
        return typing.cast("StreamKey", jsii.invoke(self, "addStreamKey", [id]))


@jsii.interface(jsii_type="monocdk.aws_ivs.IPlaybackKeyPair")
class IPlaybackKeyPair(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents an IVS Playback Key Pair.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IPlaybackKeyPairProxy"]:
        return _IPlaybackKeyPairProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="playbackKeyPairArn")
    def playback_key_pair_arn(self) -> builtins.str:
        '''(experimental) Key-pair ARN.

        For example: arn:aws:ivs:us-west-2:693991300569:playback-key/f99cde61-c2b0-4df3-8941-ca7d38acca1a

        :stability: experimental
        :attribute: true
        '''
        ...


class _IPlaybackKeyPairProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) Represents an IVS Playback Key Pair.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_ivs.IPlaybackKeyPair"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="playbackKeyPairArn")
    def playback_key_pair_arn(self) -> builtins.str:
        '''(experimental) Key-pair ARN.

        For example: arn:aws:ivs:us-west-2:693991300569:playback-key/f99cde61-c2b0-4df3-8941-ca7d38acca1a

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "playbackKeyPairArn"))


@jsii.interface(jsii_type="monocdk.aws_ivs.IStreamKey")
class IStreamKey(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents an IVS Stream Key.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IStreamKeyProxy"]:
        return _IStreamKeyProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamKeyArn")
    def stream_key_arn(self) -> builtins.str:
        '''(experimental) The stream-key ARN.

        For example: arn:aws:ivs:us-west-2:123456789012:stream-key/g1H2I3j4k5L6

        :stability: experimental
        :attribute: true
        '''
        ...


class _IStreamKeyProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) Represents an IVS Stream Key.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_ivs.IStreamKey"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamKeyArn")
    def stream_key_arn(self) -> builtins.str:
        '''(experimental) The stream-key ARN.

        For example: arn:aws:ivs:us-west-2:123456789012:stream-key/g1H2I3j4k5L6

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "streamKeyArn"))


@jsii.enum(jsii_type="monocdk.aws_ivs.LatencyMode")
class LatencyMode(enum.Enum):
    '''(experimental) Channel latency mode.

    :stability: experimental
    '''

    LOW = "LOW"
    '''(experimental) Use LOW to minimize broadcaster-to-viewer latency for interactive broadcasts.

    :stability: experimental
    '''
    NORMAL = "NORMAL"
    '''(experimental) Use NORMAL for broadcasts that do not require viewer interaction.

    :stability: experimental
    '''


@jsii.implements(IPlaybackKeyPair)
class PlaybackKeyPair(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ivs.PlaybackKeyPair",
):
    '''(experimental) A new IVS Playback Key Pair.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        public_key_material: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param public_key_material: (experimental) The public portion of a customer-generated key pair.
        :param name: (experimental) An arbitrary string (a nickname) assigned to a playback key pair that helps the customer identify that resource. The value does not need to be unique. Default: None

        :stability: experimental
        '''
        props = PlaybackKeyPairProps(
            public_key_material=public_key_material, name=name
        )

        jsii.create(PlaybackKeyPair, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="playbackKeyPairArn")
    def playback_key_pair_arn(self) -> builtins.str:
        '''(experimental) Key-pair ARN.

        For example: arn:aws:ivs:us-west-2:693991300569:playback-key/f99cde61-c2b0-4df3-8941-ca7d38acca1a

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "playbackKeyPairArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="playbackKeyPairFingerprint")
    def playback_key_pair_fingerprint(self) -> builtins.str:
        '''(experimental) Key-pair identifier.

        For example: 98:0d:1a:a0:19:96:1e:ea:0a:0a:2c:9a:42:19:2b:e7

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "playbackKeyPairFingerprint"))


@jsii.data_type(
    jsii_type="monocdk.aws_ivs.PlaybackKeyPairProps",
    jsii_struct_bases=[],
    name_mapping={"public_key_material": "publicKeyMaterial", "name": "name"},
)
class PlaybackKeyPairProps:
    def __init__(
        self,
        *,
        public_key_material: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for creating a new Playback Key Pair.

        :param public_key_material: (experimental) The public portion of a customer-generated key pair.
        :param name: (experimental) An arbitrary string (a nickname) assigned to a playback key pair that helps the customer identify that resource. The value does not need to be unique. Default: None

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "public_key_material": public_key_material,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def public_key_material(self) -> builtins.str:
        '''(experimental) The public portion of a customer-generated key pair.

        :stability: experimental
        '''
        result = self._values.get("public_key_material")
        assert result is not None, "Required property 'public_key_material' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) An arbitrary string (a nickname) assigned to a playback key pair that helps the customer identify that resource.

        The value does not need to be unique.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PlaybackKeyPairProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IStreamKey)
class StreamKey(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ivs.StreamKey",
):
    '''(experimental) A new IVS Stream Key.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        channel: IChannel,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param channel: (experimental) Channel ARN for the stream.

        :stability: experimental
        '''
        props = StreamKeyProps(channel=channel)

        jsii.create(StreamKey, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamKeyArn")
    def stream_key_arn(self) -> builtins.str:
        '''(experimental) The stream-key ARN.

        For example: arn:aws:ivs:us-west-2:123456789012:stream-key/g1H2I3j4k5L6

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "streamKeyArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamKeyValue")
    def stream_key_value(self) -> builtins.str:
        '''(experimental) The stream-key value.

        For example: sk_us-west-2_abcdABCDefgh_567890abcdef

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "streamKeyValue"))


@jsii.data_type(
    jsii_type="monocdk.aws_ivs.StreamKeyProps",
    jsii_struct_bases=[],
    name_mapping={"channel": "channel"},
)
class StreamKeyProps:
    def __init__(self, *, channel: IChannel) -> None:
        '''(experimental) Properties for creating a new Stream Key.

        :param channel: (experimental) Channel ARN for the stream.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "channel": channel,
        }

    @builtins.property
    def channel(self) -> IChannel:
        '''(experimental) Channel ARN for the stream.

        :stability: experimental
        '''
        result = self._values.get("channel")
        assert result is not None, "Required property 'channel' is missing"
        return typing.cast(IChannel, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IChannel)
class Channel(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ivs.Channel",
):
    '''(experimental) A new IVS channel.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        authorized: typing.Optional[builtins.bool] = None,
        latency_mode: typing.Optional[LatencyMode] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[ChannelType] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param authorized: (experimental) Whether the channel is authorized. If you wish to make an authorized channel, you will need to ensure that a PlaybackKeyPair has been uploaded to your account as this is used to validate the signed JWT that is required for authorization Default: false
        :param latency_mode: (experimental) Channel latency mode. Default: LatencyMode.LOW
        :param name: (experimental) Channel name. Default: - None
        :param type: (experimental) The channel type, which determines the allowable resolution and bitrate. If you exceed the allowable resolution or bitrate, the stream will disconnect immediately Default: ChannelType.STANDARD

        :stability: experimental
        '''
        props = ChannelProps(
            authorized=authorized, latency_mode=latency_mode, name=name, type=type
        )

        jsii.create(Channel, self, [scope, id, props])

    @jsii.member(jsii_name="fromChannelArn") # type: ignore[misc]
    @builtins.classmethod
    def from_channel_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        channel_arn: builtins.str,
    ) -> IChannel:
        '''(experimental) Import an existing channel.

        :param scope: -
        :param id: -
        :param channel_arn: -

        :stability: experimental
        '''
        return typing.cast(IChannel, jsii.sinvoke(cls, "fromChannelArn", [scope, id, channel_arn]))

    @jsii.member(jsii_name="addStreamKey")
    def add_stream_key(self, id: builtins.str) -> StreamKey:
        '''(experimental) Adds a stream key for this IVS Channel.

        :param id: -

        :stability: experimental
        '''
        return typing.cast(StreamKey, jsii.invoke(self, "addStreamKey", [id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="channelArn")
    def channel_arn(self) -> builtins.str:
        '''(experimental) The channel ARN.

        For example: arn:aws:ivs:us-west-2:123456789012:channel/abcdABCDefgh

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="channelIngestEndpoint")
    def channel_ingest_endpoint(self) -> builtins.str:
        '''(experimental) Channel ingest endpoint, part of the definition of an ingest server, used when you set up streaming software.

        For example: a1b2c3d4e5f6.global-contribute.live-video.net

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelIngestEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="channelPlaybackUrl")
    def channel_playback_url(self) -> builtins.str:
        '''(experimental) Channel playback URL.

        For example:
        https://a1b2c3d4e5f6.us-west-2.playback.live-video.net/api/video/v1/us-west-2.123456789012.channel.abcdEFGH.m3u8

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelPlaybackUrl"))


__all__ = [
    "CfnChannel",
    "CfnChannelProps",
    "CfnPlaybackKeyPair",
    "CfnPlaybackKeyPairProps",
    "CfnStreamKey",
    "CfnStreamKeyProps",
    "Channel",
    "ChannelProps",
    "ChannelType",
    "IChannel",
    "IPlaybackKeyPair",
    "IStreamKey",
    "LatencyMode",
    "PlaybackKeyPair",
    "PlaybackKeyPairProps",
    "StreamKey",
    "StreamKeyProps",
]

publication.publish()
