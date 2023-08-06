'''
[![NPM version](https://badge.fury.io/js/cdk-ssm-parameter-store.svg)](https://badge.fury.io/js/cdk-ssm-parameter-store)
[![PyPI version](https://badge.fury.io/py/cdk-ssm-parameter-store.svg)](https://badge.fury.io/py/cdk-ssm-parameter-store)
![Release](https://github.com/pahud/cdk-ssm-parameter-store/workflows/Release/badge.svg)

# cdk-ssm-parameter-store

AWS CDK construct that allows you to get the latest `Version` of the AWS SSM Parameters.

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk_ssm_parameter_store as param

stack = Stack(app, "testing-stack", env=env)

p = param.Provider(stack, "ParameterProvider")
foo_version = p.get("Foo").get_att_string("Version")
bar_version = p.get("Bar").get_att_string("Version")

CfnOutput(stack, "FooVersion", value=foo_version)
CfnOutput(stack, "BarVersion", value=bar_version)
```
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


class Provider(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-ssm-parameter-store.Provider",
):
    '''Parameter Provider.'''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        latest: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param latest: always get the latest parameter. Default: true
        '''
        props = ProviderProps(latest=latest)

        jsii.create(Provider, self, [scope, id, props])

    @jsii.member(jsii_name="get")
    def get(self, name: builtins.str) -> aws_cdk.core.CustomResource:
        '''return the parameter resource.

        :param name: -
        '''
        return typing.cast(aws_cdk.core.CustomResource, jsii.invoke(self, "get", [name]))


@jsii.data_type(
    jsii_type="cdk-ssm-parameter-store.ProviderProps",
    jsii_struct_bases=[],
    name_mapping={"latest": "latest"},
)
class ProviderProps:
    def __init__(self, *, latest: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param latest: always get the latest parameter. Default: true
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if latest is not None:
            self._values["latest"] = latest

    @builtins.property
    def latest(self) -> typing.Optional[builtins.bool]:
        '''always get the latest parameter.

        :default: true
        '''
        result = self._values.get("latest")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Provider",
    "ProviderProps",
]

publication.publish()
