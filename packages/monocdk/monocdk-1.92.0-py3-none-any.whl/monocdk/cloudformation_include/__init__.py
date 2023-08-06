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
    CfnCondition as _CfnCondition_79795035,
    CfnElement as _CfnElement_3c01f138,
    CfnHook as _CfnHook_02bf9fbf,
    CfnMapping as _CfnMapping_40a28af7,
    CfnOutput as _CfnOutput_a4d857a8,
    CfnParameter as _CfnParameter_3e6f99ac,
    CfnResource as _CfnResource_e0a482dc,
    CfnRule as _CfnRule_c48d2c85,
    NestedStack as _NestedStack_9b94bddc,
)


class CfnInclude(
    _CfnElement_3c01f138,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.cloudformation_include.CfnInclude",
):
    '''(experimental) Construct to import an existing CloudFormation template file into a CDK application.

    All resources defined in the template file can be retrieved by calling the {@link getResource} method.
    Any modifications made on the returned resource objects will be reflected in the resulting CDK template.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        template_file: builtins.str,
        load_nested_stacks: typing.Optional[typing.Mapping[builtins.str, "CfnIncludeProps"]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        preserve_logical_ids: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param template_file: (experimental) Path to the template file. Both JSON and YAML template formats are supported.
        :param load_nested_stacks: (experimental) Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from the {@link CfnInclude.getNestedStack} method (but will still be accessible from the {@link CfnInclude.getResource} method). If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: (experimental) Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced
        :param preserve_logical_ids: (experimental) Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file. If you're vending a Construct using an existing CloudFormation template, make sure to pass this as ``false``. **Note**: regardless of whether this option is true or false, the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element, as specified in the template file. Default: true

        :stability: experimental
        '''
        props = CfnIncludeProps(
            template_file=template_file,
            load_nested_stacks=load_nested_stacks,
            parameters=parameters,
            preserve_logical_ids=preserve_logical_ids,
        )

        jsii.create(CfnInclude, self, [scope, id, props])

    @jsii.member(jsii_name="getCondition")
    def get_condition(self, condition_name: builtins.str) -> _CfnCondition_79795035:
        '''(experimental) Returns the CfnCondition object from the 'Conditions' section of the CloudFormation template with the given name.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Condition with the given name is not present in the template,
        throws an exception.

        :param condition_name: the name of the Condition in the CloudFormation template file.

        :stability: experimental
        '''
        return typing.cast(_CfnCondition_79795035, jsii.invoke(self, "getCondition", [condition_name]))

    @jsii.member(jsii_name="getHook")
    def get_hook(self, hook_logical_id: builtins.str) -> _CfnHook_02bf9fbf:
        '''(experimental) Returns the CfnHook object from the 'Hooks' section of the included CloudFormation template with the given logical ID.

        Any modifications performed on the returned object will be reflected in the resulting CDK template.

        If a Hook with the given logical ID is not present in the template,
        an exception will be thrown.

        :param hook_logical_id: the logical ID of the Hook in the included CloudFormation template's 'Hooks' section.

        :stability: experimental
        '''
        return typing.cast(_CfnHook_02bf9fbf, jsii.invoke(self, "getHook", [hook_logical_id]))

    @jsii.member(jsii_name="getMapping")
    def get_mapping(self, mapping_name: builtins.str) -> _CfnMapping_40a28af7:
        '''(experimental) Returns the CfnMapping object from the 'Mappings' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Mapping with the given name is not present in the template,
        an exception will be thrown.

        :param mapping_name: the name of the Mapping in the template to retrieve.

        :stability: experimental
        '''
        return typing.cast(_CfnMapping_40a28af7, jsii.invoke(self, "getMapping", [mapping_name]))

    @jsii.member(jsii_name="getNestedStack")
    def get_nested_stack(self, logical_id: builtins.str) -> "IncludedNestedStack":
        '''(experimental) Returns a loaded NestedStack with name logicalId.

        For a nested stack to be returned by this method,
        it must be specified either in the {@link CfnIncludeProps.loadNestedStacks} property,
        or through the {@link loadNestedStack} method.

        :param logical_id: the ID of the stack to retrieve, as it appears in the template.

        :stability: experimental
        '''
        return typing.cast("IncludedNestedStack", jsii.invoke(self, "getNestedStack", [logical_id]))

    @jsii.member(jsii_name="getOutput")
    def get_output(self, logical_id: builtins.str) -> _CfnOutput_a4d857a8:
        '''(experimental) Returns the CfnOutput object from the 'Outputs' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If an Output with the given name is not present in the template,
        throws an exception.

        :param logical_id: the name of the output to retrieve.

        :stability: experimental
        '''
        return typing.cast(_CfnOutput_a4d857a8, jsii.invoke(self, "getOutput", [logical_id]))

    @jsii.member(jsii_name="getParameter")
    def get_parameter(self, parameter_name: builtins.str) -> _CfnParameter_3e6f99ac:
        '''(experimental) Returns the CfnParameter object from the 'Parameters' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Parameter with the given name is not present in the template,
        throws an exception.

        :param parameter_name: the name of the parameter to retrieve.

        :stability: experimental
        '''
        return typing.cast(_CfnParameter_3e6f99ac, jsii.invoke(self, "getParameter", [parameter_name]))

    @jsii.member(jsii_name="getResource")
    def get_resource(self, logical_id: builtins.str) -> _CfnResource_e0a482dc:
        '''(experimental) Returns the low-level CfnResource from the template with the given logical ID.

        Any modifications performed on that resource will be reflected in the resulting CDK template.

        The returned object will be of the proper underlying class;
        you can always cast it to the correct type in your code::

            // assume the template contains an AWS::S3::Bucket with logical ID 'Bucket'
            const cfnBucket = cfnTemplate.getResource('Bucket') as s3.CfnBucket;
            // cfnBucket is of type s3.CfnBucket

        If the template does not contain a resource with the given logical ID,
        an exception will be thrown.

        :param logical_id: the logical ID of the resource in the CloudFormation template file.

        :stability: experimental
        '''
        return typing.cast(_CfnResource_e0a482dc, jsii.invoke(self, "getResource", [logical_id]))

    @jsii.member(jsii_name="getRule")
    def get_rule(self, rule_name: builtins.str) -> _CfnRule_c48d2c85:
        '''(experimental) Returns the CfnRule object from the 'Rules' section of the CloudFormation template with the given name.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Rule with the given name is not present in the template,
        an exception will be thrown.

        :param rule_name: the name of the Rule in the CloudFormation template.

        :stability: experimental
        '''
        return typing.cast(_CfnRule_c48d2c85, jsii.invoke(self, "getRule", [rule_name]))

    @jsii.member(jsii_name="loadNestedStack")
    def load_nested_stack(
        self,
        logical_id: builtins.str,
        *,
        template_file: builtins.str,
        load_nested_stacks: typing.Optional[typing.Mapping[builtins.str, "CfnIncludeProps"]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        preserve_logical_ids: typing.Optional[builtins.bool] = None,
    ) -> "IncludedNestedStack":
        '''(experimental) Includes a template for a child stack inside of this parent template.

        A child with this logical ID must exist in the template,
        and be of type AWS::CloudFormation::Stack.
        This is equivalent to specifying the value in the {@link CfnIncludeProps.loadNestedStacks}
        property on object construction.

        :param logical_id: the ID of the stack to retrieve, as it appears in the template.
        :param template_file: (experimental) Path to the template file. Both JSON and YAML template formats are supported.
        :param load_nested_stacks: (experimental) Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from the {@link CfnInclude.getNestedStack} method (but will still be accessible from the {@link CfnInclude.getResource} method). If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: (experimental) Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced
        :param preserve_logical_ids: (experimental) Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file. If you're vending a Construct using an existing CloudFormation template, make sure to pass this as ``false``. **Note**: regardless of whether this option is true or false, the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element, as specified in the template file. Default: true

        :return: the same {@link IncludedNestedStack} object that {@link getNestedStack} returns for this logical ID

        :stability: experimental
        '''
        nested_stack_props = CfnIncludeProps(
            template_file=template_file,
            load_nested_stacks=load_nested_stacks,
            parameters=parameters,
            preserve_logical_ids=preserve_logical_ids,
        )

        return typing.cast("IncludedNestedStack", jsii.invoke(self, "loadNestedStack", [logical_id, nested_stack_props]))


@jsii.data_type(
    jsii_type="monocdk.cloudformation_include.CfnIncludeProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_file": "templateFile",
        "load_nested_stacks": "loadNestedStacks",
        "parameters": "parameters",
        "preserve_logical_ids": "preserveLogicalIds",
    },
)
class CfnIncludeProps:
    def __init__(
        self,
        *,
        template_file: builtins.str,
        load_nested_stacks: typing.Optional[typing.Mapping[builtins.str, "CfnIncludeProps"]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        preserve_logical_ids: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Construction properties of {@link CfnInclude}.

        :param template_file: (experimental) Path to the template file. Both JSON and YAML template formats are supported.
        :param load_nested_stacks: (experimental) Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from the {@link CfnInclude.getNestedStack} method (but will still be accessible from the {@link CfnInclude.getResource} method). If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: (experimental) Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced
        :param preserve_logical_ids: (experimental) Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file. If you're vending a Construct using an existing CloudFormation template, make sure to pass this as ``false``. **Note**: regardless of whether this option is true or false, the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element, as specified in the template file. Default: true

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "template_file": template_file,
        }
        if load_nested_stacks is not None:
            self._values["load_nested_stacks"] = load_nested_stacks
        if parameters is not None:
            self._values["parameters"] = parameters
        if preserve_logical_ids is not None:
            self._values["preserve_logical_ids"] = preserve_logical_ids

    @builtins.property
    def template_file(self) -> builtins.str:
        '''(experimental) Path to the template file.

        Both JSON and YAML template formats are supported.

        :stability: experimental
        '''
        result = self._values.get("template_file")
        assert result is not None, "Required property 'template_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_nested_stacks(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "CfnIncludeProps"]]:
        '''(experimental) Specifies the template files that define nested stacks that should be included.

        If your template specifies a stack that isn't included here, it won't be created as a NestedStack
        resource, and it won't be accessible from the {@link CfnInclude.getNestedStack} method
        (but will still be accessible from the {@link CfnInclude.getResource} method).

        If you include a stack here with an ID that isn't in the template,
        or is in the template but is not a nested stack,
        template creation will fail and an error will be thrown.

        :default: - no nested stacks will be included

        :stability: experimental
        '''
        result = self._values.get("load_nested_stacks")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "CfnIncludeProps"]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Specifies parameters to be replaced by the values in this mapping.

        Any parameters in the template that aren't specified here will be left unmodified.
        If you include a parameter here with an ID that isn't in the template,
        template creation will fail and an error will be thrown.

        :default: - no parameters will be replaced

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def preserve_logical_ids(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file.

        If you're vending a Construct using an existing CloudFormation template,
        make sure to pass this as ``false``.

        **Note**: regardless of whether this option is true or false,
        the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element,
        as specified in the template file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("preserve_logical_ids")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIncludeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloudformation_include.IncludedNestedStack",
    jsii_struct_bases=[],
    name_mapping={"included_template": "includedTemplate", "stack": "stack"},
)
class IncludedNestedStack:
    def __init__(
        self,
        *,
        included_template: CfnInclude,
        stack: _NestedStack_9b94bddc,
    ) -> None:
        '''(experimental) The type returned from {@link CfnInclude.getNestedStack}. Contains both the NestedStack object and CfnInclude representations of the child stack.

        :param included_template: (experimental) The CfnInclude that represents the template, which can be used to access Resources and other template elements.
        :param stack: (experimental) The NestedStack object which represents the scope of the template.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "included_template": included_template,
            "stack": stack,
        }

    @builtins.property
    def included_template(self) -> CfnInclude:
        '''(experimental) The CfnInclude that represents the template, which can be used to access Resources and other template elements.

        :stability: experimental
        '''
        result = self._values.get("included_template")
        assert result is not None, "Required property 'included_template' is missing"
        return typing.cast(CfnInclude, result)

    @builtins.property
    def stack(self) -> _NestedStack_9b94bddc:
        '''(experimental) The NestedStack object which represents the scope of the template.

        :stability: experimental
        '''
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return typing.cast(_NestedStack_9b94bddc, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludedNestedStack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnInclude",
    "CfnIncludeProps",
    "IncludedNestedStack",
]

publication.publish()
