import json
import logging
import logging.handlers
import sys


import backoff
import requests

log = logging.getLogger(__name__)


def is_windows():
    return sys.platform.startswith("win")


def read_stdout(proc, lines):
    """ Reads all remaining stdout """
    buffer = []
    if proc and proc.stdout:
        while True:
            line = proc.stdout.readline()
            if not line and proc.poll() is not None:
                return
            log.debug("Action stdout: %s", line.rstrip())
            # under windows, there is a timing issue with poll() that can cause us
            # to append many empty lines at the end
            # We avoid this without truncating empty lines in the middle of the output by only
            # adding to lines when current line is nonempty.
            buffer.append(line)
            if line.strip():
                lines.extend(buffer)
                buffer = []
    return None


# 24h is also equal to the maximum task timeout
MAXIMUM_API_REQUEST_RETRY_DURATION_SECONDS = 24 * 3600
# max. 5 minutes between attempts
MAXIMUM_API_REQUEST_WAIT_TIME_SECONDS = 300


def api_response_predicate(r):
    """
    Currently, we retry on
    502 Bad Gateway
    503 Service Unavailable
    504 Gateway Timeout
    """

    return r.status_code in [502, 503, 504]


def setup_backoff_handler(handler=None):
    bl = logging.getLogger("backoff")
    if len([h for h in bl.handlers if not isinstance(h, logging.NullHandler)]) == 0:
        if handler is None:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "[%(asctime)s %(levelname)s/%(threadName)s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)
        logging.getLogger("backoff").addHandler(handler)


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
def report_action_result(njinn_api, action_output, action_context, result_url):
    """
    Report action result of the task to the Njinn API.
    """

    config = njinn_api.config
    action_output["context"] = action_context
    if not "state_info" in action_output and "state" in action_output:
        action_output["state_info"] = action_output["state"]

    action_output["worker"] = config.worker_name

    log.info(f"Calling {result_url} with action output {json.dumps(action_output)}")

    r = njinn_api.put(result_url, json=action_output)
    if r.status_code == 413:
        if action_output["log"]:
            log.warning("Request too large, trying with a truncated log")
            first_lines = "\n".join(action_output["log"][:1000].split("\n")[:-1])
            last_lines = "\n".join(action_output["log"][-1000:].split("\n")[1:])
            truncated_log = (
                "Log too long - Truncated version: \n\n"
                + first_lines
                + "\n...(output omitted here)...\n"
                + last_lines
            )
            action_output["log"] = truncated_log
            r = njinn_api.put(result_url, json=action_output)

    log.info(f"Response: {r.status_code} {r.text}")
    return r

