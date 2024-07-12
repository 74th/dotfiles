from invoke.tasks import task
from invoke.context import Context
import invoke


@task
def rust_install(c: Context):
    c.run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh", pty=True)


def list_packages() -> list[str]:
    pkg = [
        "lsd",
        "binstall",
        "bat",
        "ripgrep",
        "cargo-generate",
    ]
    return pkg


def list_installed(c: Context) -> list[str]:
    installed: list[str] = []
    r = c.run("cargo install --list")
    assert r
    lines = r.stdout
    for line in lines.split("\n"):
        if line and line[0] == " ":
            continue
        s = line.split(" ")
        if len(s) >= 2:
            installed.append(s[0])
    return installed


@task(default=True)
def install(c: Context):
    r = c.run("which cargo", warn=True)
    assert r
    if r.failed:
        print("!! cargo not found !!")
        return
    pkgs = list_packages()
    installed = list_installed(c)
    targets = set(pkgs) - set(installed)
    if len(targets) > 0:
        c.run("cargo install " + " ".join(targets))
