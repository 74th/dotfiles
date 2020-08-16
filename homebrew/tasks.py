from invoke import task
import invoke
import detect
from invoke import Context


def _list_minimal(c):
    pkgs = []

    # bash
    pkgs += [
        "peco",

        # alternate cat
        "bat",
    ]

    return pkgs


def _list_minimal_mac(c):
    pkgs = []

    # bash
    pkgs += [
        "git",
        "vim",
        "python",
    ]

    return pkgs


def _list_packages(c):
    pkgs = []

    if detect.osx:
        pkgs += ["coreutils"]

    # CLI toolset
    pkgs += [
        "sqlite",
        "ghq",
        "github/gh/gh",
        "bat",
    ]

    # develop
    pkgs += [
        "hub",
        "nodenv",
        "golangci/tap/golangci-lint",
    ]

    # cloud
    pkgs += [
        "awscli",
        "tfenv",
    ]
    if detect.osx:
        pkgs += [
            "gnuplot",
        ]

    if detect.osx:
        pkgs += ["homebrew/cask/docker"]

    # kubernetes
    pkgs += [
        "kubernetes-cli",
        "kubectx",
        "stern",
    ]

    if detect.osx:
        # fonts
        pkgs += [
            "homebrew/cask-fonts/font-source-code-pro",
            "homebrew/cask-fonts/font-source-han-code-jp",
            "homebrew/cask-fonts/font-sourcecodepro-nerd-font",
            "homebrew/cask-fonts/font-fira-code",
            "homebrew/cask-fonts/font-hasklig",
            "homebrew/cask/gimp",
        ]
        pkgs += [
            # 小さいカレンダー
            "homebrew/cask/day-o",
        ]
    return pkgs


def setHome(c: invoke.Context) -> dict:
    env = {}
    if len(c.run("echo $HOME", hide=True).stdout.strip()) == 0:
        env["HOME"] = c.run("cd ~;pwd", hide=True).stdout.strip()
    return env


@task(default=True)
def default(c):
    update(c)
    install(c)


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
    pkgs = []
    if detect.linux:
        pkgs = [
            "python3",
            "openssl@1.1",
            "autoconf",
            "bzip2",
            "libbsd",
            "libffi",
            "libyaml",
            "m4",
            "ncurses",
            "node-build",
            "patchelf",
            "perl",
            "pkg-config",
            "readline",
            "unzip",
            "util-linux",
            "zlib",
            "xz",
        ]

    c.run("brew unlink " + " ".join(pkgs))
