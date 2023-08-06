[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-dynamodb-seeder

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-dynamodb-seeder)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-dynamodb-seeder/)

> A seeder for dynamodb tables

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-dynamodb-seeder
```

Python:

```bash
pip install cloudcomponents.cdk-dynamodb-seeder
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import path as path
from aws_cdk.core import Construct, Stack, StackProps, RemovalPolicy
from aws_cdk.aws_dynamodb import Table, AttributeType
from aws_cdk.aws_s3 import Bucket
from cloudcomponents.cdk_dynamodb_seeder import DynamoDBSeeder, Seeds

class DynamoDBSeederStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        table = Table(self, "Table",
            partition_key=Attribute(
                name="id",
                type=AttributeType.NUMBER
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        DynamoDBSeeder(self, "JsonFileSeeder",
            table=table,
            seeds=Seeds.from_json_file(path.join(__dirname, "..", "seeds.json"))
        )

        DynamoDBSeeder(self, "InlineSeeder",
            table=table,
            seeds=Seeds.from_inline([{
                "id": 3,
                "column": "foo"
            }, {
                "id": 4,
                "column": "bar"
            }
            ])
        )

        seeds_bucket = Bucket.from_bucket_name(self, "SeedsBucket", "my-seeds-bucket")

        DynamoDBSeeder(self, "BucketSeeder",
            table=table,
            seeds=Seeds.from_bucket(seeds_bucket, "seeds.json")
        )
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-dynamodb-seeder/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-dynamodb-seeder/LICENSE)
