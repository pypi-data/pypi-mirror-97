from .helpers import fetch_requirements, write_yml


def update_layer(service, runtime, environment):

    print(f"Initializing {service}...")

    try:
        fetch_requirements()
    except RuntimeError as e:
        print(f'\033[91m{e}\033[0m')

    write_yml(service, runtime, environment)

    print('\033[92mDone! Now run `awslayer deploy` to re-deploy layer to AWS Lambda.\033[0m')