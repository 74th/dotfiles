from invoke.tasks import task
from invoke.context import Context
import detect


def _list_packages(c):
    pkgs = []

    if detect.osx:
        pkgs += [
            "coreutils",
            "git",
            "python",
            "gh",
            "ghq",
            "gpg",
            "pinentry",
            "pipx",
            "pnpm",
            "direnv",
            "peco",
            "nodenv",
            "unar",
            "trash-cli",
            "pnpm",
        ]

    # CLI toolset
    pkgs += [
        "ghq",
    ]

    # develop
    pkgs += []

    # cloud
    pkgs += [
        "tfenv",
    ]

    # fonts
    pkgs += [
        "font-monaspace",
        "font-monaspace-nerd-font",
        "font-source-code-pro",
        "font-moralerspace",
        "font-moralerspace-jpdoc",
        "font-moralerspace-hw",
    ]

    return pkgs


def setHome(c: Context) -> dict:
    env = {}
    r = c.run("echo $HOME", hide=True)
    assert r is not None
    if len(r.stdout.strip()) == 0:
        r = c.run("cd ~;pwd", hide=True)
        assert r is not None
        env["HOME"] = r.stdout.strip()
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
    pkgs = _list_packages(c)
    installed = c.run("brew list").stdout.split("\n")
    pkgs = set(pkgs) - set(installed)
    env = setHome(c)
    if len(pkgs) > 0:
        c.run("brew install " + " ".join(pkgs), env=env)
    unlink(c)


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
