# AWS Cloud Development Kit Library

[![experimental](http://badges.github.io/stability-badges/dist/experimental.svg)](http://github.com/badges/stability-badges)

The AWS CDK construct library provides APIs to define your CDK application and add
CDK constructs to the application.

## Usage

### Upgrade from CDK 1.x

When upgrading from CDK 1.x, remove all dependencies to individual CDK packages
from your dependencies file and follow the rest of the sections.

### Installation

To use this package, you need to declare this package and the `constructs` package as
dependencies.

According to the kind of project you are developing:

* For projects that are CDK libraries, declare them both under the `devDependencies`
  **and** `peerDependencies` sections.
* For CDK apps, declare them under the `dependencies` section only.

### Use in your code

#### Classic import

You can use a classic import to get access to each service namespaces:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk_lib import core, aws_s3 as s3

app = core.App()
stack = core.Stack(app, "TestStack")

s3.Bucket(stack, "TestBucket")
```

#### Barrel import

Alternatively, you can use "barrel" imports:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
from aws_cdk_lib import App, Stack
from aws_cdk_lib.aws_s3 import Bucket

app = App()
stack = Stack(app, "TestStack")

Bucket(stack, "TestBucket")
```
