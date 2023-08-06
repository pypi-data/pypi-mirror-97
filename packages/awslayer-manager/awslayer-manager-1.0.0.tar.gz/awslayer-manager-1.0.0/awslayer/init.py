from pathlib import Path
from .helpers import fetch_requirements, write_yml


def init_layer(service, runtime):

    print(f"Initializing {service}...")

    Path('layer/package').mkdir(parents=True, exist_ok=True)

    fetch_requirements()

    write_yml(service, runtime)

    print("\033[92mDone! Now run `awslayer deploy` to deploy layer to AWS Lambda.\033[0m")
