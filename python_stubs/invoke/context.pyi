from contextlib import contextmanager
from typing import Union, Optional

class Result:
    stdout: str
    failed: bool
    ok: bool

class Context:
    def run(
        self,
        cmd: str,
        echo:Optional[bool] = None,
        warn:Optional[bool] = None,
        hide:Optional[Union[str, bool]] = None)->Result:...
    @contextmanager
    def cd(self, path: str):...
