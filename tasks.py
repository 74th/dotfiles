import glob
import sys
import os
from pathlib import Path
import invoke
from invoke import Context, task, collection
import detect

import homebrew.tasks as homebrew
import git.tasks as git
import arm_ubuntu.tasks as arm_ubuntu

ns = collection.Collection()
ns.add_collection(ns.from_module(arm_ubuntu, "arm-ubuntu"))


def get_home():
    home = os.environ.get("HOME", None)
    if home is not None:
        return home
    if detect.mac:
        return "/Users/nnyn"
    return "/home/nnyn"


HOME = get_home()


def get_archi(c):
    return c.run("uname -p").stdout.strip()


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
    if c.run("test -e ~/dotfiles", warn=True, hide="both").failed:
        c.run("git clone https://github.com/74th/dotfiles.git", echo=True)
        return
    with c.cd("~/dotfiles"):
        c.run("git pull")


@task
def rehash_pyenv(c):
    if c.run("test -e .pyenv", warn=True).ok:
        print("## rehash pyenv")
        c.run("pyenv rehash")


ns.add_task(rehash_pyenv)


@task
def bashrc(c):
    print("## ~/.bashrc")
    delete_file("~/.bashrc")
    c.run('echo "source ~/dotfiles/bashrc/bashrc" >> ~/.bashrc')


ns.add_task(bashrc)


@task
def macos(c):
    print("## MacOS")
    c.run("mkdir -p ~/.config")
    c.run("defaults write -g ApplePressAndHoldEnabled -bool false")
    c.run("mkdir -p ~/bin")

    # macvim-kaoriya 用の mvim
    if os.path.exists("/Applications/MacVim.app/Contents/bin/"):
        c.run("ln -sf /Applications/MacVim.app/Contents/bin/* ~/bin/")
        c.run("ln -sf /Applications/MacVim.app/Contents/bin/vim ~/bin/vi")

    # karabiner-elements
    c.run("rm -rf ~/.config/karabiner")
    c.run("ln -s ~/dotfiles/karabiner-elements ~/.config/karabiner")

    # 環境変数
    c.run("mkdir -p ~/Library/LaunchAgents")
    if os.path.exists("~/Library/LaunchAgents/setenv.plist"):
        c.run("launchctl unload ~/Library/LaunchAgents/setenv.plist")
    else:
        c.run(
            "ln -s ~/dotfiles/mac_env/setenv.plist ~/Library/LaunchAgents/setenv.plist"
        )
    c.run("launchctl load ~/Library/LaunchAgents/setenv.plist")


ns.add_task(macos)


@task
def vimrc(c, no_extension=False):
    print("## vimrc")
    has = False
    if os.path.exists("~/.vimrc"):
        r = c.run("cat ~/.vimrc")
        has = r.stdout.find("dotfiles") > 0
    if not has:
        c.run('echo "source ~/dotfiles/vimrc/vimrc.vim" >>~/.vimrc')

    has = False
    if os.path.exists("~/.gvimrc"):
        r = c.run("cat ~/.gvimrc")
        has = r.stdout.find("dotfiles") > 0
    if not has:
        c.run('echo "source ~/dotfiles/vimrc/gvimrc.vim" >>~/.gvimrc')

    if not no_extension:
        c.run("mkdir -p ~/.vim/autoload")
        c.run(
            "curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim",
        )
        c.run("vi +PlugInstall +qall", hide="both", warn=True)


ns.add_task(vimrc)


@task
def pypi(c):
    def _install(c, pkgs):
        pkgs_str = " ".join(pkgs)
        if detect.mac:
            c.run(
                "/usr/local/bin/pip3 install --upgrade " + pkgs_str,
                env={"PYTHONPATH": "/usr/local/bin/python3"},
            )
        else:
            c.run("pip3 install --upgrade " + pkgs_str)

    # must packages
    pkgs = ["invoke", "pyyaml", "mypy"]
    if sys.version_info.minor >= 6:
        pkgs += ["black"]

    # xonsh
    pkgs += [
        "xonsh[ptk]",
        "xontrib-readable-traceback",
        "xonsh-docker-tabcomplete",
        "xontrib-z",
        "xonsh-direnv",
    ]

    _install(c, pkgs)


ns.add_task(pypi)


@task
def xonsh(c):
    c.run("ln -fs ~/dotfiles/xonsh/xonshrc.py ~/.xonshrc")


ns.add_task(xonsh)


@task
def screenrc(c):
    c.run("cp ~/dotfiles/screenrc/screenrc ~/.screenrc")


ns.add_task(screenrc)


@task(default=True)
def install(c):
    update_package_manager(c)
    create_basic_dir(c)
    archi = get_archi(c)
    if archi == "x86_64":
        homebrew.default(c)
    if archi == "aarch64":
        arm_ubuntu.install(c)
    checkout_dotfiles(c)
    rehash_pyenv(c)
    bashrc(c)
    git.set_config(c)
    if os == "macos":
        macos(c)
    vimrc(c)
    pypi(c)
    xonsh(c)


ns.add_task(install)


@task
def install_small(c):
    create_basic_dir(c)
    bashrc(c)
    vimrc(c)
    pypi(c)
    xonsh(c)


ns.add_task(install_small)

ns.add_collection(ns.from_module(homebrew), "homebrew")
ns.add_collection(ns.from_module(git), "git")
