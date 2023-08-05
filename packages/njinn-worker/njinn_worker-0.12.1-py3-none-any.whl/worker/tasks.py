import os
import signal
import subprocess
from multiprocessing import Process
from pathlib import Path
from time import sleep

from celery import exceptions
from celery.signals import after_setup_logger, after_setup_task_logger
from celery.utils.log import get_task_logger
from celery.worker.control import control_command, inspect_command

from worker import shared_logging

# use absolute paths to be consistent & compatible bewteen worker code and the scripts
from worker.api_client import NjinnAPI
from worker.celery_utils import get_celery_app
from worker.config import ActionExecutionConfig, WorkerConfig
from worker.utils import is_windows, report_action_result


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logger.addHandler(shared_logging.shared_handler)


@after_setup_task_logger.connect
def setup_task_loggers(logger, *args, **kwargs):
    logger.addHandler(shared_logging.shared_handler)


config = WorkerConfig().load_from_file().update_from_api()
app = get_celery_app(config.messaging_url)
log = get_task_logger(__name__)
pid = os.getpid()


@app.task(name="njinn_execute")
def njinn_execute(action, pack, action_context):
    proc = None
    working_dir = None

    try:
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        log.info("Njinn task initiating %s %s", pid, os.getpid())

        action_execution_id = action_context.get("action_execution_id")
        working_dir = os.path.join("working", action_execution_id)
        log.debug("Creating working directory %s", working_dir)
        os.makedirs(working_dir)

        ActionExecutionConfig(
            working_dir,
            config_path=os.path.abspath(config.config_path),
            action=action,
            pack=pack,
            action_context=action_context,
        ).save()

        # Run detached, without a shell, and start a new group
        if is_windows():
            py_cmd = "python.exe"
        else:
            py_cmd = "python"

        cmd = [
            py_cmd,
            "action_task.py",
            f"{working_dir}",
        ]

        log.info("Running: %s", cmd)
        env = os.environ.copy()
        env["njinn_secrets_key"] = config.secrets_key
        proc = subprocess.Popen(cmd, cwd=dir_path, start_new_session=True, env=env)
        proc.wait()
        log.info("Finished waiting.")
    except exceptions.SoftTimeLimitExceeded:
        log.info("Timeout")

        if proc:
            try:
                log.info("Trying to terminate child proces %s", proc.pid)
                proc.terminate()
            except Exception as e:
                log.warning("Problem terminating child process: %s", e)
        else:
            log.warning("No process found to terminate")

    return None


@inspect_command(args=[("action_context", dict)])
def njinn_upload_action_execution_log(state, action_context):
    log.info("Uploading log for %s", action_context)
    task_log_dir = "./task_logs"
    logfile = os.path.join(
        task_log_dir,
        f"{action_context['execution_id']}-{action_context['task_name']}-{action_context['action_execution_id']}.log",
    )
    try:
        with open(logfile, "rt") as f:
            log_content = f.read()
        report_action_result(
            NjinnAPI(config),
            {"log": log_content},
            action_context,
            "/api/v1/workercom/action_execution_log",
        )
    except:
        log.debug("Could not read: %s", logfile)
    return {}


@control_command(args=[("action_execution_id", str)])
def njinn_cancel_action_execution(state, action_execution_id):
    log.info("Cancel requested for %s.", action_execution_id)
    pid_dir = Path(__file__).parent / "pids"
    pidfile = pid_dir / f"{action_execution_id}.pid"
    if pidfile.exists():
        try:
            pid = int(float(pidfile.read_text().split("\n")[0]))
            log.info(
                "Terminating action process for %s with PID %s",
                action_execution_id,
                pid,
            )
            os.kill(pid, signal.SIGTERM)
        except FileNotFoundError:
            log.info("Not running anymore %s.", action_execution_id)
        except Exception as e:
            log.warning(
                "Error cancelling task %s: %s", action_execution_id, str(e), exc_info=e
            )
    else:
        log.info("Not running anymore %s.", action_execution_id)
    return {}


@inspect_command()
def njinn_upload_worker_log(state):
    # ensure buffer isn't empty
    log.info("Worker log requested by server.")
    shared_logging.flush()
    return {}


@inspect_command(args=[("log_level", str)])
def njinn_set_log_level(state, log_level):
    log.info("Ignoring log level change to %s", log_level)
    # shared_logging.set_level(log_level)
    # log.debug("This is a debug message after log level change.")
    # log.info("This is a info message after log level change.")
    # log.warning("This is a warning message after log level change.")
    # log.error("This is a error message after log level change.")
    return {}


@inspect_command(
    args=[("action", str), ("pack", str), ("action_context", dict), ("timeout", int)],
)
def run_ad_hoc(state, action, pack, action_context, timeout):
    """
    Run `njinn_execute` in separate process and wait `timeout` seconds for a result.
    If the action execution is longer than `timeout` command return and
    forget about it (however it's still processed).
    """

    p = Process(target=njinn_execute, args=(action, pack, action_context))
    p.start()
    t = 0
    while t <= timeout:
        sleep_value = 0.1
        sleep(sleep_value)
        t += sleep_value
        if not p.is_alive():
            break

