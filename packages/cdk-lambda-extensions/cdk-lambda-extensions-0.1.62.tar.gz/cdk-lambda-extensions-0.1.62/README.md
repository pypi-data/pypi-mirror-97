[![NPM version](https://badge.fury.io/js/cdk-lambda-extensions.svg)](https://badge.fury.io/js/cdk-lambda-extensions)
[![PyPI version](https://badge.fury.io/py/cdk-lambda-extensions.svg)](https://badge.fury.io/py/cdk-lambda-extensions)
![Release](https://github.com/pahud/cdk-lambda-extensions/workflows/Release/badge.svg)

# cdk-lambda-extensions

AWS CDK construct library that allows you to add any [AWS Lambda Extensions](https://docs.aws.amazon.com/lambda/latest/dg/using-extensions.html) to the Lambda functions.

# Sample

To add `s3-logs-extension-demo` extension from the [aws-lambda-extensions](https://github.com/aws-samples/aws-lambda-extensions) github repository:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# prepare the s3 bucket for the lambda logs
bucket = s3.Bucket(self, "DemoBucket")

# prepare the Function
fn = Function(self, "Handler",
    code=lambda_.Code.from_asset(path.join(__dirname, "../aws-lambda-extensions/s3-logs-extension-demo/functionsrc")),
    runtime=lambda_.Runtime.PYTHON_3_8,
    handler="lambda_function.lambda_handler",
    memory_size=128,
    environment={
        "S3_BUCKET_NAME": bucket.bucket_name
    }
)
bucket.grant_write(fn)

# plug the `s3-logs-extension` in the lambda function
fn.add_extension(S3LogsExtension(self, "S3BucketExtention").extension)
```
