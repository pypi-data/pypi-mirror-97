import shutil
from pathlib import Path

from .helpers import fetch_requirements, write_yml


def init_layer(service, runtime):
    print(f"Initializing {service}...")

    Path('layer/package').mkdir(parents=True, exist_ok=True)

    try:
        fetch_requirements()
    except RuntimeError as e:
        print(f'\033[91m{e}\033[0m')
        shutil.rmtree('layer/package')

    write_yml(service, runtime)

    print("\033[92mDone! Now run `awslayer deploy` to deploy layer to AWS Lambda.\033[0m")
