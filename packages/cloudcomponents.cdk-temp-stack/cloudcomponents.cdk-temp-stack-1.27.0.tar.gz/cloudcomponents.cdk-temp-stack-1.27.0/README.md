[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-temp-stack

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-temp-stack)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-temp-stack/)

> A stack that destroys itself after a given time (ttl)

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-temp-stack
```

Python:

```bash
pip install cloudcomponents.cdk-temp-stack
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
~/usr/bin / envnode

from source_map_support.register import
from aws_cdk.core import App, Duration

from ..temp_infra_stack import TempInfraStack

app = App()

TempInfraStack(app, "TempInfraStack",
    env=Environment(
        region=process.env.DEFAULT_REGION,
        account=process.env.CDK_DEFAULT_ACCOUNT
    ),
    ttl=Duration.minutes(10)
)

# temp-infra-stack.ts

from aws_cdk.core import Construct
from aws_cdk.aws_ec2 import Vpc
from cloudcomponents.cdk_temp_stack import TempStack, TempStackProps

class TempInfraStack(TempStack):
    def __init__(self, scope, id, *, ttl, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, ttl=ttl, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        Vpc(self, "VPC")
```

## TimeToLive Construct

Alternatively, you can also add the TimeToLive construct to your stack

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# your stack

from aws_cdk.core import Construct, Stack, StackProps, Duration
from cloudcomponents.cdk_temp_stack import TimeToLive

class YourStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        TimeToLive(self, "TimeToLive",
            ttl=Duration.minutes(10)
        )
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-temp-stack/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-temp-stack/LICENSE)
