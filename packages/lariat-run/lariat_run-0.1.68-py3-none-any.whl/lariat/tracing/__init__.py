from .local_context import LocalContext
import os

service_name = os.environ.get("LARIAT_SERVICE_NAME", "default")
dry_run = bool(os.environ.get("LARIAT_DRY_RUN", False))
file_output = os.environ.get("LARIAT_FILE_OUTPUT", None)

headless = bool(os.environ.get("LARIAT_HEADLESS_MODE", False))
headless_output = os.environ.get("LARIAT_HEADLESS_MODE_OUTPUT", "./lariat_data")

if file_output or headless:
    dry_run = True

DefaultContext = LocalContext(
    service=service_name,
    span_id=0,
    dry_run=dry_run,
    file_output=file_output,
    headless=headless,
    headless_output=headless_output,
)

import atexit

atexit.register(DefaultContext.flush_buffer_to_agent)
atexit.register(DefaultContext.close_auto_main_span)
atexit.register(DefaultContext.stop_metrics_thread)
