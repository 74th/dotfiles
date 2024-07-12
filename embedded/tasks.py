import pathlib
import json

from invoke.tasks import task
from invoke.context import Context

from rust.tasks import list_installed as list_installed_cargo

UBUNTU_PACKAGES = {
    "build-essential",
    "libnewlib-dev",
    "gcc-riscv64-unknown-elf",
    "gcc-arm-none-eabi",
    "libnewlib-arm-none-eabi",
    "libstdc++-arm-none-eabi-newlib",
    "libusb-1.0-0-dev",
    "libudev-dev",
    "gdb-multiarch",
    "make",
    "pkg-config",
    "cmake",
    "gcc",
    "g++",
}

PIPX_PACKAGES = {
    "platformio",
    "esptool",
    "pyocd",
}

CARGO_PACKAGES = {
    "wlink",
    "wchisp",
    "espflash",
    "cargo-espflash",
    "probe-rs-tools",
}

OTHER_PACKAGES = {
    (
        "arduino-cli",
        "curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh",
    )
}


@task
def install_with_pipx(c: Context):
    r = c.run("pipx list --json", hide=True)
    assert r

    installed = set(json.loads(r.stdout)["venvs"].keys())

    targets = list(PIPX_PACKAGES - installed)

    for t in targets:
        c.run(f"pipx install {t}")


@task
def install_with_cargo(c: Context):
    installed = list_installed_cargo(c)

    targets = list(CARGO_PACKAGES - set(installed))

    for t in targets:
        c.run(f"cargo binstall -y {t}")


@task
def install_with_apt(c: Context):
    r = c.run("apt list --installed", hide=True)
    assert r

    installed: list[str] = []
    for l in r.stdout.splitlines():
        installed.append(l.split("/")[0].strip())

    targets = list(UBUNTU_PACKAGES - set(installed))

    if not targets:
        return

    c.run("sudo apt update")
    c.run("sudo apt install -y " + " ".join(targets))


def install_other(c: Context, package: str, cmd: str):
    with c.cd(pathlib.Path("~").expanduser()):
        r = c.run(f"which {package}", warn=True/
        assert r is not None
        if r.failed:
            c.run(cmd, pty=True)


@task
def install_others(c: Context):
    for package, cmd in OTHER_PACKAGES:
        install_other(c, package, cmd)


@task
def install(c: Context):
    install_with_apt(c)
    install_with_pipx(c)
    install_with_cargo(c)
    install_others(c)
