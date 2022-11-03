from typing import List
from invoke import task
import invoke
import detect
from invoke import Context


def _is_arm_macos(c) -> bool:
    if not detect.osx:
        return False
    return c.run("uname -p").stdout.count("arm") > 0


def _list_minimal(c):
    pkgs = []

    return pkgs


def _list_minimal_mac(c):
    pkgs = []

    pkgs += [
        "git",
        "macvim",
        "python",
    ]

    return pkgs


def _list_packages(c):
    pkgs = []

    is_arm_macos = _is_arm_macos(c)

    if detect.osx:
        pkgs += ["coreutils"]

    # CLI toolset
    pkgs += [
        "ghq",
        "gh",
    ]

    # develop
    pkgs += []

    # cloud
    pkgs += [
        "tfenv",
    ]

    # kubernetes
    if not is_arm_macos:
        pkgs += [
            "kubectx",
        ]

    return pkgs


def setHome(c: invoke.Context) -> dict:
    env = {}
    if len(c.run("echo $HOME", hide=True).stdout.strip()) == 0:
        env["HOME"] = c.run("cd ~;pwd", hide=True).stdout.strip()
    return env


@task(default=True)
def default(c):
    if c.run("which brew", warn=True).failed:
        return
    update(c)
    install(c)
    unlink(c)


@task
def update(c):
    env = setHome(c)
    c.run("brew update", env=env)
    c.run("brew upgrade", env=env)
    c.run("brew cleanup", env=env)


@task
def install(c):
    pkgs = _list_minimal(c)
    pkgs += _list_packages(c)
    installed = c.run("brew list").stdout.split("\n")
    pkgs = set(pkgs) - set(installed)
    env = setHome(c)
    if len(pkgs) > 0:
        c.run("brew install " + " ".join(pkgs), env=env)
    unlink(c)


@task
def install_minimal(c):
    pkgs = _list_minimal(c)
    if detect.mac:
        pkgs += _list_minimal_mac(c)
    installed = c.run("brew list").stdout.split("\n")
    pkgs = set(pkgs) - set(installed)
    env = setHome(c)
    if len(pkgs) > 0:
        c.run("brew install " + " ".join(pkgs), env=env)


@task
def show_dependency(c):
    c.run("brew deps --tree --installed")


@task
def unlink(c):
    installed = c.run("brew list").stdout.split("\n")
    pkgs = [
        "go",
    ]
    if detect.linux:
        pkgs += [
            "openssl@1.1",
            "python@3.9",
            "autoconf",
            "patchelf",
            "bzip2",
            "libbsd",
            "m4",
            "ncurses",
            "node-build",
            "perl",
            "pkg-config",
            "readline",
            "unzip",
            "util-linux",
            "zlib",
            "kubernetes-cli",
        ]
    unlink: list[str] = [pkg for pkg in pkgs if pkg in installed]
    if not unlink:
        return

    c.run("brew unlink " + " ".join(unlink))
