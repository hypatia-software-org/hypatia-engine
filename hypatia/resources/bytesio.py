import io

from hypatia import class_default

@class_default
class BytesIO(io.BytesIO):
    def __init__(self, respack, path, initial_bytes):
        super().__init__(initial_bytes)
        self._respack = respack
        self._path_in_respack = path
        self._modified = False

    def write(self, b):
        super().write(b)
        self._modified = True

    def flush(self):
        self._respack._update_file_contents(self._path_in_respack, self.getvalue())

    def close(self):
        self.flush()
        super().close()
