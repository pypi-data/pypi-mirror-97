import subprocess

from lariat.patch.statsd_config import DEFAULT_STATSD_CLIENT as STATSD_CLIENT

import logging

log = logging.getLogger(__name__)


def patch():
    try:
        _run = subprocess.run

        def run_patched(*args, **kwargs):
            """
            New run function
            """
            with STATSD_CLIENT.timer(
                "subprocess.run", meta={"args": str(args), "kwargs": str(kwargs),}
            ):
                return _run(*args, **kwargs)

        subprocess.run = run_patched
    except Exception:
        log.info("cannot patch subprocess.run")

    try:
        _call = subprocess.call

        def call_patched(*args, **kwargs):
            """
            New call function
            """
            with STATSD_CLIENT.timer(
                "subprocess.call", meta={"args": str(args), "kwargs": str(kwargs),}
            ):
                return _call(*args, **kwargs)

        subprocess.call = call_patched
    except Exception:
        log.info("cannot patch subprocess.call")

    try:
        _Popen = subprocess.Popen

        class popen_patched(_Popen):
            def __init__(self, *args, **kwargs):
                """
                New Popen constructor
                """
                with STATSD_CLIENT.timer(
                    "subprocess.Popen", meta={"args": str(args), "kwargs": str(kwargs),}
                ):
                    super().__init__(*args, **kwargs)

        subprocess.Popen = popen_patched
        # TODO
    except Exception:
        log.info("cannot patch subprocess.Popen")

    try:
        _check_call = subprocess.check_call

        def check_call_patched(*args, **kwargs):
            """
            New check_call function
            """
            with STATSD_CLIENT.timer(
                "subprocess.check_call",
                meta={"args": str(args), "kwargs": str(kwargs),},
            ):
                return _check_call(*args, **kwargs)

        subprocess.check_call = check_call_patched
    except Exception:
        log.info("cannot patch subprocess.check_call")

    try:
        _check_output = subprocess.check_output

        def check_output_patched(*args, **kwargs):
            """
            New check_output function
            """
            with STATSD_CLIENT.timer(
                "subprocess.check_output",
                meta={"args": str(args), "kwargs": str(kwargs),},
            ):
                return _check_output(*args, **kwargs)

        subprocess.check_output = check_output_patched
    except Exception:
        log.info("cannot patch subprocess.check_output")
