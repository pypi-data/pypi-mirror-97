from collections import namedtuple

SPAN_RECORD_BASE = namedtuple(
    "SpanRecord",
    "parent_id, span_id, start_time, trace_id, service, operation, end_time, children, meta",
)


class SPAN_RECORD(SPAN_RECORD_BASE):
    def convert_span_record_to_key_value(self):
        """
        This is a separate function only so we can modify this code if asdict() is deprecated.
        :param span_record:
        :return:
        """
        return self._asdict()
