'''
[![NPM version](https://badge.fury.io/js/cdk-stack-resource-rename.svg)](https://badge.fury.io/js/cdk-stack-resource-rename)
[![PyPI version](https://badge.fury.io/py/cdk-stack-resource-rename.svg)](https://badge.fury.io/py/cdk-stack-resource-rename)
[![Nuget version](https://badge.fury.io/nu/cdk-stack-resource-rename.svg)](https://badge.fury.io/nu/CdkUtils.Aspects.ResourceRename)
![Release](https://github.com/yglcode/cdk-stack-resource-rename/workflows/Release/badge.svg)

## StackResourceRenamer

#### A CDK aspect, StackResourceRenamer renames CDK stack name and stack's subordinate resources' physical names, so that a CDK stack can be used to create multiple stacks in same AWS environment without confliction.

### API: [API.md](https://github.com/yglcode/cdk-stack-resource-rename/blob/main/API.md)

Two main use cases:

1. rename custom resources names in stack, so that stack can be reused and replicated:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
StackResourceRenamer.rename(stack,
    rename=(resName, _)=>{
            return resName+'-'+alias;
        }
)
```

1. for resources without custom name, which by default will use unique id AWS auto generate as its physical id, we can create a more readable and identifiable name, for testing, debugging or metrics monitoring environments.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
StackResourceRenamer.rename(stack, {
    "rename": (_, typeName)=>{
            counts[typeName]++;
            return projectName+'-'+serviceName+'-'+typeName+'-'+counts[typeName];
        }
}, user_custom_name_only=False)
```

### Samples

*typescript*

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_stack_resource_rename import StackResourceRenamer

app = core.App()
stack = core.Stack(app, "my-stack")

alias = stack.node.try_get_context("alias")
if alias:
    # if alias is defined, rename stack and resources' custom names
    StackResourceRenamer.rename(stack,
        rename=(resName, _)=>{
                    return resName+'-'+alias;
                }
    )

# resources in stack
bucket = s3.Bucket(stack, "bucket",
    bucket_name="my-bucket"
)
```

*python*

```python
from cdk_stack_resource_rename import (StackResourceRenamer, IRenameOperation)

@jsii.implements(IRenameOperation)
class RenameOper:
    def __init__(self, alias):
        self.alias=alias
    def rename(self, resName, typeName):
        return resName+'-'+self.alias

class AppStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        ......
        alias = self.node.try_get_context("alias")
        if alias != None:
            # if alias is defined, rename stack/resources' custom names
            StackResourceRenamer.rename(self, RenameOper(alias))
```

*java*

```java
import cdkutils.aspects.resourcerename.StackResourceRenamer;
import cdkutils.aspects.resourcerename.IRenameOperation;

public class AppStack extends Stack {
    ......
    String alias = (String) this.getNode().tryGetContext("alias");
    if (alias != null) {
        StackResourceRenamer.rename(this, new IRenameOperation() {
            public String rename(String resName, String typeName) {
                return resName + "-"+alias;
            }
        });
    }
```

*csharp*

```csharp
using CdkUtils.Aspects.ResourceRename;
public class RenameOper: Amazon.JSII.Runtime.Deputy.DeputyBase, IRenameOperation {
    private string alias;
    public RenameOper(string alias) {
        this.alias=alias;
    }
    public string Rename(string resName, string typeName) {
        return resName+"-"+alias;
    }
}
public class AppStack : Stack
{
    internal AppStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
    {
        ......
        var alias = (string)this.Node.TryGetContext("alias");
        if (alias!=null) {
            StackResourceRenamer.Rename(this, new RenameOper(alias));
        }
```

To create multiple stacks:

`cdk -c alias=a1 deploy  `
will create a stack: my-stack-a1 with my-bucket-a1.

To create more stacks: my-stack-a2 with my-bucket-a2, my-stack-a3 with my-bucket-a3:

`cdk -c alias=a2 deploy`

`cdk -c alias=a3 deploy`
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


@jsii.interface(jsii_type="cdk-stack-resource-rename.IRenameOperation")
class IRenameOperation(typing_extensions.Protocol):
    '''Interface of operation used to rename stack and its resources.'''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IRenameOperationProxy"]:
        return _IRenameOperationProxy

    @jsii.member(jsii_name="rename")
    def rename(
        self,
        resource_name: builtins.str,
        resource_type: builtins.str,
    ) -> builtins.str:
        '''Rename method to rename stack and its resources' physical names.

        AWS generated physical names are not changed unless StackResourceRenamer
        is created with RenameProps{ userCustomNameOnly:false }.
        The updated stack name or resource's name is returned.

        :param resource_name: The original resource physical name (if it is not user specified custom name, it is a AWS generated name/token, can be checked with cdk.Token.isUnresolved()).
        :param resource_type: The type name of CFN resource.
        '''
        ...


class _IRenameOperationProxy:
    '''Interface of operation used to rename stack and its resources.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-stack-resource-rename.IRenameOperation"

    @jsii.member(jsii_name="rename")
    def rename(
        self,
        resource_name: builtins.str,
        resource_type: builtins.str,
    ) -> builtins.str:
        '''Rename method to rename stack and its resources' physical names.

        AWS generated physical names are not changed unless StackResourceRenamer
        is created with RenameProps{ userCustomNameOnly:false }.
        The updated stack name or resource's name is returned.

        :param resource_name: The original resource physical name (if it is not user specified custom name, it is a AWS generated name/token, can be checked with cdk.Token.isUnresolved()).
        :param resource_type: The type name of CFN resource.
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "rename", [resource_name, resource_type]))


@jsii.data_type(
    jsii_type="cdk-stack-resource-rename.RenameProps",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_resource_types": "excludeResourceTypes",
        "include_resource_types": "includeResourceTypes",
        "irregular_resource_names": "irregularResourceNames",
        "user_custom_name_only": "userCustomNameOnly",
    },
)
class RenameProps:
    def __init__(
        self,
        *,
        exclude_resource_types: typing.Optional[typing.List[builtins.str]] = None,
        include_resource_types: typing.Optional[typing.List[builtins.str]] = None,
        irregular_resource_names: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_custom_name_only: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Properties to control rename process.

        :param exclude_resource_types: An array of Resource Types whose physical names could not be changed. An empty array will allow the renaming for all resources. A non-empty array will apply rename operation only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types whose physical names could be updated. An empty array will not allow any renaming to resources. A non-empty array will allow renaming only if the Resource type is in this array. Default: []
        :param irregular_resource_names: Mapping of resourceType names to physicalName fields for resources whose physicalName field donot follow the regular naming conventions: ``${resourceType}``+'Name'. Default: {}
        :param user_custom_name_only: Only rename user provided custom names. If set to false, rename() will be invoked for all resources names with or without custom names. Default: True
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if exclude_resource_types is not None:
            self._values["exclude_resource_types"] = exclude_resource_types
        if include_resource_types is not None:
            self._values["include_resource_types"] = include_resource_types
        if irregular_resource_names is not None:
            self._values["irregular_resource_names"] = irregular_resource_names
        if user_custom_name_only is not None:
            self._values["user_custom_name_only"] = user_custom_name_only

    @builtins.property
    def exclude_resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of Resource Types whose physical names could not be changed.

        An empty array will allow the renaming for all resources. A non-empty
        array will apply rename operation only if the Resource type is not in
        this array.

        :default: []
        '''
        result = self._values.get("exclude_resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of Resource Types whose physical names could be updated.

        An empty array will not allow any renaming to resources. A
        non-empty array will allow renaming only if the Resource type is in
        this array.

        :default: []
        '''
        result = self._values.get("include_resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def irregular_resource_names(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping of resourceType names to physicalName fields for resources whose physicalName field donot follow the regular naming conventions: ``${resourceType}``+'Name'.

        :default: {}
        '''
        result = self._values.get("irregular_resource_names")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def user_custom_name_only(self) -> typing.Optional[builtins.bool]:
        '''Only rename user provided custom names.

        If set to false, rename() will be invoked for all resources names with or without custom names.

        :default: True
        '''
        result = self._values.get("user_custom_name_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IAspect)
class StackResourceRenamer(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-stack-resource-rename.StackResourceRenamer",
):
    '''StackResourceRenamer renames stack name and stack's subordinate resources' physical names, so that a CDK stack can be used to create multiple stacks in same AWS environment.'''

    def __init__(
        self,
        rename_oper: IRenameOperation,
        *,
        exclude_resource_types: typing.Optional[typing.List[builtins.str]] = None,
        include_resource_types: typing.Optional[typing.List[builtins.str]] = None,
        irregular_resource_names: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_custom_name_only: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Construct a new StackResourceRenamer.

        :param rename_oper: RenameOperation is used to rename stack name and resources' physical names. AWS generated physical names are not changed unless the "props" is set with RenameProps{userCustomNameOnly:false}
        :param exclude_resource_types: An array of Resource Types whose physical names could not be changed. An empty array will allow the renaming for all resources. A non-empty array will apply rename operation only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types whose physical names could be updated. An empty array will not allow any renaming to resources. A non-empty array will allow renaming only if the Resource type is in this array. Default: []
        :param irregular_resource_names: Mapping of resourceType names to physicalName fields for resources whose physicalName field donot follow the regular naming conventions: ``${resourceType}``+'Name'. Default: {}
        :param user_custom_name_only: Only rename user provided custom names. If set to false, rename() will be invoked for all resources names with or without custom names. Default: True
        '''
        props = RenameProps(
            exclude_resource_types=exclude_resource_types,
            include_resource_types=include_resource_types,
            irregular_resource_names=irregular_resource_names,
            user_custom_name_only=user_custom_name_only,
        )

        jsii.create(StackResourceRenamer, self, [rename_oper, props])

    @jsii.member(jsii_name="rename") # type: ignore[misc]
    @builtins.classmethod
    def rename(
        cls,
        stack: aws_cdk.core.IConstruct,
        rename_oper: IRenameOperation,
        *,
        exclude_resource_types: typing.Optional[typing.List[builtins.str]] = None,
        include_resource_types: typing.Optional[typing.List[builtins.str]] = None,
        irregular_resource_names: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_custom_name_only: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Static method to rename a stack and all its subordinate resources.

        :param stack: The stack (and all its children resources) to be renamed.
        :param rename_oper: RenameOperation is used to rename stack name and resources' physical names. AWS generated physical names are not changed unless the "props" is set with RenameProps{userCustomNameOnly:false}
        :param exclude_resource_types: An array of Resource Types whose physical names could not be changed. An empty array will allow the renaming for all resources. A non-empty array will apply rename operation only if the Resource type is not in this array. Default: []
        :param include_resource_types: An array of Resource Types whose physical names could be updated. An empty array will not allow any renaming to resources. A non-empty array will allow renaming only if the Resource type is in this array. Default: []
        :param irregular_resource_names: Mapping of resourceType names to physicalName fields for resources whose physicalName field donot follow the regular naming conventions: ``${resourceType}``+'Name'. Default: {}
        :param user_custom_name_only: Only rename user provided custom names. If set to false, rename() will be invoked for all resources names with or without custom names. Default: True
        '''
        props = RenameProps(
            exclude_resource_types=exclude_resource_types,
            include_resource_types=include_resource_types,
            irregular_resource_names=irregular_resource_names,
            user_custom_name_only=user_custom_name_only,
        )

        return typing.cast(None, jsii.sinvoke(cls, "rename", [stack, rename_oper, props]))

    @jsii.member(jsii_name="isTarget")
    def is_target(self, res_name: typing.Any) -> builtins.bool:
        '''check if a resName(resource name) is a valid target for rename;

        :param res_name: -
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "isTarget", [res_name]))

    @jsii.member(jsii_name="renameResource")
    def _rename_resource(
        self,
        node: aws_cdk.core.IConstruct,
        res_type_name: builtins.str,
    ) -> None:
        '''Rename a CFN resource or stack.

        :param node: CFN resource or stack.
        :param res_type_name: The type name of CFN resource.
        '''
        return typing.cast(None, jsii.invoke(self, "renameResource", [node, res_type_name]))

    @jsii.member(jsii_name="visit")
    def visit(self, node: aws_cdk.core.IConstruct) -> None:
        '''Implement core.IAspect interface.

        :param node: CFN resources to be renamed.
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


__all__ = [
    "IRenameOperation",
    "RenameProps",
    "StackResourceRenamer",
]

publication.publish()
