import re
from invoke.tasks import task
from invoke.context import Context


def npm_packages() -> list[str]:
    pkg = [
        "fkill-cli",
        "npm",
        "@vivliostyle/cli",
        "gts",
        "yarn",
    ]
    return pkg


def rust_packages() -> list[str]:
    pkg = []
    return pkg


def npm_installed(c: Context) -> list[str]:
    installed: list[str] = []
    r = c.run("npm ls -g", hide=True)
    assert r is not None
    lines = r.stdout
    for line in lines.split("\n"):
        m = re.match(r"^[├└]─[-┬] (\S+)@[\d.]+", line)
        if m:
            installed.append(m.groups()[0])
    return installed


@task
def npm(c: Context):
    r = c.run("which npm", warn=True)
    assert r is not None
    if r.failed:
        print("!! npm not found !!")
        return
    pkgs = npm_packages()
    installed = npm_installed(c)
    targets = set(pkgs) - set(installed)
    if len(targets) > 0:
        c.run("npm install -g " + " ".join(targets))


@task
def upgrade_npm(c: Context):
    r = c.run("which npm", warn=True)
    assert r is not None
    if r.failed:
        print("!! npm not found !!")
        return
    pkgs = npm_packages()
    c.run("npm upgrade -g " + " ".join(pkgs))


def rust_installed(c: Context) -> list[str]:
    installed: list[str] = []
    r = c.run("cargo install --list")
    assert r is not None
    lines = r.stdout
    for line in lines.split("\n"):
        if line and line[0] == " ":
            continue
        s = line.split(" ")
        if len(s) >= 2:
            installed.append(s[0])
    return installed


@task
def rust(c: Context):
    r = c.run("which cargo", warn=True)
    assert r is not None
    if r.failed:
        print("!! cargo not found !!")
        return
    pkgs = rust_packages()
    installed = rust_installed(c)
    targets = set(pkgs) - set(installed)
    if len(targets) > 0:
        c.run("cargo install " + " ".join(targets))


@task
def install(c: Context):
    npm(c)
    rust(c)
