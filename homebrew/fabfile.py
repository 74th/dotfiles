# -*- coding: utf-8 -*-
from fabric import task
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
        "openssh",
        "redis",
    ]

    # develop
    pkgs += [
        "git",
        "node",
        "openssl",
        "sqlite",
        "jq",
        "protobuf",
        "gcc",
        "gdb",
        "go",
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
        "kubernetes-helm",
        "kubectx",
        "stern",
        "kubespy",
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
            # ディスク領域可視化
            "homebrew/cask/disk-inventory-x",
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
    c: invoke.Context
    env = setHome(c)
    c.run("brew update", env=env)
    c.run("brew upgrade", env=env)


@task
def install(c):
    c: invoke.Context
    pkgs = _list_packages(c)
    env = setHome(c)
    c.run("brew install " + " ".join(pkgs) , env=env)
