[![awscdk-jsii-template](https://img.shields.io/badge/built%20with-awscdk--jsii--template-blue)](https://github.com/pahud/awscdk-jsii-template)
[![NPM version](https://badge.fury.io/js/cdk-soca.svg)](https://badge.fury.io/js/cdk-soca)
[![PyPI version](https://badge.fury.io/py/cdk-soca.svg)](https://badge.fury.io/py/cdk-soca)
![Release](https://github.com/pahud/cdk-soca/workflows/Release/badge.svg)

# Welcome to `cdk-soca`

`cdk-soca` is an AWS CDK construct library that allows you to create the [Scale-Out Computing on AWS](https://aws.amazon.com/tw/solutions/implementations/scale-out-computing-on-aws/) with AWS CDK in `TypeScript` or `Python`.

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk_soca as soca

# create the CDK application
app = App()

# create the stack in the CDK app
stack = Stack(app, "soca-testing-stack")

# create the workload in the CDK stack
soca.Workload(stack, "Workload")
```

That's all!
