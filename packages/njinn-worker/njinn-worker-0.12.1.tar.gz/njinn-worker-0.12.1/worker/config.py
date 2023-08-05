import json
import os
import socket
import sys
from collections.abc import MutableMapping
from configparser import ConfigParser
from time import sleep

import requests
import backoff
import logging

# use absolute paths to be consistent & compatible bewteen worker code and the scripts
from worker.api_client import NjinnAPI
from worker.utils import (
    MAXIMUM_API_REQUEST_RETRY_DURATION_SECONDS,
    MAXIMUM_API_REQUEST_WAIT_TIME_SECONDS,
    api_response_predicate,
    setup_backoff_handler,
)

log = logging.getLogger(__file__)
setup_backoff_handler()


def get_config_path():
    working_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.getenv("NJINN_WORKER_CONFIG")
    config_file = "worker.ini"
    if not config_path:
        if sys.platform in ("linux2", "linux"):
            config_path = f"/etc/njinn/{config_file}"
        else:
            config_path = os.path.join(working_dir, config_file)
    return config_path


class WorkerConfig:
    """
    WorkerConfig

    Contains all configuration required to run the worker.
    Only attributes intended to be stored in the config file are handled
    via a ConfigParser, the others are simple attributes.

    This is kept transparent to the users of this class by using properties.
    """

    def __init__(self, config_path=None):
        self.config_path = config_path or get_config_path()
        self.config = ConfigParser()
        self.njinn_api = None
        self.secrets_key = None
        self.queues = None
        self.messaging_url = None

    def __read(self):
        self.config.read(self.config_path)

    def update_api(self):
        self.njinn_api = NjinnAPI(config=self)
        return self.njinn_api

    def update_logging(self):
        for handler in log.handlers:
            handler.setLevel(self.log_level)

    def load_from_file(self):
        """
        Loads a valid config from an existing file
        """
        self.__read()
        self.update_api()
        self.update_logging()
        return self

    def save(self):
        """
        Saves the parts of the config that aren't loaded from the API to the file.
        """
        config_copy = ConfigParser()
        config_copy["DEFAULT"] = {
            k: v
            for k, v in self.config["DEFAULT"].items()
            if k in ["id", "njinn_api", "secret", "name", "concurrency", "pid_file"]
        }
        if "logging" in self.config:
            config_copy["logging"] = {
                k: v for k, v in self.config["logging"].items() if k.startswith("log_")
            }

        try:
            with open(self.config_path, "w") as configfile:
                config_copy.write(configfile)
        except OSError:
            print("Could not write to the configuration file.", file=sys.stderr)
            sys.exit(4)

    def initialize(self):
        """
        Ensures a valid config is present in self.config_path, and loads existing
        values into self.config
        """
        config_dir = os.path.dirname(os.path.realpath(self.config_path))
        os.makedirs(config_dir, exist_ok=True)
        self.__read()

        self.njinn_api_url = self.config.get(
            "DEFAULT", "njinn_api", fallback=os.getenv("NJINN_WORKER_API", "")
        )
        self.jwt_secret = self.config.get(
            "DEFAULT", "secret", fallback=os.getenv("NJINN_WORKER_SECRET", "")
        )
        self.worker_name = self.config.get(
            "DEFAULT",
            "name",
            fallback=os.getenv("NJINN_WORKER_NAME", socket.gethostname()),
        )
        self.save()
        self.update_api()
        self.update_logging()
        return self

    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.RequestException,
        max_value=MAXIMUM_API_REQUEST_WAIT_TIME_SECONDS,
        max_time=MAXIMUM_API_REQUEST_RETRY_DURATION_SECONDS,
    )
    @backoff.on_predicate(
        backoff.expo,
        api_response_predicate,
        max_value=MAXIMUM_API_REQUEST_WAIT_TIME_SECONDS,
        max_time=MAXIMUM_API_REQUEST_RETRY_DURATION_SECONDS,
    )
    def __update_from_api(self):
        worker_name = self.worker_name
        url = f"/api/v1/workercom/config/{worker_name}"
        return self.njinn_api.get(url)

    def update_from_api(self):
        worker_name = self.worker_name
        url = f"/api/v1/workercom/config/{worker_name}"

        response = self.__update_from_api()
        if response.status_code != 200:
            if response.status_code == 404:
                print("Could not authenticate the worker.", file=sys.stderr)
                sys.exit(2)
            else:
                print(
                    f"Error when calling the API ({self.njinn_api.get_url(url)}). Returned with status code {response.status_code}: {response.text}",
                    file=sys.stderr,
                )
                sys.exit(9)
        else:
            self.worker_id = str(response.json()["id"])
            self.worker_name = response.json()["name"]
            self.queues = response.json()["queues"]
            self.messaging_url = os.getenv(
                "NJINN_MESSAGING_URL", response.json()["messaging_url"]
            )
            self.secrets_key = response.json()["secrets_key"]
        self.update_api()
        self.update_logging()
        return self

    def is_valid(self):
        api = self.config.get("DEFAULT", "njinn_api", fallback="")
        secret = self.config.get("DEFAULT", "secret", fallback="")
        name = self.config.get("DEFAULT", "name", fallback="")

        if not api.strip():
            print("No API URL in the config.")
            return False
        if not secret.strip():
            print("No secret in the config.")
            return False
        if not name.strip():
            print("No worker name in the config.")
            return False

        return True

    @property
    def worker_name(self):
        return self.config.get("DEFAULT", "name", fallback=None)

    @worker_name.setter
    def worker_name(self, worker_name):
        self.config["DEFAULT"]["name"] = worker_name

    @property
    def jwt_secret(self):
        return self.config.get("DEFAULT", "secret")

    @jwt_secret.setter
    def jwt_secret(self, jwt_secret):
        self.config["DEFAULT"]["secret"] = jwt_secret

    @property
    def njinn_api_url(self):
        return self.config.get("DEFAULT", "njinn_api")

    @njinn_api_url.setter
    def njinn_api_url(self, njinn_api_url):
        self.config["DEFAULT"]["njinn_api"] = njinn_api_url

    @property
    def pidfile(self):
        return self.config.get("DEFAULT", "pid_file", fallback="./worker.pid")

    @pidfile.setter
    def pidfile(self, pidfile):
        self.config["DEFAULT"]["pid_file"] = pidfile

    @property
    def worker_id(self):
        return self.config.getint("DEFAULT", "id")

    @worker_id.setter
    def worker_id(self, worker_id):
        self.config["DEFAULT"]["id"] = worker_id

    @property
    def concurrency(self):
        # always let env var win
        return int(
            os.getenv(
                "NJINN_WORKER_CONCURRENCY",
                self.config.getint("DEFAULT", "concurrency", fallback=0),
            )
        )

    @concurrency.setter
    def concurrency(self, concurrency):
        self.config["DEFAULT"]["concurrency"] = concurrency

    @property
    def log_level(self):
        return self.config.get("logging", "log_level", fallback="INFO")

    @log_level.setter
    def log_level(self, log_level):
        if not self.config.has_section("logging"):
            self.config.add_section("logging")
        self.config["logging"]["log_level"] = log_level


class ActionExecutionConfig:
    def __init__(
        self,
        working_dir,
        config_path=None,
        action=None,
        pack=None,
        action_context=None,
    ):
        self.working_dir = working_dir
        self.input_file_path = os.path.join(working_dir, "in.json")
        self.config_path = config_path
        self.action = action
        self.pack = pack
        self.action_context = action_context
        self.secrets_key = os.getenv("njinn_secrets_key")
        self.njinn_api = None
        self.worker_config = None

    def load(self):
        with open(self.input_file_path) as input_file:
            self.input = json.load(input_file)

        self.config_path = self.input["config_path"]
        self.action = self.input["action"]
        self.pack = self.input["pack"]
        self.action_context = self.input["action_context"]
        self.njinn_api = NjinnAPI(
            config_path=self.config_path, execution_id=self.execution_id
        )
        self.worker_config = self.njinn_api.config
        return self

    @property
    def execution_id(self):
        return (self.action_context or {}).get("execution_id")

    @property
    def njinn_execution_id(self):
        return (self.action_context or {}).get("njinn_execution_id")

    @property
    def task_name(self):
        return (self.action_context or {}).get("task_name")

    @property
    def action_execution_id(self):
        return (self.action_context or {}).get("action_execution_id")

    def save(self):
        input_file_content = {
            "config_path": self.config_path,
            "action": self.action,
            "pack": self.pack,
            "action_context": self.action_context,
        }

        with open(self.input_file_path, "w") as fp:
            json.dump(input_file_content, fp)
