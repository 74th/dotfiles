import re
from typing import List, cast
from invoke import task
import invoke


def npm_packages(small=False) -> list[str]:
    pkg = [
        "fkill-cli",
        "npm",
        "@vivliostyle/cli",
        "gts",
        "yarn",
    ]
    return pkg


def rust_packages(small=False) -> list[str]:
    pkg = []
    return pkg


def npm_installed(c: invoke.Context) -> list[str]:
    installed: list[str] = []
    lines = cast(str, c.run("npm ls -g", hide=True).stdout)
    for line in lines.split("\n"):
        m = re.match(r"^[├└]─[-┬] (\S+)@[\d.]+", line)
        if m:
            installed.append(m.groups()[0])
    return installed


@task
def npm(c, small=False):
    if c.run("which npm", warn=True).failed:
        print("!! npm not found !!")
        return
    pkgs = npm_packages()
    installed = npm_installed(c)
    targets = set(pkgs) - set(installed)
    if len(targets) > 0:
        c.run("npm install -g " + " ".join(targets))


@task
def upgrade_npm(c, small=False):
    if c.run("which npm", warn=True).failed:
        print("!! npm not found !!")
        return
    pkgs = npm_packages()
    c.run("npm upgrade -g " + " ".join(pkgs))


def rust_installed(c: invoke.Context) -> list[str]:
    installed: list[str] = []
    lines = c.run("cargo install --list").stdout
    for line in lines.split("\n"):
        if line and line[0] == " ":
            continue
        s = line.split(" ")
        if len(s) >= 2:
            installed.append(s[0])
    return installed


@task
def rust(c, small=False):
    if c.run("which cargo", warn=True).failed:
        print("!! cargo not found !!")
        return
    pkgs = rust_packages()
    installed = rust_installed(c)
    targets = set(pkgs) - set(installed)
    if len(targets) > 0:
        c.run("cargo install " + " ".join(targets))


@task
def install(c, small=True):
    npm(c, small)
    rust(c, small)
