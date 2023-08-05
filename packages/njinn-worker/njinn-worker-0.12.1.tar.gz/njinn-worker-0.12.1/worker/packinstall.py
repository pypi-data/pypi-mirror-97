import os
import shutil
import subprocess
from datetime import datetime
from glob import glob
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import backoff
import requests
import virtualenv
from celery.utils.log import get_task_logger
from filelock import FileLock

# use absolute paths to be consistent & compatible bewteen worker code and the scripts
from worker.utils import (
    MAXIMUM_API_REQUEST_RETRY_DURATION_SECONDS,
    MAXIMUM_API_REQUEST_WAIT_TIME_SECONDS,
    api_response_predicate,
    is_windows,
    read_stdout,
    setup_backoff_handler,
)

log = get_task_logger(__name__)
setup_backoff_handler()


def fileset(directory):
    files = []
    for dirpath, _, filelist in os.walk(directory):
        for filename in filelist:
            files.append(os.path.relpath(os.path.join(dirpath, filename), directory))
    return files


class PackInstallation:
    def __init__(self, pack_identifier, njinn_api, base_path=None):
        # use for testing only
        self.base_path = (
            os.path.dirname(os.path.realpath(__file__))
            if base_path is None
            else base_path
        )
        self.pack_namespace, self.pack_name = pack_identifier.split(".")
        self.qualified_name = f"{self.pack_namespace}/{self.pack_name}"
        self.njinn_api = njinn_api
        self.target_path = f"{self.base_path}/packs/{self.qualified_name}"
        self.venv_base_path = f"{self.base_path}/venv/{self.qualified_name}"
        self.display_name = self.qualified_name
        self.status = None
        self.bundle_status_base_path = None
        self.venv_path = None
        self.bundle_status_file_name = None

    @staticmethod
    def identifier_from_status_filename(status_filename):
        dirname = Path(status_filename).parent
        pack_name = dirname.name
        pack_namespace = dirname.parent.name
        return f"{pack_namespace}.{pack_name}"

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
    def __get_metadata(self):
        pack_api = "/api/v1/workercom/packs/" + self.qualified_name
        response = self.njinn_api.get(pack_api)
        return response

    def get_metadata(self):
        response = self.__get_metadata()

        if response.status_code != requests.codes.ok:
            raise Exception(
                f"Problem trying to get pack {self.qualified_name}. API responded with ({response.status_code}): {response.text}"
            )
        self.metadata = response.json()
        if "version_identifier" in self.metadata and len(
            self.metadata["version_identifier"]
        ):
            self.version_identifier = self.metadata["version_identifier"]
            self.venv_path = f"{self.venv_base_path}/{self.version_identifier}"
            self.bundle_status_base_path = (
                f"{self.base_path}/bundle_status/{self.qualified_name}"
            )
            self.bundle_status_file_name = (
                f"{self.bundle_status_base_path}/{self.version_identifier}-log.txt"
            )
            if "title" in self.metadata:
                self.display_name = f"{self.qualified_name} ({self.metadata['title']})"
        else:
            raise ValueError("Direct clone from git is not supported anymore.")
        log.debug("%s: Downloaded metadata.", self.display_name)

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
    def __download_pack_zip(self, temp_zip_name):
        log.debug(
            "%s: Downloading version %s from API.",
            self.display_name,
            self.version_identifier,
        )
        pack_bundle_url = f"/api/v1/workercom/packs/{self.qualified_name}/bundle"
        return self.njinn_api.get(pack_bundle_url)

    def download_pack_zip(self, temp_zip_name):
        response = self.__download_pack_zip(temp_zip_name)
        if response.status_code != requests.codes.ok:
            raise Exception(
                f"Problem trying to get pack {self.qualified_name} bundle. API responded with ({response.status_code}): {response.text}"
            )
        log.info(
            "%s: Downloaded version %s from API.",
            self.display_name,
            self.version_identifier,
        )
        with open(temp_zip_name, "wb") as f:
            f.write(response.content)

    def sync_target_from_zip(self, temp_zip_name):
        """ 
        Sync self.target_path with the zipfile and create/update environment according to its contents
        """

        os.makedirs(self.target_path, exist_ok=True)

        # Attempt installation.
        # Remove self.target_path after failed initial installation, since we use its existence
        # to determine whether to create a new environment or update an existing one.
        try:
            with TemporaryDirectory() as temp_dir:
                with ZipFile(temp_zip_name) as zip_file:
                    zip_file.extractall(path=temp_dir)
                    source_files = fileset(temp_dir)
                    target_files = fileset(self.target_path)
                    for filename in source_files:
                        log.info("%s: Copying %s", self.display_name, filename)
                        target_filename = os.path.join(self.target_path, filename)
                        os.makedirs(os.path.dirname(target_filename), exist_ok=True)
                        shutil.move(os.path.join(temp_dir, filename), target_filename)
                    for filename in [f for f in target_files if not f in source_files]:
                        log.info(
                            "%s: Removing %s which does not exist in bundled version of action.",
                            self.display_name,
                            filename,
                        )
                        os.remove(os.path.join(self.target_path, filename))
            self.on_change()
        except Exception as e:
            log.warning("Error during pack installation: %s", e)
            if os.path.exists(self.target_path):
                log.info(
                    "%s Cleaning up %s after failed initial installation.",
                    self.display_name,
                    self.target_path,
                )
                try:
                    shutil.rmtree(self.target_path)
                except Exception as e:
                    log.warning(
                        "%s Failed to clean up %s after failed installation: %s",
                        self.display_name,
                        self.target_path,
                        e,
                    )
            raise e

    def on_bundle_setup_success(self):
        """ Writes new and removes old status files from the bundle directory """
        os.makedirs(self.bundle_status_base_path, exist_ok=True)
        with open(self.bundle_status_file_name, "wt") as status_file:
            status_file.write(f"Installed {datetime.now()}")

        for some_bundle_status_file in glob(f"{self.bundle_status_base_path}/*"):
            if os.path.normpath(self.bundle_status_file_name) != os.path.normpath(
                some_bundle_status_file
            ):
                log.info("Removing old status file %s", some_bundle_status_file)
                try:
                    os.remove(some_bundle_status_file)
                except Exception as e:
                    log.warning("Failed to delete %s: %s", some_bundle_status_file, e)

    def get_pack_from_api(self):
        """ Install/update the pack from the API """
        # skip if already finished successfully, determined by whether the status file exists
        if os.path.isfile(self.bundle_status_file_name):
            with open(self.bundle_status_file_name, "rt") as status_file:
                status_text = status_file.read()
            log.debug("%s: bundle is up to date: %s", self.display_name, status_text)
            self.status = f"Pack {self.display_name} using version identifier {self.version_identifier} ({status_text}) provided by API."
            return

        # save to a temporary directory and install
        with TemporaryDirectory() as temp_dir:
            temp_zip_name = f"{temp_dir}/temp.zip"
            self.download_pack_zip(temp_zip_name)
            self.sync_target_from_zip(temp_zip_name)

        self.on_bundle_setup_success()

        self.status = f"Pack {self.display_name} set up based on version identifier {self.version_identifier} provided by API."
        log.info(self.status)

    def create_venv(self):
        virtualenv.create_environment(self.venv_path, clear=True)

    def on_change(self):

        if os.path.exists(self.venv_path):
            # Can happen if we install version A then B then A
            # In this case we assume all tasks using the old target dir have finished.
            log.info(
                "Removing existing venv directory %s for %s",
                self.venv_path,
                self.display_name,
            )
            shutil.rmtree(self.venv_path)
        log.debug("%s: Creating venv in %s.", self.display_name, self.venv_path)
        self.create_venv()
        self.__install_worker_dependencies()
        self.install_requirements()
        self.__log_freeze_output()

    def get_version_identifier_from_repo(self, repo):
        try:
            self.version_identifier = repo.active_branch.commit.hexsha
        except Exception as e:
            log.warning("Error getting version identifier from repo: %s", e)

    def setup(self):
        self.get_metadata()
        log.info("%s: Setting up inside: %s", self.display_name, self.target_path)
        log.debug("%s: Locking %s", self.display_name, self.lock_name)
        with FileLock(self.lock_name):
            log.debug(
                "%s: Using version %s provided by API.",
                self.display_name,
                self.version_identifier,
            )
            self.get_pack_from_api()

    def run_pip(self, pip_argline, log=log):
        """
        Runs pip in a cross-platform way
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        command = f"pip --disable-pip-version-check {pip_argline}"
        log.info("%s: Running %s", self.display_name, command)
        # shell=True is needed for env to work on Windows
        result = subprocess.Popen(
            command,
            universal_newlines=True,
            cwd=dir_path,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            shell=True,
            env=self.virtualenv_env(),
        )
        lines = []
        read_stdout(result, lines)
        if result.returncode != 0:
            raise ValueError(f"Nonzero return code: {result.returncode}")
        return [l.strip() for l in lines]

    def __log_freeze_output(self, log=log):
        log.info(
            "%s: Dependencies %s", self.display_name, ", ".join(self.run_pip("freeze")),
        )

    def __install_worker_dependencies(self, log=log):
        """
        Only call this variant inside a lock
        """
        log.info("%s: Installing default dependencies.", self.display_name)
        self.run_pip(
            'install "requests >=2.21, <2.22" "PyJWT==1.7.1" "requests-jwt==0.5.3" "bcrypt ==3.1.7" "cryptography==2.9.2" "backoff ==1.10.0"',
            log=log,
        )

    def __migrate_dirs(self, log=log):
        """
        One venv per pack version - Introduced with worker 0.10.1
        """
        if os.path.exists(self.venv_base_path) and not os.path.exists(self.venv_path):
            shutil.rmtree(self.venv_base_path)
            # re-create venv - this is required because Windows venvs cannot be migrated
            # due to absolute paths being added to pip executable.
            # To be cautious, we do the same for Linux.
            self.on_change()
        # workaround for error in 0.10.1 - 0.11.2, which tried to migrate windows venvs.
        elif is_windows() and os.path.exists(self.venv_path):
            # We can detect this by observing that activate.bat does not contain the version identifier,
            # i.e. the full venv path, i.e.
            # set "VIRTUAL_ENV=C:\some\where\worker\venv\njinn\base"
            # instead of
            # set "VIRTUAL_ENV=C:\some\where\worker\venv\njinn\base\107d97e1b1e807cc33c0fcb810b29400192c5a01"
            with open(self.get_bin_dir() / "activate.bat") as f:
                activate_bat = f.read()
            if self.version_identifier not in activate_bat:
                log.info("Re-creating venv inside %s", self.venv_path)
                self.on_change()

    def __clear_dirs(self, log=log):
        for filename in os.listdir(self.venv_base_path):
            norm_path = os.path.normpath(
                os.path.abspath(os.path.join(self.venv_base_path, filename))
            )
            if os.path.isdir(norm_path) and not norm_path == os.path.normpath(
                os.path.abspath(self.venv_path)
            ):
                log.info(
                    "%s: Removing obsolete venv directory %s",
                    self.display_name,
                    norm_path,
                )
                shutil.rmtree(norm_path)

    def on_startup(self, log=log):
        """
        Perform startup actions for pack installation:
        * Migrate to current venv directory structure
        * Clear obsolete venv directories
        * Install the worker dependencies inside the venvs
        """

        self.get_metadata()
        with FileLock(self.lock_name):
            self.__migrate_dirs(log=log)
            self.__clear_dirs(log=log)
            self.__install_worker_dependencies(log=log)
            self.__log_freeze_output(log=log)

    def install_requirements(self):
        """
        Install requirements if 'requirements.txt' file is provided. 
        """

        log.info("%s: Installing package specific dependencies.", self.display_name)
        requirements_path = (Path(self.target_path) / "requirements.txt").resolve()

        if os.path.exists(requirements_path):
            self.run_pip(f'install -r "{requirements_path}"')
        else:
            log.warning("Requirements file %s doesn't exist", requirements_path)

    def get_bin_dir(self):
        if is_windows():
            # https://virtualenv.pypa.io/en/latest/userguide/#windows-notes
            binary_dir = "Scripts"
        else:
            binary_dir = "bin"
        return Path(self.venv_path) / binary_dir

    def get_python(self):
        if is_windows():
            python_executable = "python.exe"
        else:
            python_executable = "python"
        return str((self.get_bin_dir() / python_executable).resolve())

    def virtualenv_env(self):
        """
        Creates a copy of the current system environment variables modified for
        running commands inside this pack's virtualenv, mimicking what the
        activate scripts do.
        """

        # if already in a virtualenv, this is set to the original PATH by activate - use this.
        old_path = os.environ.get("_OLD_VIRTUAL_PATH", os.environ["PATH"])
        if is_windows():
            # https://en.wikipedia.org/wiki/PATH_(variable)#DOS,_OS/2,_and_Windows
            path_sep = ";"
        else:
            path_sep = ":"
        virtualenv_bin_dir = self.get_bin_dir().resolve()
        # Fail instead of accidentally messing with parent environment.
        assert virtualenv_bin_dir.exists(), (
            f"Pack installation in unexpected state - virtualenv bin directory does not exist: {virtualenv_bin_dir}",
        )
        new_path = f"{str(virtualenv_bin_dir)}{path_sep}{old_path}"
        env_copy = os.environ.copy()
        # play nice with existing virtualenvs, see comment above
        env_copy["_OLD_VIRTUAL_PATH"] = old_path
        env_copy["PATH"] = new_path
        return env_copy

    @property
    def lock_name(self):
        return self.qualified_name.replace("/", ".") + ".lock"
