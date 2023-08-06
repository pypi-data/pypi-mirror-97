#!/usr/bin/env python
from __future__ import print_function

from distutils import spawn
import os
import os.path as path
import sys
import logging
import argparse
import json
#from urllib import request

from lariat.config import TracerConfig

if os.environ.get("LARIAT_DEBUG"):
    logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

USAGE = """
lariat-run <my_program>

Example: lariat-run python main.py

Flags:
--output $FILE  Dump Lariat Trace output to the path indicated by $FILE. The trace is NOT sent to Lariat's cloud service
--upload $FILE  Upload trace at the path indicated by $FILE
--headless Enable Headless mode. Dump all Lariat Trace output (including infrastructure metrics) to a long-term archival directory. The data is NOT sent to Lariat's cloud service
--output-dir In Headless Mode, specify the archive directory. When not specified, defaults to $PWD/lariat_data. --output-dir is a no-op when --headless is not passed
-h, --help Show this help message

Example:
# Output trace to a file called trace.json
lariat-run --output trace.json python main.py
# Upload trace at path "trace.json"
lariat-run --upload trace.json

Example:
# Archive output in default archive directory
lariat-run --headless python main.py
# Archive output in /var/log/lariat
lariat-run --headless --output-dir /var/log/lariat  python main.py

Use --output and --upload for one-off sanity checks when you eventually intend to send data to Lariat's cloud.

Use --headless and --output-dir for long-term setups where data will be archived outside of Lariat's cloud.
"""


def _root():
    return os.path.dirname(path.abspath(path.join(__file__, "../")))


def _add_bootstrap_to_pythonpath(bootstrap_dir):
    """
    Add our bootstrap directory to the head of $PYTHONPATH to ensure
    it is loaded before program code
    """
    python_path = os.environ.get("PYTHONPATH", "")

    if python_path:
        new_path = "%s%s%s" % (bootstrap_dir, os.path.pathsep, os.environ["PYTHONPATH"])
        os.environ["PYTHONPATH"] = new_path
    else:
        os.environ["PYTHONPATH"] = bootstrap_dir


def _make_metrics_payload(data):
    if "metrics" not in data or "id" not in data:
        return None

    return {"id": data["id"], "metrics": data["metrics"]}


def _make_trace_payload(data):
    if "traces" in data:
        return data

    if "id" in data:
        # Assume data is from headless mode
        id = data["id"]

        payload = {"traces": [{"id": id, "trace": data["trace"]}]}
        return payload

    return data


def _upload_file(path):
    url = TracerConfig.host + TracerConfig.traces_url
    data = open(path, "rb")
    traces = json.load(data)
    payload = _make_trace_payload(traces)
    metrics = _make_metrics_payload(traces)

    formatted = json.dumps(payload).encode("utf-8")

    req = request.Request(url, data=formatted)
    req.add_header("Content-Type", "application/json")
    resp = request.urlopen(req)

    if metrics is not None:
        formatted_metrics = json.dumps(metrics).encode("utf-8")
        req = request.Request(
            TracerConfig.host + TracerConfig.metrics_url, data=formatted_metrics
        )
        req.add_header("Content-Type", "application/json")
        resp = request.urlopen(req)

    if len(payload["traces"]) > 0:
        for trace in payload["traces"]:
            log.warning(
                "Access the trace for your execution on Lariat: %s",
                "{}/traces/{}".format(TracerConfig.host, trace["id"]),
            )


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        return

    log.debug("sys.argv: %s", sys.argv)

    parser = argparse.ArgumentParser(prog="lariat-run", usage=USAGE)
    parser.add_argument("--upload", type=str, required=False)

    parser.add_argument(
        "--output", type=str, required=False,
    )

    parser.add_argument("--headless", action="store_true", required=False)

    parser.add_argument(
        "--output-dir", type=str, required=False,
    )

    args, stem = parser.parse_known_args()
    if args.upload is not None:
        _upload_file(args.upload)
        return

    if args.output:
        os.environ["LARIAT_DRY_RUN"] = "true"
        os.environ["LARIAT_FILE_OUTPUT"] = args.output

    if args.headless:
        os.environ["LARIAT_DRY_RUN"] = "true"
        os.environ["LARIAT_HEADLESS_MODE"] = "true"
        if args.output_dir is not None:
            os.environ["LARIAT_HEADLESS_MODE_OUTPUT"] = args.output_dir

    log.debug("parsed args: %s stem: %s", args, stem)

    root_dir = _root()
    bootstrap_dir = os.path.join(root_dir, "bootstrap")
    log.debug("lariat bootstrap: %s", bootstrap_dir)

    _add_bootstrap_to_pythonpath(bootstrap_dir)
    log.debug("PYTHONPATH: %s", os.environ["PYTHONPATH"])
    log.debug("sys.path: %s", sys.path)

    executable = stem[0]
    executable_args = stem[1:]

    # Find the executable path
    executable = spawn.find_executable(executable)
    log.debug("program executable: %s", executable)
    log.debug("program executable args: %s", executable_args)

    if "LARIAT_SERVICE_NAME" not in os.environ:
        # infer service name from program command-line
        service_name = os.path.basename(executable)
        os.environ["LARIAT_SERVICE_NAME"] = service_name

    pid = os.getpid()
    log.debug("Process: %s", pid)
    os.environ["LARIAT_PID"] = str(pid)

    os.execl(executable, executable, *executable_args)
