from typing import cast
import glob
import sys
import os
from os import path
import invoke
from invoke import task, Collection
import detect

import homebrew.tasks as homebrew
import git.tasks as git
import arm_ubuntu.tasks as arm_ubuntu
import ubuntu.tasks as ubuntu
import golang.tasks as go
import python_pip.tasks as python_pip
import vscode.tasks as vscode
import rust.tasks as rust

ns = Collection()
ns.add_collection(ns.from_module(arm_ubuntu), "arm-ubuntu")


def get_home():
    home = os.environ.get("HOME", None)
    if home is not None:
        return home
    if detect.mac:
        return "/Users/nnyn"
    return "/home/nnyn"


HOME = get_home()
GHQ_DIR = path.join(HOME, "ghq")


def get_archi(c):
    c = cast(invoke.Context, c)
    return c.run("uname -p").stdout.strip()


def get_hostname(c):
    c = cast(invoke.Context, c)
    return c.run("hostname").stdout.strip()


def update_package_manager(c: invoke.Context):
    print("update package manager")
    if detect.linux:
        c.run("sudo apt-get update", echo=True)
    if detect.mac:
        c.run("brew update", echo=True)


def delete_file(path: str):
    if os.path.exists(path):
        os.remove(path)


def create_basic_dir(c):
    d = os.path.join(HOME, "bin")
    if not os.path.exists(d):
        os.mkdir(d)


def checkout_dotfiles(c: invoke.Context):
    print("checkout and update dotfiles")
    if c.run(f"test -e {HOME}/dotfiles", warn=True, hide="both").failed:
        c.run("git clone https://github.com/74th/dotfiles.git", echo=True)
        return
    with c.cd(f"{HOME}/dotfiles"):
        c.run("git pull")


@task
def pyenv(c):
    c = cast(invoke.Context, c)
    pyenv_dir = f"{HOME}/.pyenv"
    if not path.exists(pyenv_dir):
        c.run("ghq get github.com/pyenv/pyenv")
        c.run(f"ln -s {GHQ_DIR}/github.com/pyenv/pyenv {pyenv_dir}")
        if detect.linux:
            c.run(
                f"sudo apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev"
            )


ns.add_task(pyenv)


@task
def rehash_pyenv(c_):
    c: invoke.Context = c_
    if c.run("test -e pyenv", warn=True).ok:
        print("## rehash pyenv")
        c.run("pyenv rehash")


ns.add_task(rehash_pyenv)


@task
def bashrc(c):
    print(f"## {HOME}/.bashrc")
    bashrc = f"{HOME}/.bashrc"
    if os.path.exists(bashrc):
        with open(bashrc, "r") as f:
            body: str = f.read()
        if body.find(f"source {HOME}/dotfiles/bashrc/bashrc") > -1:
            return
    c.run(f'echo "source {HOME}/dotfiles/bashrc/bashrc" >> {HOME}/.bashrc')


ns.add_task(bashrc)


@task
def macos(c):
    print("## MacOS")
    c.run(f"mkdir -p {HOME}/.config")
    c.run("defaults write -g ApplePressAndHoldEnabled -bool false")
    c.run(f"mkdir -p {HOME}/bin")

    # macvim-kaoriya 用の mvim
    if os.path.exists("/Applications/MacVim.app/Contents/bin/"):
        c.run(f"ln -sf /Applications/MacVim.app/Contents/bin/* {HOME}/bin/")
        c.run(f"ln -sf /Applications/MacVim.app/Contents/bin/vim {HOME}/bin/vi")

    # karabiner-elements
    c.run(f"rm -rf {HOME}/.config/karabiner")
    c.run(f"ln -s {HOME}/dotfiles/karabiner-elements {HOME}/.config/karabiner")

    # 環境変数
    c.run(f"mkdir -p {HOME}/Library/LaunchAgents")
    if os.path.exists(f"{HOME}/Library/LaunchAgents/setenv.plist"):
        c.run(f"launchctl unload {HOME}/Library/LaunchAgents/setenv.plist")
    else:
        c.run(
            f"ln -s {HOME}/dotfiles/mac_env/setenv.plist {HOME}/Library/LaunchAgents/setenv.plist"
        )
    c.run(f"launchctl load {HOME}/Library/LaunchAgents/setenv.plist")


ns.add_task(macos)


@task
def vimrc(c, no_extension=False):
    print("## vimrc")
    has = False
    if os.path.exists(f"{HOME}/.vimrc"):
        r = c.run(f"cat {HOME}/.vimrc")
        has = r.stdout.find("dotfiles") > 0
    if not has:
        c.run(f'echo "source {HOME}/dotfiles/vimrc/vimrc.vim" >>{HOME}/.vimrc')

    has = False
    if os.path.exists(f"{HOME}/.gvimrc"):
        r = c.run(f"cat {HOME}/.gvimrc")
        has = r.stdout.find("dotfiles") > 0
    if not has:
        c.run(f'echo "source {HOME}/dotfiles/vimrc/gvimrc.vim" >>{HOME}/.gvimrc')

    if not no_extension:
        c.run(f"mkdir -p {HOME}/.vim/autoload")
        c.run(
            f"curl -fLo {HOME}/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim",
        )
        c.run("vi +PlugInstall +qall", hide="both", warn=True)


ns.add_task(vimrc)


@task
def xonsh(c):
    c.run(f"ln -fs {HOME}/dotfiles/xonsh/xonshrc.py {HOME}/.xonshrc")


ns.add_task(xonsh)


@task
def screenrc(c):
    c.run(f"cp {HOME}/dotfiles/screenrc/screenrc {HOME}/.screenrc")


ns.add_task(screenrc)


@task
def starship(c):
    c.run(f"ln -fs {HOME}/dotfiles/starship/starship.toml {HOME}/.config/")


ns.add_task(starship)


@task(default=True)
def install(c):
    update_package_manager(c)
    create_basic_dir(c)
    archi = get_archi(c)
    hostname = get_hostname(c)
    if archi == "x86_64":
        homebrew.default(c)
    if archi == "aarch64":
        arm_ubuntu.install(c)
    if detect.linux and ubuntu.is_ubuntu():
        ubuntu.install(c)
        if hostname in ["miriam", "kukrushka"]:
            ubuntu.desktop_install(c)
    checkout_dotfiles(c)
    pyenv(c)
    rehash_pyenv(c)
    bashrc(c)
    git.set_config(c)
    git.chmod_config(c)
    go.download_packages(c)
    if detect.linux and ubuntu.is_ubuntu():
        go.install_ubuntu(c)
    if os == "macos":
        macos(c)
    vimrc(c)
    python_pip.install(c)
    xonsh(c)


ns.add_task(install)


@task
def install_small(c):
    create_basic_dir(c)
    bashrc(c)
    git.set_config(c)
    git.chmod_config(c)
    if detect.osx:
        homebrew.install_minimal(c)
    python_pip.install_small(c)
    xonsh(c)


ns.add_task(install_small)

ns.add_collection(ns.from_module(homebrew), "homebrew")
ns.add_collection(ns.from_module(git), "git")
ns.add_collection(ns.from_module(ubuntu), "ubuntu")
ns.add_collection(ns.from_module(go), "go")
ns.add_collection(ns.from_module(rust), "rust")
ns.add_collection(ns.from_module(python_pip), "pip")
ns.add_collection(ns.from_module(vscode), "vscode")
