from . import defaults
import os


class CommandLineConfig(object):
    def get_host(self):
        return None


class EnvConfig(object):
    def get_host(self):
        return os.environ.get("LARIAT_HOST", None)

    def get_trace_template_path(self):
        return os.environ.get("LARIAT_TRACE_TEMPLATE_PATH", None)

    def get_dry_run(self):
        return os.environ.get("LARIAT_DRY_RUN", None) or os.environ.get("LARIAT_HEADLESS_MODE", None)


class BaseConfig(object):
    def __init__(self):
        self.command_line = CommandLineConfig()
        self.env = EnvConfig()

    @property
    def dry_run(self):
        self.env.get_dry_run() or defaults.DRY_RUN

    @property
    def host(self):
        return self.command_line.get_host() or self.env.get_host() or defaults.HOST

    @property
    def traces_url(self):
        return defaults.TRACES_URL

    @property
    def metrics_url(self):
        return defaults.METRICS_URL

    @property
    def request_buffer_size(self):
        return defaults.REQUEST_BUFFER_SIZE

    @property
    def trace_template_path(self):
        return self.env.get_trace_template_path() or defaults.TRACE_TEMPLATE_PATH

    @property
    def metrics_max_buffer_size(self):
        return defaults.METRICS_MAX_BUFFER_SIZE

    @property
    def metrics_reporting_interval(self):
        return defaults.METRICS_REPORTING_INTERVAL
