"""
Bootstrapping code that is run when using the `lariat-run` Python entrypoint
Add all monkey-patching that needs to run by default here
"""
from __future__ import print_function

import os
import logging
log = logging.getLogger(__name__)

# Perform gevent patching as early as possible in the application before
# importing more of the library internals.
if os.environ.get("LARIAT_GEVENT_PATCH_ALL", "false").lower() in ("true", "1"):
    import gevent.monkey
    gevent.monkey.patch_all()

import threading

from lariat.metrics import MetricsThread

try:
    from lariat.patch import patch_all

    patch_all()  # noqa

    from lariat.patch.statsd_config import DEFAULT_STATSD_CLIENT as stats
    from lariat.tracing import DefaultContext

    if os.environ.get("LARIAT_TELEMETRY_MODE", "false").lower() in ("true", "1"):
        _main_timer = stats.timer("main")
        setattr(stats, "_main_timer", _main_timer)
        _main_timer.start()
        stop = threading.Event()
        thread = MetricsThread(stop, DefaultContext.trace_id)
        thread.start()
        setattr(stats, "_metrics_thread", thread)
        setattr(stats, "_metrics_stop", stop)
except Exception as e:
    log.exception(e)
    log.warning("errors configuring Lariat tracing")
