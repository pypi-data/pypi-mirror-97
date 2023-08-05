import configparser
import os
import shutil
import sys
import shutil

import click

# use absolute paths to be consistent & compatible bewteen worker code and the scripts
from worker.config import WorkerConfig, get_config_path
from worker.njinnworker import NjinnWorker
from worker import shared_logging


@click.command()
@click.option("-a", "--api", "api", help="Njinn API url.")
@click.option(
    "--clear-packs",
    "clear_packs",
    is_flag=True,
    help="Remove all packs and environments",
)
@click.argument("token", required=False)
def main(api=None, clear_packs=False, token=None):
    # windows celery fix: https://github.com/celery/celery/issues/4081
    os.environ["FORKED_BY_MULTIPROCESSING"] = "1"
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    if clear_packs:
        base_path = os.path.dirname(os.path.realpath(__file__))
        for subdirectory_name in ["bundle_status", "packs", "venv"]:
            subdirectory = os.path.join(base_path, subdirectory_name)
            if os.path.exists(subdirectory):
                print("Deleting", os.path.abspath(subdirectory))
                shutil.rmtree(subdirectory)
    njinn_url = sys.argv[-2] if len(sys.argv) > 2 else os.getenv("NJINN_URL")
    registration_token = token or os.getenv("NJINN_WORKER_TOKEN")
    print("Config file:", get_config_path())
    shared_logging.initialize()
    worker = NjinnWorker(registration_token=registration_token, njinn_url=njinn_url)
    print("Working Directory:", worker.working_dir)
    worker.start()


if __name__ == "__main__":
    main()
