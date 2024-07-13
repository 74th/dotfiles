from invoke.tasks import task
from invoke.context import Context
import invoke


@task
def install_rust(c: Context):
    c.run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh", pty=True)


@task
def install_binstall(c: Context):
    r = c.run("which cargo-binstall", warn=True, hide=True)
    assert r is not None
    if r.ok:
        return
    c.run(
        "curl -L --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/cargo-bins/cargo-binstall/main/install-from-binstall-release.sh | bash",
        pty=True,
    )


def list_packages() -> list[str]:
    pkg = [
        "lsd",
        "bat",
        "ripgrep",
        "cargo-generate",
    ]
    return pkg


def list_installed(c: Context) -> list[str]:
    installed: list[str] = []
    r = c.run("cargo install --list", hide=True)
    assert r is not None
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
    install_binstall(c)

    r = c.run("which cargo", warn=True)
    assert r is not None
    if r.failed:
        print("!! cargo not found !!")
        return
    pkgs = list_packages()
    installed = list_installed(c)
    targets = set(pkgs) - set(installed)
    if len(targets) > 0:
        c.run("cargo binstall -y " + " ".join(targets))
