from pathlib import Path

import detect
from invoke.tasks import task
from invoke.context import Context


@task
def set_system_python_link(c: Context):
    if detect.mac:
        paths = [
            Path("/opt/homebrew/bin/python3"),
            Path("/usr/local/bin/python3"),
            Path("/usr/bin/python3"),
            Path("/bin/python3"),
        ]
    else:
        paths = [
            Path("/usr/local/bin/python3"),
            Path("/usr/bin/python3"),
            Path("/bin/python3"),
        ]
    for p in paths:
        if not p.exists():
            continue
        r = c.run(f"ln -sf {p} /usr/local/bin/system-python", warn=True)
        assert r is not None
        if r.ok:
            return
        c.run(f"sudo ln -sf {p} /usr/local/bin/system-python")
        return
