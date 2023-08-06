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
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_iam import Grant as _Grant_bcb5eae7, IGrantable as _IGrantable_4c5a91d1
from ..aws_kms import IKey as _IKey_36930160


@jsii.implements(_IInspectable_82c04a63)
class CfnStream(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kinesis.CfnStream",
):
    '''A CloudFormation ``AWS::Kinesis::Stream``.

    :cloudformationResource: AWS::Kinesis::Stream
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        shard_count: jsii.Number,
        name: typing.Optional[builtins.str] = None,
        retention_period_hours: typing.Optional[jsii.Number] = None,
        stream_encryption: typing.Optional[typing.Union["CfnStream.StreamEncryptionProperty", _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::Kinesis::Stream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param shard_count: ``AWS::Kinesis::Stream.ShardCount``.
        :param name: ``AWS::Kinesis::Stream.Name``.
        :param retention_period_hours: ``AWS::Kinesis::Stream.RetentionPeriodHours``.
        :param stream_encryption: ``AWS::Kinesis::Stream.StreamEncryption``.
        :param tags: ``AWS::Kinesis::Stream.Tags``.
        '''
        props = CfnStreamProps(
            shard_count=shard_count,
            name=name,
            retention_period_hours=retention_period_hours,
            stream_encryption=stream_encryption,
            tags=tags,
        )

        jsii.create(CfnStream, self, [scope, id, props])

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Kinesis::Stream.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="shardCount")
    def shard_count(self) -> jsii.Number:
        '''``AWS::Kinesis::Stream.ShardCount``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-shardcount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "shardCount"))

    @shard_count.setter
    def shard_count(self, value: jsii.Number) -> None:
        jsii.set(self, "shardCount", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Kinesis::Stream.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="retentionPeriodHours")
    def retention_period_hours(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Kinesis::Stream.RetentionPeriodHours``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-retentionperiodhours
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriodHours"))

    @retention_period_hours.setter
    def retention_period_hours(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "retentionPeriodHours", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamEncryption")
    def stream_encryption(
        self,
    ) -> typing.Optional[typing.Union["CfnStream.StreamEncryptionProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Kinesis::Stream.StreamEncryption``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-streamencryption
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStream.StreamEncryptionProperty", _IResolvable_a771d0ef]], jsii.get(self, "streamEncryption"))

    @stream_encryption.setter
    def stream_encryption(
        self,
        value: typing.Optional[typing.Union["CfnStream.StreamEncryptionProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "streamEncryption", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesis.CfnStream.StreamEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType", "key_id": "keyId"},
    )
    class StreamEncryptionProperty:
        def __init__(
            self,
            *,
            encryption_type: builtins.str,
            key_id: builtins.str,
        ) -> None:
            '''
            :param encryption_type: ``CfnStream.StreamEncryptionProperty.EncryptionType``.
            :param key_id: ``CfnStream.StreamEncryptionProperty.KeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "encryption_type": encryption_type,
                "key_id": key_id,
            }

        @builtins.property
        def encryption_type(self) -> builtins.str:
            '''``CfnStream.StreamEncryptionProperty.EncryptionType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html#cfn-kinesis-stream-streamencryption-encryptiontype
            '''
            result = self._values.get("encryption_type")
            assert result is not None, "Required property 'encryption_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_id(self) -> builtins.str:
            '''``CfnStream.StreamEncryptionProperty.KeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html#cfn-kinesis-stream-streamencryption-keyid
            '''
            result = self._values.get("key_id")
            assert result is not None, "Required property 'key_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnStreamConsumer(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kinesis.CfnStreamConsumer",
):
    '''A CloudFormation ``AWS::Kinesis::StreamConsumer``.

    :cloudformationResource: AWS::Kinesis::StreamConsumer
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        consumer_name: builtins.str,
        stream_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Kinesis::StreamConsumer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param consumer_name: ``AWS::Kinesis::StreamConsumer.ConsumerName``.
        :param stream_arn: ``AWS::Kinesis::StreamConsumer.StreamARN``.
        '''
        props = CfnStreamConsumerProps(
            consumer_name=consumer_name, stream_arn=stream_arn
        )

        jsii.create(CfnStreamConsumer, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrConsumerArn")
    def attr_consumer_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ConsumerARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConsumerArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrConsumerCreationTimestamp")
    def attr_consumer_creation_timestamp(self) -> builtins.str:
        '''
        :cloudformationAttribute: ConsumerCreationTimestamp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConsumerCreationTimestamp"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrConsumerName")
    def attr_consumer_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: ConsumerName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConsumerName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrConsumerStatus")
    def attr_consumer_status(self) -> builtins.str:
        '''
        :cloudformationAttribute: ConsumerStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConsumerStatus"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrStreamArn")
    def attr_stream_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: StreamARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStreamArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="consumerName")
    def consumer_name(self) -> builtins.str:
        '''``AWS::Kinesis::StreamConsumer.ConsumerName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-consumername
        '''
        return typing.cast(builtins.str, jsii.get(self, "consumerName"))

    @consumer_name.setter
    def consumer_name(self, value: builtins.str) -> None:
        jsii.set(self, "consumerName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> builtins.str:
        '''``AWS::Kinesis::StreamConsumer.StreamARN``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-streamarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "streamArn"))

    @stream_arn.setter
    def stream_arn(self, value: builtins.str) -> None:
        jsii.set(self, "streamArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_kinesis.CfnStreamConsumerProps",
    jsii_struct_bases=[],
    name_mapping={"consumer_name": "consumerName", "stream_arn": "streamArn"},
)
class CfnStreamConsumerProps:
    def __init__(
        self,
        *,
        consumer_name: builtins.str,
        stream_arn: builtins.str,
    ) -> None:
        '''Properties for defining a ``AWS::Kinesis::StreamConsumer``.

        :param consumer_name: ``AWS::Kinesis::StreamConsumer.ConsumerName``.
        :param stream_arn: ``AWS::Kinesis::StreamConsumer.StreamARN``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "consumer_name": consumer_name,
            "stream_arn": stream_arn,
        }

    @builtins.property
    def consumer_name(self) -> builtins.str:
        '''``AWS::Kinesis::StreamConsumer.ConsumerName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-consumername
        '''
        result = self._values.get("consumer_name")
        assert result is not None, "Required property 'consumer_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream_arn(self) -> builtins.str:
        '''``AWS::Kinesis::StreamConsumer.StreamARN``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-streamarn
        '''
        result = self._values.get("stream_arn")
        assert result is not None, "Required property 'stream_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamConsumerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_kinesis.CfnStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "shard_count": "shardCount",
        "name": "name",
        "retention_period_hours": "retentionPeriodHours",
        "stream_encryption": "streamEncryption",
        "tags": "tags",
    },
)
class CfnStreamProps:
    def __init__(
        self,
        *,
        shard_count: jsii.Number,
        name: typing.Optional[builtins.str] = None,
        retention_period_hours: typing.Optional[jsii.Number] = None,
        stream_encryption: typing.Optional[typing.Union[CfnStream.StreamEncryptionProperty, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Kinesis::Stream``.

        :param shard_count: ``AWS::Kinesis::Stream.ShardCount``.
        :param name: ``AWS::Kinesis::Stream.Name``.
        :param retention_period_hours: ``AWS::Kinesis::Stream.RetentionPeriodHours``.
        :param stream_encryption: ``AWS::Kinesis::Stream.StreamEncryption``.
        :param tags: ``AWS::Kinesis::Stream.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "shard_count": shard_count,
        }
        if name is not None:
            self._values["name"] = name
        if retention_period_hours is not None:
            self._values["retention_period_hours"] = retention_period_hours
        if stream_encryption is not None:
            self._values["stream_encryption"] = stream_encryption
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def shard_count(self) -> jsii.Number:
        '''``AWS::Kinesis::Stream.ShardCount``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-shardcount
        '''
        result = self._values.get("shard_count")
        assert result is not None, "Required property 'shard_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Kinesis::Stream.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_period_hours(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Kinesis::Stream.RetentionPeriodHours``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-retentionperiodhours
        '''
        result = self._values.get("retention_period_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stream_encryption(
        self,
    ) -> typing.Optional[typing.Union[CfnStream.StreamEncryptionProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Kinesis::Stream.StreamEncryption``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-streamencryption
        '''
        result = self._values.get("stream_encryption")
        return typing.cast(typing.Optional[typing.Union[CfnStream.StreamEncryptionProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Kinesis::Stream.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_kinesis.IStream")
class IStream(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A Kinesis Stream.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IStreamProxy"]:
        return _IStreamProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> builtins.str:
        '''(experimental) The ARN of the stream.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        '''(experimental) The name of the stream.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) Optional KMS encryption key associated with this stream.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the indicated permissions on this stream to the provided IAM principal.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to decrypt the
        contents of the stream will also be granted.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grants read/write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to encrypt the
        contents of the stream will also be granted.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _IStreamProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) A Kinesis Stream.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_kinesis.IStream"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> builtins.str:
        '''(experimental) The ARN of the stream.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "streamArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        '''(experimental) The name of the stream.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "streamName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) Optional KMS encryption key associated with this stream.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IKey_36930160], jsii.get(self, "encryptionKey"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the indicated permissions on this stream to the provided IAM principal.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to decrypt the
        contents of the stream will also be granted.

        :param grantee: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grants read/write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        :param grantee: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantReadWrite", [grantee]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to encrypt the
        contents of the stream will also be granted.

        :param grantee: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [grantee]))


@jsii.implements(IStream)
class Stream(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kinesis.Stream",
):
    '''(experimental) A Kinesis stream.

    Can be encrypted with a KMS key.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        encryption: typing.Optional["StreamEncryption"] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        retention_period: typing.Optional[_Duration_070aa057] = None,
        shard_count: typing.Optional[jsii.Number] = None,
        stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param encryption: (experimental) The kind of server-side encryption to apply to this stream. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - StreamEncryption.KMS if encrypted Streams are supported in the region or StreamEncryption.UNENCRYPTED otherwise. StreamEncryption.KMS if an encryption key is supplied through the encryptionKey property
        :param encryption_key: (experimental) External KMS key to use for stream encryption. The 'encryption' property must be set to "Kms". Default: - Kinesis Data Streams master key ('/alias/aws/kinesis'). If encryption is set to StreamEncryption.KMS and this property is undefined, a new KMS key will be created and associated with this stream.
        :param retention_period: (experimental) The number of hours for the data records that are stored in shards to remain accessible. Default: Duration.hours(24)
        :param shard_count: (experimental) The number of shards for the stream. Default: 1
        :param stream_name: (experimental) Enforces a particular physical stream name. Default: 

        :stability: experimental
        '''
        props = StreamProps(
            encryption=encryption,
            encryption_key=encryption_key,
            retention_period=retention_period,
            shard_count=shard_count,
            stream_name=stream_name,
        )

        jsii.create(Stream, self, [scope, id, props])

    @jsii.member(jsii_name="fromStreamArn") # type: ignore[misc]
    @builtins.classmethod
    def from_stream_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        stream_arn: builtins.str,
    ) -> IStream:
        '''(experimental) Import an existing Kinesis Stream provided an ARN.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param stream_arn: Stream ARN (i.e. arn:aws:kinesis:::stream/Foo).

        :stability: experimental
        '''
        return typing.cast(IStream, jsii.sinvoke(cls, "fromStreamArn", [scope, id, stream_arn]))

    @jsii.member(jsii_name="fromStreamAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_stream_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        stream_arn: builtins.str,
        encryption_key: typing.Optional[_IKey_36930160] = None,
    ) -> IStream:
        '''(experimental) Creates a Stream construct that represents an external stream.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param stream_arn: (experimental) The ARN of the stream.
        :param encryption_key: (experimental) The KMS key securing the contents of the stream if encryption is enabled. Default: - No encryption

        :stability: experimental
        '''
        attrs = StreamAttributes(stream_arn=stream_arn, encryption_key=encryption_key)

        return typing.cast(IStream, jsii.sinvoke(cls, "fromStreamAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the indicated permissions on this stream to the given IAM principal (Role/Group/User).

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to decrypt the
        contents of the stream will also be granted.

        :param grantee: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grants read/write permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        :param grantee: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantReadWrite", [grantee]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for this stream and its contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to ues the key to decrypt the
        contents of the stream will also be granted.

        :param grantee: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [grantee]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamArn")
    def stream_arn(self) -> builtins.str:
        '''(experimental) The ARN of the stream.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "streamArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        '''(experimental) The name of the stream.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "streamName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) Optional KMS encryption key associated with this stream.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IKey_36930160], jsii.get(self, "encryptionKey"))


@jsii.data_type(
    jsii_type="monocdk.aws_kinesis.StreamAttributes",
    jsii_struct_bases=[],
    name_mapping={"stream_arn": "streamArn", "encryption_key": "encryptionKey"},
)
class StreamAttributes:
    def __init__(
        self,
        *,
        stream_arn: builtins.str,
        encryption_key: typing.Optional[_IKey_36930160] = None,
    ) -> None:
        '''(experimental) A reference to a stream.

        The easiest way to instantiate is to call
        ``stream.export()``. Then, the consumer can use ``Stream.import(this, ref)`` and
        get a ``Stream``.

        :param stream_arn: (experimental) The ARN of the stream.
        :param encryption_key: (experimental) The KMS key securing the contents of the stream if encryption is enabled. Default: - No encryption

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "stream_arn": stream_arn,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def stream_arn(self) -> builtins.str:
        '''(experimental) The ARN of the stream.

        :stability: experimental
        '''
        result = self._values.get("stream_arn")
        assert result is not None, "Required property 'stream_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The KMS key securing the contents of the stream if encryption is enabled.

        :default: - No encryption

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_kinesis.StreamEncryption")
class StreamEncryption(enum.Enum):
    '''(experimental) What kind of server-side encryption to apply to this stream.

    :stability: experimental
    '''

    UNENCRYPTED = "UNENCRYPTED"
    '''(experimental) Records in the stream are not encrypted.

    :stability: experimental
    '''
    KMS = "KMS"
    '''(experimental) Server-side encryption with a KMS key managed by the user.

    If ``encryptionKey`` is specified, this key will be used, otherwise, one will be defined.

    :stability: experimental
    '''
    MANAGED = "MANAGED"
    '''(experimental) Server-side encryption with a master key managed by Amazon Kinesis.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_kinesis.StreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "retention_period": "retentionPeriod",
        "shard_count": "shardCount",
        "stream_name": "streamName",
    },
)
class StreamProps:
    def __init__(
        self,
        *,
        encryption: typing.Optional[StreamEncryption] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        retention_period: typing.Optional[_Duration_070aa057] = None,
        shard_count: typing.Optional[jsii.Number] = None,
        stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a Kinesis Stream.

        :param encryption: (experimental) The kind of server-side encryption to apply to this stream. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - StreamEncryption.KMS if encrypted Streams are supported in the region or StreamEncryption.UNENCRYPTED otherwise. StreamEncryption.KMS if an encryption key is supplied through the encryptionKey property
        :param encryption_key: (experimental) External KMS key to use for stream encryption. The 'encryption' property must be set to "Kms". Default: - Kinesis Data Streams master key ('/alias/aws/kinesis'). If encryption is set to StreamEncryption.KMS and this property is undefined, a new KMS key will be created and associated with this stream.
        :param retention_period: (experimental) The number of hours for the data records that are stored in shards to remain accessible. Default: Duration.hours(24)
        :param shard_count: (experimental) The number of shards for the stream. Default: 1
        :param stream_name: (experimental) Enforces a particular physical stream name. Default: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if shard_count is not None:
            self._values["shard_count"] = shard_count
        if stream_name is not None:
            self._values["stream_name"] = stream_name

    @builtins.property
    def encryption(self) -> typing.Optional[StreamEncryption]:
        '''(experimental) The kind of server-side encryption to apply to this stream.

        If you choose KMS, you can specify a KMS key via ``encryptionKey``. If
        encryption key is not specified, a key will automatically be created.

        :default:

        - StreamEncryption.KMS if encrypted Streams are supported in the region
        or StreamEncryption.UNENCRYPTED otherwise.
        StreamEncryption.KMS if an encryption key is supplied through the encryptionKey property

        :stability: experimental
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[StreamEncryption], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) External KMS key to use for stream encryption.

        The 'encryption' property must be set to "Kms".

        :default:

        - Kinesis Data Streams master key ('/alias/aws/kinesis').
        If encryption is set to StreamEncryption.KMS and this property is undefined, a new KMS key
        will be created and associated with this stream.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def retention_period(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The number of hours for the data records that are stored in shards to remain accessible.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def shard_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of shards for the stream.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("shard_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stream_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Enforces a particular physical stream name.

        :default:

        :stability: experimental
        '''
        result = self._values.get("stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnStream",
    "CfnStreamConsumer",
    "CfnStreamConsumerProps",
    "CfnStreamProps",
    "IStream",
    "Stream",
    "StreamAttributes",
    "StreamEncryption",
    "StreamProps",
]

publication.publish()
