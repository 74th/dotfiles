from typing import List
from invoke import task
import invoke


def list_packages() -> List[str]:
    pkg = [
        "lsd",
        "bat",
        "ripgrep",
    ]
    return pkg


def list_installed(c: invoke.Context) -> List[str]:
    installed: List[str] = []
    lines = c.run("cargo install --list").stdout
    for line in lines.split("\n"):
        if line and line[0] == " ":
            continue
        s = line.split(" ")
        if len(s) >= 2:
            installed.append(s[0])
    return installed


@task(default=True)
def install(c):
    if c.run("which cargo", warn=True).failed:
        print("!! cargo not found !!")
        return
    pkgs = list_packages()
    installed = list_installed(c)
    targets = set(pkgs) - set(installed)
    if len(targets) > 0:
        c.run("cargo install " + " ".join(targets))
