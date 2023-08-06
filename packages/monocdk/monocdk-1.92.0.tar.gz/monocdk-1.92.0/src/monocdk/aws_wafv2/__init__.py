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
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnIPSet(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_wafv2.CfnIPSet",
):
    '''A CloudFormation ``AWS::WAFv2::IPSet``.

    :cloudformationResource: AWS::WAFv2::IPSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html
    '''

    def __init__(
        self,
        scope_: _Construct_e78e779f,
        id: builtins.str,
        *,
        addresses: typing.List[builtins.str],
        ip_address_version: builtins.str,
        scope: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFv2::IPSet``.

        :param scope_: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param addresses: ``AWS::WAFv2::IPSet.Addresses``.
        :param ip_address_version: ``AWS::WAFv2::IPSet.IPAddressVersion``.
        :param scope: ``AWS::WAFv2::IPSet.Scope``.
        :param description: ``AWS::WAFv2::IPSet.Description``.
        :param name: ``AWS::WAFv2::IPSet.Name``.
        :param tags: ``AWS::WAFv2::IPSet.Tags``.
        '''
        props = CfnIPSetProps(
            addresses=addresses,
            ip_address_version=ip_address_version,
            scope=scope,
            description=description,
            name=name,
            tags=tags,
        )

        jsii.create(CfnIPSet, self, [scope_, id, props])

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
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::WAFv2::IPSet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html#cfn-wafv2-ipset-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="addresses")
    def addresses(self) -> typing.List[builtins.str]:
        '''``AWS::WAFv2::IPSet.Addresses``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html#cfn-wafv2-ipset-addresses
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addresses"))

    @addresses.setter
    def addresses(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "addresses", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ipAddressVersion")
    def ip_address_version(self) -> builtins.str:
        '''``AWS::WAFv2::IPSet.IPAddressVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html#cfn-wafv2-ipset-ipaddressversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "ipAddressVersion"))

    @ip_address_version.setter
    def ip_address_version(self, value: builtins.str) -> None:
        jsii.set(self, "ipAddressVersion", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        '''``AWS::WAFv2::IPSet.Scope``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html#cfn-wafv2-ipset-scope
        '''
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        jsii.set(self, "scope", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::IPSet.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html#cfn-wafv2-ipset-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::IPSet.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html#cfn-wafv2-ipset-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_wafv2.CfnIPSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "addresses": "addresses",
        "ip_address_version": "ipAddressVersion",
        "scope": "scope",
        "description": "description",
        "name": "name",
        "tags": "tags",
    },
)
class CfnIPSetProps:
    def __init__(
        self,
        *,
        addresses: typing.List[builtins.str],
        ip_address_version: builtins.str,
        scope: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::WAFv2::IPSet``.

        :param addresses: ``AWS::WAFv2::IPSet.Addresses``.
        :param ip_address_version: ``AWS::WAFv2::IPSet.IPAddressVersion``.
        :param scope: ``AWS::WAFv2::IPSet.Scope``.
        :param description: ``AWS::WAFv2::IPSet.Description``.
        :param name: ``AWS::WAFv2::IPSet.Name``.
        :param tags: ``AWS::WAFv2::IPSet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "addresses": addresses,
            "ip_address_version": ip_address_version,
            "scope": scope,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def addresses(self) -> typing.List[builtins.str]:
        '''``AWS::WAFv2::IPSet.Addresses``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html#cfn-wafv2-ipset-addresses
        '''
        result = self._values.get("addresses")
        assert result is not None, "Required property 'addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ip_address_version(self) -> builtins.str:
        '''``AWS::WAFv2::IPSet.IPAddressVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html#cfn-wafv2-ipset-ipaddressversion
        '''
        result = self._values.get("ip_address_version")
        assert result is not None, "Required property 'ip_address_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''``AWS::WAFv2::IPSet.Scope``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html#cfn-wafv2-ipset-scope
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::IPSet.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html#cfn-wafv2-ipset-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::IPSet.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html#cfn-wafv2-ipset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::WAFv2::IPSet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-ipset.html#cfn-wafv2-ipset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIPSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRegexPatternSet(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_wafv2.CfnRegexPatternSet",
):
    '''A CloudFormation ``AWS::WAFv2::RegexPatternSet``.

    :cloudformationResource: AWS::WAFv2::RegexPatternSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-regexpatternset.html
    '''

    def __init__(
        self,
        scope_: _Construct_e78e779f,
        id: builtins.str,
        *,
        regular_expression_list: typing.List[builtins.str],
        scope: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFv2::RegexPatternSet``.

        :param scope_: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param regular_expression_list: ``AWS::WAFv2::RegexPatternSet.RegularExpressionList``.
        :param scope: ``AWS::WAFv2::RegexPatternSet.Scope``.
        :param description: ``AWS::WAFv2::RegexPatternSet.Description``.
        :param name: ``AWS::WAFv2::RegexPatternSet.Name``.
        :param tags: ``AWS::WAFv2::RegexPatternSet.Tags``.
        '''
        props = CfnRegexPatternSetProps(
            regular_expression_list=regular_expression_list,
            scope=scope,
            description=description,
            name=name,
            tags=tags,
        )

        jsii.create(CfnRegexPatternSet, self, [scope_, id, props])

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
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::WAFv2::RegexPatternSet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-regexpatternset.html#cfn-wafv2-regexpatternset-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="regularExpressionList")
    def regular_expression_list(self) -> typing.List[builtins.str]:
        '''``AWS::WAFv2::RegexPatternSet.RegularExpressionList``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-regexpatternset.html#cfn-wafv2-regexpatternset-regularexpressionlist
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "regularExpressionList"))

    @regular_expression_list.setter
    def regular_expression_list(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "regularExpressionList", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        '''``AWS::WAFv2::RegexPatternSet.Scope``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-regexpatternset.html#cfn-wafv2-regexpatternset-scope
        '''
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        jsii.set(self, "scope", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::RegexPatternSet.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-regexpatternset.html#cfn-wafv2-regexpatternset-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::RegexPatternSet.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-regexpatternset.html#cfn-wafv2-regexpatternset-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_wafv2.CfnRegexPatternSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "regular_expression_list": "regularExpressionList",
        "scope": "scope",
        "description": "description",
        "name": "name",
        "tags": "tags",
    },
)
class CfnRegexPatternSetProps:
    def __init__(
        self,
        *,
        regular_expression_list: typing.List[builtins.str],
        scope: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::WAFv2::RegexPatternSet``.

        :param regular_expression_list: ``AWS::WAFv2::RegexPatternSet.RegularExpressionList``.
        :param scope: ``AWS::WAFv2::RegexPatternSet.Scope``.
        :param description: ``AWS::WAFv2::RegexPatternSet.Description``.
        :param name: ``AWS::WAFv2::RegexPatternSet.Name``.
        :param tags: ``AWS::WAFv2::RegexPatternSet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-regexpatternset.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "regular_expression_list": regular_expression_list,
            "scope": scope,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def regular_expression_list(self) -> typing.List[builtins.str]:
        '''``AWS::WAFv2::RegexPatternSet.RegularExpressionList``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-regexpatternset.html#cfn-wafv2-regexpatternset-regularexpressionlist
        '''
        result = self._values.get("regular_expression_list")
        assert result is not None, "Required property 'regular_expression_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''``AWS::WAFv2::RegexPatternSet.Scope``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-regexpatternset.html#cfn-wafv2-regexpatternset-scope
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::RegexPatternSet.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-regexpatternset.html#cfn-wafv2-regexpatternset-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::RegexPatternSet.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-regexpatternset.html#cfn-wafv2-regexpatternset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::WAFv2::RegexPatternSet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-regexpatternset.html#cfn-wafv2-regexpatternset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRegexPatternSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRuleGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_wafv2.CfnRuleGroup",
):
    '''A CloudFormation ``AWS::WAFv2::RuleGroup``.

    :cloudformationResource: AWS::WAFv2::RuleGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html
    '''

    def __init__(
        self,
        scope_: _Construct_e78e779f,
        id: builtins.str,
        *,
        capacity: jsii.Number,
        scope: builtins.str,
        visibility_config: typing.Union["CfnRuleGroup.VisibilityConfigProperty", _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.RuleProperty", _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFv2::RuleGroup``.

        :param scope_: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param capacity: ``AWS::WAFv2::RuleGroup.Capacity``.
        :param scope: ``AWS::WAFv2::RuleGroup.Scope``.
        :param visibility_config: ``AWS::WAFv2::RuleGroup.VisibilityConfig``.
        :param description: ``AWS::WAFv2::RuleGroup.Description``.
        :param name: ``AWS::WAFv2::RuleGroup.Name``.
        :param rules: ``AWS::WAFv2::RuleGroup.Rules``.
        :param tags: ``AWS::WAFv2::RuleGroup.Tags``.
        '''
        props = CfnRuleGroupProps(
            capacity=capacity,
            scope=scope,
            visibility_config=visibility_config,
            description=description,
            name=name,
            rules=rules,
            tags=tags,
        )

        jsii.create(CfnRuleGroup, self, [scope_, id, props])

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
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::WAFv2::RuleGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        '''``AWS::WAFv2::RuleGroup.Capacity``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-capacity
        '''
        return typing.cast(jsii.Number, jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(self, value: jsii.Number) -> None:
        jsii.set(self, "capacity", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        '''``AWS::WAFv2::RuleGroup.Scope``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-scope
        '''
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        jsii.set(self, "scope", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="visibilityConfig")
    def visibility_config(
        self,
    ) -> typing.Union["CfnRuleGroup.VisibilityConfigProperty", _IResolvable_a771d0ef]:
        '''``AWS::WAFv2::RuleGroup.VisibilityConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-visibilityconfig
        '''
        return typing.cast(typing.Union["CfnRuleGroup.VisibilityConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "visibilityConfig"))

    @visibility_config.setter
    def visibility_config(
        self,
        value: typing.Union["CfnRuleGroup.VisibilityConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "visibilityConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::RuleGroup.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::RuleGroup.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rules")
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.RuleProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::WAFv2::RuleGroup.Rules``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-rules
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.RuleProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "rules"))

    @rules.setter
    def rules(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.RuleProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "rules", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.AndStatementOneProperty",
        jsii_struct_bases=[],
        name_mapping={"statements": "statements"},
    )
    class AndStatementOneProperty:
        def __init__(
            self,
            *,
            statements: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatementTwoProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param statements: ``CfnRuleGroup.AndStatementOneProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-andstatementone.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "statements": statements,
            }

        @builtins.property
        def statements(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatementTwoProperty", _IResolvable_a771d0ef]]]:
            '''``CfnRuleGroup.AndStatementOneProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-andstatementone.html#cfn-wafv2-rulegroup-andstatementone-statements
            '''
            result = self._values.get("statements")
            assert result is not None, "Required property 'statements' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatementTwoProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AndStatementOneProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.AndStatementTwoProperty",
        jsii_struct_bases=[],
        name_mapping={"statements": "statements"},
    )
    class AndStatementTwoProperty:
        def __init__(
            self,
            *,
            statements: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatementThreeProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param statements: ``CfnRuleGroup.AndStatementTwoProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-andstatementtwo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "statements": statements,
            }

        @builtins.property
        def statements(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatementThreeProperty", _IResolvable_a771d0ef]]]:
            '''``CfnRuleGroup.AndStatementTwoProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-andstatementtwo.html#cfn-wafv2-rulegroup-andstatementtwo-statements
            '''
            result = self._values.get("statements")
            assert result is not None, "Required property 'statements' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatementThreeProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AndStatementTwoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.ByteMatchStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_to_match": "fieldToMatch",
            "positional_constraint": "positionalConstraint",
            "text_transformations": "textTransformations",
            "search_string": "searchString",
            "search_string_base64": "searchStringBase64",
        },
    )
    class ByteMatchStatementProperty:
        def __init__(
            self,
            *,
            field_to_match: typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef],
            positional_constraint: builtins.str,
            text_transformations: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]],
            search_string: typing.Optional[builtins.str] = None,
            search_string_base64: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param field_to_match: ``CfnRuleGroup.ByteMatchStatementProperty.FieldToMatch``.
            :param positional_constraint: ``CfnRuleGroup.ByteMatchStatementProperty.PositionalConstraint``.
            :param text_transformations: ``CfnRuleGroup.ByteMatchStatementProperty.TextTransformations``.
            :param search_string: ``CfnRuleGroup.ByteMatchStatementProperty.SearchString``.
            :param search_string_base64: ``CfnRuleGroup.ByteMatchStatementProperty.SearchStringBase64``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-bytematchstatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "field_to_match": field_to_match,
                "positional_constraint": positional_constraint,
                "text_transformations": text_transformations,
            }
            if search_string is not None:
                self._values["search_string"] = search_string
            if search_string_base64 is not None:
                self._values["search_string_base64"] = search_string_base64

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef]:
            '''``CfnRuleGroup.ByteMatchStatementProperty.FieldToMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-bytematchstatement.html#cfn-wafv2-rulegroup-bytematchstatement-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def positional_constraint(self) -> builtins.str:
            '''``CfnRuleGroup.ByteMatchStatementProperty.PositionalConstraint``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-bytematchstatement.html#cfn-wafv2-rulegroup-bytematchstatement-positionalconstraint
            '''
            result = self._values.get("positional_constraint")
            assert result is not None, "Required property 'positional_constraint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def text_transformations(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]]:
            '''``CfnRuleGroup.ByteMatchStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-bytematchstatement.html#cfn-wafv2-rulegroup-bytematchstatement-texttransformations
            '''
            result = self._values.get("text_transformations")
            assert result is not None, "Required property 'text_transformations' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def search_string(self) -> typing.Optional[builtins.str]:
            '''``CfnRuleGroup.ByteMatchStatementProperty.SearchString``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-bytematchstatement.html#cfn-wafv2-rulegroup-bytematchstatement-searchstring
            '''
            result = self._values.get("search_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def search_string_base64(self) -> typing.Optional[builtins.str]:
            '''``CfnRuleGroup.ByteMatchStatementProperty.SearchStringBase64``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-bytematchstatement.html#cfn-wafv2-rulegroup-bytematchstatement-searchstringbase64
            '''
            result = self._values.get("search_string_base64")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ByteMatchStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.FieldToMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "all_query_arguments": "allQueryArguments",
            "body": "body",
            "method": "method",
            "query_string": "queryString",
            "single_header": "singleHeader",
            "single_query_argument": "singleQueryArgument",
            "uri_path": "uriPath",
        },
    )
    class FieldToMatchProperty:
        def __init__(
            self,
            *,
            all_query_arguments: typing.Any = None,
            body: typing.Any = None,
            method: typing.Any = None,
            query_string: typing.Any = None,
            single_header: typing.Any = None,
            single_query_argument: typing.Any = None,
            uri_path: typing.Any = None,
        ) -> None:
            '''
            :param all_query_arguments: ``CfnRuleGroup.FieldToMatchProperty.AllQueryArguments``.
            :param body: ``CfnRuleGroup.FieldToMatchProperty.Body``.
            :param method: ``CfnRuleGroup.FieldToMatchProperty.Method``.
            :param query_string: ``CfnRuleGroup.FieldToMatchProperty.QueryString``.
            :param single_header: ``CfnRuleGroup.FieldToMatchProperty.SingleHeader``.
            :param single_query_argument: ``CfnRuleGroup.FieldToMatchProperty.SingleQueryArgument``.
            :param uri_path: ``CfnRuleGroup.FieldToMatchProperty.UriPath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-fieldtomatch.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if all_query_arguments is not None:
                self._values["all_query_arguments"] = all_query_arguments
            if body is not None:
                self._values["body"] = body
            if method is not None:
                self._values["method"] = method
            if query_string is not None:
                self._values["query_string"] = query_string
            if single_header is not None:
                self._values["single_header"] = single_header
            if single_query_argument is not None:
                self._values["single_query_argument"] = single_query_argument
            if uri_path is not None:
                self._values["uri_path"] = uri_path

        @builtins.property
        def all_query_arguments(self) -> typing.Any:
            '''``CfnRuleGroup.FieldToMatchProperty.AllQueryArguments``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-fieldtomatch.html#cfn-wafv2-rulegroup-fieldtomatch-allqueryarguments
            '''
            result = self._values.get("all_query_arguments")
            return typing.cast(typing.Any, result)

        @builtins.property
        def body(self) -> typing.Any:
            '''``CfnRuleGroup.FieldToMatchProperty.Body``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-fieldtomatch.html#cfn-wafv2-rulegroup-fieldtomatch-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Any, result)

        @builtins.property
        def method(self) -> typing.Any:
            '''``CfnRuleGroup.FieldToMatchProperty.Method``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-fieldtomatch.html#cfn-wafv2-rulegroup-fieldtomatch-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Any, result)

        @builtins.property
        def query_string(self) -> typing.Any:
            '''``CfnRuleGroup.FieldToMatchProperty.QueryString``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-fieldtomatch.html#cfn-wafv2-rulegroup-fieldtomatch-querystring
            '''
            result = self._values.get("query_string")
            return typing.cast(typing.Any, result)

        @builtins.property
        def single_header(self) -> typing.Any:
            '''``CfnRuleGroup.FieldToMatchProperty.SingleHeader``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-fieldtomatch.html#cfn-wafv2-rulegroup-fieldtomatch-singleheader
            '''
            result = self._values.get("single_header")
            return typing.cast(typing.Any, result)

        @builtins.property
        def single_query_argument(self) -> typing.Any:
            '''``CfnRuleGroup.FieldToMatchProperty.SingleQueryArgument``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-fieldtomatch.html#cfn-wafv2-rulegroup-fieldtomatch-singlequeryargument
            '''
            result = self._values.get("single_query_argument")
            return typing.cast(typing.Any, result)

        @builtins.property
        def uri_path(self) -> typing.Any:
            '''``CfnRuleGroup.FieldToMatchProperty.UriPath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-fieldtomatch.html#cfn-wafv2-rulegroup-fieldtomatch-uripath
            '''
            result = self._values.get("uri_path")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldToMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.ForwardedIPConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "fallback_behavior": "fallbackBehavior",
            "header_name": "headerName",
        },
    )
    class ForwardedIPConfigurationProperty:
        def __init__(
            self,
            *,
            fallback_behavior: builtins.str,
            header_name: builtins.str,
        ) -> None:
            '''
            :param fallback_behavior: ``CfnRuleGroup.ForwardedIPConfigurationProperty.FallbackBehavior``.
            :param header_name: ``CfnRuleGroup.ForwardedIPConfigurationProperty.HeaderName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-forwardedipconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "fallback_behavior": fallback_behavior,
                "header_name": header_name,
            }

        @builtins.property
        def fallback_behavior(self) -> builtins.str:
            '''``CfnRuleGroup.ForwardedIPConfigurationProperty.FallbackBehavior``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-forwardedipconfiguration.html#cfn-wafv2-rulegroup-forwardedipconfiguration-fallbackbehavior
            '''
            result = self._values.get("fallback_behavior")
            assert result is not None, "Required property 'fallback_behavior' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def header_name(self) -> builtins.str:
            '''``CfnRuleGroup.ForwardedIPConfigurationProperty.HeaderName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-forwardedipconfiguration.html#cfn-wafv2-rulegroup-forwardedipconfiguration-headername
            '''
            result = self._values.get("header_name")
            assert result is not None, "Required property 'header_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardedIPConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.GeoMatchStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "country_codes": "countryCodes",
            "forwarded_ip_config": "forwardedIpConfig",
        },
    )
    class GeoMatchStatementProperty:
        def __init__(
            self,
            *,
            country_codes: typing.Optional[typing.List[builtins.str]] = None,
            forwarded_ip_config: typing.Optional[typing.Union["CfnRuleGroup.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param country_codes: ``CfnRuleGroup.GeoMatchStatementProperty.CountryCodes``.
            :param forwarded_ip_config: ``CfnRuleGroup.GeoMatchStatementProperty.ForwardedIPConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-geomatchstatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if country_codes is not None:
                self._values["country_codes"] = country_codes
            if forwarded_ip_config is not None:
                self._values["forwarded_ip_config"] = forwarded_ip_config

        @builtins.property
        def country_codes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnRuleGroup.GeoMatchStatementProperty.CountryCodes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-geomatchstatement.html#cfn-wafv2-rulegroup-geomatchstatement-countrycodes
            '''
            result = self._values.get("country_codes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def forwarded_ip_config(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.GeoMatchStatementProperty.ForwardedIPConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-geomatchstatement.html#cfn-wafv2-rulegroup-geomatchstatement-forwardedipconfig
            '''
            result = self._values.get("forwarded_ip_config")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeoMatchStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.interface(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.IPSetForwardedIPConfigurationProperty"
    )
    class IPSetForwardedIPConfigurationProperty(typing_extensions.Protocol):
        '''
        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetforwardedipconfiguration.html
        '''

        @builtins.staticmethod
        def __jsii_proxy_class__() -> typing.Type["_IPSetForwardedIPConfigurationPropertyProxy"]:
            return _IPSetForwardedIPConfigurationPropertyProxy

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="fallbackBehavior")
        def fallback_behavior(self) -> builtins.str:
            '''``CfnRuleGroup.IPSetForwardedIPConfigurationProperty.FallbackBehavior``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetforwardedipconfiguration.html#cfn-wafv2-rulegroup-ipsetforwardedipconfiguration-fallbackbehavior
            '''
            ...

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="headerName")
        def header_name(self) -> builtins.str:
            '''``CfnRuleGroup.IPSetForwardedIPConfigurationProperty.HeaderName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetforwardedipconfiguration.html#cfn-wafv2-rulegroup-ipsetforwardedipconfiguration-headername
            '''
            ...

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="position")
        def position(self) -> builtins.str:
            '''``CfnRuleGroup.IPSetForwardedIPConfigurationProperty.Position``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetforwardedipconfiguration.html#cfn-wafv2-rulegroup-ipsetforwardedipconfiguration-position
            '''
            ...


    class _IPSetForwardedIPConfigurationPropertyProxy:
        '''
        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetforwardedipconfiguration.html
        '''

        __jsii_type__: typing.ClassVar[str] = "monocdk.aws_wafv2.CfnRuleGroup.IPSetForwardedIPConfigurationProperty"

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="fallbackBehavior")
        def fallback_behavior(self) -> builtins.str:
            '''``CfnRuleGroup.IPSetForwardedIPConfigurationProperty.FallbackBehavior``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetforwardedipconfiguration.html#cfn-wafv2-rulegroup-ipsetforwardedipconfiguration-fallbackbehavior
            '''
            return typing.cast(builtins.str, jsii.get(self, "fallbackBehavior"))

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="headerName")
        def header_name(self) -> builtins.str:
            '''``CfnRuleGroup.IPSetForwardedIPConfigurationProperty.HeaderName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetforwardedipconfiguration.html#cfn-wafv2-rulegroup-ipsetforwardedipconfiguration-headername
            '''
            return typing.cast(builtins.str, jsii.get(self, "headerName"))

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="position")
        def position(self) -> builtins.str:
            '''``CfnRuleGroup.IPSetForwardedIPConfigurationProperty.Position``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetforwardedipconfiguration.html#cfn-wafv2-rulegroup-ipsetforwardedipconfiguration-position
            '''
            return typing.cast(builtins.str, jsii.get(self, "position"))

    @jsii.interface(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.IPSetReferenceStatementProperty"
    )
    class IPSetReferenceStatementProperty(typing_extensions.Protocol):
        '''
        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetreferencestatement.html
        '''

        @builtins.staticmethod
        def __jsii_proxy_class__() -> typing.Type["_IPSetReferenceStatementPropertyProxy"]:
            return _IPSetReferenceStatementPropertyProxy

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="arn")
        def arn(self) -> builtins.str:
            '''``CfnRuleGroup.IPSetReferenceStatementProperty.Arn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetreferencestatement.html#cfn-wafv2-rulegroup-ipsetreferencestatement-arn
            '''
            ...

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="ipSetForwardedIpConfig")
        def ip_set_forwarded_ip_config(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.IPSetForwardedIPConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.IPSetReferenceStatementProperty.IPSetForwardedIPConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetreferencestatement.html#cfn-wafv2-rulegroup-ipsetreferencestatement-ipsetforwardedipconfig
            '''
            ...


    class _IPSetReferenceStatementPropertyProxy:
        '''
        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetreferencestatement.html
        '''

        __jsii_type__: typing.ClassVar[str] = "monocdk.aws_wafv2.CfnRuleGroup.IPSetReferenceStatementProperty"

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="arn")
        def arn(self) -> builtins.str:
            '''``CfnRuleGroup.IPSetReferenceStatementProperty.Arn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetreferencestatement.html#cfn-wafv2-rulegroup-ipsetreferencestatement-arn
            '''
            return typing.cast(builtins.str, jsii.get(self, "arn"))

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="ipSetForwardedIpConfig")
        def ip_set_forwarded_ip_config(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.IPSetForwardedIPConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.IPSetReferenceStatementProperty.IPSetForwardedIPConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ipsetreferencestatement.html#cfn-wafv2-rulegroup-ipsetreferencestatement-ipsetforwardedipconfig
            '''
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.IPSetForwardedIPConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "ipSetForwardedIpConfig"))

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.NotStatementOneProperty",
        jsii_struct_bases=[],
        name_mapping={"statement": "statement"},
    )
    class NotStatementOneProperty:
        def __init__(
            self,
            *,
            statement: typing.Union["CfnRuleGroup.StatementTwoProperty", _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param statement: ``CfnRuleGroup.NotStatementOneProperty.Statement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-notstatementone.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "statement": statement,
            }

        @builtins.property
        def statement(
            self,
        ) -> typing.Union["CfnRuleGroup.StatementTwoProperty", _IResolvable_a771d0ef]:
            '''``CfnRuleGroup.NotStatementOneProperty.Statement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-notstatementone.html#cfn-wafv2-rulegroup-notstatementone-statement
            '''
            result = self._values.get("statement")
            assert result is not None, "Required property 'statement' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.StatementTwoProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotStatementOneProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.NotStatementTwoProperty",
        jsii_struct_bases=[],
        name_mapping={"statement": "statement"},
    )
    class NotStatementTwoProperty:
        def __init__(
            self,
            *,
            statement: typing.Union["CfnRuleGroup.StatementThreeProperty", _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param statement: ``CfnRuleGroup.NotStatementTwoProperty.Statement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-notstatementtwo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "statement": statement,
            }

        @builtins.property
        def statement(
            self,
        ) -> typing.Union["CfnRuleGroup.StatementThreeProperty", _IResolvable_a771d0ef]:
            '''``CfnRuleGroup.NotStatementTwoProperty.Statement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-notstatementtwo.html#cfn-wafv2-rulegroup-notstatementtwo-statement
            '''
            result = self._values.get("statement")
            assert result is not None, "Required property 'statement' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.StatementThreeProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotStatementTwoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.OrStatementOneProperty",
        jsii_struct_bases=[],
        name_mapping={"statements": "statements"},
    )
    class OrStatementOneProperty:
        def __init__(
            self,
            *,
            statements: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatementTwoProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param statements: ``CfnRuleGroup.OrStatementOneProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-orstatementone.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "statements": statements,
            }

        @builtins.property
        def statements(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatementTwoProperty", _IResolvable_a771d0ef]]]:
            '''``CfnRuleGroup.OrStatementOneProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-orstatementone.html#cfn-wafv2-rulegroup-orstatementone-statements
            '''
            result = self._values.get("statements")
            assert result is not None, "Required property 'statements' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatementTwoProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrStatementOneProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.OrStatementTwoProperty",
        jsii_struct_bases=[],
        name_mapping={"statements": "statements"},
    )
    class OrStatementTwoProperty:
        def __init__(
            self,
            *,
            statements: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatementThreeProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param statements: ``CfnRuleGroup.OrStatementTwoProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-orstatementtwo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "statements": statements,
            }

        @builtins.property
        def statements(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatementThreeProperty", _IResolvable_a771d0ef]]]:
            '''``CfnRuleGroup.OrStatementTwoProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-orstatementtwo.html#cfn-wafv2-rulegroup-orstatementtwo-statements
            '''
            result = self._values.get("statements")
            assert result is not None, "Required property 'statements' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatementThreeProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrStatementTwoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.RateBasedStatementOneProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregate_key_type": "aggregateKeyType",
            "limit": "limit",
            "forwarded_ip_config": "forwardedIpConfig",
            "scope_down_statement": "scopeDownStatement",
        },
    )
    class RateBasedStatementOneProperty:
        def __init__(
            self,
            *,
            aggregate_key_type: builtins.str,
            limit: jsii.Number,
            forwarded_ip_config: typing.Optional[typing.Union["CfnRuleGroup.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]] = None,
            scope_down_statement: typing.Optional[typing.Union["CfnRuleGroup.StatementTwoProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param aggregate_key_type: ``CfnRuleGroup.RateBasedStatementOneProperty.AggregateKeyType``.
            :param limit: ``CfnRuleGroup.RateBasedStatementOneProperty.Limit``.
            :param forwarded_ip_config: ``CfnRuleGroup.RateBasedStatementOneProperty.ForwardedIPConfig``.
            :param scope_down_statement: ``CfnRuleGroup.RateBasedStatementOneProperty.ScopeDownStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ratebasedstatementone.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "aggregate_key_type": aggregate_key_type,
                "limit": limit,
            }
            if forwarded_ip_config is not None:
                self._values["forwarded_ip_config"] = forwarded_ip_config
            if scope_down_statement is not None:
                self._values["scope_down_statement"] = scope_down_statement

        @builtins.property
        def aggregate_key_type(self) -> builtins.str:
            '''``CfnRuleGroup.RateBasedStatementOneProperty.AggregateKeyType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ratebasedstatementone.html#cfn-wafv2-rulegroup-ratebasedstatementone-aggregatekeytype
            '''
            result = self._values.get("aggregate_key_type")
            assert result is not None, "Required property 'aggregate_key_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def limit(self) -> jsii.Number:
            '''``CfnRuleGroup.RateBasedStatementOneProperty.Limit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ratebasedstatementone.html#cfn-wafv2-rulegroup-ratebasedstatementone-limit
            '''
            result = self._values.get("limit")
            assert result is not None, "Required property 'limit' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def forwarded_ip_config(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.RateBasedStatementOneProperty.ForwardedIPConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ratebasedstatementone.html#cfn-wafv2-rulegroup-ratebasedstatementone-forwardedipconfig
            '''
            result = self._values.get("forwarded_ip_config")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def scope_down_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.StatementTwoProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.RateBasedStatementOneProperty.ScopeDownStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ratebasedstatementone.html#cfn-wafv2-rulegroup-ratebasedstatementone-scopedownstatement
            '''
            result = self._values.get("scope_down_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.StatementTwoProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RateBasedStatementOneProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.RateBasedStatementTwoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregate_key_type": "aggregateKeyType",
            "limit": "limit",
            "forwarded_ip_config": "forwardedIpConfig",
            "scope_down_statement": "scopeDownStatement",
        },
    )
    class RateBasedStatementTwoProperty:
        def __init__(
            self,
            *,
            aggregate_key_type: builtins.str,
            limit: jsii.Number,
            forwarded_ip_config: typing.Optional[typing.Union["CfnRuleGroup.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]] = None,
            scope_down_statement: typing.Optional[typing.Union["CfnRuleGroup.StatementThreeProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param aggregate_key_type: ``CfnRuleGroup.RateBasedStatementTwoProperty.AggregateKeyType``.
            :param limit: ``CfnRuleGroup.RateBasedStatementTwoProperty.Limit``.
            :param forwarded_ip_config: ``CfnRuleGroup.RateBasedStatementTwoProperty.ForwardedIPConfig``.
            :param scope_down_statement: ``CfnRuleGroup.RateBasedStatementTwoProperty.ScopeDownStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ratebasedstatementtwo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "aggregate_key_type": aggregate_key_type,
                "limit": limit,
            }
            if forwarded_ip_config is not None:
                self._values["forwarded_ip_config"] = forwarded_ip_config
            if scope_down_statement is not None:
                self._values["scope_down_statement"] = scope_down_statement

        @builtins.property
        def aggregate_key_type(self) -> builtins.str:
            '''``CfnRuleGroup.RateBasedStatementTwoProperty.AggregateKeyType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ratebasedstatementtwo.html#cfn-wafv2-rulegroup-ratebasedstatementtwo-aggregatekeytype
            '''
            result = self._values.get("aggregate_key_type")
            assert result is not None, "Required property 'aggregate_key_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def limit(self) -> jsii.Number:
            '''``CfnRuleGroup.RateBasedStatementTwoProperty.Limit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ratebasedstatementtwo.html#cfn-wafv2-rulegroup-ratebasedstatementtwo-limit
            '''
            result = self._values.get("limit")
            assert result is not None, "Required property 'limit' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def forwarded_ip_config(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.RateBasedStatementTwoProperty.ForwardedIPConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ratebasedstatementtwo.html#cfn-wafv2-rulegroup-ratebasedstatementtwo-forwardedipconfig
            '''
            result = self._values.get("forwarded_ip_config")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def scope_down_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.StatementThreeProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.RateBasedStatementTwoProperty.ScopeDownStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ratebasedstatementtwo.html#cfn-wafv2-rulegroup-ratebasedstatementtwo-scopedownstatement
            '''
            result = self._values.get("scope_down_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.StatementThreeProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RateBasedStatementTwoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.RegexPatternSetReferenceStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "field_to_match": "fieldToMatch",
            "text_transformations": "textTransformations",
        },
    )
    class RegexPatternSetReferenceStatementProperty:
        def __init__(
            self,
            *,
            arn: builtins.str,
            field_to_match: typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef],
            text_transformations: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param arn: ``CfnRuleGroup.RegexPatternSetReferenceStatementProperty.Arn``.
            :param field_to_match: ``CfnRuleGroup.RegexPatternSetReferenceStatementProperty.FieldToMatch``.
            :param text_transformations: ``CfnRuleGroup.RegexPatternSetReferenceStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-regexpatternsetreferencestatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "arn": arn,
                "field_to_match": field_to_match,
                "text_transformations": text_transformations,
            }

        @builtins.property
        def arn(self) -> builtins.str:
            '''``CfnRuleGroup.RegexPatternSetReferenceStatementProperty.Arn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-regexpatternsetreferencestatement.html#cfn-wafv2-rulegroup-regexpatternsetreferencestatement-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef]:
            '''``CfnRuleGroup.RegexPatternSetReferenceStatementProperty.FieldToMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-regexpatternsetreferencestatement.html#cfn-wafv2-rulegroup-regexpatternsetreferencestatement-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def text_transformations(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]]:
            '''``CfnRuleGroup.RegexPatternSetReferenceStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-regexpatternsetreferencestatement.html#cfn-wafv2-rulegroup-regexpatternsetreferencestatement-texttransformations
            '''
            result = self._values.get("text_transformations")
            assert result is not None, "Required property 'text_transformations' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegexPatternSetReferenceStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.RuleActionProperty",
        jsii_struct_bases=[],
        name_mapping={"allow": "allow", "block": "block", "count": "count"},
    )
    class RuleActionProperty:
        def __init__(
            self,
            *,
            allow: typing.Any = None,
            block: typing.Any = None,
            count: typing.Any = None,
        ) -> None:
            '''
            :param allow: ``CfnRuleGroup.RuleActionProperty.Allow``.
            :param block: ``CfnRuleGroup.RuleActionProperty.Block``.
            :param count: ``CfnRuleGroup.RuleActionProperty.Count``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ruleaction.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if allow is not None:
                self._values["allow"] = allow
            if block is not None:
                self._values["block"] = block
            if count is not None:
                self._values["count"] = count

        @builtins.property
        def allow(self) -> typing.Any:
            '''``CfnRuleGroup.RuleActionProperty.Allow``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ruleaction.html#cfn-wafv2-rulegroup-ruleaction-allow
            '''
            result = self._values.get("allow")
            return typing.cast(typing.Any, result)

        @builtins.property
        def block(self) -> typing.Any:
            '''``CfnRuleGroup.RuleActionProperty.Block``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ruleaction.html#cfn-wafv2-rulegroup-ruleaction-block
            '''
            result = self._values.get("block")
            return typing.cast(typing.Any, result)

        @builtins.property
        def count(self) -> typing.Any:
            '''``CfnRuleGroup.RuleActionProperty.Count``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-ruleaction.html#cfn-wafv2-rulegroup-ruleaction-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "priority": "priority",
            "statement": "statement",
            "visibility_config": "visibilityConfig",
            "action": "action",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            priority: jsii.Number,
            statement: typing.Union["CfnRuleGroup.StatementOneProperty", _IResolvable_a771d0ef],
            visibility_config: typing.Union["CfnRuleGroup.VisibilityConfigProperty", _IResolvable_a771d0ef],
            action: typing.Optional[typing.Union["CfnRuleGroup.RuleActionProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param name: ``CfnRuleGroup.RuleProperty.Name``.
            :param priority: ``CfnRuleGroup.RuleProperty.Priority``.
            :param statement: ``CfnRuleGroup.RuleProperty.Statement``.
            :param visibility_config: ``CfnRuleGroup.RuleProperty.VisibilityConfig``.
            :param action: ``CfnRuleGroup.RuleProperty.Action``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-rule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "priority": priority,
                "statement": statement,
                "visibility_config": visibility_config,
            }
            if action is not None:
                self._values["action"] = action

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnRuleGroup.RuleProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-rule.html#cfn-wafv2-rulegroup-rule-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def priority(self) -> jsii.Number:
            '''``CfnRuleGroup.RuleProperty.Priority``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-rule.html#cfn-wafv2-rulegroup-rule-priority
            '''
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def statement(
            self,
        ) -> typing.Union["CfnRuleGroup.StatementOneProperty", _IResolvable_a771d0ef]:
            '''``CfnRuleGroup.RuleProperty.Statement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-rule.html#cfn-wafv2-rulegroup-rule-statement
            '''
            result = self._values.get("statement")
            assert result is not None, "Required property 'statement' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.StatementOneProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def visibility_config(
            self,
        ) -> typing.Union["CfnRuleGroup.VisibilityConfigProperty", _IResolvable_a771d0ef]:
            '''``CfnRuleGroup.RuleProperty.VisibilityConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-rule.html#cfn-wafv2-rulegroup-rule-visibilityconfig
            '''
            result = self._values.get("visibility_config")
            assert result is not None, "Required property 'visibility_config' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.VisibilityConfigProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.RuleActionProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.RuleProperty.Action``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-rule.html#cfn-wafv2-rulegroup-rule-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.RuleActionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.SizeConstraintStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "field_to_match": "fieldToMatch",
            "size": "size",
            "text_transformations": "textTransformations",
        },
    )
    class SizeConstraintStatementProperty:
        def __init__(
            self,
            *,
            comparison_operator: builtins.str,
            field_to_match: typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef],
            size: jsii.Number,
            text_transformations: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param comparison_operator: ``CfnRuleGroup.SizeConstraintStatementProperty.ComparisonOperator``.
            :param field_to_match: ``CfnRuleGroup.SizeConstraintStatementProperty.FieldToMatch``.
            :param size: ``CfnRuleGroup.SizeConstraintStatementProperty.Size``.
            :param text_transformations: ``CfnRuleGroup.SizeConstraintStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-sizeconstraintstatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "comparison_operator": comparison_operator,
                "field_to_match": field_to_match,
                "size": size,
                "text_transformations": text_transformations,
            }

        @builtins.property
        def comparison_operator(self) -> builtins.str:
            '''``CfnRuleGroup.SizeConstraintStatementProperty.ComparisonOperator``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-sizeconstraintstatement.html#cfn-wafv2-rulegroup-sizeconstraintstatement-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            assert result is not None, "Required property 'comparison_operator' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef]:
            '''``CfnRuleGroup.SizeConstraintStatementProperty.FieldToMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-sizeconstraintstatement.html#cfn-wafv2-rulegroup-sizeconstraintstatement-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def size(self) -> jsii.Number:
            '''``CfnRuleGroup.SizeConstraintStatementProperty.Size``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-sizeconstraintstatement.html#cfn-wafv2-rulegroup-sizeconstraintstatement-size
            '''
            result = self._values.get("size")
            assert result is not None, "Required property 'size' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def text_transformations(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]]:
            '''``CfnRuleGroup.SizeConstraintStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-sizeconstraintstatement.html#cfn-wafv2-rulegroup-sizeconstraintstatement-texttransformations
            '''
            result = self._values.get("text_transformations")
            assert result is not None, "Required property 'text_transformations' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SizeConstraintStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.SqliMatchStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_to_match": "fieldToMatch",
            "text_transformations": "textTransformations",
        },
    )
    class SqliMatchStatementProperty:
        def __init__(
            self,
            *,
            field_to_match: typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef],
            text_transformations: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param field_to_match: ``CfnRuleGroup.SqliMatchStatementProperty.FieldToMatch``.
            :param text_transformations: ``CfnRuleGroup.SqliMatchStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-sqlimatchstatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "field_to_match": field_to_match,
                "text_transformations": text_transformations,
            }

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef]:
            '''``CfnRuleGroup.SqliMatchStatementProperty.FieldToMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-sqlimatchstatement.html#cfn-wafv2-rulegroup-sqlimatchstatement-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def text_transformations(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]]:
            '''``CfnRuleGroup.SqliMatchStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-sqlimatchstatement.html#cfn-wafv2-rulegroup-sqlimatchstatement-texttransformations
            '''
            result = self._values.get("text_transformations")
            assert result is not None, "Required property 'text_transformations' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqliMatchStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.StatementOneProperty",
        jsii_struct_bases=[],
        name_mapping={
            "and_statement": "andStatement",
            "byte_match_statement": "byteMatchStatement",
            "geo_match_statement": "geoMatchStatement",
            "ip_set_reference_statement": "ipSetReferenceStatement",
            "not_statement": "notStatement",
            "or_statement": "orStatement",
            "rate_based_statement": "rateBasedStatement",
            "regex_pattern_set_reference_statement": "regexPatternSetReferenceStatement",
            "size_constraint_statement": "sizeConstraintStatement",
            "sqli_match_statement": "sqliMatchStatement",
            "xss_match_statement": "xssMatchStatement",
        },
    )
    class StatementOneProperty:
        def __init__(
            self,
            *,
            and_statement: typing.Optional[typing.Union["CfnRuleGroup.AndStatementOneProperty", _IResolvable_a771d0ef]] = None,
            byte_match_statement: typing.Optional[typing.Union["CfnRuleGroup.ByteMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            geo_match_statement: typing.Optional[typing.Union["CfnRuleGroup.GeoMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            ip_set_reference_statement: typing.Optional[typing.Union["CfnRuleGroup.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            not_statement: typing.Optional[typing.Union["CfnRuleGroup.NotStatementOneProperty", _IResolvable_a771d0ef]] = None,
            or_statement: typing.Optional[typing.Union["CfnRuleGroup.OrStatementOneProperty", _IResolvable_a771d0ef]] = None,
            rate_based_statement: typing.Optional[typing.Union["CfnRuleGroup.RateBasedStatementOneProperty", _IResolvable_a771d0ef]] = None,
            regex_pattern_set_reference_statement: typing.Optional[typing.Union["CfnRuleGroup.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            size_constraint_statement: typing.Optional[typing.Union["CfnRuleGroup.SizeConstraintStatementProperty", _IResolvable_a771d0ef]] = None,
            sqli_match_statement: typing.Optional[typing.Union["CfnRuleGroup.SqliMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            xss_match_statement: typing.Optional[typing.Union["CfnRuleGroup.XssMatchStatementProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param and_statement: ``CfnRuleGroup.StatementOneProperty.AndStatement``.
            :param byte_match_statement: ``CfnRuleGroup.StatementOneProperty.ByteMatchStatement``.
            :param geo_match_statement: ``CfnRuleGroup.StatementOneProperty.GeoMatchStatement``.
            :param ip_set_reference_statement: ``CfnRuleGroup.StatementOneProperty.IPSetReferenceStatement``.
            :param not_statement: ``CfnRuleGroup.StatementOneProperty.NotStatement``.
            :param or_statement: ``CfnRuleGroup.StatementOneProperty.OrStatement``.
            :param rate_based_statement: ``CfnRuleGroup.StatementOneProperty.RateBasedStatement``.
            :param regex_pattern_set_reference_statement: ``CfnRuleGroup.StatementOneProperty.RegexPatternSetReferenceStatement``.
            :param size_constraint_statement: ``CfnRuleGroup.StatementOneProperty.SizeConstraintStatement``.
            :param sqli_match_statement: ``CfnRuleGroup.StatementOneProperty.SqliMatchStatement``.
            :param xss_match_statement: ``CfnRuleGroup.StatementOneProperty.XssMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementone.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if and_statement is not None:
                self._values["and_statement"] = and_statement
            if byte_match_statement is not None:
                self._values["byte_match_statement"] = byte_match_statement
            if geo_match_statement is not None:
                self._values["geo_match_statement"] = geo_match_statement
            if ip_set_reference_statement is not None:
                self._values["ip_set_reference_statement"] = ip_set_reference_statement
            if not_statement is not None:
                self._values["not_statement"] = not_statement
            if or_statement is not None:
                self._values["or_statement"] = or_statement
            if rate_based_statement is not None:
                self._values["rate_based_statement"] = rate_based_statement
            if regex_pattern_set_reference_statement is not None:
                self._values["regex_pattern_set_reference_statement"] = regex_pattern_set_reference_statement
            if size_constraint_statement is not None:
                self._values["size_constraint_statement"] = size_constraint_statement
            if sqli_match_statement is not None:
                self._values["sqli_match_statement"] = sqli_match_statement
            if xss_match_statement is not None:
                self._values["xss_match_statement"] = xss_match_statement

        @builtins.property
        def and_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.AndStatementOneProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementOneProperty.AndStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementone.html#cfn-wafv2-rulegroup-statementone-andstatement
            '''
            result = self._values.get("and_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.AndStatementOneProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def byte_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.ByteMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementOneProperty.ByteMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementone.html#cfn-wafv2-rulegroup-statementone-bytematchstatement
            '''
            result = self._values.get("byte_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.ByteMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def geo_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.GeoMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementOneProperty.GeoMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementone.html#cfn-wafv2-rulegroup-statementone-geomatchstatement
            '''
            result = self._values.get("geo_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.GeoMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ip_set_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementOneProperty.IPSetReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementone.html#cfn-wafv2-rulegroup-statementone-ipsetreferencestatement
            '''
            result = self._values.get("ip_set_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def not_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.NotStatementOneProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementOneProperty.NotStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementone.html#cfn-wafv2-rulegroup-statementone-notstatement
            '''
            result = self._values.get("not_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.NotStatementOneProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def or_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.OrStatementOneProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementOneProperty.OrStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementone.html#cfn-wafv2-rulegroup-statementone-orstatement
            '''
            result = self._values.get("or_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.OrStatementOneProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rate_based_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.RateBasedStatementOneProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementOneProperty.RateBasedStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementone.html#cfn-wafv2-rulegroup-statementone-ratebasedstatement
            '''
            result = self._values.get("rate_based_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.RateBasedStatementOneProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def regex_pattern_set_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementOneProperty.RegexPatternSetReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementone.html#cfn-wafv2-rulegroup-statementone-regexpatternsetreferencestatement
            '''
            result = self._values.get("regex_pattern_set_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def size_constraint_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.SizeConstraintStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementOneProperty.SizeConstraintStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementone.html#cfn-wafv2-rulegroup-statementone-sizeconstraintstatement
            '''
            result = self._values.get("size_constraint_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.SizeConstraintStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sqli_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.SqliMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementOneProperty.SqliMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementone.html#cfn-wafv2-rulegroup-statementone-sqlimatchstatement
            '''
            result = self._values.get("sqli_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.SqliMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def xss_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.XssMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementOneProperty.XssMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementone.html#cfn-wafv2-rulegroup-statementone-xssmatchstatement
            '''
            result = self._values.get("xss_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.XssMatchStatementProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatementOneProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.StatementThreeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "byte_match_statement": "byteMatchStatement",
            "geo_match_statement": "geoMatchStatement",
            "ip_set_reference_statement": "ipSetReferenceStatement",
            "regex_pattern_set_reference_statement": "regexPatternSetReferenceStatement",
            "size_constraint_statement": "sizeConstraintStatement",
            "sqli_match_statement": "sqliMatchStatement",
            "xss_match_statement": "xssMatchStatement",
        },
    )
    class StatementThreeProperty:
        def __init__(
            self,
            *,
            byte_match_statement: typing.Optional[typing.Union["CfnRuleGroup.ByteMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            geo_match_statement: typing.Optional[typing.Union["CfnRuleGroup.GeoMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            ip_set_reference_statement: typing.Optional[typing.Union["CfnRuleGroup.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            regex_pattern_set_reference_statement: typing.Optional[typing.Union["CfnRuleGroup.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            size_constraint_statement: typing.Optional[typing.Union["CfnRuleGroup.SizeConstraintStatementProperty", _IResolvable_a771d0ef]] = None,
            sqli_match_statement: typing.Optional[typing.Union["CfnRuleGroup.SqliMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            xss_match_statement: typing.Optional[typing.Union["CfnRuleGroup.XssMatchStatementProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param byte_match_statement: ``CfnRuleGroup.StatementThreeProperty.ByteMatchStatement``.
            :param geo_match_statement: ``CfnRuleGroup.StatementThreeProperty.GeoMatchStatement``.
            :param ip_set_reference_statement: ``CfnRuleGroup.StatementThreeProperty.IPSetReferenceStatement``.
            :param regex_pattern_set_reference_statement: ``CfnRuleGroup.StatementThreeProperty.RegexPatternSetReferenceStatement``.
            :param size_constraint_statement: ``CfnRuleGroup.StatementThreeProperty.SizeConstraintStatement``.
            :param sqli_match_statement: ``CfnRuleGroup.StatementThreeProperty.SqliMatchStatement``.
            :param xss_match_statement: ``CfnRuleGroup.StatementThreeProperty.XssMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementthree.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if byte_match_statement is not None:
                self._values["byte_match_statement"] = byte_match_statement
            if geo_match_statement is not None:
                self._values["geo_match_statement"] = geo_match_statement
            if ip_set_reference_statement is not None:
                self._values["ip_set_reference_statement"] = ip_set_reference_statement
            if regex_pattern_set_reference_statement is not None:
                self._values["regex_pattern_set_reference_statement"] = regex_pattern_set_reference_statement
            if size_constraint_statement is not None:
                self._values["size_constraint_statement"] = size_constraint_statement
            if sqli_match_statement is not None:
                self._values["sqli_match_statement"] = sqli_match_statement
            if xss_match_statement is not None:
                self._values["xss_match_statement"] = xss_match_statement

        @builtins.property
        def byte_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.ByteMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementThreeProperty.ByteMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementthree.html#cfn-wafv2-rulegroup-statementthree-bytematchstatement
            '''
            result = self._values.get("byte_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.ByteMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def geo_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.GeoMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementThreeProperty.GeoMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementthree.html#cfn-wafv2-rulegroup-statementthree-geomatchstatement
            '''
            result = self._values.get("geo_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.GeoMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ip_set_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementThreeProperty.IPSetReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementthree.html#cfn-wafv2-rulegroup-statementthree-ipsetreferencestatement
            '''
            result = self._values.get("ip_set_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def regex_pattern_set_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementThreeProperty.RegexPatternSetReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementthree.html#cfn-wafv2-rulegroup-statementthree-regexpatternsetreferencestatement
            '''
            result = self._values.get("regex_pattern_set_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def size_constraint_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.SizeConstraintStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementThreeProperty.SizeConstraintStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementthree.html#cfn-wafv2-rulegroup-statementthree-sizeconstraintstatement
            '''
            result = self._values.get("size_constraint_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.SizeConstraintStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sqli_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.SqliMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementThreeProperty.SqliMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementthree.html#cfn-wafv2-rulegroup-statementthree-sqlimatchstatement
            '''
            result = self._values.get("sqli_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.SqliMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def xss_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.XssMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementThreeProperty.XssMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementthree.html#cfn-wafv2-rulegroup-statementthree-xssmatchstatement
            '''
            result = self._values.get("xss_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.XssMatchStatementProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatementThreeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.StatementTwoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "and_statement": "andStatement",
            "byte_match_statement": "byteMatchStatement",
            "geo_match_statement": "geoMatchStatement",
            "ip_set_reference_statement": "ipSetReferenceStatement",
            "not_statement": "notStatement",
            "or_statement": "orStatement",
            "rate_based_statement": "rateBasedStatement",
            "regex_pattern_set_reference_statement": "regexPatternSetReferenceStatement",
            "size_constraint_statement": "sizeConstraintStatement",
            "sqli_match_statement": "sqliMatchStatement",
            "xss_match_statement": "xssMatchStatement",
        },
    )
    class StatementTwoProperty:
        def __init__(
            self,
            *,
            and_statement: typing.Optional[typing.Union["CfnRuleGroup.AndStatementTwoProperty", _IResolvable_a771d0ef]] = None,
            byte_match_statement: typing.Optional[typing.Union["CfnRuleGroup.ByteMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            geo_match_statement: typing.Optional[typing.Union["CfnRuleGroup.GeoMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            ip_set_reference_statement: typing.Optional[typing.Union["CfnRuleGroup.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            not_statement: typing.Optional[typing.Union["CfnRuleGroup.NotStatementTwoProperty", _IResolvable_a771d0ef]] = None,
            or_statement: typing.Optional[typing.Union["CfnRuleGroup.OrStatementTwoProperty", _IResolvable_a771d0ef]] = None,
            rate_based_statement: typing.Optional[typing.Union["CfnRuleGroup.RateBasedStatementTwoProperty", _IResolvable_a771d0ef]] = None,
            regex_pattern_set_reference_statement: typing.Optional[typing.Union["CfnRuleGroup.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            size_constraint_statement: typing.Optional[typing.Union["CfnRuleGroup.SizeConstraintStatementProperty", _IResolvable_a771d0ef]] = None,
            sqli_match_statement: typing.Optional[typing.Union["CfnRuleGroup.SqliMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            xss_match_statement: typing.Optional[typing.Union["CfnRuleGroup.XssMatchStatementProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param and_statement: ``CfnRuleGroup.StatementTwoProperty.AndStatement``.
            :param byte_match_statement: ``CfnRuleGroup.StatementTwoProperty.ByteMatchStatement``.
            :param geo_match_statement: ``CfnRuleGroup.StatementTwoProperty.GeoMatchStatement``.
            :param ip_set_reference_statement: ``CfnRuleGroup.StatementTwoProperty.IPSetReferenceStatement``.
            :param not_statement: ``CfnRuleGroup.StatementTwoProperty.NotStatement``.
            :param or_statement: ``CfnRuleGroup.StatementTwoProperty.OrStatement``.
            :param rate_based_statement: ``CfnRuleGroup.StatementTwoProperty.RateBasedStatement``.
            :param regex_pattern_set_reference_statement: ``CfnRuleGroup.StatementTwoProperty.RegexPatternSetReferenceStatement``.
            :param size_constraint_statement: ``CfnRuleGroup.StatementTwoProperty.SizeConstraintStatement``.
            :param sqli_match_statement: ``CfnRuleGroup.StatementTwoProperty.SqliMatchStatement``.
            :param xss_match_statement: ``CfnRuleGroup.StatementTwoProperty.XssMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementtwo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if and_statement is not None:
                self._values["and_statement"] = and_statement
            if byte_match_statement is not None:
                self._values["byte_match_statement"] = byte_match_statement
            if geo_match_statement is not None:
                self._values["geo_match_statement"] = geo_match_statement
            if ip_set_reference_statement is not None:
                self._values["ip_set_reference_statement"] = ip_set_reference_statement
            if not_statement is not None:
                self._values["not_statement"] = not_statement
            if or_statement is not None:
                self._values["or_statement"] = or_statement
            if rate_based_statement is not None:
                self._values["rate_based_statement"] = rate_based_statement
            if regex_pattern_set_reference_statement is not None:
                self._values["regex_pattern_set_reference_statement"] = regex_pattern_set_reference_statement
            if size_constraint_statement is not None:
                self._values["size_constraint_statement"] = size_constraint_statement
            if sqli_match_statement is not None:
                self._values["sqli_match_statement"] = sqli_match_statement
            if xss_match_statement is not None:
                self._values["xss_match_statement"] = xss_match_statement

        @builtins.property
        def and_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.AndStatementTwoProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementTwoProperty.AndStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementtwo.html#cfn-wafv2-rulegroup-statementtwo-andstatement
            '''
            result = self._values.get("and_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.AndStatementTwoProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def byte_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.ByteMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementTwoProperty.ByteMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementtwo.html#cfn-wafv2-rulegroup-statementtwo-bytematchstatement
            '''
            result = self._values.get("byte_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.ByteMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def geo_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.GeoMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementTwoProperty.GeoMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementtwo.html#cfn-wafv2-rulegroup-statementtwo-geomatchstatement
            '''
            result = self._values.get("geo_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.GeoMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ip_set_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementTwoProperty.IPSetReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementtwo.html#cfn-wafv2-rulegroup-statementtwo-ipsetreferencestatement
            '''
            result = self._values.get("ip_set_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def not_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.NotStatementTwoProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementTwoProperty.NotStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementtwo.html#cfn-wafv2-rulegroup-statementtwo-notstatement
            '''
            result = self._values.get("not_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.NotStatementTwoProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def or_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.OrStatementTwoProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementTwoProperty.OrStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementtwo.html#cfn-wafv2-rulegroup-statementtwo-orstatement
            '''
            result = self._values.get("or_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.OrStatementTwoProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rate_based_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.RateBasedStatementTwoProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementTwoProperty.RateBasedStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementtwo.html#cfn-wafv2-rulegroup-statementtwo-ratebasedstatement
            '''
            result = self._values.get("rate_based_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.RateBasedStatementTwoProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def regex_pattern_set_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementTwoProperty.RegexPatternSetReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementtwo.html#cfn-wafv2-rulegroup-statementtwo-regexpatternsetreferencestatement
            '''
            result = self._values.get("regex_pattern_set_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def size_constraint_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.SizeConstraintStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementTwoProperty.SizeConstraintStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementtwo.html#cfn-wafv2-rulegroup-statementtwo-sizeconstraintstatement
            '''
            result = self._values.get("size_constraint_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.SizeConstraintStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sqli_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.SqliMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementTwoProperty.SqliMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementtwo.html#cfn-wafv2-rulegroup-statementtwo-sqlimatchstatement
            '''
            result = self._values.get("sqli_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.SqliMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def xss_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.XssMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnRuleGroup.StatementTwoProperty.XssMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-statementtwo.html#cfn-wafv2-rulegroup-statementtwo-xssmatchstatement
            '''
            result = self._values.get("xss_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.XssMatchStatementProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatementTwoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.TextTransformationProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "type": "type"},
    )
    class TextTransformationProperty:
        def __init__(self, *, priority: jsii.Number, type: builtins.str) -> None:
            '''
            :param priority: ``CfnRuleGroup.TextTransformationProperty.Priority``.
            :param type: ``CfnRuleGroup.TextTransformationProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-texttransformation.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "priority": priority,
                "type": type,
            }

        @builtins.property
        def priority(self) -> jsii.Number:
            '''``CfnRuleGroup.TextTransformationProperty.Priority``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-texttransformation.html#cfn-wafv2-rulegroup-texttransformation-priority
            '''
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnRuleGroup.TextTransformationProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-texttransformation.html#cfn-wafv2-rulegroup-texttransformation-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextTransformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.VisibilityConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_metrics_enabled": "cloudWatchMetricsEnabled",
            "metric_name": "metricName",
            "sampled_requests_enabled": "sampledRequestsEnabled",
        },
    )
    class VisibilityConfigProperty:
        def __init__(
            self,
            *,
            cloud_watch_metrics_enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            metric_name: builtins.str,
            sampled_requests_enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param cloud_watch_metrics_enabled: ``CfnRuleGroup.VisibilityConfigProperty.CloudWatchMetricsEnabled``.
            :param metric_name: ``CfnRuleGroup.VisibilityConfigProperty.MetricName``.
            :param sampled_requests_enabled: ``CfnRuleGroup.VisibilityConfigProperty.SampledRequestsEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-visibilityconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "cloud_watch_metrics_enabled": cloud_watch_metrics_enabled,
                "metric_name": metric_name,
                "sampled_requests_enabled": sampled_requests_enabled,
            }

        @builtins.property
        def cloud_watch_metrics_enabled(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnRuleGroup.VisibilityConfigProperty.CloudWatchMetricsEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-visibilityconfig.html#cfn-wafv2-rulegroup-visibilityconfig-cloudwatchmetricsenabled
            '''
            result = self._values.get("cloud_watch_metrics_enabled")
            assert result is not None, "Required property 'cloud_watch_metrics_enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def metric_name(self) -> builtins.str:
            '''``CfnRuleGroup.VisibilityConfigProperty.MetricName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-visibilityconfig.html#cfn-wafv2-rulegroup-visibilityconfig-metricname
            '''
            result = self._values.get("metric_name")
            assert result is not None, "Required property 'metric_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sampled_requests_enabled(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnRuleGroup.VisibilityConfigProperty.SampledRequestsEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-visibilityconfig.html#cfn-wafv2-rulegroup-visibilityconfig-sampledrequestsenabled
            '''
            result = self._values.get("sampled_requests_enabled")
            assert result is not None, "Required property 'sampled_requests_enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VisibilityConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnRuleGroup.XssMatchStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_to_match": "fieldToMatch",
            "text_transformations": "textTransformations",
        },
    )
    class XssMatchStatementProperty:
        def __init__(
            self,
            *,
            field_to_match: typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef],
            text_transformations: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param field_to_match: ``CfnRuleGroup.XssMatchStatementProperty.FieldToMatch``.
            :param text_transformations: ``CfnRuleGroup.XssMatchStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-xssmatchstatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "field_to_match": field_to_match,
                "text_transformations": text_transformations,
            }

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef]:
            '''``CfnRuleGroup.XssMatchStatementProperty.FieldToMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-xssmatchstatement.html#cfn-wafv2-rulegroup-xssmatchstatement-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.FieldToMatchProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def text_transformations(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]]:
            '''``CfnRuleGroup.XssMatchStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-rulegroup-xssmatchstatement.html#cfn-wafv2-rulegroup-xssmatchstatement-texttransformations
            '''
            result = self._values.get("text_transformations")
            assert result is not None, "Required property 'text_transformations' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TextTransformationProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "XssMatchStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_wafv2.CfnRuleGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "scope": "scope",
        "visibility_config": "visibilityConfig",
        "description": "description",
        "name": "name",
        "rules": "rules",
        "tags": "tags",
    },
)
class CfnRuleGroupProps:
    def __init__(
        self,
        *,
        capacity: jsii.Number,
        scope: builtins.str,
        visibility_config: typing.Union[CfnRuleGroup.VisibilityConfigProperty, _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRuleGroup.RuleProperty, _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::WAFv2::RuleGroup``.

        :param capacity: ``AWS::WAFv2::RuleGroup.Capacity``.
        :param scope: ``AWS::WAFv2::RuleGroup.Scope``.
        :param visibility_config: ``AWS::WAFv2::RuleGroup.VisibilityConfig``.
        :param description: ``AWS::WAFv2::RuleGroup.Description``.
        :param name: ``AWS::WAFv2::RuleGroup.Name``.
        :param rules: ``AWS::WAFv2::RuleGroup.Rules``.
        :param tags: ``AWS::WAFv2::RuleGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "capacity": capacity,
            "scope": scope,
            "visibility_config": visibility_config,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if rules is not None:
            self._values["rules"] = rules
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def capacity(self) -> jsii.Number:
        '''``AWS::WAFv2::RuleGroup.Capacity``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-capacity
        '''
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''``AWS::WAFv2::RuleGroup.Scope``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-scope
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def visibility_config(
        self,
    ) -> typing.Union[CfnRuleGroup.VisibilityConfigProperty, _IResolvable_a771d0ef]:
        '''``AWS::WAFv2::RuleGroup.VisibilityConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-visibilityconfig
        '''
        result = self._values.get("visibility_config")
        assert result is not None, "Required property 'visibility_config' is missing"
        return typing.cast(typing.Union[CfnRuleGroup.VisibilityConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::RuleGroup.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::RuleGroup.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRuleGroup.RuleProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::WAFv2::RuleGroup.Rules``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRuleGroup.RuleProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::WAFv2::RuleGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-rulegroup.html#cfn-wafv2-rulegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnWebACL(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_wafv2.CfnWebACL",
):
    '''A CloudFormation ``AWS::WAFv2::WebACL``.

    :cloudformationResource: AWS::WAFv2::WebACL
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html
    '''

    def __init__(
        self,
        scope_: _Construct_e78e779f,
        id: builtins.str,
        *,
        default_action: typing.Union["CfnWebACL.DefaultActionProperty", _IResolvable_a771d0ef],
        scope: builtins.str,
        visibility_config: typing.Union["CfnWebACL.VisibilityConfigProperty", _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.RuleProperty", _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::WAFv2::WebACL``.

        :param scope_: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param default_action: ``AWS::WAFv2::WebACL.DefaultAction``.
        :param scope: ``AWS::WAFv2::WebACL.Scope``.
        :param visibility_config: ``AWS::WAFv2::WebACL.VisibilityConfig``.
        :param description: ``AWS::WAFv2::WebACL.Description``.
        :param name: ``AWS::WAFv2::WebACL.Name``.
        :param rules: ``AWS::WAFv2::WebACL.Rules``.
        :param tags: ``AWS::WAFv2::WebACL.Tags``.
        '''
        props = CfnWebACLProps(
            default_action=default_action,
            scope=scope,
            visibility_config=visibility_config,
            description=description,
            name=name,
            rules=rules,
            tags=tags,
        )

        jsii.create(CfnWebACL, self, [scope_, id, props])

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
    @jsii.member(jsii_name="attrCapacity")
    def attr_capacity(self) -> jsii.Number:
        '''
        :cloudformationAttribute: Capacity
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrCapacity"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::WAFv2::WebACL.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultAction")
    def default_action(
        self,
    ) -> typing.Union["CfnWebACL.DefaultActionProperty", _IResolvable_a771d0ef]:
        '''``AWS::WAFv2::WebACL.DefaultAction``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-defaultaction
        '''
        return typing.cast(typing.Union["CfnWebACL.DefaultActionProperty", _IResolvable_a771d0ef], jsii.get(self, "defaultAction"))

    @default_action.setter
    def default_action(
        self,
        value: typing.Union["CfnWebACL.DefaultActionProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "defaultAction", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        '''``AWS::WAFv2::WebACL.Scope``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-scope
        '''
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        jsii.set(self, "scope", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="visibilityConfig")
    def visibility_config(
        self,
    ) -> typing.Union["CfnWebACL.VisibilityConfigProperty", _IResolvable_a771d0ef]:
        '''``AWS::WAFv2::WebACL.VisibilityConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-visibilityconfig
        '''
        return typing.cast(typing.Union["CfnWebACL.VisibilityConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "visibilityConfig"))

    @visibility_config.setter
    def visibility_config(
        self,
        value: typing.Union["CfnWebACL.VisibilityConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "visibilityConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::WebACL.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::WebACL.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rules")
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.RuleProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::WAFv2::WebACL.Rules``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-rules
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.RuleProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "rules"))

    @rules.setter
    def rules(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.RuleProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "rules", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.AndStatementOneProperty",
        jsii_struct_bases=[],
        name_mapping={"statements": "statements"},
    )
    class AndStatementOneProperty:
        def __init__(
            self,
            *,
            statements: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.StatementTwoProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param statements: ``CfnWebACL.AndStatementOneProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-andstatementone.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "statements": statements,
            }

        @builtins.property
        def statements(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.StatementTwoProperty", _IResolvable_a771d0ef]]]:
            '''``CfnWebACL.AndStatementOneProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-andstatementone.html#cfn-wafv2-webacl-andstatementone-statements
            '''
            result = self._values.get("statements")
            assert result is not None, "Required property 'statements' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.StatementTwoProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AndStatementOneProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.AndStatementTwoProperty",
        jsii_struct_bases=[],
        name_mapping={"statements": "statements"},
    )
    class AndStatementTwoProperty:
        def __init__(
            self,
            *,
            statements: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.StatementThreeProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param statements: ``CfnWebACL.AndStatementTwoProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-andstatementtwo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "statements": statements,
            }

        @builtins.property
        def statements(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.StatementThreeProperty", _IResolvable_a771d0ef]]]:
            '''``CfnWebACL.AndStatementTwoProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-andstatementtwo.html#cfn-wafv2-webacl-andstatementtwo-statements
            '''
            result = self._values.get("statements")
            assert result is not None, "Required property 'statements' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.StatementThreeProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AndStatementTwoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.ByteMatchStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_to_match": "fieldToMatch",
            "positional_constraint": "positionalConstraint",
            "text_transformations": "textTransformations",
            "search_string": "searchString",
            "search_string_base64": "searchStringBase64",
        },
    )
    class ByteMatchStatementProperty:
        def __init__(
            self,
            *,
            field_to_match: typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef],
            positional_constraint: builtins.str,
            text_transformations: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]],
            search_string: typing.Optional[builtins.str] = None,
            search_string_base64: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param field_to_match: ``CfnWebACL.ByteMatchStatementProperty.FieldToMatch``.
            :param positional_constraint: ``CfnWebACL.ByteMatchStatementProperty.PositionalConstraint``.
            :param text_transformations: ``CfnWebACL.ByteMatchStatementProperty.TextTransformations``.
            :param search_string: ``CfnWebACL.ByteMatchStatementProperty.SearchString``.
            :param search_string_base64: ``CfnWebACL.ByteMatchStatementProperty.SearchStringBase64``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-bytematchstatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "field_to_match": field_to_match,
                "positional_constraint": positional_constraint,
                "text_transformations": text_transformations,
            }
            if search_string is not None:
                self._values["search_string"] = search_string
            if search_string_base64 is not None:
                self._values["search_string_base64"] = search_string_base64

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef]:
            '''``CfnWebACL.ByteMatchStatementProperty.FieldToMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-bytematchstatement.html#cfn-wafv2-webacl-bytematchstatement-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def positional_constraint(self) -> builtins.str:
            '''``CfnWebACL.ByteMatchStatementProperty.PositionalConstraint``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-bytematchstatement.html#cfn-wafv2-webacl-bytematchstatement-positionalconstraint
            '''
            result = self._values.get("positional_constraint")
            assert result is not None, "Required property 'positional_constraint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def text_transformations(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]]:
            '''``CfnWebACL.ByteMatchStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-bytematchstatement.html#cfn-wafv2-webacl-bytematchstatement-texttransformations
            '''
            result = self._values.get("text_transformations")
            assert result is not None, "Required property 'text_transformations' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def search_string(self) -> typing.Optional[builtins.str]:
            '''``CfnWebACL.ByteMatchStatementProperty.SearchString``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-bytematchstatement.html#cfn-wafv2-webacl-bytematchstatement-searchstring
            '''
            result = self._values.get("search_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def search_string_base64(self) -> typing.Optional[builtins.str]:
            '''``CfnWebACL.ByteMatchStatementProperty.SearchStringBase64``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-bytematchstatement.html#cfn-wafv2-webacl-bytematchstatement-searchstringbase64
            '''
            result = self._values.get("search_string_base64")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ByteMatchStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.DefaultActionProperty",
        jsii_struct_bases=[],
        name_mapping={"allow": "allow", "block": "block"},
    )
    class DefaultActionProperty:
        def __init__(
            self,
            *,
            allow: typing.Any = None,
            block: typing.Any = None,
        ) -> None:
            '''
            :param allow: ``CfnWebACL.DefaultActionProperty.Allow``.
            :param block: ``CfnWebACL.DefaultActionProperty.Block``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-defaultaction.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if allow is not None:
                self._values["allow"] = allow
            if block is not None:
                self._values["block"] = block

        @builtins.property
        def allow(self) -> typing.Any:
            '''``CfnWebACL.DefaultActionProperty.Allow``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-defaultaction.html#cfn-wafv2-webacl-defaultaction-allow
            '''
            result = self._values.get("allow")
            return typing.cast(typing.Any, result)

        @builtins.property
        def block(self) -> typing.Any:
            '''``CfnWebACL.DefaultActionProperty.Block``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-defaultaction.html#cfn-wafv2-webacl-defaultaction-block
            '''
            result = self._values.get("block")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.ExcludedRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class ExcludedRuleProperty:
        def __init__(self, *, name: builtins.str) -> None:
            '''
            :param name: ``CfnWebACL.ExcludedRuleProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-excludedrule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnWebACL.ExcludedRuleProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-excludedrule.html#cfn-wafv2-webacl-excludedrule-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExcludedRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.FieldToMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "all_query_arguments": "allQueryArguments",
            "body": "body",
            "method": "method",
            "query_string": "queryString",
            "single_header": "singleHeader",
            "single_query_argument": "singleQueryArgument",
            "uri_path": "uriPath",
        },
    )
    class FieldToMatchProperty:
        def __init__(
            self,
            *,
            all_query_arguments: typing.Any = None,
            body: typing.Any = None,
            method: typing.Any = None,
            query_string: typing.Any = None,
            single_header: typing.Any = None,
            single_query_argument: typing.Any = None,
            uri_path: typing.Any = None,
        ) -> None:
            '''
            :param all_query_arguments: ``CfnWebACL.FieldToMatchProperty.AllQueryArguments``.
            :param body: ``CfnWebACL.FieldToMatchProperty.Body``.
            :param method: ``CfnWebACL.FieldToMatchProperty.Method``.
            :param query_string: ``CfnWebACL.FieldToMatchProperty.QueryString``.
            :param single_header: ``CfnWebACL.FieldToMatchProperty.SingleHeader``.
            :param single_query_argument: ``CfnWebACL.FieldToMatchProperty.SingleQueryArgument``.
            :param uri_path: ``CfnWebACL.FieldToMatchProperty.UriPath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-fieldtomatch.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if all_query_arguments is not None:
                self._values["all_query_arguments"] = all_query_arguments
            if body is not None:
                self._values["body"] = body
            if method is not None:
                self._values["method"] = method
            if query_string is not None:
                self._values["query_string"] = query_string
            if single_header is not None:
                self._values["single_header"] = single_header
            if single_query_argument is not None:
                self._values["single_query_argument"] = single_query_argument
            if uri_path is not None:
                self._values["uri_path"] = uri_path

        @builtins.property
        def all_query_arguments(self) -> typing.Any:
            '''``CfnWebACL.FieldToMatchProperty.AllQueryArguments``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-fieldtomatch.html#cfn-wafv2-webacl-fieldtomatch-allqueryarguments
            '''
            result = self._values.get("all_query_arguments")
            return typing.cast(typing.Any, result)

        @builtins.property
        def body(self) -> typing.Any:
            '''``CfnWebACL.FieldToMatchProperty.Body``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-fieldtomatch.html#cfn-wafv2-webacl-fieldtomatch-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Any, result)

        @builtins.property
        def method(self) -> typing.Any:
            '''``CfnWebACL.FieldToMatchProperty.Method``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-fieldtomatch.html#cfn-wafv2-webacl-fieldtomatch-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Any, result)

        @builtins.property
        def query_string(self) -> typing.Any:
            '''``CfnWebACL.FieldToMatchProperty.QueryString``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-fieldtomatch.html#cfn-wafv2-webacl-fieldtomatch-querystring
            '''
            result = self._values.get("query_string")
            return typing.cast(typing.Any, result)

        @builtins.property
        def single_header(self) -> typing.Any:
            '''``CfnWebACL.FieldToMatchProperty.SingleHeader``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-fieldtomatch.html#cfn-wafv2-webacl-fieldtomatch-singleheader
            '''
            result = self._values.get("single_header")
            return typing.cast(typing.Any, result)

        @builtins.property
        def single_query_argument(self) -> typing.Any:
            '''``CfnWebACL.FieldToMatchProperty.SingleQueryArgument``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-fieldtomatch.html#cfn-wafv2-webacl-fieldtomatch-singlequeryargument
            '''
            result = self._values.get("single_query_argument")
            return typing.cast(typing.Any, result)

        @builtins.property
        def uri_path(self) -> typing.Any:
            '''``CfnWebACL.FieldToMatchProperty.UriPath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-fieldtomatch.html#cfn-wafv2-webacl-fieldtomatch-uripath
            '''
            result = self._values.get("uri_path")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldToMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.ForwardedIPConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "fallback_behavior": "fallbackBehavior",
            "header_name": "headerName",
        },
    )
    class ForwardedIPConfigurationProperty:
        def __init__(
            self,
            *,
            fallback_behavior: builtins.str,
            header_name: builtins.str,
        ) -> None:
            '''
            :param fallback_behavior: ``CfnWebACL.ForwardedIPConfigurationProperty.FallbackBehavior``.
            :param header_name: ``CfnWebACL.ForwardedIPConfigurationProperty.HeaderName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-forwardedipconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "fallback_behavior": fallback_behavior,
                "header_name": header_name,
            }

        @builtins.property
        def fallback_behavior(self) -> builtins.str:
            '''``CfnWebACL.ForwardedIPConfigurationProperty.FallbackBehavior``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-forwardedipconfiguration.html#cfn-wafv2-webacl-forwardedipconfiguration-fallbackbehavior
            '''
            result = self._values.get("fallback_behavior")
            assert result is not None, "Required property 'fallback_behavior' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def header_name(self) -> builtins.str:
            '''``CfnWebACL.ForwardedIPConfigurationProperty.HeaderName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-forwardedipconfiguration.html#cfn-wafv2-webacl-forwardedipconfiguration-headername
            '''
            result = self._values.get("header_name")
            assert result is not None, "Required property 'header_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardedIPConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.GeoMatchStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "country_codes": "countryCodes",
            "forwarded_ip_config": "forwardedIpConfig",
        },
    )
    class GeoMatchStatementProperty:
        def __init__(
            self,
            *,
            country_codes: typing.Optional[typing.List[builtins.str]] = None,
            forwarded_ip_config: typing.Optional[typing.Union["CfnWebACL.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param country_codes: ``CfnWebACL.GeoMatchStatementProperty.CountryCodes``.
            :param forwarded_ip_config: ``CfnWebACL.GeoMatchStatementProperty.ForwardedIPConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-geomatchstatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if country_codes is not None:
                self._values["country_codes"] = country_codes
            if forwarded_ip_config is not None:
                self._values["forwarded_ip_config"] = forwarded_ip_config

        @builtins.property
        def country_codes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnWebACL.GeoMatchStatementProperty.CountryCodes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-geomatchstatement.html#cfn-wafv2-webacl-geomatchstatement-countrycodes
            '''
            result = self._values.get("country_codes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def forwarded_ip_config(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.GeoMatchStatementProperty.ForwardedIPConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-geomatchstatement.html#cfn-wafv2-webacl-geomatchstatement-forwardedipconfig
            '''
            result = self._values.get("forwarded_ip_config")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeoMatchStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.interface(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.IPSetForwardedIPConfigurationProperty"
    )
    class IPSetForwardedIPConfigurationProperty(typing_extensions.Protocol):
        '''
        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetforwardedipconfiguration.html
        '''

        @builtins.staticmethod
        def __jsii_proxy_class__() -> typing.Type["_IPSetForwardedIPConfigurationPropertyProxy"]:
            return _IPSetForwardedIPConfigurationPropertyProxy

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="fallbackBehavior")
        def fallback_behavior(self) -> builtins.str:
            '''``CfnWebACL.IPSetForwardedIPConfigurationProperty.FallbackBehavior``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetforwardedipconfiguration.html#cfn-wafv2-webacl-ipsetforwardedipconfiguration-fallbackbehavior
            '''
            ...

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="headerName")
        def header_name(self) -> builtins.str:
            '''``CfnWebACL.IPSetForwardedIPConfigurationProperty.HeaderName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetforwardedipconfiguration.html#cfn-wafv2-webacl-ipsetforwardedipconfiguration-headername
            '''
            ...

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="position")
        def position(self) -> builtins.str:
            '''``CfnWebACL.IPSetForwardedIPConfigurationProperty.Position``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetforwardedipconfiguration.html#cfn-wafv2-webacl-ipsetforwardedipconfiguration-position
            '''
            ...


    class _IPSetForwardedIPConfigurationPropertyProxy:
        '''
        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetforwardedipconfiguration.html
        '''

        __jsii_type__: typing.ClassVar[str] = "monocdk.aws_wafv2.CfnWebACL.IPSetForwardedIPConfigurationProperty"

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="fallbackBehavior")
        def fallback_behavior(self) -> builtins.str:
            '''``CfnWebACL.IPSetForwardedIPConfigurationProperty.FallbackBehavior``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetforwardedipconfiguration.html#cfn-wafv2-webacl-ipsetforwardedipconfiguration-fallbackbehavior
            '''
            return typing.cast(builtins.str, jsii.get(self, "fallbackBehavior"))

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="headerName")
        def header_name(self) -> builtins.str:
            '''``CfnWebACL.IPSetForwardedIPConfigurationProperty.HeaderName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetforwardedipconfiguration.html#cfn-wafv2-webacl-ipsetforwardedipconfiguration-headername
            '''
            return typing.cast(builtins.str, jsii.get(self, "headerName"))

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="position")
        def position(self) -> builtins.str:
            '''``CfnWebACL.IPSetForwardedIPConfigurationProperty.Position``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetforwardedipconfiguration.html#cfn-wafv2-webacl-ipsetforwardedipconfiguration-position
            '''
            return typing.cast(builtins.str, jsii.get(self, "position"))

    @jsii.interface(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.IPSetReferenceStatementProperty"
    )
    class IPSetReferenceStatementProperty(typing_extensions.Protocol):
        '''
        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetreferencestatement.html
        '''

        @builtins.staticmethod
        def __jsii_proxy_class__() -> typing.Type["_IPSetReferenceStatementPropertyProxy"]:
            return _IPSetReferenceStatementPropertyProxy

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="arn")
        def arn(self) -> builtins.str:
            '''``CfnWebACL.IPSetReferenceStatementProperty.Arn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetreferencestatement.html#cfn-wafv2-webacl-ipsetreferencestatement-arn
            '''
            ...

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="ipSetForwardedIpConfig")
        def ip_set_forwarded_ip_config(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.IPSetForwardedIPConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.IPSetReferenceStatementProperty.IPSetForwardedIPConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetreferencestatement.html#cfn-wafv2-webacl-ipsetreferencestatement-ipsetforwardedipconfig
            '''
            ...


    class _IPSetReferenceStatementPropertyProxy:
        '''
        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetreferencestatement.html
        '''

        __jsii_type__: typing.ClassVar[str] = "monocdk.aws_wafv2.CfnWebACL.IPSetReferenceStatementProperty"

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="arn")
        def arn(self) -> builtins.str:
            '''``CfnWebACL.IPSetReferenceStatementProperty.Arn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetreferencestatement.html#cfn-wafv2-webacl-ipsetreferencestatement-arn
            '''
            return typing.cast(builtins.str, jsii.get(self, "arn"))

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="ipSetForwardedIpConfig")
        def ip_set_forwarded_ip_config(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.IPSetForwardedIPConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.IPSetReferenceStatementProperty.IPSetForwardedIPConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ipsetreferencestatement.html#cfn-wafv2-webacl-ipsetreferencestatement-ipsetforwardedipconfig
            '''
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.IPSetForwardedIPConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "ipSetForwardedIpConfig"))

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.ManagedRuleGroupStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "vendor_name": "vendorName",
            "excluded_rules": "excludedRules",
        },
    )
    class ManagedRuleGroupStatementProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            vendor_name: builtins.str,
            excluded_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.ExcludedRuleProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param name: ``CfnWebACL.ManagedRuleGroupStatementProperty.Name``.
            :param vendor_name: ``CfnWebACL.ManagedRuleGroupStatementProperty.VendorName``.
            :param excluded_rules: ``CfnWebACL.ManagedRuleGroupStatementProperty.ExcludedRules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-managedrulegroupstatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "vendor_name": vendor_name,
            }
            if excluded_rules is not None:
                self._values["excluded_rules"] = excluded_rules

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnWebACL.ManagedRuleGroupStatementProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-managedrulegroupstatement.html#cfn-wafv2-webacl-managedrulegroupstatement-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def vendor_name(self) -> builtins.str:
            '''``CfnWebACL.ManagedRuleGroupStatementProperty.VendorName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-managedrulegroupstatement.html#cfn-wafv2-webacl-managedrulegroupstatement-vendorname
            '''
            result = self._values.get("vendor_name")
            assert result is not None, "Required property 'vendor_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def excluded_rules(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.ExcludedRuleProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnWebACL.ManagedRuleGroupStatementProperty.ExcludedRules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-managedrulegroupstatement.html#cfn-wafv2-webacl-managedrulegroupstatement-excludedrules
            '''
            result = self._values.get("excluded_rules")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.ExcludedRuleProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedRuleGroupStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.NotStatementOneProperty",
        jsii_struct_bases=[],
        name_mapping={"statement": "statement"},
    )
    class NotStatementOneProperty:
        def __init__(
            self,
            *,
            statement: typing.Union["CfnWebACL.StatementTwoProperty", _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param statement: ``CfnWebACL.NotStatementOneProperty.Statement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-notstatementone.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "statement": statement,
            }

        @builtins.property
        def statement(
            self,
        ) -> typing.Union["CfnWebACL.StatementTwoProperty", _IResolvable_a771d0ef]:
            '''``CfnWebACL.NotStatementOneProperty.Statement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-notstatementone.html#cfn-wafv2-webacl-notstatementone-statement
            '''
            result = self._values.get("statement")
            assert result is not None, "Required property 'statement' is missing"
            return typing.cast(typing.Union["CfnWebACL.StatementTwoProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotStatementOneProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.NotStatementTwoProperty",
        jsii_struct_bases=[],
        name_mapping={"statement": "statement"},
    )
    class NotStatementTwoProperty:
        def __init__(
            self,
            *,
            statement: typing.Union["CfnWebACL.StatementThreeProperty", _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param statement: ``CfnWebACL.NotStatementTwoProperty.Statement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-notstatementtwo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "statement": statement,
            }

        @builtins.property
        def statement(
            self,
        ) -> typing.Union["CfnWebACL.StatementThreeProperty", _IResolvable_a771d0ef]:
            '''``CfnWebACL.NotStatementTwoProperty.Statement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-notstatementtwo.html#cfn-wafv2-webacl-notstatementtwo-statement
            '''
            result = self._values.get("statement")
            assert result is not None, "Required property 'statement' is missing"
            return typing.cast(typing.Union["CfnWebACL.StatementThreeProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotStatementTwoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.OrStatementOneProperty",
        jsii_struct_bases=[],
        name_mapping={"statements": "statements"},
    )
    class OrStatementOneProperty:
        def __init__(
            self,
            *,
            statements: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.StatementTwoProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param statements: ``CfnWebACL.OrStatementOneProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-orstatementone.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "statements": statements,
            }

        @builtins.property
        def statements(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.StatementTwoProperty", _IResolvable_a771d0ef]]]:
            '''``CfnWebACL.OrStatementOneProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-orstatementone.html#cfn-wafv2-webacl-orstatementone-statements
            '''
            result = self._values.get("statements")
            assert result is not None, "Required property 'statements' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.StatementTwoProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrStatementOneProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.OrStatementTwoProperty",
        jsii_struct_bases=[],
        name_mapping={"statements": "statements"},
    )
    class OrStatementTwoProperty:
        def __init__(
            self,
            *,
            statements: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.StatementThreeProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param statements: ``CfnWebACL.OrStatementTwoProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-orstatementtwo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "statements": statements,
            }

        @builtins.property
        def statements(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.StatementThreeProperty", _IResolvable_a771d0ef]]]:
            '''``CfnWebACL.OrStatementTwoProperty.Statements``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-orstatementtwo.html#cfn-wafv2-webacl-orstatementtwo-statements
            '''
            result = self._values.get("statements")
            assert result is not None, "Required property 'statements' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.StatementThreeProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrStatementTwoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.OverrideActionProperty",
        jsii_struct_bases=[],
        name_mapping={"count": "count", "none": "none"},
    )
    class OverrideActionProperty:
        def __init__(
            self,
            *,
            count: typing.Any = None,
            none: typing.Any = None,
        ) -> None:
            '''
            :param count: ``CfnWebACL.OverrideActionProperty.Count``.
            :param none: ``CfnWebACL.OverrideActionProperty.None``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-overrideaction.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count
            if none is not None:
                self._values["none"] = none

        @builtins.property
        def count(self) -> typing.Any:
            '''``CfnWebACL.OverrideActionProperty.Count``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-overrideaction.html#cfn-wafv2-webacl-overrideaction-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Any, result)

        @builtins.property
        def none(self) -> typing.Any:
            '''``CfnWebACL.OverrideActionProperty.None``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-overrideaction.html#cfn-wafv2-webacl-overrideaction-none
            '''
            result = self._values.get("none")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OverrideActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.RateBasedStatementOneProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregate_key_type": "aggregateKeyType",
            "limit": "limit",
            "forwarded_ip_config": "forwardedIpConfig",
            "scope_down_statement": "scopeDownStatement",
        },
    )
    class RateBasedStatementOneProperty:
        def __init__(
            self,
            *,
            aggregate_key_type: builtins.str,
            limit: jsii.Number,
            forwarded_ip_config: typing.Optional[typing.Union["CfnWebACL.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]] = None,
            scope_down_statement: typing.Optional[typing.Union["CfnWebACL.StatementTwoProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param aggregate_key_type: ``CfnWebACL.RateBasedStatementOneProperty.AggregateKeyType``.
            :param limit: ``CfnWebACL.RateBasedStatementOneProperty.Limit``.
            :param forwarded_ip_config: ``CfnWebACL.RateBasedStatementOneProperty.ForwardedIPConfig``.
            :param scope_down_statement: ``CfnWebACL.RateBasedStatementOneProperty.ScopeDownStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ratebasedstatementone.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "aggregate_key_type": aggregate_key_type,
                "limit": limit,
            }
            if forwarded_ip_config is not None:
                self._values["forwarded_ip_config"] = forwarded_ip_config
            if scope_down_statement is not None:
                self._values["scope_down_statement"] = scope_down_statement

        @builtins.property
        def aggregate_key_type(self) -> builtins.str:
            '''``CfnWebACL.RateBasedStatementOneProperty.AggregateKeyType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ratebasedstatementone.html#cfn-wafv2-webacl-ratebasedstatementone-aggregatekeytype
            '''
            result = self._values.get("aggregate_key_type")
            assert result is not None, "Required property 'aggregate_key_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def limit(self) -> jsii.Number:
            '''``CfnWebACL.RateBasedStatementOneProperty.Limit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ratebasedstatementone.html#cfn-wafv2-webacl-ratebasedstatementone-limit
            '''
            result = self._values.get("limit")
            assert result is not None, "Required property 'limit' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def forwarded_ip_config(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.RateBasedStatementOneProperty.ForwardedIPConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ratebasedstatementone.html#cfn-wafv2-webacl-ratebasedstatementone-forwardedipconfig
            '''
            result = self._values.get("forwarded_ip_config")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def scope_down_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.StatementTwoProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.RateBasedStatementOneProperty.ScopeDownStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ratebasedstatementone.html#cfn-wafv2-webacl-ratebasedstatementone-scopedownstatement
            '''
            result = self._values.get("scope_down_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.StatementTwoProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RateBasedStatementOneProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.RateBasedStatementTwoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregate_key_type": "aggregateKeyType",
            "limit": "limit",
            "forwarded_ip_config": "forwardedIpConfig",
            "scope_down_statement": "scopeDownStatement",
        },
    )
    class RateBasedStatementTwoProperty:
        def __init__(
            self,
            *,
            aggregate_key_type: builtins.str,
            limit: jsii.Number,
            forwarded_ip_config: typing.Optional[typing.Union["CfnWebACL.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]] = None,
            scope_down_statement: typing.Optional[typing.Union["CfnWebACL.StatementThreeProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param aggregate_key_type: ``CfnWebACL.RateBasedStatementTwoProperty.AggregateKeyType``.
            :param limit: ``CfnWebACL.RateBasedStatementTwoProperty.Limit``.
            :param forwarded_ip_config: ``CfnWebACL.RateBasedStatementTwoProperty.ForwardedIPConfig``.
            :param scope_down_statement: ``CfnWebACL.RateBasedStatementTwoProperty.ScopeDownStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ratebasedstatementtwo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "aggregate_key_type": aggregate_key_type,
                "limit": limit,
            }
            if forwarded_ip_config is not None:
                self._values["forwarded_ip_config"] = forwarded_ip_config
            if scope_down_statement is not None:
                self._values["scope_down_statement"] = scope_down_statement

        @builtins.property
        def aggregate_key_type(self) -> builtins.str:
            '''``CfnWebACL.RateBasedStatementTwoProperty.AggregateKeyType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ratebasedstatementtwo.html#cfn-wafv2-webacl-ratebasedstatementtwo-aggregatekeytype
            '''
            result = self._values.get("aggregate_key_type")
            assert result is not None, "Required property 'aggregate_key_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def limit(self) -> jsii.Number:
            '''``CfnWebACL.RateBasedStatementTwoProperty.Limit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ratebasedstatementtwo.html#cfn-wafv2-webacl-ratebasedstatementtwo-limit
            '''
            result = self._values.get("limit")
            assert result is not None, "Required property 'limit' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def forwarded_ip_config(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.RateBasedStatementTwoProperty.ForwardedIPConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ratebasedstatementtwo.html#cfn-wafv2-webacl-ratebasedstatementtwo-forwardedipconfig
            '''
            result = self._values.get("forwarded_ip_config")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.ForwardedIPConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def scope_down_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.StatementThreeProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.RateBasedStatementTwoProperty.ScopeDownStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ratebasedstatementtwo.html#cfn-wafv2-webacl-ratebasedstatementtwo-scopedownstatement
            '''
            result = self._values.get("scope_down_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.StatementThreeProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RateBasedStatementTwoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.RegexPatternSetReferenceStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "field_to_match": "fieldToMatch",
            "text_transformations": "textTransformations",
        },
    )
    class RegexPatternSetReferenceStatementProperty:
        def __init__(
            self,
            *,
            arn: builtins.str,
            field_to_match: typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef],
            text_transformations: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param arn: ``CfnWebACL.RegexPatternSetReferenceStatementProperty.Arn``.
            :param field_to_match: ``CfnWebACL.RegexPatternSetReferenceStatementProperty.FieldToMatch``.
            :param text_transformations: ``CfnWebACL.RegexPatternSetReferenceStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-regexpatternsetreferencestatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "arn": arn,
                "field_to_match": field_to_match,
                "text_transformations": text_transformations,
            }

        @builtins.property
        def arn(self) -> builtins.str:
            '''``CfnWebACL.RegexPatternSetReferenceStatementProperty.Arn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-regexpatternsetreferencestatement.html#cfn-wafv2-webacl-regexpatternsetreferencestatement-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef]:
            '''``CfnWebACL.RegexPatternSetReferenceStatementProperty.FieldToMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-regexpatternsetreferencestatement.html#cfn-wafv2-webacl-regexpatternsetreferencestatement-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def text_transformations(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]]:
            '''``CfnWebACL.RegexPatternSetReferenceStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-regexpatternsetreferencestatement.html#cfn-wafv2-webacl-regexpatternsetreferencestatement-texttransformations
            '''
            result = self._values.get("text_transformations")
            assert result is not None, "Required property 'text_transformations' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegexPatternSetReferenceStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.RuleActionProperty",
        jsii_struct_bases=[],
        name_mapping={"allow": "allow", "block": "block", "count": "count"},
    )
    class RuleActionProperty:
        def __init__(
            self,
            *,
            allow: typing.Any = None,
            block: typing.Any = None,
            count: typing.Any = None,
        ) -> None:
            '''
            :param allow: ``CfnWebACL.RuleActionProperty.Allow``.
            :param block: ``CfnWebACL.RuleActionProperty.Block``.
            :param count: ``CfnWebACL.RuleActionProperty.Count``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ruleaction.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if allow is not None:
                self._values["allow"] = allow
            if block is not None:
                self._values["block"] = block
            if count is not None:
                self._values["count"] = count

        @builtins.property
        def allow(self) -> typing.Any:
            '''``CfnWebACL.RuleActionProperty.Allow``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ruleaction.html#cfn-wafv2-webacl-ruleaction-allow
            '''
            result = self._values.get("allow")
            return typing.cast(typing.Any, result)

        @builtins.property
        def block(self) -> typing.Any:
            '''``CfnWebACL.RuleActionProperty.Block``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ruleaction.html#cfn-wafv2-webacl-ruleaction-block
            '''
            result = self._values.get("block")
            return typing.cast(typing.Any, result)

        @builtins.property
        def count(self) -> typing.Any:
            '''``CfnWebACL.RuleActionProperty.Count``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-ruleaction.html#cfn-wafv2-webacl-ruleaction-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.RuleGroupReferenceStatementProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "excluded_rules": "excludedRules"},
    )
    class RuleGroupReferenceStatementProperty:
        def __init__(
            self,
            *,
            arn: builtins.str,
            excluded_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.ExcludedRuleProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param arn: ``CfnWebACL.RuleGroupReferenceStatementProperty.Arn``.
            :param excluded_rules: ``CfnWebACL.RuleGroupReferenceStatementProperty.ExcludedRules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-rulegroupreferencestatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "arn": arn,
            }
            if excluded_rules is not None:
                self._values["excluded_rules"] = excluded_rules

        @builtins.property
        def arn(self) -> builtins.str:
            '''``CfnWebACL.RuleGroupReferenceStatementProperty.Arn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-rulegroupreferencestatement.html#cfn-wafv2-webacl-rulegroupreferencestatement-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def excluded_rules(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.ExcludedRuleProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnWebACL.RuleGroupReferenceStatementProperty.ExcludedRules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-rulegroupreferencestatement.html#cfn-wafv2-webacl-rulegroupreferencestatement-excludedrules
            '''
            result = self._values.get("excluded_rules")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.ExcludedRuleProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleGroupReferenceStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "priority": "priority",
            "statement": "statement",
            "visibility_config": "visibilityConfig",
            "action": "action",
            "override_action": "overrideAction",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            priority: jsii.Number,
            statement: typing.Union["CfnWebACL.StatementOneProperty", _IResolvable_a771d0ef],
            visibility_config: typing.Union["CfnWebACL.VisibilityConfigProperty", _IResolvable_a771d0ef],
            action: typing.Optional[typing.Union["CfnWebACL.RuleActionProperty", _IResolvable_a771d0ef]] = None,
            override_action: typing.Optional[typing.Union["CfnWebACL.OverrideActionProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param name: ``CfnWebACL.RuleProperty.Name``.
            :param priority: ``CfnWebACL.RuleProperty.Priority``.
            :param statement: ``CfnWebACL.RuleProperty.Statement``.
            :param visibility_config: ``CfnWebACL.RuleProperty.VisibilityConfig``.
            :param action: ``CfnWebACL.RuleProperty.Action``.
            :param override_action: ``CfnWebACL.RuleProperty.OverrideAction``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-rule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "priority": priority,
                "statement": statement,
                "visibility_config": visibility_config,
            }
            if action is not None:
                self._values["action"] = action
            if override_action is not None:
                self._values["override_action"] = override_action

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnWebACL.RuleProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-rule.html#cfn-wafv2-webacl-rule-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def priority(self) -> jsii.Number:
            '''``CfnWebACL.RuleProperty.Priority``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-rule.html#cfn-wafv2-webacl-rule-priority
            '''
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def statement(
            self,
        ) -> typing.Union["CfnWebACL.StatementOneProperty", _IResolvable_a771d0ef]:
            '''``CfnWebACL.RuleProperty.Statement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-rule.html#cfn-wafv2-webacl-rule-statement
            '''
            result = self._values.get("statement")
            assert result is not None, "Required property 'statement' is missing"
            return typing.cast(typing.Union["CfnWebACL.StatementOneProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def visibility_config(
            self,
        ) -> typing.Union["CfnWebACL.VisibilityConfigProperty", _IResolvable_a771d0ef]:
            '''``CfnWebACL.RuleProperty.VisibilityConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-rule.html#cfn-wafv2-webacl-rule-visibilityconfig
            '''
            result = self._values.get("visibility_config")
            assert result is not None, "Required property 'visibility_config' is missing"
            return typing.cast(typing.Union["CfnWebACL.VisibilityConfigProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.RuleActionProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.RuleProperty.Action``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-rule.html#cfn-wafv2-webacl-rule-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.RuleActionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def override_action(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.OverrideActionProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.RuleProperty.OverrideAction``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-rule.html#cfn-wafv2-webacl-rule-overrideaction
            '''
            result = self._values.get("override_action")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.OverrideActionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.SizeConstraintStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "field_to_match": "fieldToMatch",
            "size": "size",
            "text_transformations": "textTransformations",
        },
    )
    class SizeConstraintStatementProperty:
        def __init__(
            self,
            *,
            comparison_operator: builtins.str,
            field_to_match: typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef],
            size: jsii.Number,
            text_transformations: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param comparison_operator: ``CfnWebACL.SizeConstraintStatementProperty.ComparisonOperator``.
            :param field_to_match: ``CfnWebACL.SizeConstraintStatementProperty.FieldToMatch``.
            :param size: ``CfnWebACL.SizeConstraintStatementProperty.Size``.
            :param text_transformations: ``CfnWebACL.SizeConstraintStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-sizeconstraintstatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "comparison_operator": comparison_operator,
                "field_to_match": field_to_match,
                "size": size,
                "text_transformations": text_transformations,
            }

        @builtins.property
        def comparison_operator(self) -> builtins.str:
            '''``CfnWebACL.SizeConstraintStatementProperty.ComparisonOperator``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-sizeconstraintstatement.html#cfn-wafv2-webacl-sizeconstraintstatement-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            assert result is not None, "Required property 'comparison_operator' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef]:
            '''``CfnWebACL.SizeConstraintStatementProperty.FieldToMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-sizeconstraintstatement.html#cfn-wafv2-webacl-sizeconstraintstatement-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def size(self) -> jsii.Number:
            '''``CfnWebACL.SizeConstraintStatementProperty.Size``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-sizeconstraintstatement.html#cfn-wafv2-webacl-sizeconstraintstatement-size
            '''
            result = self._values.get("size")
            assert result is not None, "Required property 'size' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def text_transformations(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]]:
            '''``CfnWebACL.SizeConstraintStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-sizeconstraintstatement.html#cfn-wafv2-webacl-sizeconstraintstatement-texttransformations
            '''
            result = self._values.get("text_transformations")
            assert result is not None, "Required property 'text_transformations' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SizeConstraintStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.SqliMatchStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_to_match": "fieldToMatch",
            "text_transformations": "textTransformations",
        },
    )
    class SqliMatchStatementProperty:
        def __init__(
            self,
            *,
            field_to_match: typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef],
            text_transformations: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param field_to_match: ``CfnWebACL.SqliMatchStatementProperty.FieldToMatch``.
            :param text_transformations: ``CfnWebACL.SqliMatchStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-sqlimatchstatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "field_to_match": field_to_match,
                "text_transformations": text_transformations,
            }

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef]:
            '''``CfnWebACL.SqliMatchStatementProperty.FieldToMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-sqlimatchstatement.html#cfn-wafv2-webacl-sqlimatchstatement-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def text_transformations(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]]:
            '''``CfnWebACL.SqliMatchStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-sqlimatchstatement.html#cfn-wafv2-webacl-sqlimatchstatement-texttransformations
            '''
            result = self._values.get("text_transformations")
            assert result is not None, "Required property 'text_transformations' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqliMatchStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.StatementOneProperty",
        jsii_struct_bases=[],
        name_mapping={
            "and_statement": "andStatement",
            "byte_match_statement": "byteMatchStatement",
            "geo_match_statement": "geoMatchStatement",
            "ip_set_reference_statement": "ipSetReferenceStatement",
            "managed_rule_group_statement": "managedRuleGroupStatement",
            "not_statement": "notStatement",
            "or_statement": "orStatement",
            "rate_based_statement": "rateBasedStatement",
            "regex_pattern_set_reference_statement": "regexPatternSetReferenceStatement",
            "rule_group_reference_statement": "ruleGroupReferenceStatement",
            "size_constraint_statement": "sizeConstraintStatement",
            "sqli_match_statement": "sqliMatchStatement",
            "xss_match_statement": "xssMatchStatement",
        },
    )
    class StatementOneProperty:
        def __init__(
            self,
            *,
            and_statement: typing.Optional[typing.Union["CfnWebACL.AndStatementOneProperty", _IResolvable_a771d0ef]] = None,
            byte_match_statement: typing.Optional[typing.Union["CfnWebACL.ByteMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            geo_match_statement: typing.Optional[typing.Union["CfnWebACL.GeoMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            ip_set_reference_statement: typing.Optional[typing.Union["CfnWebACL.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            managed_rule_group_statement: typing.Optional[typing.Union["CfnWebACL.ManagedRuleGroupStatementProperty", _IResolvable_a771d0ef]] = None,
            not_statement: typing.Optional[typing.Union["CfnWebACL.NotStatementOneProperty", _IResolvable_a771d0ef]] = None,
            or_statement: typing.Optional[typing.Union["CfnWebACL.OrStatementOneProperty", _IResolvable_a771d0ef]] = None,
            rate_based_statement: typing.Optional[typing.Union["CfnWebACL.RateBasedStatementOneProperty", _IResolvable_a771d0ef]] = None,
            regex_pattern_set_reference_statement: typing.Optional[typing.Union["CfnWebACL.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            rule_group_reference_statement: typing.Optional[typing.Union["CfnWebACL.RuleGroupReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            size_constraint_statement: typing.Optional[typing.Union["CfnWebACL.SizeConstraintStatementProperty", _IResolvable_a771d0ef]] = None,
            sqli_match_statement: typing.Optional[typing.Union["CfnWebACL.SqliMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            xss_match_statement: typing.Optional[typing.Union["CfnWebACL.XssMatchStatementProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param and_statement: ``CfnWebACL.StatementOneProperty.AndStatement``.
            :param byte_match_statement: ``CfnWebACL.StatementOneProperty.ByteMatchStatement``.
            :param geo_match_statement: ``CfnWebACL.StatementOneProperty.GeoMatchStatement``.
            :param ip_set_reference_statement: ``CfnWebACL.StatementOneProperty.IPSetReferenceStatement``.
            :param managed_rule_group_statement: ``CfnWebACL.StatementOneProperty.ManagedRuleGroupStatement``.
            :param not_statement: ``CfnWebACL.StatementOneProperty.NotStatement``.
            :param or_statement: ``CfnWebACL.StatementOneProperty.OrStatement``.
            :param rate_based_statement: ``CfnWebACL.StatementOneProperty.RateBasedStatement``.
            :param regex_pattern_set_reference_statement: ``CfnWebACL.StatementOneProperty.RegexPatternSetReferenceStatement``.
            :param rule_group_reference_statement: ``CfnWebACL.StatementOneProperty.RuleGroupReferenceStatement``.
            :param size_constraint_statement: ``CfnWebACL.StatementOneProperty.SizeConstraintStatement``.
            :param sqli_match_statement: ``CfnWebACL.StatementOneProperty.SqliMatchStatement``.
            :param xss_match_statement: ``CfnWebACL.StatementOneProperty.XssMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if and_statement is not None:
                self._values["and_statement"] = and_statement
            if byte_match_statement is not None:
                self._values["byte_match_statement"] = byte_match_statement
            if geo_match_statement is not None:
                self._values["geo_match_statement"] = geo_match_statement
            if ip_set_reference_statement is not None:
                self._values["ip_set_reference_statement"] = ip_set_reference_statement
            if managed_rule_group_statement is not None:
                self._values["managed_rule_group_statement"] = managed_rule_group_statement
            if not_statement is not None:
                self._values["not_statement"] = not_statement
            if or_statement is not None:
                self._values["or_statement"] = or_statement
            if rate_based_statement is not None:
                self._values["rate_based_statement"] = rate_based_statement
            if regex_pattern_set_reference_statement is not None:
                self._values["regex_pattern_set_reference_statement"] = regex_pattern_set_reference_statement
            if rule_group_reference_statement is not None:
                self._values["rule_group_reference_statement"] = rule_group_reference_statement
            if size_constraint_statement is not None:
                self._values["size_constraint_statement"] = size_constraint_statement
            if sqli_match_statement is not None:
                self._values["sqli_match_statement"] = sqli_match_statement
            if xss_match_statement is not None:
                self._values["xss_match_statement"] = xss_match_statement

        @builtins.property
        def and_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.AndStatementOneProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.AndStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-andstatement
            '''
            result = self._values.get("and_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.AndStatementOneProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def byte_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.ByteMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.ByteMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-bytematchstatement
            '''
            result = self._values.get("byte_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.ByteMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def geo_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.GeoMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.GeoMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-geomatchstatement
            '''
            result = self._values.get("geo_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.GeoMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ip_set_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.IPSetReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-ipsetreferencestatement
            '''
            result = self._values.get("ip_set_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def managed_rule_group_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.ManagedRuleGroupStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.ManagedRuleGroupStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-managedrulegroupstatement
            '''
            result = self._values.get("managed_rule_group_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.ManagedRuleGroupStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def not_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.NotStatementOneProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.NotStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-notstatement
            '''
            result = self._values.get("not_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.NotStatementOneProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def or_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.OrStatementOneProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.OrStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-orstatement
            '''
            result = self._values.get("or_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.OrStatementOneProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rate_based_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.RateBasedStatementOneProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.RateBasedStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-ratebasedstatement
            '''
            result = self._values.get("rate_based_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.RateBasedStatementOneProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def regex_pattern_set_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.RegexPatternSetReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-regexpatternsetreferencestatement
            '''
            result = self._values.get("regex_pattern_set_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rule_group_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.RuleGroupReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.RuleGroupReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-rulegroupreferencestatement
            '''
            result = self._values.get("rule_group_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.RuleGroupReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def size_constraint_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.SizeConstraintStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.SizeConstraintStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-sizeconstraintstatement
            '''
            result = self._values.get("size_constraint_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.SizeConstraintStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sqli_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.SqliMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.SqliMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-sqlimatchstatement
            '''
            result = self._values.get("sqli_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.SqliMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def xss_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.XssMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementOneProperty.XssMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementone.html#cfn-wafv2-webacl-statementone-xssmatchstatement
            '''
            result = self._values.get("xss_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.XssMatchStatementProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatementOneProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.StatementThreeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "byte_match_statement": "byteMatchStatement",
            "geo_match_statement": "geoMatchStatement",
            "ip_set_reference_statement": "ipSetReferenceStatement",
            "managed_rule_group_statement": "managedRuleGroupStatement",
            "regex_pattern_set_reference_statement": "regexPatternSetReferenceStatement",
            "rule_group_reference_statement": "ruleGroupReferenceStatement",
            "size_constraint_statement": "sizeConstraintStatement",
            "sqli_match_statement": "sqliMatchStatement",
            "xss_match_statement": "xssMatchStatement",
        },
    )
    class StatementThreeProperty:
        def __init__(
            self,
            *,
            byte_match_statement: typing.Optional[typing.Union["CfnWebACL.ByteMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            geo_match_statement: typing.Optional[typing.Union["CfnWebACL.GeoMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            ip_set_reference_statement: typing.Optional[typing.Union["CfnWebACL.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            managed_rule_group_statement: typing.Optional[typing.Union["CfnWebACL.ManagedRuleGroupStatementProperty", _IResolvable_a771d0ef]] = None,
            regex_pattern_set_reference_statement: typing.Optional[typing.Union["CfnWebACL.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            rule_group_reference_statement: typing.Optional[typing.Union["CfnWebACL.RuleGroupReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            size_constraint_statement: typing.Optional[typing.Union["CfnWebACL.SizeConstraintStatementProperty", _IResolvable_a771d0ef]] = None,
            sqli_match_statement: typing.Optional[typing.Union["CfnWebACL.SqliMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            xss_match_statement: typing.Optional[typing.Union["CfnWebACL.XssMatchStatementProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param byte_match_statement: ``CfnWebACL.StatementThreeProperty.ByteMatchStatement``.
            :param geo_match_statement: ``CfnWebACL.StatementThreeProperty.GeoMatchStatement``.
            :param ip_set_reference_statement: ``CfnWebACL.StatementThreeProperty.IPSetReferenceStatement``.
            :param managed_rule_group_statement: ``CfnWebACL.StatementThreeProperty.ManagedRuleGroupStatement``.
            :param regex_pattern_set_reference_statement: ``CfnWebACL.StatementThreeProperty.RegexPatternSetReferenceStatement``.
            :param rule_group_reference_statement: ``CfnWebACL.StatementThreeProperty.RuleGroupReferenceStatement``.
            :param size_constraint_statement: ``CfnWebACL.StatementThreeProperty.SizeConstraintStatement``.
            :param sqli_match_statement: ``CfnWebACL.StatementThreeProperty.SqliMatchStatement``.
            :param xss_match_statement: ``CfnWebACL.StatementThreeProperty.XssMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementthree.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if byte_match_statement is not None:
                self._values["byte_match_statement"] = byte_match_statement
            if geo_match_statement is not None:
                self._values["geo_match_statement"] = geo_match_statement
            if ip_set_reference_statement is not None:
                self._values["ip_set_reference_statement"] = ip_set_reference_statement
            if managed_rule_group_statement is not None:
                self._values["managed_rule_group_statement"] = managed_rule_group_statement
            if regex_pattern_set_reference_statement is not None:
                self._values["regex_pattern_set_reference_statement"] = regex_pattern_set_reference_statement
            if rule_group_reference_statement is not None:
                self._values["rule_group_reference_statement"] = rule_group_reference_statement
            if size_constraint_statement is not None:
                self._values["size_constraint_statement"] = size_constraint_statement
            if sqli_match_statement is not None:
                self._values["sqli_match_statement"] = sqli_match_statement
            if xss_match_statement is not None:
                self._values["xss_match_statement"] = xss_match_statement

        @builtins.property
        def byte_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.ByteMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementThreeProperty.ByteMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementthree.html#cfn-wafv2-webacl-statementthree-bytematchstatement
            '''
            result = self._values.get("byte_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.ByteMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def geo_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.GeoMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementThreeProperty.GeoMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementthree.html#cfn-wafv2-webacl-statementthree-geomatchstatement
            '''
            result = self._values.get("geo_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.GeoMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ip_set_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementThreeProperty.IPSetReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementthree.html#cfn-wafv2-webacl-statementthree-ipsetreferencestatement
            '''
            result = self._values.get("ip_set_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def managed_rule_group_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.ManagedRuleGroupStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementThreeProperty.ManagedRuleGroupStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementthree.html#cfn-wafv2-webacl-statementthree-managedrulegroupstatement
            '''
            result = self._values.get("managed_rule_group_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.ManagedRuleGroupStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def regex_pattern_set_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementThreeProperty.RegexPatternSetReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementthree.html#cfn-wafv2-webacl-statementthree-regexpatternsetreferencestatement
            '''
            result = self._values.get("regex_pattern_set_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rule_group_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.RuleGroupReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementThreeProperty.RuleGroupReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementthree.html#cfn-wafv2-webacl-statementthree-rulegroupreferencestatement
            '''
            result = self._values.get("rule_group_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.RuleGroupReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def size_constraint_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.SizeConstraintStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementThreeProperty.SizeConstraintStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementthree.html#cfn-wafv2-webacl-statementthree-sizeconstraintstatement
            '''
            result = self._values.get("size_constraint_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.SizeConstraintStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sqli_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.SqliMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementThreeProperty.SqliMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementthree.html#cfn-wafv2-webacl-statementthree-sqlimatchstatement
            '''
            result = self._values.get("sqli_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.SqliMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def xss_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.XssMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementThreeProperty.XssMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementthree.html#cfn-wafv2-webacl-statementthree-xssmatchstatement
            '''
            result = self._values.get("xss_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.XssMatchStatementProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatementThreeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.StatementTwoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "and_statement": "andStatement",
            "byte_match_statement": "byteMatchStatement",
            "geo_match_statement": "geoMatchStatement",
            "ip_set_reference_statement": "ipSetReferenceStatement",
            "managed_rule_group_statement": "managedRuleGroupStatement",
            "not_statement": "notStatement",
            "or_statement": "orStatement",
            "rate_based_statement": "rateBasedStatement",
            "regex_pattern_set_reference_statement": "regexPatternSetReferenceStatement",
            "rule_group_reference_statement": "ruleGroupReferenceStatement",
            "size_constraint_statement": "sizeConstraintStatement",
            "sqli_match_statement": "sqliMatchStatement",
            "xss_match_statement": "xssMatchStatement",
        },
    )
    class StatementTwoProperty:
        def __init__(
            self,
            *,
            and_statement: typing.Optional[typing.Union["CfnWebACL.AndStatementTwoProperty", _IResolvable_a771d0ef]] = None,
            byte_match_statement: typing.Optional[typing.Union["CfnWebACL.ByteMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            geo_match_statement: typing.Optional[typing.Union["CfnWebACL.GeoMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            ip_set_reference_statement: typing.Optional[typing.Union["CfnWebACL.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            managed_rule_group_statement: typing.Optional[typing.Union["CfnWebACL.ManagedRuleGroupStatementProperty", _IResolvable_a771d0ef]] = None,
            not_statement: typing.Optional[typing.Union["CfnWebACL.NotStatementTwoProperty", _IResolvable_a771d0ef]] = None,
            or_statement: typing.Optional[typing.Union["CfnWebACL.OrStatementTwoProperty", _IResolvable_a771d0ef]] = None,
            rate_based_statement: typing.Optional[typing.Union["CfnWebACL.RateBasedStatementTwoProperty", _IResolvable_a771d0ef]] = None,
            regex_pattern_set_reference_statement: typing.Optional[typing.Union["CfnWebACL.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            rule_group_reference_statement: typing.Optional[typing.Union["CfnWebACL.RuleGroupReferenceStatementProperty", _IResolvable_a771d0ef]] = None,
            size_constraint_statement: typing.Optional[typing.Union["CfnWebACL.SizeConstraintStatementProperty", _IResolvable_a771d0ef]] = None,
            sqli_match_statement: typing.Optional[typing.Union["CfnWebACL.SqliMatchStatementProperty", _IResolvable_a771d0ef]] = None,
            xss_match_statement: typing.Optional[typing.Union["CfnWebACL.XssMatchStatementProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param and_statement: ``CfnWebACL.StatementTwoProperty.AndStatement``.
            :param byte_match_statement: ``CfnWebACL.StatementTwoProperty.ByteMatchStatement``.
            :param geo_match_statement: ``CfnWebACL.StatementTwoProperty.GeoMatchStatement``.
            :param ip_set_reference_statement: ``CfnWebACL.StatementTwoProperty.IPSetReferenceStatement``.
            :param managed_rule_group_statement: ``CfnWebACL.StatementTwoProperty.ManagedRuleGroupStatement``.
            :param not_statement: ``CfnWebACL.StatementTwoProperty.NotStatement``.
            :param or_statement: ``CfnWebACL.StatementTwoProperty.OrStatement``.
            :param rate_based_statement: ``CfnWebACL.StatementTwoProperty.RateBasedStatement``.
            :param regex_pattern_set_reference_statement: ``CfnWebACL.StatementTwoProperty.RegexPatternSetReferenceStatement``.
            :param rule_group_reference_statement: ``CfnWebACL.StatementTwoProperty.RuleGroupReferenceStatement``.
            :param size_constraint_statement: ``CfnWebACL.StatementTwoProperty.SizeConstraintStatement``.
            :param sqli_match_statement: ``CfnWebACL.StatementTwoProperty.SqliMatchStatement``.
            :param xss_match_statement: ``CfnWebACL.StatementTwoProperty.XssMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if and_statement is not None:
                self._values["and_statement"] = and_statement
            if byte_match_statement is not None:
                self._values["byte_match_statement"] = byte_match_statement
            if geo_match_statement is not None:
                self._values["geo_match_statement"] = geo_match_statement
            if ip_set_reference_statement is not None:
                self._values["ip_set_reference_statement"] = ip_set_reference_statement
            if managed_rule_group_statement is not None:
                self._values["managed_rule_group_statement"] = managed_rule_group_statement
            if not_statement is not None:
                self._values["not_statement"] = not_statement
            if or_statement is not None:
                self._values["or_statement"] = or_statement
            if rate_based_statement is not None:
                self._values["rate_based_statement"] = rate_based_statement
            if regex_pattern_set_reference_statement is not None:
                self._values["regex_pattern_set_reference_statement"] = regex_pattern_set_reference_statement
            if rule_group_reference_statement is not None:
                self._values["rule_group_reference_statement"] = rule_group_reference_statement
            if size_constraint_statement is not None:
                self._values["size_constraint_statement"] = size_constraint_statement
            if sqli_match_statement is not None:
                self._values["sqli_match_statement"] = sqli_match_statement
            if xss_match_statement is not None:
                self._values["xss_match_statement"] = xss_match_statement

        @builtins.property
        def and_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.AndStatementTwoProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.AndStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-andstatement
            '''
            result = self._values.get("and_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.AndStatementTwoProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def byte_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.ByteMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.ByteMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-bytematchstatement
            '''
            result = self._values.get("byte_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.ByteMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def geo_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.GeoMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.GeoMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-geomatchstatement
            '''
            result = self._values.get("geo_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.GeoMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def ip_set_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.IPSetReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-ipsetreferencestatement
            '''
            result = self._values.get("ip_set_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.IPSetReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def managed_rule_group_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.ManagedRuleGroupStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.ManagedRuleGroupStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-managedrulegroupstatement
            '''
            result = self._values.get("managed_rule_group_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.ManagedRuleGroupStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def not_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.NotStatementTwoProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.NotStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-notstatement
            '''
            result = self._values.get("not_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.NotStatementTwoProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def or_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.OrStatementTwoProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.OrStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-orstatement
            '''
            result = self._values.get("or_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.OrStatementTwoProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rate_based_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.RateBasedStatementTwoProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.RateBasedStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-ratebasedstatement
            '''
            result = self._values.get("rate_based_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.RateBasedStatementTwoProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def regex_pattern_set_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.RegexPatternSetReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-regexpatternsetreferencestatement
            '''
            result = self._values.get("regex_pattern_set_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.RegexPatternSetReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rule_group_reference_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.RuleGroupReferenceStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.RuleGroupReferenceStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-rulegroupreferencestatement
            '''
            result = self._values.get("rule_group_reference_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.RuleGroupReferenceStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def size_constraint_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.SizeConstraintStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.SizeConstraintStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-sizeconstraintstatement
            '''
            result = self._values.get("size_constraint_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.SizeConstraintStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sqli_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.SqliMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.SqliMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-sqlimatchstatement
            '''
            result = self._values.get("sqli_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.SqliMatchStatementProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def xss_match_statement(
            self,
        ) -> typing.Optional[typing.Union["CfnWebACL.XssMatchStatementProperty", _IResolvable_a771d0ef]]:
            '''``CfnWebACL.StatementTwoProperty.XssMatchStatement``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-statementtwo.html#cfn-wafv2-webacl-statementtwo-xssmatchstatement
            '''
            result = self._values.get("xss_match_statement")
            return typing.cast(typing.Optional[typing.Union["CfnWebACL.XssMatchStatementProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatementTwoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.TextTransformationProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "type": "type"},
    )
    class TextTransformationProperty:
        def __init__(self, *, priority: jsii.Number, type: builtins.str) -> None:
            '''
            :param priority: ``CfnWebACL.TextTransformationProperty.Priority``.
            :param type: ``CfnWebACL.TextTransformationProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-texttransformation.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "priority": priority,
                "type": type,
            }

        @builtins.property
        def priority(self) -> jsii.Number:
            '''``CfnWebACL.TextTransformationProperty.Priority``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-texttransformation.html#cfn-wafv2-webacl-texttransformation-priority
            '''
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnWebACL.TextTransformationProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-texttransformation.html#cfn-wafv2-webacl-texttransformation-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextTransformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.VisibilityConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_metrics_enabled": "cloudWatchMetricsEnabled",
            "metric_name": "metricName",
            "sampled_requests_enabled": "sampledRequestsEnabled",
        },
    )
    class VisibilityConfigProperty:
        def __init__(
            self,
            *,
            cloud_watch_metrics_enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            metric_name: builtins.str,
            sampled_requests_enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param cloud_watch_metrics_enabled: ``CfnWebACL.VisibilityConfigProperty.CloudWatchMetricsEnabled``.
            :param metric_name: ``CfnWebACL.VisibilityConfigProperty.MetricName``.
            :param sampled_requests_enabled: ``CfnWebACL.VisibilityConfigProperty.SampledRequestsEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-visibilityconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "cloud_watch_metrics_enabled": cloud_watch_metrics_enabled,
                "metric_name": metric_name,
                "sampled_requests_enabled": sampled_requests_enabled,
            }

        @builtins.property
        def cloud_watch_metrics_enabled(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnWebACL.VisibilityConfigProperty.CloudWatchMetricsEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-visibilityconfig.html#cfn-wafv2-webacl-visibilityconfig-cloudwatchmetricsenabled
            '''
            result = self._values.get("cloud_watch_metrics_enabled")
            assert result is not None, "Required property 'cloud_watch_metrics_enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def metric_name(self) -> builtins.str:
            '''``CfnWebACL.VisibilityConfigProperty.MetricName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-visibilityconfig.html#cfn-wafv2-webacl-visibilityconfig-metricname
            '''
            result = self._values.get("metric_name")
            assert result is not None, "Required property 'metric_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sampled_requests_enabled(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnWebACL.VisibilityConfigProperty.SampledRequestsEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-visibilityconfig.html#cfn-wafv2-webacl-visibilityconfig-sampledrequestsenabled
            '''
            result = self._values.get("sampled_requests_enabled")
            assert result is not None, "Required property 'sampled_requests_enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VisibilityConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wafv2.CfnWebACL.XssMatchStatementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_to_match": "fieldToMatch",
            "text_transformations": "textTransformations",
        },
    )
    class XssMatchStatementProperty:
        def __init__(
            self,
            *,
            field_to_match: typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef],
            text_transformations: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param field_to_match: ``CfnWebACL.XssMatchStatementProperty.FieldToMatch``.
            :param text_transformations: ``CfnWebACL.XssMatchStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-xssmatchstatement.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "field_to_match": field_to_match,
                "text_transformations": text_transformations,
            }

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef]:
            '''``CfnWebACL.XssMatchStatementProperty.FieldToMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-xssmatchstatement.html#cfn-wafv2-webacl-xssmatchstatement-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            assert result is not None, "Required property 'field_to_match' is missing"
            return typing.cast(typing.Union["CfnWebACL.FieldToMatchProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def text_transformations(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]]:
            '''``CfnWebACL.XssMatchStatementProperty.TextTransformations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafv2-webacl-xssmatchstatement.html#cfn-wafv2-webacl-xssmatchstatement-texttransformations
            '''
            result = self._values.get("text_transformations")
            assert result is not None, "Required property 'text_transformations' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnWebACL.TextTransformationProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "XssMatchStatementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnWebACLAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_wafv2.CfnWebACLAssociation",
):
    '''A CloudFormation ``AWS::WAFv2::WebACLAssociation``.

    :cloudformationResource: AWS::WAFv2::WebACLAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webaclassociation.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        resource_arn: builtins.str,
        web_acl_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::WAFv2::WebACLAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_arn: ``AWS::WAFv2::WebACLAssociation.ResourceArn``.
        :param web_acl_arn: ``AWS::WAFv2::WebACLAssociation.WebACLArn``.
        '''
        props = CfnWebACLAssociationProps(
            resource_arn=resource_arn, web_acl_arn=web_acl_arn
        )

        jsii.create(CfnWebACLAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        '''``AWS::WAFv2::WebACLAssociation.ResourceArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webaclassociation.html#cfn-wafv2-webaclassociation-resourcearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        jsii.set(self, "resourceArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="webAclArn")
    def web_acl_arn(self) -> builtins.str:
        '''``AWS::WAFv2::WebACLAssociation.WebACLArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webaclassociation.html#cfn-wafv2-webaclassociation-webaclarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "webAclArn"))

    @web_acl_arn.setter
    def web_acl_arn(self, value: builtins.str) -> None:
        jsii.set(self, "webAclArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_wafv2.CfnWebACLAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "web_acl_arn": "webAclArn"},
)
class CfnWebACLAssociationProps:
    def __init__(
        self,
        *,
        resource_arn: builtins.str,
        web_acl_arn: builtins.str,
    ) -> None:
        '''Properties for defining a ``AWS::WAFv2::WebACLAssociation``.

        :param resource_arn: ``AWS::WAFv2::WebACLAssociation.ResourceArn``.
        :param web_acl_arn: ``AWS::WAFv2::WebACLAssociation.WebACLArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webaclassociation.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "resource_arn": resource_arn,
            "web_acl_arn": web_acl_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''``AWS::WAFv2::WebACLAssociation.ResourceArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webaclassociation.html#cfn-wafv2-webaclassociation-resourcearn
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def web_acl_arn(self) -> builtins.str:
        '''``AWS::WAFv2::WebACLAssociation.WebACLArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webaclassociation.html#cfn-wafv2-webaclassociation-webaclarn
        '''
        result = self._values.get("web_acl_arn")
        assert result is not None, "Required property 'web_acl_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWebACLAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_wafv2.CfnWebACLProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_action": "defaultAction",
        "scope": "scope",
        "visibility_config": "visibilityConfig",
        "description": "description",
        "name": "name",
        "rules": "rules",
        "tags": "tags",
    },
)
class CfnWebACLProps:
    def __init__(
        self,
        *,
        default_action: typing.Union[CfnWebACL.DefaultActionProperty, _IResolvable_a771d0ef],
        scope: builtins.str,
        visibility_config: typing.Union[CfnWebACL.VisibilityConfigProperty, _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnWebACL.RuleProperty, _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::WAFv2::WebACL``.

        :param default_action: ``AWS::WAFv2::WebACL.DefaultAction``.
        :param scope: ``AWS::WAFv2::WebACL.Scope``.
        :param visibility_config: ``AWS::WAFv2::WebACL.VisibilityConfig``.
        :param description: ``AWS::WAFv2::WebACL.Description``.
        :param name: ``AWS::WAFv2::WebACL.Name``.
        :param rules: ``AWS::WAFv2::WebACL.Rules``.
        :param tags: ``AWS::WAFv2::WebACL.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "default_action": default_action,
            "scope": scope,
            "visibility_config": visibility_config,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if rules is not None:
            self._values["rules"] = rules
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def default_action(
        self,
    ) -> typing.Union[CfnWebACL.DefaultActionProperty, _IResolvable_a771d0ef]:
        '''``AWS::WAFv2::WebACL.DefaultAction``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-defaultaction
        '''
        result = self._values.get("default_action")
        assert result is not None, "Required property 'default_action' is missing"
        return typing.cast(typing.Union[CfnWebACL.DefaultActionProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''``AWS::WAFv2::WebACL.Scope``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-scope
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def visibility_config(
        self,
    ) -> typing.Union[CfnWebACL.VisibilityConfigProperty, _IResolvable_a771d0ef]:
        '''``AWS::WAFv2::WebACL.VisibilityConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-visibilityconfig
        '''
        result = self._values.get("visibility_config")
        assert result is not None, "Required property 'visibility_config' is missing"
        return typing.cast(typing.Union[CfnWebACL.VisibilityConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::WebACL.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::WAFv2::WebACL.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnWebACL.RuleProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::WAFv2::WebACL.Rules``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnWebACL.RuleProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::WAFv2::WebACL.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafv2-webacl.html#cfn-wafv2-webacl-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWebACLProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnIPSet",
    "CfnIPSetProps",
    "CfnRegexPatternSet",
    "CfnRegexPatternSetProps",
    "CfnRuleGroup",
    "CfnRuleGroupProps",
    "CfnWebACL",
    "CfnWebACLAssociation",
    "CfnWebACLAssociationProps",
    "CfnWebACLProps",
]

publication.publish()
