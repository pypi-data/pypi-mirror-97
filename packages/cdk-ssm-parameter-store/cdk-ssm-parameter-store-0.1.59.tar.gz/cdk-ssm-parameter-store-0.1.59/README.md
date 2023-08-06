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
