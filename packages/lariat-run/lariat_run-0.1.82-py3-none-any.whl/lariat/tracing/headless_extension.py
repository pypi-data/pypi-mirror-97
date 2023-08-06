import os
import json
import logging

log = logging.getLogger(__name__)

if os.environ.get("LARIAT_DEBUG"):
    logging.basicConfig(level=logging.DEBUG)


class HeadlessExtension(object):
    def set_output_directory(self, path):
        self._dir = path

    def set_output_file(self, filepath):
        self._file = filepath

    def write(self, out):
        if hasattr(self, "_file"):
            for fpath, output in out.items():
                with open(self._file, "w") as f:
                    json.dump(output, f)
                log.info("Wrote trace to file %s", self._file)
        elif hasattr(self, "_dir"):
            try:
                if not os.path.exists(self._dir):
                    os.makedirs(self._dir, exist_ok=True)
            except OSError:
                log.error("Could not create directory %s", self._dir)
                return

            for fpath, output in out.items():
                fullpath = os.path.join(self._dir, fpath)
                with open(fullpath, "w") as f:
                    json.dump(output, f)

                log.info("Wrote trace to file %s", fullpath)
