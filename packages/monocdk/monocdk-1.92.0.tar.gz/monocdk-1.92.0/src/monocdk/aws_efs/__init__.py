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
    IDependable as _IDependable_1175c9f7,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    Size as _Size_7fbd4337,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_ec2 import (
    Connections as _Connections_57ccbda9,
    IConnectable as _IConnectable_c1c0e72c,
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_kms import IKey as _IKey_36930160


@jsii.data_type(
    jsii_type="monocdk.aws_efs.AccessPointAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "access_point_arn": "accessPointArn",
        "access_point_id": "accessPointId",
        "file_system": "fileSystem",
    },
)
class AccessPointAttributes:
    def __init__(
        self,
        *,
        access_point_arn: typing.Optional[builtins.str] = None,
        access_point_id: typing.Optional[builtins.str] = None,
        file_system: typing.Optional["IFileSystem"] = None,
    ) -> None:
        '''(experimental) Attributes that can be specified when importing an AccessPoint.

        :param access_point_arn: (experimental) The ARN of the AccessPoint One of this, or {@link accessPointId} is required. Default: - determined based on accessPointId
        :param access_point_id: (experimental) The ID of the AccessPoint One of this, or {@link accessPointArn} is required. Default: - determined based on accessPointArn
        :param file_system: (experimental) The EFS file system. Default: - no EFS file system

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if access_point_arn is not None:
            self._values["access_point_arn"] = access_point_arn
        if access_point_id is not None:
            self._values["access_point_id"] = access_point_id
        if file_system is not None:
            self._values["file_system"] = file_system

    @builtins.property
    def access_point_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the AccessPoint One of this, or {@link accessPointId} is required.

        :default: - determined based on accessPointId

        :stability: experimental
        '''
        result = self._values.get("access_point_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_point_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of the AccessPoint One of this, or {@link accessPointArn} is required.

        :default: - determined based on accessPointArn

        :stability: experimental
        '''
        result = self._values.get("access_point_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system(self) -> typing.Optional["IFileSystem"]:
        '''(experimental) The EFS file system.

        :default: - no EFS file system

        :stability: experimental
        '''
        result = self._values.get("file_system")
        return typing.cast(typing.Optional["IFileSystem"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPointAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.AccessPointOptions",
    jsii_struct_bases=[],
    name_mapping={
        "create_acl": "createAcl",
        "path": "path",
        "posix_user": "posixUser",
    },
)
class AccessPointOptions:
    def __init__(
        self,
        *,
        create_acl: typing.Optional["Acl"] = None,
        path: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional["PosixUser"] = None,
    ) -> None:
        '''(experimental) Options to create an AccessPoint.

        :param create_acl: (experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: (experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: (experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced

        :stability: experimental
        '''
        if isinstance(create_acl, dict):
            create_acl = Acl(**create_acl)
        if isinstance(posix_user, dict):
            posix_user = PosixUser(**posix_user)
        self._values: typing.Dict[str, typing.Any] = {}
        if create_acl is not None:
            self._values["create_acl"] = create_acl
        if path is not None:
            self._values["path"] = path
        if posix_user is not None:
            self._values["posix_user"] = posix_user

    @builtins.property
    def create_acl(self) -> typing.Optional["Acl"]:
        '''(experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory.

        If the
        root directory specified by ``path`` does not exist, EFS creates the root directory and applies the
        permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``.

        :default: - None. The directory specified by ``path`` must exist.

        :stability: experimental
        '''
        result = self._values.get("create_acl")
        return typing.cast(typing.Optional["Acl"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system.

        :default: '/'

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def posix_user(self) -> typing.Optional["PosixUser"]:
        '''(experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point.

        Specify this to enforce a user identity using an access point.

        :default: - user identity not enforced

        :see: - `Enforcing a User Identity Using an Access Point <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>`_
        :stability: experimental
        '''
        result = self._values.get("posix_user")
        return typing.cast(typing.Optional["PosixUser"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPointOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.AccessPointProps",
    jsii_struct_bases=[AccessPointOptions],
    name_mapping={
        "create_acl": "createAcl",
        "path": "path",
        "posix_user": "posixUser",
        "file_system": "fileSystem",
    },
)
class AccessPointProps(AccessPointOptions):
    def __init__(
        self,
        *,
        create_acl: typing.Optional["Acl"] = None,
        path: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional["PosixUser"] = None,
        file_system: "IFileSystem",
    ) -> None:
        '''(experimental) Properties for the AccessPoint.

        :param create_acl: (experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: (experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: (experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced
        :param file_system: (experimental) The efs filesystem.

        :stability: experimental
        '''
        if isinstance(create_acl, dict):
            create_acl = Acl(**create_acl)
        if isinstance(posix_user, dict):
            posix_user = PosixUser(**posix_user)
        self._values: typing.Dict[str, typing.Any] = {
            "file_system": file_system,
        }
        if create_acl is not None:
            self._values["create_acl"] = create_acl
        if path is not None:
            self._values["path"] = path
        if posix_user is not None:
            self._values["posix_user"] = posix_user

    @builtins.property
    def create_acl(self) -> typing.Optional["Acl"]:
        '''(experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory.

        If the
        root directory specified by ``path`` does not exist, EFS creates the root directory and applies the
        permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``.

        :default: - None. The directory specified by ``path`` must exist.

        :stability: experimental
        '''
        result = self._values.get("create_acl")
        return typing.cast(typing.Optional["Acl"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system.

        :default: '/'

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def posix_user(self) -> typing.Optional["PosixUser"]:
        '''(experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point.

        Specify this to enforce a user identity using an access point.

        :default: - user identity not enforced

        :see: - `Enforcing a User Identity Using an Access Point <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>`_
        :stability: experimental
        '''
        result = self._values.get("posix_user")
        return typing.cast(typing.Optional["PosixUser"], result)

    @builtins.property
    def file_system(self) -> "IFileSystem":
        '''(experimental) The efs filesystem.

        :stability: experimental
        '''
        result = self._values.get("file_system")
        assert result is not None, "Required property 'file_system' is missing"
        return typing.cast("IFileSystem", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.Acl",
    jsii_struct_bases=[],
    name_mapping={
        "owner_gid": "ownerGid",
        "owner_uid": "ownerUid",
        "permissions": "permissions",
    },
)
class Acl:
    def __init__(
        self,
        *,
        owner_gid: builtins.str,
        owner_uid: builtins.str,
        permissions: builtins.str,
    ) -> None:
        '''(experimental) Permissions as POSIX ACL.

        :param owner_gid: (experimental) Specifies the POSIX group ID to apply to the RootDirectory. Accepts values from 0 to 2^32 (4294967295).
        :param owner_uid: (experimental) Specifies the POSIX user ID to apply to the RootDirectory. Accepts values from 0 to 2^32 (4294967295).
        :param permissions: (experimental) Specifies the POSIX permissions to apply to the RootDirectory, in the format of an octal number representing the file's mode bits.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "owner_gid": owner_gid,
            "owner_uid": owner_uid,
            "permissions": permissions,
        }

    @builtins.property
    def owner_gid(self) -> builtins.str:
        '''(experimental) Specifies the POSIX group ID to apply to the RootDirectory.

        Accepts values from 0 to 2^32 (4294967295).

        :stability: experimental
        '''
        result = self._values.get("owner_gid")
        assert result is not None, "Required property 'owner_gid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner_uid(self) -> builtins.str:
        '''(experimental) Specifies the POSIX user ID to apply to the RootDirectory.

        Accepts values from 0 to 2^32 (4294967295).

        :stability: experimental
        '''
        result = self._values.get("owner_uid")
        assert result is not None, "Required property 'owner_uid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permissions(self) -> builtins.str:
        '''(experimental) Specifies the POSIX permissions to apply to the RootDirectory, in the format of an octal number representing the file's mode bits.

        :stability: experimental
        '''
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Acl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAccessPoint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_efs.CfnAccessPoint",
):
    '''A CloudFormation ``AWS::EFS::AccessPoint``.

    :cloudformationResource: AWS::EFS::AccessPoint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        file_system_id: builtins.str,
        access_point_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAccessPoint.AccessPointTagProperty", _IResolvable_a771d0ef]]]] = None,
        client_token: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional[typing.Union["CfnAccessPoint.PosixUserProperty", _IResolvable_a771d0ef]] = None,
        root_directory: typing.Optional[typing.Union["CfnAccessPoint.RootDirectoryProperty", _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::EFS::AccessPoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param file_system_id: ``AWS::EFS::AccessPoint.FileSystemId``.
        :param access_point_tags: ``AWS::EFS::AccessPoint.AccessPointTags``.
        :param client_token: ``AWS::EFS::AccessPoint.ClientToken``.
        :param posix_user: ``AWS::EFS::AccessPoint.PosixUser``.
        :param root_directory: ``AWS::EFS::AccessPoint.RootDirectory``.
        '''
        props = CfnAccessPointProps(
            file_system_id=file_system_id,
            access_point_tags=access_point_tags,
            client_token=client_token,
            posix_user=posix_user,
            root_directory=root_directory,
        )

        jsii.create(CfnAccessPoint, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrAccessPointId")
    def attr_access_point_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: AccessPointId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAccessPointId"))

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
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        '''``AWS::EFS::AccessPoint.FileSystemId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-filesystemid
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @file_system_id.setter
    def file_system_id(self, value: builtins.str) -> None:
        jsii.set(self, "fileSystemId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessPointTags")
    def access_point_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAccessPoint.AccessPointTagProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::EFS::AccessPoint.AccessPointTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-accesspointtags
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAccessPoint.AccessPointTagProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "accessPointTags"))

    @access_point_tags.setter
    def access_point_tags(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAccessPoint.AccessPointTagProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "accessPointTags", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientToken")
    def client_token(self) -> typing.Optional[builtins.str]:
        '''``AWS::EFS::AccessPoint.ClientToken``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-clienttoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientToken"))

    @client_token.setter
    def client_token(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clientToken", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="posixUser")
    def posix_user(
        self,
    ) -> typing.Optional[typing.Union["CfnAccessPoint.PosixUserProperty", _IResolvable_a771d0ef]]:
        '''``AWS::EFS::AccessPoint.PosixUser``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-posixuser
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAccessPoint.PosixUserProperty", _IResolvable_a771d0ef]], jsii.get(self, "posixUser"))

    @posix_user.setter
    def posix_user(
        self,
        value: typing.Optional[typing.Union["CfnAccessPoint.PosixUserProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "posixUser", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rootDirectory")
    def root_directory(
        self,
    ) -> typing.Optional[typing.Union["CfnAccessPoint.RootDirectoryProperty", _IResolvable_a771d0ef]]:
        '''``AWS::EFS::AccessPoint.RootDirectory``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-rootdirectory
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAccessPoint.RootDirectoryProperty", _IResolvable_a771d0ef]], jsii.get(self, "rootDirectory"))

    @root_directory.setter
    def root_directory(
        self,
        value: typing.Optional[typing.Union["CfnAccessPoint.RootDirectoryProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "rootDirectory", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnAccessPoint.AccessPointTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class AccessPointTagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param key: ``CfnAccessPoint.AccessPointTagProperty.Key``.
            :param value: ``CfnAccessPoint.AccessPointTagProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-accesspointtag.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''``CfnAccessPoint.AccessPointTagProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-accesspointtag.html#cfn-efs-accesspoint-accesspointtag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''``CfnAccessPoint.AccessPointTagProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-accesspointtag.html#cfn-efs-accesspoint-accesspointtag-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessPointTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnAccessPoint.CreationInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "owner_gid": "ownerGid",
            "owner_uid": "ownerUid",
            "permissions": "permissions",
        },
    )
    class CreationInfoProperty:
        def __init__(
            self,
            *,
            owner_gid: builtins.str,
            owner_uid: builtins.str,
            permissions: builtins.str,
        ) -> None:
            '''
            :param owner_gid: ``CfnAccessPoint.CreationInfoProperty.OwnerGid``.
            :param owner_uid: ``CfnAccessPoint.CreationInfoProperty.OwnerUid``.
            :param permissions: ``CfnAccessPoint.CreationInfoProperty.Permissions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-creationinfo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "owner_gid": owner_gid,
                "owner_uid": owner_uid,
                "permissions": permissions,
            }

        @builtins.property
        def owner_gid(self) -> builtins.str:
            '''``CfnAccessPoint.CreationInfoProperty.OwnerGid``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-creationinfo.html#cfn-efs-accesspoint-creationinfo-ownergid
            '''
            result = self._values.get("owner_gid")
            assert result is not None, "Required property 'owner_gid' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def owner_uid(self) -> builtins.str:
            '''``CfnAccessPoint.CreationInfoProperty.OwnerUid``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-creationinfo.html#cfn-efs-accesspoint-creationinfo-owneruid
            '''
            result = self._values.get("owner_uid")
            assert result is not None, "Required property 'owner_uid' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def permissions(self) -> builtins.str:
            '''``CfnAccessPoint.CreationInfoProperty.Permissions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-creationinfo.html#cfn-efs-accesspoint-creationinfo-permissions
            '''
            result = self._values.get("permissions")
            assert result is not None, "Required property 'permissions' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreationInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnAccessPoint.PosixUserProperty",
        jsii_struct_bases=[],
        name_mapping={"gid": "gid", "uid": "uid", "secondary_gids": "secondaryGids"},
    )
    class PosixUserProperty:
        def __init__(
            self,
            *,
            gid: builtins.str,
            uid: builtins.str,
            secondary_gids: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            '''
            :param gid: ``CfnAccessPoint.PosixUserProperty.Gid``.
            :param uid: ``CfnAccessPoint.PosixUserProperty.Uid``.
            :param secondary_gids: ``CfnAccessPoint.PosixUserProperty.SecondaryGids``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-posixuser.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "gid": gid,
                "uid": uid,
            }
            if secondary_gids is not None:
                self._values["secondary_gids"] = secondary_gids

        @builtins.property
        def gid(self) -> builtins.str:
            '''``CfnAccessPoint.PosixUserProperty.Gid``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-posixuser.html#cfn-efs-accesspoint-posixuser-gid
            '''
            result = self._values.get("gid")
            assert result is not None, "Required property 'gid' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def uid(self) -> builtins.str:
            '''``CfnAccessPoint.PosixUserProperty.Uid``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-posixuser.html#cfn-efs-accesspoint-posixuser-uid
            '''
            result = self._values.get("uid")
            assert result is not None, "Required property 'uid' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def secondary_gids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnAccessPoint.PosixUserProperty.SecondaryGids``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-posixuser.html#cfn-efs-accesspoint-posixuser-secondarygids
            '''
            result = self._values.get("secondary_gids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PosixUserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnAccessPoint.RootDirectoryProperty",
        jsii_struct_bases=[],
        name_mapping={"creation_info": "creationInfo", "path": "path"},
    )
    class RootDirectoryProperty:
        def __init__(
            self,
            *,
            creation_info: typing.Optional[typing.Union["CfnAccessPoint.CreationInfoProperty", _IResolvable_a771d0ef]] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param creation_info: ``CfnAccessPoint.RootDirectoryProperty.CreationInfo``.
            :param path: ``CfnAccessPoint.RootDirectoryProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-rootdirectory.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if creation_info is not None:
                self._values["creation_info"] = creation_info
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def creation_info(
            self,
        ) -> typing.Optional[typing.Union["CfnAccessPoint.CreationInfoProperty", _IResolvable_a771d0ef]]:
            '''``CfnAccessPoint.RootDirectoryProperty.CreationInfo``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-rootdirectory.html#cfn-efs-accesspoint-rootdirectory-creationinfo
            '''
            result = self._values.get("creation_info")
            return typing.cast(typing.Optional[typing.Union["CfnAccessPoint.CreationInfoProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''``CfnAccessPoint.RootDirectoryProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-rootdirectory.html#cfn-efs-accesspoint-rootdirectory-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RootDirectoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.CfnAccessPointProps",
    jsii_struct_bases=[],
    name_mapping={
        "file_system_id": "fileSystemId",
        "access_point_tags": "accessPointTags",
        "client_token": "clientToken",
        "posix_user": "posixUser",
        "root_directory": "rootDirectory",
    },
)
class CfnAccessPointProps:
    def __init__(
        self,
        *,
        file_system_id: builtins.str,
        access_point_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAccessPoint.AccessPointTagProperty, _IResolvable_a771d0ef]]]] = None,
        client_token: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional[typing.Union[CfnAccessPoint.PosixUserProperty, _IResolvable_a771d0ef]] = None,
        root_directory: typing.Optional[typing.Union[CfnAccessPoint.RootDirectoryProperty, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::EFS::AccessPoint``.

        :param file_system_id: ``AWS::EFS::AccessPoint.FileSystemId``.
        :param access_point_tags: ``AWS::EFS::AccessPoint.AccessPointTags``.
        :param client_token: ``AWS::EFS::AccessPoint.ClientToken``.
        :param posix_user: ``AWS::EFS::AccessPoint.PosixUser``.
        :param root_directory: ``AWS::EFS::AccessPoint.RootDirectory``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "file_system_id": file_system_id,
        }
        if access_point_tags is not None:
            self._values["access_point_tags"] = access_point_tags
        if client_token is not None:
            self._values["client_token"] = client_token
        if posix_user is not None:
            self._values["posix_user"] = posix_user
        if root_directory is not None:
            self._values["root_directory"] = root_directory

    @builtins.property
    def file_system_id(self) -> builtins.str:
        '''``AWS::EFS::AccessPoint.FileSystemId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-filesystemid
        '''
        result = self._values.get("file_system_id")
        assert result is not None, "Required property 'file_system_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_point_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAccessPoint.AccessPointTagProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::EFS::AccessPoint.AccessPointTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-accesspointtags
        '''
        result = self._values.get("access_point_tags")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAccessPoint.AccessPointTagProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        '''``AWS::EFS::AccessPoint.ClientToken``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-clienttoken
        '''
        result = self._values.get("client_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def posix_user(
        self,
    ) -> typing.Optional[typing.Union[CfnAccessPoint.PosixUserProperty, _IResolvable_a771d0ef]]:
        '''``AWS::EFS::AccessPoint.PosixUser``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-posixuser
        '''
        result = self._values.get("posix_user")
        return typing.cast(typing.Optional[typing.Union[CfnAccessPoint.PosixUserProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def root_directory(
        self,
    ) -> typing.Optional[typing.Union[CfnAccessPoint.RootDirectoryProperty, _IResolvable_a771d0ef]]:
        '''``AWS::EFS::AccessPoint.RootDirectory``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-rootdirectory
        '''
        result = self._values.get("root_directory")
        return typing.cast(typing.Optional[typing.Union[CfnAccessPoint.RootDirectoryProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFileSystem(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_efs.CfnFileSystem",
):
    '''A CloudFormation ``AWS::EFS::FileSystem``.

    :cloudformationResource: AWS::EFS::FileSystem
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        backup_policy: typing.Optional[typing.Union["CfnFileSystem.BackupPolicyProperty", _IResolvable_a771d0ef]] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        file_system_policy: typing.Any = None,
        file_system_tags: typing.Optional[typing.List["CfnFileSystem.ElasticFileSystemTagProperty"]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        lifecycle_policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFileSystem.LifecyclePolicyProperty", _IResolvable_a771d0ef]]]] = None,
        performance_mode: typing.Optional[builtins.str] = None,
        provisioned_throughput_in_mibps: typing.Optional[jsii.Number] = None,
        throughput_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::EFS::FileSystem``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param backup_policy: ``AWS::EFS::FileSystem.BackupPolicy``.
        :param encrypted: ``AWS::EFS::FileSystem.Encrypted``.
        :param file_system_policy: ``AWS::EFS::FileSystem.FileSystemPolicy``.
        :param file_system_tags: ``AWS::EFS::FileSystem.FileSystemTags``.
        :param kms_key_id: ``AWS::EFS::FileSystem.KmsKeyId``.
        :param lifecycle_policies: ``AWS::EFS::FileSystem.LifecyclePolicies``.
        :param performance_mode: ``AWS::EFS::FileSystem.PerformanceMode``.
        :param provisioned_throughput_in_mibps: ``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.
        :param throughput_mode: ``AWS::EFS::FileSystem.ThroughputMode``.
        '''
        props = CfnFileSystemProps(
            backup_policy=backup_policy,
            encrypted=encrypted,
            file_system_policy=file_system_policy,
            file_system_tags=file_system_tags,
            kms_key_id=kms_key_id,
            lifecycle_policies=lifecycle_policies,
            performance_mode=performance_mode,
            provisioned_throughput_in_mibps=provisioned_throughput_in_mibps,
            throughput_mode=throughput_mode,
        )

        jsii.create(CfnFileSystem, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrFileSystemId")
    def attr_file_system_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: FileSystemId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFileSystemId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::EFS::FileSystem.FileSystemTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystemtags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileSystemPolicy")
    def file_system_policy(self) -> typing.Any:
        '''``AWS::EFS::FileSystem.FileSystemPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystempolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "fileSystemPolicy"))

    @file_system_policy.setter
    def file_system_policy(self, value: typing.Any) -> None:
        jsii.set(self, "fileSystemPolicy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPolicy")
    def backup_policy(
        self,
    ) -> typing.Optional[typing.Union["CfnFileSystem.BackupPolicyProperty", _IResolvable_a771d0ef]]:
        '''``AWS::EFS::FileSystem.BackupPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-backuppolicy
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFileSystem.BackupPolicyProperty", _IResolvable_a771d0ef]], jsii.get(self, "backupPolicy"))

    @backup_policy.setter
    def backup_policy(
        self,
        value: typing.Optional[typing.Union["CfnFileSystem.BackupPolicyProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "backupPolicy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encrypted")
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::EFS::FileSystem.Encrypted``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-encrypted
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "encrypted"))

    @encrypted.setter
    def encrypted(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "encrypted", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::EFS::FileSystem.KmsKeyId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lifecyclePolicies")
    def lifecycle_policies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFileSystem.LifecyclePolicyProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::EFS::FileSystem.LifecyclePolicies``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-lifecyclepolicies
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFileSystem.LifecyclePolicyProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "lifecyclePolicies"))

    @lifecycle_policies.setter
    def lifecycle_policies(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFileSystem.LifecyclePolicyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "lifecyclePolicies", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="performanceMode")
    def performance_mode(self) -> typing.Optional[builtins.str]:
        '''``AWS::EFS::FileSystem.PerformanceMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-performancemode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "performanceMode"))

    @performance_mode.setter
    def performance_mode(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "performanceMode", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="provisionedThroughputInMibps")
    def provisioned_throughput_in_mibps(self) -> typing.Optional[jsii.Number]:
        '''``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-provisionedthroughputinmibps
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedThroughputInMibps"))

    @provisioned_throughput_in_mibps.setter
    def provisioned_throughput_in_mibps(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "provisionedThroughputInMibps", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="throughputMode")
    def throughput_mode(self) -> typing.Optional[builtins.str]:
        '''``AWS::EFS::FileSystem.ThroughputMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-throughputmode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "throughputMode"))

    @throughput_mode.setter
    def throughput_mode(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "throughputMode", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnFileSystem.BackupPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class BackupPolicyProperty:
        def __init__(self, *, status: builtins.str) -> None:
            '''
            :param status: ``CfnFileSystem.BackupPolicyProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-backuppolicy.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "status": status,
            }

        @builtins.property
        def status(self) -> builtins.str:
            '''``CfnFileSystem.BackupPolicyProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-backuppolicy.html#cfn-efs-filesystem-backuppolicy-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackupPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnFileSystem.ElasticFileSystemTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ElasticFileSystemTagProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: ``CfnFileSystem.ElasticFileSystemTagProperty.Key``.
            :param value: ``CfnFileSystem.ElasticFileSystemTagProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-elasticfilesystemtag.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnFileSystem.ElasticFileSystemTagProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-elasticfilesystemtag.html#cfn-efs-filesystem-elasticfilesystemtag-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnFileSystem.ElasticFileSystemTagProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-elasticfilesystemtag.html#cfn-efs-filesystem-elasticfilesystemtag-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticFileSystemTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_efs.CfnFileSystem.LifecyclePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"transition_to_ia": "transitionToIa"},
    )
    class LifecyclePolicyProperty:
        def __init__(self, *, transition_to_ia: builtins.str) -> None:
            '''
            :param transition_to_ia: ``CfnFileSystem.LifecyclePolicyProperty.TransitionToIA``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-lifecyclepolicy.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "transition_to_ia": transition_to_ia,
            }

        @builtins.property
        def transition_to_ia(self) -> builtins.str:
            '''``CfnFileSystem.LifecyclePolicyProperty.TransitionToIA``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-lifecyclepolicy.html#cfn-efs-filesystem-lifecyclepolicy-transitiontoia
            '''
            result = self._values.get("transition_to_ia")
            assert result is not None, "Required property 'transition_to_ia' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecyclePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.CfnFileSystemProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_policy": "backupPolicy",
        "encrypted": "encrypted",
        "file_system_policy": "fileSystemPolicy",
        "file_system_tags": "fileSystemTags",
        "kms_key_id": "kmsKeyId",
        "lifecycle_policies": "lifecyclePolicies",
        "performance_mode": "performanceMode",
        "provisioned_throughput_in_mibps": "provisionedThroughputInMibps",
        "throughput_mode": "throughputMode",
    },
)
class CfnFileSystemProps:
    def __init__(
        self,
        *,
        backup_policy: typing.Optional[typing.Union[CfnFileSystem.BackupPolicyProperty, _IResolvable_a771d0ef]] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        file_system_policy: typing.Any = None,
        file_system_tags: typing.Optional[typing.List[CfnFileSystem.ElasticFileSystemTagProperty]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        lifecycle_policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFileSystem.LifecyclePolicyProperty, _IResolvable_a771d0ef]]]] = None,
        performance_mode: typing.Optional[builtins.str] = None,
        provisioned_throughput_in_mibps: typing.Optional[jsii.Number] = None,
        throughput_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::EFS::FileSystem``.

        :param backup_policy: ``AWS::EFS::FileSystem.BackupPolicy``.
        :param encrypted: ``AWS::EFS::FileSystem.Encrypted``.
        :param file_system_policy: ``AWS::EFS::FileSystem.FileSystemPolicy``.
        :param file_system_tags: ``AWS::EFS::FileSystem.FileSystemTags``.
        :param kms_key_id: ``AWS::EFS::FileSystem.KmsKeyId``.
        :param lifecycle_policies: ``AWS::EFS::FileSystem.LifecyclePolicies``.
        :param performance_mode: ``AWS::EFS::FileSystem.PerformanceMode``.
        :param provisioned_throughput_in_mibps: ``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.
        :param throughput_mode: ``AWS::EFS::FileSystem.ThroughputMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if backup_policy is not None:
            self._values["backup_policy"] = backup_policy
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if file_system_policy is not None:
            self._values["file_system_policy"] = file_system_policy
        if file_system_tags is not None:
            self._values["file_system_tags"] = file_system_tags
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if lifecycle_policies is not None:
            self._values["lifecycle_policies"] = lifecycle_policies
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if provisioned_throughput_in_mibps is not None:
            self._values["provisioned_throughput_in_mibps"] = provisioned_throughput_in_mibps
        if throughput_mode is not None:
            self._values["throughput_mode"] = throughput_mode

    @builtins.property
    def backup_policy(
        self,
    ) -> typing.Optional[typing.Union[CfnFileSystem.BackupPolicyProperty, _IResolvable_a771d0ef]]:
        '''``AWS::EFS::FileSystem.BackupPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-backuppolicy
        '''
        result = self._values.get("backup_policy")
        return typing.cast(typing.Optional[typing.Union[CfnFileSystem.BackupPolicyProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::EFS::FileSystem.Encrypted``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-encrypted
        '''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def file_system_policy(self) -> typing.Any:
        '''``AWS::EFS::FileSystem.FileSystemPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystempolicy
        '''
        result = self._values.get("file_system_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def file_system_tags(
        self,
    ) -> typing.Optional[typing.List[CfnFileSystem.ElasticFileSystemTagProperty]]:
        '''``AWS::EFS::FileSystem.FileSystemTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystemtags
        '''
        result = self._values.get("file_system_tags")
        return typing.cast(typing.Optional[typing.List[CfnFileSystem.ElasticFileSystemTagProperty]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::EFS::FileSystem.KmsKeyId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_policies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFileSystem.LifecyclePolicyProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::EFS::FileSystem.LifecyclePolicies``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-lifecyclepolicies
        '''
        result = self._values.get("lifecycle_policies")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFileSystem.LifecyclePolicyProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def performance_mode(self) -> typing.Optional[builtins.str]:
        '''``AWS::EFS::FileSystem.PerformanceMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-performancemode
        '''
        result = self._values.get("performance_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_throughput_in_mibps(self) -> typing.Optional[jsii.Number]:
        '''``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-provisionedthroughputinmibps
        '''
        result = self._values.get("provisioned_throughput_in_mibps")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput_mode(self) -> typing.Optional[builtins.str]:
        '''``AWS::EFS::FileSystem.ThroughputMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-throughputmode
        '''
        result = self._values.get("throughput_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFileSystemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnMountTarget(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_efs.CfnMountTarget",
):
    '''A CloudFormation ``AWS::EFS::MountTarget``.

    :cloudformationResource: AWS::EFS::MountTarget
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        file_system_id: builtins.str,
        security_groups: typing.List[builtins.str],
        subnet_id: builtins.str,
        ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::EFS::MountTarget``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param file_system_id: ``AWS::EFS::MountTarget.FileSystemId``.
        :param security_groups: ``AWS::EFS::MountTarget.SecurityGroups``.
        :param subnet_id: ``AWS::EFS::MountTarget.SubnetId``.
        :param ip_address: ``AWS::EFS::MountTarget.IpAddress``.
        '''
        props = CfnMountTargetProps(
            file_system_id=file_system_id,
            security_groups=security_groups,
            subnet_id=subnet_id,
            ip_address=ip_address,
        )

        jsii.create(CfnMountTarget, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrIpAddress")
    def attr_ip_address(self) -> builtins.str:
        '''
        :cloudformationAttribute: IpAddress
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrIpAddress"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        '''``AWS::EFS::MountTarget.FileSystemId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-filesystemid
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @file_system_id.setter
    def file_system_id(self, value: builtins.str) -> None:
        jsii.set(self, "fileSystemId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        '''``AWS::EFS::MountTarget.SecurityGroups``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-securitygroups
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "securityGroups", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        '''``AWS::EFS::MountTarget.SubnetId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-subnetid
        '''
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        jsii.set(self, "subnetId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''``AWS::EFS::MountTarget.IpAddress``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-ipaddress
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ipAddress", value)


@jsii.data_type(
    jsii_type="monocdk.aws_efs.CfnMountTargetProps",
    jsii_struct_bases=[],
    name_mapping={
        "file_system_id": "fileSystemId",
        "security_groups": "securityGroups",
        "subnet_id": "subnetId",
        "ip_address": "ipAddress",
    },
)
class CfnMountTargetProps:
    def __init__(
        self,
        *,
        file_system_id: builtins.str,
        security_groups: typing.List[builtins.str],
        subnet_id: builtins.str,
        ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::EFS::MountTarget``.

        :param file_system_id: ``AWS::EFS::MountTarget.FileSystemId``.
        :param security_groups: ``AWS::EFS::MountTarget.SecurityGroups``.
        :param subnet_id: ``AWS::EFS::MountTarget.SubnetId``.
        :param ip_address: ``AWS::EFS::MountTarget.IpAddress``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "file_system_id": file_system_id,
            "security_groups": security_groups,
            "subnet_id": subnet_id,
        }
        if ip_address is not None:
            self._values["ip_address"] = ip_address

    @builtins.property
    def file_system_id(self) -> builtins.str:
        '''``AWS::EFS::MountTarget.FileSystemId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-filesystemid
        '''
        result = self._values.get("file_system_id")
        assert result is not None, "Required property 'file_system_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_groups(self) -> typing.List[builtins.str]:
        '''``AWS::EFS::MountTarget.SecurityGroups``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-securitygroups
        '''
        result = self._values.get("security_groups")
        assert result is not None, "Required property 'security_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''``AWS::EFS::MountTarget.SubnetId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-subnetid
        '''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''``AWS::EFS::MountTarget.IpAddress``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-ipaddress
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMountTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.FileSystemAttributes",
    jsii_struct_bases=[],
    name_mapping={"file_system_id": "fileSystemId", "security_group": "securityGroup"},
)
class FileSystemAttributes:
    def __init__(
        self,
        *,
        file_system_id: builtins.str,
        security_group: _ISecurityGroup_cdbba9d3,
    ) -> None:
        '''(experimental) Properties that describe an existing EFS file system.

        :param file_system_id: (experimental) The File System's ID.
        :param security_group: (experimental) The security group of the file system.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "file_system_id": file_system_id,
            "security_group": security_group,
        }

    @builtins.property
    def file_system_id(self) -> builtins.str:
        '''(experimental) The File System's ID.

        :stability: experimental
        '''
        result = self._values.get("file_system_id")
        assert result is not None, "Required property 'file_system_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group(self) -> _ISecurityGroup_cdbba9d3:
        '''(experimental) The security group of the file system.

        :stability: experimental
        '''
        result = self._values.get("security_group")
        assert result is not None, "Required property 'security_group' is missing"
        return typing.cast(_ISecurityGroup_cdbba9d3, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileSystemAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_efs.FileSystemProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "enable_automatic_backups": "enableAutomaticBackups",
        "encrypted": "encrypted",
        "file_system_name": "fileSystemName",
        "kms_key": "kmsKey",
        "lifecycle_policy": "lifecyclePolicy",
        "performance_mode": "performanceMode",
        "provisioned_throughput_per_second": "provisionedThroughputPerSecond",
        "removal_policy": "removalPolicy",
        "security_group": "securityGroup",
        "throughput_mode": "throughputMode",
        "vpc_subnets": "vpcSubnets",
    },
)
class FileSystemProps:
    def __init__(
        self,
        *,
        vpc: _IVpc_6d1f76c4,
        enable_automatic_backups: typing.Optional[builtins.bool] = None,
        encrypted: typing.Optional[builtins.bool] = None,
        file_system_name: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
        lifecycle_policy: typing.Optional["LifecyclePolicy"] = None,
        performance_mode: typing.Optional["PerformanceMode"] = None,
        provisioned_throughput_per_second: typing.Optional[_Size_7fbd4337] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        throughput_mode: typing.Optional["ThroughputMode"] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        '''(experimental) Properties of EFS FileSystem.

        :param vpc: (experimental) VPC to launch the file system in.
        :param enable_automatic_backups: (experimental) Whether to enable automatic backups for the file system. Default: false
        :param encrypted: (experimental) Defines if the data at rest in the file system is encrypted or not. Default: false
        :param file_system_name: (experimental) The file system's name. Default: - CDK generated name
        :param kms_key: (experimental) The KMS key used for encryption. This is required to encrypt the data at rest if @encrypted is set to true. Default: - if 'encrypted' is true, the default key for EFS (/aws/elasticfilesystem) is used
        :param lifecycle_policy: (experimental) A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class. Default: - None. EFS will not transition files to the IA storage class.
        :param performance_mode: (experimental) The performance mode that the file system will operate under. An Amazon EFS file system's performance mode can't be changed after the file system has been created. Updating this property will replace the file system. Default: PerformanceMode.GENERAL_PURPOSE
        :param provisioned_throughput_per_second: (experimental) Provisioned throughput for the file system. This is a required property if the throughput mode is set to PROVISIONED. Must be at least 1MiB/s. Default: - none, errors out
        :param removal_policy: (experimental) The removal policy to apply to the file system. Default: RemovalPolicy.RETAIN
        :param security_group: (experimental) Security Group to assign to this file system. Default: - creates new security group which allows all outbound traffic
        :param throughput_mode: (experimental) Enum to mention the throughput mode of the file system. Default: ThroughputMode.BURSTING
        :param vpc_subnets: (experimental) Which subnets to place the mount target in the VPC. Default: - the Vpc default strategy if not specified

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if enable_automatic_backups is not None:
            self._values["enable_automatic_backups"] = enable_automatic_backups
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if file_system_name is not None:
            self._values["file_system_name"] = file_system_name
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if lifecycle_policy is not None:
            self._values["lifecycle_policy"] = lifecycle_policy
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if provisioned_throughput_per_second is not None:
            self._values["provisioned_throughput_per_second"] = provisioned_throughput_per_second
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_group is not None:
            self._values["security_group"] = security_group
        if throughput_mode is not None:
            self._values["throughput_mode"] = throughput_mode
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _IVpc_6d1f76c4:
        '''(experimental) VPC to launch the file system in.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_IVpc_6d1f76c4, result)

    @builtins.property
    def enable_automatic_backups(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable automatic backups for the file system.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_automatic_backups")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encrypted(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Defines if the data at rest in the file system is encrypted or not.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def file_system_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The file system's name.

        :default: - CDK generated name

        :stability: experimental
        '''
        result = self._values.get("file_system_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The KMS key used for encryption.

        This is required to encrypt the data at rest if @encrypted is set to true.

        :default: - if 'encrypted' is true, the default key for EFS (/aws/elasticfilesystem) is used

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def lifecycle_policy(self) -> typing.Optional["LifecyclePolicy"]:
        '''(experimental) A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class.

        :default: - None. EFS will not transition files to the IA storage class.

        :stability: experimental
        '''
        result = self._values.get("lifecycle_policy")
        return typing.cast(typing.Optional["LifecyclePolicy"], result)

    @builtins.property
    def performance_mode(self) -> typing.Optional["PerformanceMode"]:
        '''(experimental) The performance mode that the file system will operate under.

        An Amazon EFS file system's performance mode can't be changed after the file system has been created.
        Updating this property will replace the file system.

        :default: PerformanceMode.GENERAL_PURPOSE

        :stability: experimental
        '''
        result = self._values.get("performance_mode")
        return typing.cast(typing.Optional["PerformanceMode"], result)

    @builtins.property
    def provisioned_throughput_per_second(self) -> typing.Optional[_Size_7fbd4337]:
        '''(experimental) Provisioned throughput for the file system.

        This is a required property if the throughput mode is set to PROVISIONED.
        Must be at least 1MiB/s.

        :default: - none, errors out

        :stability: experimental
        '''
        result = self._values.get("provisioned_throughput_per_second")
        return typing.cast(typing.Optional[_Size_7fbd4337], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) The removal policy to apply to the file system.

        :default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_cdbba9d3]:
        '''(experimental) Security Group to assign to this file system.

        :default: - creates new security group which allows all outbound traffic

        :stability: experimental
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_ISecurityGroup_cdbba9d3], result)

    @builtins.property
    def throughput_mode(self) -> typing.Optional["ThroughputMode"]:
        '''(experimental) Enum to mention the throughput mode of the file system.

        :default: ThroughputMode.BURSTING

        :stability: experimental
        '''
        result = self._values.get("throughput_mode")
        return typing.cast(typing.Optional["ThroughputMode"], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to place the mount target in the VPC.

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
        return "FileSystemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_efs.IAccessPoint")
class IAccessPoint(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents an EFS AccessPoint.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IAccessPointProxy"]:
        return _IAccessPointProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> builtins.str:
        '''(experimental) The ARN of the AccessPoint.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessPointId")
    def access_point_id(self) -> builtins.str:
        '''(experimental) The ID of the AccessPoint.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> "IFileSystem":
        '''(experimental) The EFS file system.

        :stability: experimental
        '''
        ...


class _IAccessPointProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) Represents an EFS AccessPoint.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_efs.IAccessPoint"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> builtins.str:
        '''(experimental) The ARN of the AccessPoint.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessPointId")
    def access_point_id(self) -> builtins.str:
        '''(experimental) The ID of the AccessPoint.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> "IFileSystem":
        '''(experimental) The EFS file system.

        :stability: experimental
        '''
        return typing.cast("IFileSystem", jsii.get(self, "fileSystem"))


@jsii.interface(jsii_type="monocdk.aws_efs.IFileSystem")
class IFileSystem(
    _IConnectable_c1c0e72c,
    _IResource_8c1dbbbd,
    typing_extensions.Protocol,
):
    '''(experimental) Represents an Amazon EFS file system.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IFileSystemProxy"]:
        return _IFileSystemProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        '''(experimental) The ID of the file system, assigned by Amazon EFS.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mountTargetsAvailable")
    def mount_targets_available(self) -> _IDependable_1175c9f7:
        '''(experimental) Dependable that can be depended upon to ensure the mount targets of the filesystem are ready.

        :stability: experimental
        '''
        ...


class _IFileSystemProxy(
    jsii.proxy_for(_IConnectable_c1c0e72c), # type: ignore[misc]
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Represents an Amazon EFS file system.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_efs.IFileSystem"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        '''(experimental) The ID of the file system, assigned by Amazon EFS.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mountTargetsAvailable")
    def mount_targets_available(self) -> _IDependable_1175c9f7:
        '''(experimental) Dependable that can be depended upon to ensure the mount targets of the filesystem are ready.

        :stability: experimental
        '''
        return typing.cast(_IDependable_1175c9f7, jsii.get(self, "mountTargetsAvailable"))


@jsii.enum(jsii_type="monocdk.aws_efs.LifecyclePolicy")
class LifecyclePolicy(enum.Enum):
    '''(experimental) EFS Lifecycle Policy, if a file is not accessed for given days, it will move to EFS Infrequent Access.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-lifecyclepolicies
    :stability: experimental
    '''

    AFTER_7_DAYS = "AFTER_7_DAYS"
    '''(experimental) After 7 days of not being accessed.

    :stability: experimental
    '''
    AFTER_14_DAYS = "AFTER_14_DAYS"
    '''(experimental) After 14 days of not being accessed.

    :stability: experimental
    '''
    AFTER_30_DAYS = "AFTER_30_DAYS"
    '''(experimental) After 30 days of not being accessed.

    :stability: experimental
    '''
    AFTER_60_DAYS = "AFTER_60_DAYS"
    '''(experimental) After 60 days of not being accessed.

    :stability: experimental
    '''
    AFTER_90_DAYS = "AFTER_90_DAYS"
    '''(experimental) After 90 days of not being accessed.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_efs.PerformanceMode")
class PerformanceMode(enum.Enum):
    '''(experimental) EFS Performance mode.

    :see: https://docs.aws.amazon.com/efs/latest/ug/performance.html#performancemodes
    :stability: experimental
    '''

    GENERAL_PURPOSE = "GENERAL_PURPOSE"
    '''(experimental) General Purpose is ideal for latency-sensitive use cases, like web serving environments, content management systems, home directories, and general file serving.

    Recommended for the majority of Amazon EFS file systems.

    :stability: experimental
    '''
    MAX_IO = "MAX_IO"
    '''(experimental) File systems in the Max I/O mode can scale to higher levels of aggregate throughput and operations per second.

    This scaling is done with a tradeoff
    of slightly higher latencies for file metadata operations.
    Highly parallelized applications and workloads, such as big data analysis,
    media processing, and genomics analysis, can benefit from this mode.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_efs.PosixUser",
    jsii_struct_bases=[],
    name_mapping={"gid": "gid", "uid": "uid", "secondary_gids": "secondaryGids"},
)
class PosixUser:
    def __init__(
        self,
        *,
        gid: builtins.str,
        uid: builtins.str,
        secondary_gids: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''(experimental) Represents the PosixUser.

        :param gid: (experimental) The POSIX group ID used for all file system operations using this access point.
        :param uid: (experimental) The POSIX user ID used for all file system operations using this access point.
        :param secondary_gids: (experimental) Secondary POSIX group IDs used for all file system operations using this access point. Default: - None

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "gid": gid,
            "uid": uid,
        }
        if secondary_gids is not None:
            self._values["secondary_gids"] = secondary_gids

    @builtins.property
    def gid(self) -> builtins.str:
        '''(experimental) The POSIX group ID used for all file system operations using this access point.

        :stability: experimental
        '''
        result = self._values.get("gid")
        assert result is not None, "Required property 'gid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uid(self) -> builtins.str:
        '''(experimental) The POSIX user ID used for all file system operations using this access point.

        :stability: experimental
        '''
        result = self._values.get("uid")
        assert result is not None, "Required property 'uid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secondary_gids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Secondary POSIX group IDs used for all file system operations using this access point.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("secondary_gids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PosixUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_efs.ThroughputMode")
class ThroughputMode(enum.Enum):
    '''(experimental) EFS Throughput mode.

    :see: https://docs.aws.amazon.com/efs/latest/ug/performance.html#throughput-modes
    :stability: experimental
    '''

    BURSTING = "BURSTING"
    '''(experimental) This mode on Amazon EFS scales as the size of the file system in the standard storage class grows.

    :stability: experimental
    '''
    PROVISIONED = "PROVISIONED"
    '''(experimental) This mode can instantly provision the throughput of the file system (in MiB/s) independent of the amount of data stored.

    :stability: experimental
    '''


@jsii.implements(IAccessPoint)
class AccessPoint(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_efs.AccessPoint",
):
    '''(experimental) Represents the AccessPoint.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        file_system: IFileSystem,
        create_acl: typing.Optional[Acl] = None,
        path: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional[PosixUser] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param file_system: (experimental) The efs filesystem.
        :param create_acl: (experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: (experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: (experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced

        :stability: experimental
        '''
        props = AccessPointProps(
            file_system=file_system,
            create_acl=create_acl,
            path=path,
            posix_user=posix_user,
        )

        jsii.create(AccessPoint, self, [scope, id, props])

    @jsii.member(jsii_name="fromAccessPointAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_access_point_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        access_point_arn: typing.Optional[builtins.str] = None,
        access_point_id: typing.Optional[builtins.str] = None,
        file_system: typing.Optional[IFileSystem] = None,
    ) -> IAccessPoint:
        '''(experimental) Import an existing Access Point by attributes.

        :param scope: -
        :param id: -
        :param access_point_arn: (experimental) The ARN of the AccessPoint One of this, or {@link accessPointId} is required. Default: - determined based on accessPointId
        :param access_point_id: (experimental) The ID of the AccessPoint One of this, or {@link accessPointArn} is required. Default: - determined based on accessPointArn
        :param file_system: (experimental) The EFS file system. Default: - no EFS file system

        :stability: experimental
        '''
        attrs = AccessPointAttributes(
            access_point_arn=access_point_arn,
            access_point_id=access_point_id,
            file_system=file_system,
        )

        return typing.cast(IAccessPoint, jsii.sinvoke(cls, "fromAccessPointAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromAccessPointId") # type: ignore[misc]
    @builtins.classmethod
    def from_access_point_id(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        access_point_id: builtins.str,
    ) -> IAccessPoint:
        '''(experimental) Import an existing Access Point by id.

        :param scope: -
        :param id: -
        :param access_point_id: -

        :stability: experimental
        '''
        return typing.cast(IAccessPoint, jsii.sinvoke(cls, "fromAccessPointId", [scope, id, access_point_id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Access Point.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessPointId")
    def access_point_id(self) -> builtins.str:
        '''(experimental) The ID of the Access Point.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> IFileSystem:
        '''(experimental) The file system of the access point.

        :stability: experimental
        '''
        return typing.cast(IFileSystem, jsii.get(self, "fileSystem"))


@jsii.implements(IFileSystem)
class FileSystem(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_efs.FileSystem",
):
    '''(experimental) The Elastic File System implementation of IFileSystem.

    It creates a new, empty file system in Amazon Elastic File System (Amazon EFS).
    It also creates mount target (AWS::EFS::MountTarget) implicitly to mount the
    EFS file system on an Amazon Elastic Compute Cloud (Amazon EC2) instance or another resource.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
    :stability: experimental
    :resource: AWS::EFS::FileSystem
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        vpc: _IVpc_6d1f76c4,
        enable_automatic_backups: typing.Optional[builtins.bool] = None,
        encrypted: typing.Optional[builtins.bool] = None,
        file_system_name: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
        lifecycle_policy: typing.Optional[LifecyclePolicy] = None,
        performance_mode: typing.Optional[PerformanceMode] = None,
        provisioned_throughput_per_second: typing.Optional[_Size_7fbd4337] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        throughput_mode: typing.Optional[ThroughputMode] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        '''(experimental) Constructor for creating a new EFS FileSystem.

        :param scope: -
        :param id: -
        :param vpc: (experimental) VPC to launch the file system in.
        :param enable_automatic_backups: (experimental) Whether to enable automatic backups for the file system. Default: false
        :param encrypted: (experimental) Defines if the data at rest in the file system is encrypted or not. Default: false
        :param file_system_name: (experimental) The file system's name. Default: - CDK generated name
        :param kms_key: (experimental) The KMS key used for encryption. This is required to encrypt the data at rest if @encrypted is set to true. Default: - if 'encrypted' is true, the default key for EFS (/aws/elasticfilesystem) is used
        :param lifecycle_policy: (experimental) A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class. Default: - None. EFS will not transition files to the IA storage class.
        :param performance_mode: (experimental) The performance mode that the file system will operate under. An Amazon EFS file system's performance mode can't be changed after the file system has been created. Updating this property will replace the file system. Default: PerformanceMode.GENERAL_PURPOSE
        :param provisioned_throughput_per_second: (experimental) Provisioned throughput for the file system. This is a required property if the throughput mode is set to PROVISIONED. Must be at least 1MiB/s. Default: - none, errors out
        :param removal_policy: (experimental) The removal policy to apply to the file system. Default: RemovalPolicy.RETAIN
        :param security_group: (experimental) Security Group to assign to this file system. Default: - creates new security group which allows all outbound traffic
        :param throughput_mode: (experimental) Enum to mention the throughput mode of the file system. Default: ThroughputMode.BURSTING
        :param vpc_subnets: (experimental) Which subnets to place the mount target in the VPC. Default: - the Vpc default strategy if not specified

        :stability: experimental
        '''
        props = FileSystemProps(
            vpc=vpc,
            enable_automatic_backups=enable_automatic_backups,
            encrypted=encrypted,
            file_system_name=file_system_name,
            kms_key=kms_key,
            lifecycle_policy=lifecycle_policy,
            performance_mode=performance_mode,
            provisioned_throughput_per_second=provisioned_throughput_per_second,
            removal_policy=removal_policy,
            security_group=security_group,
            throughput_mode=throughput_mode,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(FileSystem, self, [scope, id, props])

    @jsii.member(jsii_name="fromFileSystemAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_file_system_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        file_system_id: builtins.str,
        security_group: _ISecurityGroup_cdbba9d3,
    ) -> IFileSystem:
        '''(experimental) Import an existing File System from the given properties.

        :param scope: -
        :param id: -
        :param file_system_id: (experimental) The File System's ID.
        :param security_group: (experimental) The security group of the file system.

        :stability: experimental
        '''
        attrs = FileSystemAttributes(
            file_system_id=file_system_id, security_group=security_group
        )

        return typing.cast(IFileSystem, jsii.sinvoke(cls, "fromFileSystemAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addAccessPoint")
    def add_access_point(
        self,
        id: builtins.str,
        *,
        create_acl: typing.Optional[Acl] = None,
        path: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional[PosixUser] = None,
    ) -> AccessPoint:
        '''(experimental) create access point from this filesystem.

        :param id: -
        :param create_acl: (experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: (experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: (experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced

        :stability: experimental
        '''
        access_point_options = AccessPointOptions(
            create_acl=create_acl, path=path, posix_user=posix_user
        )

        return typing.cast(AccessPoint, jsii.invoke(self, "addAccessPoint", [id, access_point_options]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="DEFAULT_PORT")
    def DEFAULT_PORT(cls) -> jsii.Number:
        '''(experimental) The default port File System listens on.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_PORT"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_57ccbda9:
        '''(experimental) The security groups/rules used to allow network connections to the file system.

        :stability: experimental
        '''
        return typing.cast(_Connections_57ccbda9, jsii.get(self, "connections"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        '''(experimental) The ID of the file system, assigned by Amazon EFS.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mountTargetsAvailable")
    def mount_targets_available(self) -> _IDependable_1175c9f7:
        '''(experimental) Dependable that can be depended upon to ensure the mount targets of the filesystem are ready.

        :stability: experimental
        '''
        return typing.cast(_IDependable_1175c9f7, jsii.get(self, "mountTargetsAvailable"))


__all__ = [
    "AccessPoint",
    "AccessPointAttributes",
    "AccessPointOptions",
    "AccessPointProps",
    "Acl",
    "CfnAccessPoint",
    "CfnAccessPointProps",
    "CfnFileSystem",
    "CfnFileSystemProps",
    "CfnMountTarget",
    "CfnMountTargetProps",
    "FileSystem",
    "FileSystemAttributes",
    "FileSystemProps",
    "IAccessPoint",
    "IFileSystem",
    "LifecyclePolicy",
    "PerformanceMode",
    "PosixUser",
    "ThroughputMode",
]

publication.publish()
