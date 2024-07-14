# pylint: disable=W0603
from enum import Enum
from pathlib import Path
import os

import detect
from invoke.context import Context


class Arch(Enum):
    amd64 = "amd64"
    arm64 = "arm64"
    riscv64 = "riscv64"
    unknown = "unknown"


def get_home() -> Path:
    home = os.environ.get("HOME", None)
    if home is not None:
        return Path(home)
    if detect.mac:
        return Path("/Users/nnyn")
    return Path("/home/nnyn")


HOME = get_home()
GHQ_DIR = HOME.joinpath("ghq")

__arch: Arch | None = None
__hostname: str | None = ""


def get_arch(c: Context) -> Arch:
    global __arch
    if __arch:
        return __arch

    r = c.run("uname -p")
    assert r is not None
    arch = r.stdout.strip()
    if arch == "x86_64":
        __arch = Arch.amd64
    elif arch == "aarch64":
        __arch = Arch.arm64
    elif arch == "riscv64":
        __arch = Arch.riscv64
    else:
        __arch = Arch.unknown
    return __arch


def get_hostname(c: Context):
    global __hostname
    if __hostname:
        return __hostname

    r = c.run("hostname")
    assert r is not None
    __hostname = r.stdout.strip()
    return __hostname
