from .helpers import fetch_requirements, write_yml


def update_layer(service, runtime):

    print(f"Initializing {service}...")

    fetch_requirements()

    write_yml(service, runtime)

    print('\033[92mDone! Now run `awslayer deploy` to re-deploy layer to AWS Lambda.\033[0m')