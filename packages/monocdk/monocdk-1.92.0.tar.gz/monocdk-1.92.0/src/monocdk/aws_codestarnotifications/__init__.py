import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnNotificationRule(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codestarnotifications.CfnNotificationRule",
):
    '''A CloudFormation ``AWS::CodeStarNotifications::NotificationRule``.

    :cloudformationResource: AWS::CodeStarNotifications::NotificationRule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        detail_type: builtins.str,
        event_type_ids: typing.List[builtins.str],
        name: builtins.str,
        resource: builtins.str,
        targets: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnNotificationRule.TargetProperty", _IResolvable_a771d0ef]]],
        status: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::CodeStarNotifications::NotificationRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param detail_type: ``AWS::CodeStarNotifications::NotificationRule.DetailType``.
        :param event_type_ids: ``AWS::CodeStarNotifications::NotificationRule.EventTypeIds``.
        :param name: ``AWS::CodeStarNotifications::NotificationRule.Name``.
        :param resource: ``AWS::CodeStarNotifications::NotificationRule.Resource``.
        :param targets: ``AWS::CodeStarNotifications::NotificationRule.Targets``.
        :param status: ``AWS::CodeStarNotifications::NotificationRule.Status``.
        :param tags: ``AWS::CodeStarNotifications::NotificationRule.Tags``.
        '''
        props = CfnNotificationRuleProps(
            detail_type=detail_type,
            event_type_ids=event_type_ids,
            name=name,
            resource=resource,
            targets=targets,
            status=status,
            tags=tags,
        )

        jsii.create(CfnNotificationRule, self, [scope, id, props])

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::CodeStarNotifications::NotificationRule.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="detailType")
    def detail_type(self) -> builtins.str:
        '''``AWS::CodeStarNotifications::NotificationRule.DetailType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-detailtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "detailType"))

    @detail_type.setter
    def detail_type(self, value: builtins.str) -> None:
        jsii.set(self, "detailType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="eventTypeIds")
    def event_type_ids(self) -> typing.List[builtins.str]:
        '''``AWS::CodeStarNotifications::NotificationRule.EventTypeIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-eventtypeids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eventTypeIds"))

    @event_type_ids.setter
    def event_type_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "eventTypeIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::CodeStarNotifications::NotificationRule.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        '''``AWS::CodeStarNotifications::NotificationRule.Resource``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-resource
        '''
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        jsii.set(self, "resource", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnNotificationRule.TargetProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::CodeStarNotifications::NotificationRule.Targets``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-targets
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnNotificationRule.TargetProperty", _IResolvable_a771d0ef]]], jsii.get(self, "targets"))

    @targets.setter
    def targets(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnNotificationRule.TargetProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "targets", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeStarNotifications::NotificationRule.Status``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "status", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_codestarnotifications.CfnNotificationRule.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={"target_address": "targetAddress", "target_type": "targetType"},
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            target_address: typing.Optional[builtins.str] = None,
            target_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param target_address: ``CfnNotificationRule.TargetProperty.TargetAddress``.
            :param target_type: ``CfnNotificationRule.TargetProperty.TargetType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestarnotifications-notificationrule-target.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if target_address is not None:
                self._values["target_address"] = target_address
            if target_type is not None:
                self._values["target_type"] = target_type

        @builtins.property
        def target_address(self) -> typing.Optional[builtins.str]:
            '''``CfnNotificationRule.TargetProperty.TargetAddress``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestarnotifications-notificationrule-target.html#cfn-codestarnotifications-notificationrule-target-targetaddress
            '''
            result = self._values.get("target_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_type(self) -> typing.Optional[builtins.str]:
            '''``CfnNotificationRule.TargetProperty.TargetType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestarnotifications-notificationrule-target.html#cfn-codestarnotifications-notificationrule-target-targettype
            '''
            result = self._values.get("target_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_codestarnotifications.CfnNotificationRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "detail_type": "detailType",
        "event_type_ids": "eventTypeIds",
        "name": "name",
        "resource": "resource",
        "targets": "targets",
        "status": "status",
        "tags": "tags",
    },
)
class CfnNotificationRuleProps:
    def __init__(
        self,
        *,
        detail_type: builtins.str,
        event_type_ids: typing.List[builtins.str],
        name: builtins.str,
        resource: builtins.str,
        targets: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnNotificationRule.TargetProperty, _IResolvable_a771d0ef]]],
        status: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``AWS::CodeStarNotifications::NotificationRule``.

        :param detail_type: ``AWS::CodeStarNotifications::NotificationRule.DetailType``.
        :param event_type_ids: ``AWS::CodeStarNotifications::NotificationRule.EventTypeIds``.
        :param name: ``AWS::CodeStarNotifications::NotificationRule.Name``.
        :param resource: ``AWS::CodeStarNotifications::NotificationRule.Resource``.
        :param targets: ``AWS::CodeStarNotifications::NotificationRule.Targets``.
        :param status: ``AWS::CodeStarNotifications::NotificationRule.Status``.
        :param tags: ``AWS::CodeStarNotifications::NotificationRule.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "detail_type": detail_type,
            "event_type_ids": event_type_ids,
            "name": name,
            "resource": resource,
            "targets": targets,
        }
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def detail_type(self) -> builtins.str:
        '''``AWS::CodeStarNotifications::NotificationRule.DetailType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-detailtype
        '''
        result = self._values.get("detail_type")
        assert result is not None, "Required property 'detail_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_type_ids(self) -> typing.List[builtins.str]:
        '''``AWS::CodeStarNotifications::NotificationRule.EventTypeIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-eventtypeids
        '''
        result = self._values.get("event_type_ids")
        assert result is not None, "Required property 'event_type_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::CodeStarNotifications::NotificationRule.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource(self) -> builtins.str:
        '''``AWS::CodeStarNotifications::NotificationRule.Resource``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-resource
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnNotificationRule.TargetProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::CodeStarNotifications::NotificationRule.Targets``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-targets
        '''
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnNotificationRule.TargetProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeStarNotifications::NotificationRule.Status``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''``AWS::CodeStarNotifications::NotificationRule.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNotificationRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnNotificationRule",
    "CfnNotificationRuleProps",
]

publication.publish()
