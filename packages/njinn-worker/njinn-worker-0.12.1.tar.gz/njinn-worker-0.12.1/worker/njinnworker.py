import configparser
import errno
import logging
import os
import platform
import signal
import sys
from glob import glob
from time import sleep
from urllib.parse import urlparse

import requests
from celery import Celery, bootsteps
from celery.bin import worker as cworker
from celery.signals import worker_shutting_down
from celery.utils.log import get_logger

# use absolute paths to be consistent & compatible bewteen worker code and the scripts
from worker.api_client import NjinnAPI
from worker.celery_utils import get_celery_app
from worker.config import WorkerConfig, get_config_path
from worker.packinstall import PackInstallation
from worker import shared_logging
from worker.utils import is_windows
from worker.version_utils import get_worker_version


class NjinnWorkerStep(bootsteps.StartStopStep):
    requires = {"celery.worker.components:Pool"}

    def __init__(self, worker, **kwargs):
        self.njinnworker = kwargs.get("njinnworker", self)

    def create(self, worker):
        pass

    def start(self, worker):
        """ Called when the celery worker is started """
        self.log = get_logger(__name__)
        self.log.info("Starting Njinn Worker")
        self.log.info("Njinn Worker version %s", get_worker_version())
        self.log.info("Using config from %s", self.njinnworker.config.config_path)
        self.log.info("Njinn API at %s", self.njinnworker.njinn_api.njinn_api)
        self.log.info("Worker PID %s", os.getpid())
        # Update base dependencies in all pack virtualenvs - these are worker specific
        for filename in glob("bundle_status/*/*/*"):
            try:
                installation = PackInstallation(
                    PackInstallation.identifier_from_status_filename(filename),
                    self.njinnworker.njinn_api,
                )
                self.log.info(
                    "Updating base dependencies for pack %s", installation.display_name
                )
                try:
                    installation.on_startup(log=self.log)
                except Exception as e:
                    self.log.warning(
                        "Could not update base dependencies for %s: %s",
                        installation.display_name,
                        e,
                        exc_info=e,
                    )
            except Exception as e:
                self.log.warning(
                    "Could not retrieve pack metadata for pack with status file %s",
                    filename,
                )
        shared_logging.start(
            self.njinnworker.njinn_api,
            self.njinnworker.config.worker_name,
            level=self.njinnworker.config.log_level,
        )
        worker_shutting_down.connect(shared_logging.stop)

    def stop(self, worker):
        """ Called when the celery worker stops """
        pass


class NjinnWorker:
    def __init__(self, registration_token=None, njinn_url=None):
        # Setup worker dir as working dir
        self.working_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(self.working_dir)

        self.config = WorkerConfig()
        self.config.initialize()

        self.platform_info = os.getenv(
            "NJINN_WORKER_PLATFORM", f"{platform.system()} ({platform.release()})"
        )
        self.version = get_worker_version()
        config_valid = self.config.is_valid()
        if not config_valid and not registration_token:
            if not config_valid:
                print(
                    "Config is invalid. Please try to register the worker again.",
                    file=sys.stderr,
                )
            else:
                print("No registration token available.", file=sys.stderr)
            sys.exit(3)

        if not config_valid and registration_token is not None:
            print("Registering the worker using the provided token.", file=sys.stderr)
            self.register(registration_token, njinn_url)

        self.njinn_api = NjinnAPI(config=self.config)

        if not self.config.is_valid():
            print(
                "Configuration is invalid. Please contact Njinn Support.",
                file=sys.stderr,
            )
            sys.exit(1)
        else:
            self.config.update_from_api()
            self.config.save()
        self.celery_app = get_celery_app(
            self.config.messaging_url, step=NjinnWorkerStep
        )
        self.update_worker_details()

    def register(self, registration_token, njinn_url):

        api_base = njinn_url or os.environ.get("NJINN_URL", "https://api.njinn.io")
        if api_base.endswith("/"):
            api_base = api_base[:-1]
        url = api_base + "/api/v1/workercom/register"

        data = {
            "registration_token": registration_token,
            "name": self.config.worker_name,
            "platform": self.platform_info,
        }
        try:
            response = requests.post(url, data)
        except requests.ConnectionError as e:
            print(
                f"Problem trying to connect to: {api_base}. Error: {e}", file=sys.stderr
            )
            sys.exit(6)

        if response.status_code != 200:
            if response.status_code == 401:
                print("The provided registration key is invalid.")
                sys.exit(5)
            else:
                print(
                    f"Error when calling the API ({url}). Returned with status code {response.status_code}: {response.text}",
                    file=sys.stderr,
                )
                sys.exit(9)
        else:
            try:
                scheme = urlparse(api_base).scheme
            except ValueError:
                scheme = "https"
            api_url = os.getenv(
                "NJINN_WORKER_API", scheme + "://" + response.json()["domain_url"]
            )
            self.config.njinn_api_url = api_url
            print("Using API URL", api_url)
            self.config.jwt_secret = response.json()["secret"]
            self.config.worker_name = response.json()["name"]

        self.njinn_api = self.config.update_api()
        self.config.save()

    def update_worker_details(self):
        url = f"/api/v1/workers/{self.config.worker_id}"

        data = {"platform": self.platform_info, "version": self.version}

        try:
            response = self.njinn_api.patch(url, data)
        except requests.ConnectionError as e:
            print(
                f"Problem trying to connect to: {self.njinn_api.njinn_api}. Error: {e}",
                file=sys.stderr,
            )
            sys.exit(6)

        if response.status_code != 200:
            print(
                f"Error when calling the API ({self.njinn_api.get_url(url)}). Returned with status code {response.status_code}: {response.text}",
                file=sys.stderr,
            )
            sys.exit(9)

    def remove_pid_if_stale(self, path):
        """
        Remove the lock if the process isn't running.
        """
        try:
            with open(path, "r") as fh:
                pid = fh.readline().strip()
                pid = int(pid)
        except Exception:
            # Ignore errors: Only existing files can be stale.
            return
        stale_pid = False
        if pid == os.getpid():
            stale_pid = True
        elif is_windows():
            try:
                os.kill(pid, 0)
            except os.error as exc:
                if exc.errno == errno.ESRCH or exc.errno == errno.EPERM:
                    stale_pid = True
            except SystemError:
                stale_pid = True
        if stale_pid:
            print("Stale pidfile exists - Removing it.", file=sys.stderr)
            os.unlink(path)

    def start(self):
        hostname = self.config.worker_name or "worker@%%n"
        queues = self.config.queues
        pidfile = self.config.pidfile
        self.remove_pid_if_stale(pidfile)

        celery_worker = cworker.worker(app=self.celery_app)
        options = {
            "optimization": "fair",
            "O": "fair",
            "queues": queues,
            "loglevel": self.config.log_level,
            "hostname": hostname,
            "njinnworker": self,
            "pidfile": pidfile,
        }
        concurrency = self.config.concurrency
        if concurrency > 0:
            options["concurrency"] = concurrency

        def sigint_handler(sig, frame):
            sys.exit(0)

        signal.signal(signal.SIGINT, sigint_handler)
        signal.signal(signal.SIGTERM, sigint_handler)

        celery_worker.run(**options)
