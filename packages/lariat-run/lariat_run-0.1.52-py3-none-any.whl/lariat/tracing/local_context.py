from collections import deque

from lariat.config import TracerConfig
from .headless_extension import HeadlessExtension

import os
import json
import random
import logging
from urllib import request
from datetime import datetime

log = logging.getLogger(__name__)

CPU_PERCENT = "cpu_percent"
MEM_PERCENT = "mem_percent"
NUM_THREADS = "num_threads"


def _make_request(url, data):
    data = data.encode("utf-8")
    req = request.Request(url, data=data)
    req.add_header("Content-Type", "application/json")
    resp = request.urlopen(req)


def _print_trace_urls(traces, host):
    if len(traces["traces"]) > 0:
        for trace in traces["traces"]:
            log.warning(
                "Access the trace for your execution on Lariat: %s",
                "{}/traces/{}".format(host, trace["id"]),
            )


class LocalContext(object):
    """
    Class that stores context about the current nested set of traces
    It keeps track of parent-child relationships

    If a span exists, it has a corresponding empty child map
    """

    def __init__(
        self,
        trace_id=None,
        span_id=None,
        service="Default",
        dry_run=False,
        file_output=None,
        headless=False,
        headless_output=None,
    ):
        if span_id is None:
            span_id = random.getrandbits(32)

        if trace_id is None:
            trace_id = random.getrandbits(32)

        self.trace_id = trace_id
        self.child_map = {}
        self.spans_by_id = {}
        self.ordered_trace_deque = deque([span_id])
        self.child_map[span_id] = []
        self.service = service
        self.trace_buffer = {self.trace_id: []}

        self._file_output = file_output
        self._dry_run = dry_run

        if headless:
            self._headless = HeadlessExtension()
            self._headless.set_output_directory(headless_output)
        else:
            self._headless = None

    def get_current_span_from_parent_tree(self):
        """
        Returns the trace that is currently at the lowest level
        in the dependency tree
        :return:
        """
        return self.ordered_trace_deque[-1]

    def remove_current_span_from_parent_tree(self):
        """
        Removes a trace from the lowest level of the dependency tree.
        :return:
        """
        self.ordered_trace_deque.pop()

    def add_new_span_to_parent_tree(self, new_trace=None):
        if new_trace is None:
            new_trace = random.getrandbits(32)
        self.child_map[new_trace] = []
        self.child_map[self.get_current_span_from_parent_tree()].append(new_trace)
        self.ordered_trace_deque.append(new_trace)

    def add_span_to_trace_buffer(self, span_record):
        span_as_map = span_record.convert_span_record_to_key_value()
        self.trace_buffer[self.trace_id].append(span_as_map)
        self.spans_by_id[span_as_map["span_id"]] = span_as_map

        if len(self.trace_buffer[self.trace_id]) >= TracerConfig.request_buffer_size:
            self.flush_buffer_to_agent()

    def _get_fully_described_child(self, child):
        span_as_map = self.spans_by_id[child]
        span_as_map["id"] = span_as_map["span_id"]
        if "data_transform" in span_as_map["meta"]:
            dt = span_as_map["meta"].pop("data_transform")
            span_as_map["data_transform"] = dt

        span_as_map["children"] = [
            self._get_fully_described_child(child) for child in span_as_map["children"]
        ]

        return span_as_map

    def _get_root(self, trace):
        # find the root span
        root = None

        for span in trace:
            if span["parent_id"] == 0:
                root = span
                break

        if not root:
            # No span found with parent_id 0. Instead select the earliest known span and consider it root.
            root = sorted(trace, key=lambda x: x["start_time"])[0]

        return root

    def _get_fully_described_trace(self, trace):
        root = self._get_root(trace)

        root["children"] = [
            self._get_fully_described_child(child) for child in root["children"]
        ]
        root["id"] = root["span_id"]

        return root

    def close_auto_main_span(self):
        from lariat.patch.statsd_config import DEFAULT_STATSD_CLIENT as stats

        if hasattr(stats, "_main_timer"):
            stats._main_timer.stop()

    def _make_headless_trace_output(self, stats, trace_list):
        filenames_to_output = {}
        for trace in trace_list["traces"]:
            start_time = trace["trace"]["start_time"]
            start_time = datetime.utcfromtimestamp(start_time / 10 ** 6)
            start_time = start_time.strftime("%Y-%m-%dT%H.%M.%S")

            filename = f"{start_time}_{trace['id']}.trace"
            trace["metrics"] = stats

            output = trace
            filenames_to_output[filename] = output

        return filenames_to_output

    def _convert_stats_to_metrics_payload(self, stats):
        metrics_payload = { "metrics": {} }
        timestamps, cpu_percent, mem_percent, num_threads = [], [], [], []

        for x in stats:
            timestamps.append(x['timestamp'])
            metrics = x['metrics']
            cpu_percent.append(metrics[CPU_PERCENT])
            mem_percent.append(metrics[MEM_PERCENT])
            num_threads.append(metrics[NUM_THREADS])

        timestamps = [x['timestamp'] for x in stats]
        cpu_percent_payload = {"timestamps": timestamps, "values": cpu_percent, "label": "CPU Percent", "unit": "%"}
        mem_percent_payload = {"timestamps": timestamps, "values": mem_percent, "label": "Mem Percent", "unit": "%"}
        num_threads_payload = {"timestamps": timestamps, "values": num_threads, "label": "Num Threads", "unit": "#"}

        metrics_payload["metrics"][CPU_PERCENT] = cpu_percent_payload
        metrics_payload["metrics"][MEM_PERCENT] = mem_percent_payload
        metrics_payload["metrics"][NUM_THREADS] = num_threads_payload

        return metrics_payload


    def _make_trace_output(self, stats, trace_list):
        files_created = []

        for trace in trace_list["traces"]:
            start_time = trace["trace"]["start_time"]
            start_time = datetime.utcfromtimestamp(start_time / 10 ** 6)
            start_time = start_time.strftime("%Y-%m-%dT%H.%M.%S")
            metrics_payload = self._convert_stats_to_metrics_payload(stats)

            trace_html_filename = f"{start_time}_{trace['id']}.trace.html"
            with open(TracerConfig.trace_template_path) as f:
                content = f.read()
                content = content.replace("{{ traceJson }}", json.dumps({"trace": trace}))
                content = content.replace("{{ metricsJson }}", json.dumps(metrics_payload))

                with open(trace_html_filename, 'w') as f2:
                    f2.write(content)

            files_created.append(trace_html_filename)

        return files_created

    def get_metric_stats_buffer(self):
        from lariat.patch.statsd_config import DEFAULT_STATSD_CLIENT as stats
        if hasattr(stats, '_metrics_thread'):
            return stats._metrics_thread.flush_stats_buffer()

        return []

    def stop_metrics_thread(self):
        from lariat.patch.statsd_config import DEFAULT_STATSD_CLIENT as stats

        if hasattr(stats, "_metrics_stop"):
            stats._metrics_stop.set()

    def flush_buffer_to_agent(self):
        # Trace payload should look like
        # { "traces": [ { "id': "xyz", "trace": {} }, ...  ] }

        # Fastpath for when import is a side-effect
        if len(self.trace_buffer) == 0:
            return

        trace_list = {"traces": []}

        for trace_id, trace in self.trace_buffer.items():
            if len(trace) > 0:
                trace_list["traces"].append(
                    {"id": trace_id, "trace": self._get_fully_described_trace(trace)}
                )

        log.debug("submitting to Lariat: %s", trace_list)
        stats = self.get_metric_stats_buffer()

        if not self._dry_run:
            try:
                _make_request(
                    TracerConfig.host + TracerConfig.traces_url, json.dumps(trace_list)
                )
                stats_data = json.dumps(
                    {"id": self.trace_id, "metrics": stats}, default=str
                )
                _make_request(
                    TracerConfig.host + TracerConfig.metrics_url, stats_data
                )
            except Exception as e:
                log.error("Failed to submit trace: %s", e)
        else:
            log.info("Dry run mode. Not submitting trace")

            if self._headless is not None:
                files_written = self._make_trace_output(stats, trace_list)
                # TODO: deprecate this since the functionality is subsumed by local viz. mode
                out = self._make_headless_trace_output(stats, trace_list)
                log.info("Wrote trace files %s", files_written)

            if self._file_output:
                with open(self._file_output, "w") as out:
                    log.info("writing trace to %s", self._file_output)
                    json.dump(trace_list, out)

        if not self._dry_run:
            _print_trace_urls(trace_list, TracerConfig.host)

        self.trace_buffer.clear()
        self.trace_buffer[self.trace_id] = []
