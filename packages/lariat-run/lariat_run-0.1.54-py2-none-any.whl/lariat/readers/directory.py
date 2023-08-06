import os

import logging
import json

from datetime import datetime

log = logging.getLogger(__name__)


class TraceResult(dict):
    @property
    def metrics(self):
        return self["metrics"]

    def _sub_tree(self, root, depth, buf):
        for child in root["children"]:
            prefix = "\t" * depth
            duration = (child["end_time"] - child["start_time"]) / 10 ** 6
            suffix = f" {duration}s"

            buf.append(f"{prefix}\\")
            buf.append(f"{prefix}{child['service']}|{child['operation']}{suffix}")
            self._sub_tree(child, depth + 1, buf)

    @property
    def tree(self, depth=1):
        trace = self["trace"]
        buf = []
        duration = (trace["end_time"] - trace["start_time"]) / 10 ** 6
        suffix = f" {duration}s"

        buf.append(f"{trace['service']}|{trace['operation']}{suffix}")

        for child in trace["children"]:
            buf.append("\t\\")
            duration = (child["end_time"] - child["start_time"]) / 10 ** 6
            suffix = f" {duration}s"
            buf.append(f"\t{child['service']}|{child['operation']}{suffix}")
            self._sub_tree(child, depth + 1, buf)
        return "\n".join(buf)

    @property
    def root(self):
        return self["trace"]


class TraceResultSet(list):
    def filter(self, execution_id=None, before=None, after=None):
        assert (
            execution_id or before or after
        ), "A filter must be provided: execution_id or before or after"

        if execution_id is not None:
            for elem in self:
                if str(elem["id"]) == str(execution_id):
                    return TraceResultSet([elem])

            return TraceResultSet([])

        before_results = set()
        if before is not None:
            for elem in self:
                dt = datetime.utcfromtimestamp(
                    int(elem["trace"]["start_time"]) / 10 ** 6
                )
                if dt <= before:
                    before_results.add(elem["id"])

        after_results = set()
        if after is not None:
            for elem in self:
                dt = datetime.utcfromtimestamp(
                    int(elem["trace"]["start_time"]) / 10 ** 6
                )

                if dt >= after:
                    after_results.add(elem["id"])

        results = []

        if before and after:
            results = list(before_results.intersection(after_results))
        elif before:
            results = list(before_results)
        elif after:
            results = list(after_results)

        return TraceResultSet([t for t in self if t["id"] in results])


class Reader(object):
    def list_dir(self, path):
        raise NotImplementedError

    def read_trace(self, trace_id):
        raise NotImplementedError

    def read_dir(self, path):
        raise NotImplementedError


class S3Reader(object):
    def read_trace(self, trace_id):
        pass

    def read_dir(self, path):
        pass

    def list_dir(self, path):
        pass


class DirectoryReader(object):
    def list_dir(self, path):
        if not os.path.isdir(path):
            raise Exception(path + " is not a directory")

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return files

    def read_trace(self, path, trace_id):
        if not os.path.isdir(path):
            raise Exception(path + " is not a directory")

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for f in files:
            if str(trace_id) in f:
                fullpath = os.path.join(path, f)
                with open(fullpath) as tracefile:
                    trace = json.load(tracefile)
                    return TraceResult(trace)

        return None

    def read_dir(self, path):
        if not os.path.isdir(path):
            raise Exception(path + " is not a directory")

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        # Read JSON files into result set
        results = []
        for f in files:
            fullpath = os.path.join(path, f)

            try:
                with open(fullpath) as tracefile:
                    trace = json.load(tracefile)
                    results.append(TraceResult(trace))
            except OSError as e:
                log.error("%s: Could not open file %s", e, f)

        return TraceResultSet(results)
