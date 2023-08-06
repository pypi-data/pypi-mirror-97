# awslayer-manager

This a simple tool to build and upload your project requirements as an AWS Lambda Layer. It extracts the requirements
from your Pipfile and installs them into a separate directory which it's deployed from. This package also supports
working with the high performance `mysqlclient` library by compiling it inside a docker container that closely mimics
the AWS Lambda environment and deploying it with the layer.

## Installation

To install this package, run
```bash
pip install awslayer-manager
```

### Requirements

- Requires your project to be using the `Serverless` framework.
- This package requires `Docker` if you're planning to work with `mysqlclient`. If not, you can omit it.

## Running
To initialize the layer run
```bash
awslayer init
```
in the project directory. This will extract requirements from your Pipfile and create a serverless.yml inside the layer
directory. Once the layer is initialized, run the following command:
```bash
awslayer deploy
```
which will install all the requirements inside the `layers/package` directory and deploy it using `sls deploy`. Once
that is done, add the following for each function in your project's serverless.yml:
```YAML
functions:
  func-name:
    handler: src/handler.func-name
    layers:
      - "${cf:stack-name.ServiceNameLayerLambdaLayerQualifiedArn}"
```
where you can find the "ServiceNameLayerLambdaLayerQualifiedArn" identifier in the CloudFormation stack.

To update requirements and runtime, run:
```bash
awslayer update
```

**NOTE:** This package will create a `layer` directory inside your project which I recommend adding to your
.gitignore file as it is fairly heavy (depending on the size of your requirements)

## Contributing
Pull requests are welcome.
