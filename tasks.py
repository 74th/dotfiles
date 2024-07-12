from typing import cast
import os
from os import path
from invoke.tasks import task
from invoke.context import Context
from invoke.collection import Collection
import detect

import homebrew.tasks as homebrew
import git.tasks as git
import arm_ubuntu.tasks as arm_ubuntu
import ubuntu.tasks as ubuntu
import golang.tasks as go
import python_pip.tasks as python_pip
import vscode.tasks as vscode
import tools.tasks as tools
import krew.tasks as krew
import rust.tasks as rust
import embedded.tasks as embedded

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


def get_archi(c: Context):
    r = c.run("uname -p")
    assert r
    return r.stdout.strip()


def get_hostname(c: Context):
    r = c.run("hostname")
    assert r
    return r.stdout.strip()


def update_default_package_manager(c):
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


@task
def pyenv(c):
    c = cast(Context, c)
    pyenv_dir = f"{HOME}/.pyenv"
    if not path.exists(pyenv_dir):
        c.run("ghq get github.com/pyenv/pyenv")
        c.run(f"ln -s {GHQ_DIR}/github.com/pyenv/pyenv {pyenv_dir}")
        if detect.linux:
            c.run(
                f"sudo apt-get install -y libreadline8 libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev"
            )


ns.add_task(pyenv)  # type: ignore


@task
def rehash_pyenv(c_):
    c: Context = c_
    r = c.run("test -e pyenv", warn=True)
    assert r
    if r.ok:
        print("## rehash pyenv")
        c.run("pyenv rehash")


ns.add_task(rehash_pyenv)  # type: ignore


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


ns.add_task(bashrc)  # type: ignore


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


ns.add_task(macos)  # type: ignore


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


ns.add_task(vimrc)  # type: ignore


@task
def xonsh(c):
    c.run(f"ln -fs {HOME}/dotfiles/xonsh/xonshrc.py {HOME}/.xonshrc")


ns.add_task(xonsh)  # type: ignore


@task
def screenrc(c):
    c.run(f"cp {HOME}/dotfiles/screenrc/screenrc {HOME}/.screenrc")


ns.add_task(screenrc)  # type: ignore


@task
def npm(c):
    if c.run("which npm", warn=True).failed:
        print("!! npm not found !!")
        return
    home = get_home()
    c.run(f"npm config set prefix {home}/npm")
    dirs = [
        f"{HOME}/npm",
        f"{HOME}/npm/bin",
        f"{HOME}/npm/share",
        f"{HOME}/npm/lib",
    ]
    for d in dirs:
        if not os.path.exists(d):
            c.run(f"mkdir {d}")


ns.add_task(npm)  # type: ignore


@task(default=True)
def install(c):
    update_default_package_manager(c)
    create_basic_dir(c)

    archi = get_archi(c)
    hostname = get_hostname(c)

    # default package managers
    if detect.linux and archi == "aarch64":
        arm_ubuntu.install(c)
    if detect.linux and ubuntu.is_ubuntu():
        ubuntu.install(c)
        if hostname in ["miriam", "kukrushka"]:
            ubuntu.desktop_install(c)

    # homebrew
    homebrew.default(c)

    # npm
    npm(c)

    # some package managers
    python_pip.install(c)
    tools.install(c)
    go.download_packages(c)
    if detect.linux and ubuntu.is_ubuntu():
        go.install_go(c)
    krew.install(c)

    # setting up
    xonsh(c)
    pyenv(c)
    bashrc(c)
    vimrc(c)
    screenrc(c)
    git.set_config(c)
    git.chmod_config(c)
    if os == "macos":
        macos(c)

    # fixing
    rehash_pyenv(c)


ns.add_task(install)  # type: ignore


@task
def install_small(c):
    update_default_package_manager(c)
    create_basic_dir(c)

    bashrc(c)
    git.set_config(c)
    git.chmod_config(c)
    if detect.osx:
        homebrew.install_minimal(c)
    python_pip.install_small(c)
    xonsh(c)


ns.add_task(install_small)  # type: ignore

ns.add_collection(ns.from_module(homebrew), "homebrew")
ns.add_collection(ns.from_module(git), "git")
ns.add_collection(ns.from_module(ubuntu), "ubuntu")
ns.add_collection(ns.from_module(go), "go")
ns.add_collection(ns.from_module(python_pip), "pip")
ns.add_collection(ns.from_module(tools), "tools")
ns.add_collection(ns.from_module(vscode), "vscode")
ns.add_collection(ns.from_module(krew), "krew")
ns.add_collection(ns.from_module(rust), "rust")
ns.add_collection(ns.from_module(embedded), "embedded")
