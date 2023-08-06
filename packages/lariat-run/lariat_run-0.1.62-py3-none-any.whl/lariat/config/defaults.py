import pathlib

HOST = "http://app.lariatdata.com"
SERVICE = "default"
FILE_OUTPUT = None
HEADLESS_MODE_OUTPUT = "./lariat_data"

TRACES_URL = "/api/traces"
METRICS_URL = "/api/metrics"
REQUEST_BUFFER_SIZE = 40

fileloc = pathlib.Path(__file__).parent.absolute()
TRACE_TEMPLATE_PATH = f"{fileloc}/../templates/trace-bundle.html"

METRICS_REPORTING_INTERVAL = 1  # seconds
METRICS_MAX_BUFFER_SIZE = 1000

DRY_RUN = False
