from sys import argv
import os
from .init import init_layer
from .update import update_layer
from .deploy import deploy_layer
from .helpers import get_service_name, get_runtime

usage_str = """
Usage:  awslayer [OPTION] COMMAND

A simple AWS Lambda Layer manager.

Options:
  -h, --help    Print usage string.

Commands:
  init          Initialize AWS Lambda Layer.
  deploy        Deploy layer to AWS Lambda.
  update        Update layer requirements.

\033[1mTo get more help with this package, contact the repo owner.\033[0m"""


def main():
    if len(argv) < 2:
        print(f"\033[91mMissing command.\033[0m")
        print(usage_str)
        exit()

    service = get_service_name()
    runtime = get_runtime()

    if argv[1] in ['-h', '--help']:
        print(usage_str)
    elif argv[1] == 'init':
        if os.path.isdir('layer')\
                and os.path.isdir('layer/package')\
                and os.path.isfile('layer/serverless.yml')\
                and os.path.isfile('layer/package/aws_requirements.txt'):
            print("\033[91mLayer initialized.\033[0m",
                  "\033[91mPlease run `awslayer update` to update requirements and the serverless yaml.\033[0m")
            print(usage_str)
        else:
            init_layer(service, runtime)
    elif argv[1] == 'deploy':
        if os.path.isdir('layer') \
                and os.path.isdir('layer/package') \
                and os.path.isfile('layer/serverless.yml') \
                and os.path.isfile('layer/package/aws_requirements.txt'):
            deploy_layer(runtime)
        else:
            print("\033[91mLayer not initialized. Please run `awslayer init`.\033[0m")
            print(usage_str)
    elif argv[1] == 'update':
        if os.path.isdir('layer') \
                and os.path.isdir('layer/package') \
                and os.path.isfile('layer/serverless.yml') \
                and os.path.isfile('layer/package/aws_requirements.txt'):
            update_layer(service, runtime)
        else:
            print("\033[91mLayer not initialized. Please run `awslayer init`.\033[0m")
            print(usage_str)
    else:
        print(f"\033[91mUnrecognized command: {argv[1]}.\033[0m")
        print(usage_str)


if __name__ == "__main__":
    main()
