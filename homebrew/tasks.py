# -*- coding: utf-8 -*-
from invoke import task
import invoke
import detect

def _list_packages(c):
    pkgs = []

    # bash
    pkgs += ["bash", "bash-completion"]

    if detect.osx:
        pkgs += ["coreutils"]

    # CLI toolset
    pkgs += [
        "wget",
        "direnv",
        "peco",
        "readline",
        "watch",
        "rsync",
        #"openssh",
        "redis",
        "sqlite",

        # alternate cat
        "bat",
    ]

    # develop
    pkgs += [
        "git",
        "hub",
        "openssl@1.1",
        "jq",
        "protobuf",
        "gcc",
        "gdb",
        "vim",
    ]

    # go
    pkgs += [
        "go",
        "dep",
    ]

    # python
    pkgs += [
        "python",
        "pyenv",
        "pyenv-virtualenv",
    ]

    # nodejs
    pkgs += [
        "nodenv",
        "node",
        "yarn",
    ]

    # cloud
    pkgs += [
        "awscli",
    ]
    if detect.osx:
        pkgs += [
            "gnuplot",
        ]

    if detect.osx:
        pkgs += [
             "homebrew/cask/docker"
        ]

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
    pkgs = _list_packages(c)
    installed = c.run("brew list").stdout.split("\n")
    pkgs = set(pkgs) - set(installed)
    env = setHome(c)
    if len(pkgs) > 0:
        c.run("brew install " + " ".join(pkgs) , env=env)
