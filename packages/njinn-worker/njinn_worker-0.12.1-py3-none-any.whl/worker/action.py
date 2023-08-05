"""
The action wrapper is responsible for
* reading input
* decrypting encrypted input
* executing the action class with the provided parameters
* writing an output file
"""

import datetime
import decimal
import importlib
import json
import os
import re
import signal
import sys
import traceback
import uuid
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

# ensure imports keep working when invoked directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# use absolute paths to be consistent & compatible bewteen worker code and the scripts
from worker.config import ActionExecutionConfig
from worker.utils import is_windows


class WorkerResultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.time, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return "Result type bytes, not supported yet."
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class Task:
    def __init__(self, working_dir):
        self.action_config = ActionExecutionConfig(working_dir).load()
        self.output_file = os.path.abspath(
            os.path.join(self.action_config.working_dir, "out.json")
        )
        self.result = dict()
        # Initialize to gracefully fail unless successful.
        self.state = "ERROR"
        self.state_info = "Unhandled error during execution."
        self.output = {"error": self.state_info}
        self.error = None

    def load_action(self):
        # import action (try)
        action_entry_point = self.action_config.action.split(":")
        if len(action_entry_point) != 2:
            raise Exception(
                f"Entrypoint(path) misconfigured, missing ':'. '{self.action_config.action}' should look like this 'folder.file:class'"
            )
        action_module = action_entry_point[0]
        action_class_name = action_entry_point[1]

        module = f"packs.{self.action_config.pack}.{action_module}"
        mod = importlib.import_module(module)
        action_class = getattr(mod, action_class_name)

        self.action = action_class()
        setattr(self.action, "_njinn", self.action_config.njinn_api)

    def decrypt_secret_value(self, value, pattern=r"SECRET\(([-A-Za-z0-9+_=]+)\)"):
        """
        Looks for an encrypted variable and decrypt if found and
        also replaces it with the decrypted variable in ``value``.
        """

        original_value = value
        value_log = str(original_value)

        if isinstance(original_value, dict):
            value = {}
            value_log = {}
            for k, v in original_value.items():
                value[k], value_log[k] = self.decrypt_secret_value(v)
        elif isinstance(original_value, str):
            secret_values = re.findall(pattern, value)
            if secret_values:
                for secret_value in secret_values:
                    f = Fernet(self.action_config.secrets_key)
                    encrypted_variable = secret_value.encode()

                    try:
                        variable = f.decrypt(encrypted_variable).decode()
                        value = re.sub(pattern, variable, value, count=1)
                    except InvalidToken:
                        print("Invalid token for decryption of secret values.")

                value_log = re.sub(pattern, "*" * 6, original_value)

        if len(value_log) > 40:
            value_log = value_log[:40] + "..."

        return value, value_log

    def prep_files_from_storage(self, value, pattern=r"FILE\(([0-9]+)\)"):
        """
        Looks for a file reference and downloads it. If found, replace the
        reference with the temp path to the file.
        """

        original_value = value

        if isinstance(original_value, dict):
            value = {}
            value_log = {}
            for k, v in original_value.items():
                value[k] = self.prep_files_from_storage(v)
        elif isinstance(original_value, str):
            files = re.findall(pattern, value)
            if files:
                for file in files:
                    file_path = self.action_config.njinn_api.download_file(
                        file, self.action_config.working_dir
                    )
                    value = re.sub(pattern, file_path, value, count=1)

        return value

    def set_action_parameters(self):
        params = self.action_config.input["action_context"]["parameters"]

        for param, value in params.items():
            value = self.prep_files_from_storage(value)
            value, value_log = self.decrypt_secret_value(value)

            setattr(self.action, param, value)

    def write_output_file(self):
        # writes self.stdout, self.stderr, self.run_return, ... to output file
        self.result["output"] = self.output
        self.result["state"] = self.state
        self.result["state_info"] = self.state_info
        with open(self.output_file, "w") as fp:
            json.dump(self.result, fp, cls=WorkerResultEncoder)

    def setup_signals(self):
        """
        Sets up handler to process signals from the OS.
        """

        def signal_handler(signum, frame):
            """Setting kill signal handler"""
            if hasattr(self.action, "on_kill"):
                print("Cancelling action.")
                self.action.on_kill()
            self.error = None
            sys.exit(0)

        signal.signal(signal.SIGTERM, signal_handler)

    def run_action(self):
        pid_dir = Path(__file__).parent / "pids"
        pid_dir.mkdir(exist_ok=True)
        pidfile = pid_dir / f"{self.action_config.action_execution_id}.pid"

        if is_windows():
            pidfile.write_text(f"{os.getpid()}\n")
        try:
            self.load_action()
            self.set_action_parameters()
            self.setup_signals()

            os.chdir(self.action_config.working_dir)

            # When someone exit()s the script, this will jump to the finally block
            # Ensure proper status handling.
            self.error = "Action execution interrupted. exit() called?"

            action_return = self.action.run()
            self.error = None

            # defaults are task failure - unset output, state and state_info
            if action_return is not None:
                if isinstance(action_return, dict):
                    self.output = action_return
                else:
                    self.output = {"result": action_return}
            else:
                self.output = None
            self.state = "SUCCESS"

            self.state_info = None
        except KeyboardInterrupt as e:
            self.error = traceback.format_exc()
        except Exception as e:
            # We assume that actions provide meaningful messages
            # but will to show a traceback if this is not the case.
            self.error = str(e)
            if self.error == "" or self.error == "None":
                self.error = traceback.format_exc()
        finally:
            if self.error is not None:
                # explicit error handling
                self.state_info = self.error
                self.output = {"error": self.state_info}
                self.state = "ERROR"
                print("Error:")
                print(self.state_info)
            self.write_output_file()
            if pidfile.exists():
                pidfile.unlink()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "Invalid call. Require exactly one argument, which is the path to the inputfile."
        )
        sys.exit(1)

    task = Task(sys.argv[1])
    task.run_action()
