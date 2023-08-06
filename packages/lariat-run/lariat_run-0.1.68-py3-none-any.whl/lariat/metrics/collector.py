from urllib import request
import threading
import os
import psutil
import time
import json

import logging

log = logging.getLogger(__name__)
from lariat.config import TracerConfig


def get_pid():
    os.environ.get("LARIAT_PID", None)


class MetricsThread(threading.Thread):

    def __init__(self, event, trace_id):
        super().__init__(daemon=True)
        self.stopped = event
        self.trace_id = trace_id
        self.stats_buffer = []
        self.process = psutil.Process(get_pid())

    def flush_stats_buffer(self):
        buf = self.stats_buffer.copy()

        self.stats_buffer[:] = []
        return buf

    def add_stats(self, *stats):
        self.stats_buffer.append(
            {
                "timestamp": int(time.time() * (10 ** 6)),
                "metrics": {
                    "cpu_times": stats[0],
                    "cpu_percent": stats[1],
                    "mem_info": stats[2],
                    "mem_percent": stats[3],
                    "num_threads": stats[4],
                    "num_ctx_switches": stats[5],
                    "num_open_files": stats[6],
                },
            }
        )

        # TODO: figure out a strategy for accumulating stats data when running in local mode
        # i.e. dry run = True
        if not TracerConfig.dry_run:
            if len(self.stats_buffer) >= TracerConfig.metrics_max_buffer_size:
                self.flush_stats_buffer()

    def log_metrics(self):
        with self.process.oneshot():
            cpu_times = self.process.cpu_times()
            cpu_percent = self.process.cpu_percent()
            mem_info = self.process.memory_info()
            mem_percent = self.process.memory_percent()
            num_threads = self.process.num_threads()
            num_ctx_switches = self.process.num_ctx_switches()

        num_open_files = len(self.process.open_files())

        self.add_stats(
            cpu_times,
            cpu_percent,
            mem_info,
            mem_percent,
            num_threads,
            num_ctx_switches,
            num_open_files,
        )

    def run(self):
        while not self.stopped.wait(TracerConfig.metrics_reporting_interval):
            # call a function
            self.log_metrics()
