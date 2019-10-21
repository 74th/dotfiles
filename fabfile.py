import glob
import os
from pathlib import Path
import invoke
from invoke import Context,task
import git as git_config
import homebrew
import detect
from fabric import Connection, runners

def get_home():
    home = os.environ.get("HOME", None)
    if home is not None:
        return home
    if detect.mac:
        return "/Users/nnyn"
    return "/home/nnyn"

HOME = get_home()


def update_package_manager(c: invoke.Context):
    print("update package manager")
    if detect.linux:
        c.run("sudo apt-get update", echo=True)
    if detect.mac:
        c.run("brew update", echo=True)


def has_file(c: invoke.Context, path: str):
    return c.run(f"ls {path}", warn=True, hide="both").ok


def delete_file(c: invoke.Context, path: str):
    if has_file(c, path):
        c.run(f"rm {path}")

def create_basic_dir(c):
    if not os.path.exists(f"{HOME}/bin"):
        os.mkdir(f"{HOME}/bin")

def checkout_dotfiles(c: invoke.Context):
    print("checkout and update dotfiles")
    if c.run("test -e ~/dotfiles", warn=True, hide="both").failed:
        c.run("git clone https://github.com/74th/dotfiles.git", echo=True)
        return
    with c.cd("~/dotfiles"):
        c.run("git pull")


@task
def rehash_pyenv(c):
    c: invoke.Context
    if c.run("test -e .pyenv", warn=True).ok:
        print("## rehash pyenv")
        c.run("pyenv rehash")


@task
def bashrc(c):
    c: invoke.Context
    print("## ~/.bashrc")
    delete_file(c, "~/.bashrc")
    c.run('echo "source ~/dotfiles/bashrc/bashrc" >> ~/.bashrc')


@task
def vscode(c, insider=False):
    c: invoke.Context
    print("## vscode")
    if detect.linux:
        if insider:
            vscode_dir = "~/.config/Code\\ -\\ Insiders/User"
        else:
            vscode_dir = "~/.config/Code/User"
    else:
        if insider:
            vscode_dir = "~/Library/Application\\ Support/Code\\ -\\ Insiders/User"
        else:
            vscode_dir = "~/Library/Application\\ Support/Code/User"

    c.run(f"mkdir -p {vscode_dir}")

    delete_file(c, f"{vscode_dir}/keybindings.json")
    c.run(f"ln -s ~/dotfiles/vscode/keybindings.json {vscode_dir}/keybindings.json")

    delete_file(c, f"{vscode_dir}/settings.json")
    c.run(f"ln -s ~/dotfiles/vscode/settings.json {vscode_dir}/settings.json")

    c.run(f"rm -rf {vscode_dir}/snippets")
    c.run(f"ln -s ~/dotfiles/vscode/snippets {vscode_dir}/snippets")


@task
def macos(c):
    c: invoke.Context
    print("## MacOS")
    c.run("mkdir -p ~/.config")
    c.run("defaults write -g ApplePressAndHoldEnabled -bool false")
    c.run("mkdir -p ~/bin")

    # macvim-kaoriya 用の mvim
    if has_file(c, "/Applications/MacVim.app/Contents/bin/"):
        c.run("ln -sf /Applications/MacVim.app/Contents/bin/* ~/bin/")
        c.run("ln -sf /Applications/MacVim.app/Contents/bin/vim ~/bin/vi")

    # karabiner-elements
    c.run("rm -rf ~/.config/karabiner")
    c.run("ln -s ~/dotfiles/karabiner-elements ~/.config/karabiner")

    # 環境変数
    c.run("mkdir -p ~/Library/LaunchAgents")
    if has_file(c, "~/Library/LaunchAgents/setenv.plist"):
        c.run("launchctl unload ~/Library/LaunchAgents/setenv.plist")
    else:
        c.run("ln -s ~/dotfiles/mac_env/setenv.plist ~/Library/LaunchAgents/setenv.plist")
    c.run("launchctl load ~/Library/LaunchAgents/setenv.plist")


@task
def vimrc(c, no_extension=False):
    c: invoke.Context
    print("## vimrc")
    has = False
    if has_file(c, "~/.vimrc"):
        r: invoke.Result = c.run("cat ~/.vimrc")
        has = r.stdout.find("dotfiles") > 0
    if not has:
        c.run('echo "source ~/dotfiles/vimrc/vimrc.vim" >>~/.vimrc')

    has = False
    if has_file(c, "~/.gvimrc"):
        r = c.run("cat ~/.gvimrc")
        has = r.stdout.find("dotfiles") > 0
    if not has:
        c.run('echo "source ~/dotfiles/vimrc/gvimrc.vim" >>~/.gvimrc')

    if not no_extension:
        c.run("mkdir -p ~/.vim/autoload")
        c.run(
            "curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
        )
        c.run("vi +PlugInstall +qall")


@task
def pypi(c):

    def _install(c, pkgs):
        pkgs_str: str = " ".join(pkgs)
        if detect.mac:
            c.run(f"/usr/local/bin/pip3 install --upgrade {pkgs_str}", env={"PYTHONPATH": "/usr/local/bin/python3"})
        else:
            c.run(f"pip3 install --upgrade {pkgs_str}")

    # must packages
    pkgs = ["fabric", "invoke", "pyyaml", "black", "mypy"]

    # xonsh
    pkgs += ["xonsh[ptk]", "xontrib-readable-traceback", "xonsh-docker-tabcomplete", "xontrib-z", "xonsh-direnv"]

    _install(c, pkgs)

@task
def xonsh(c):
    c.run("ln -fs ~/dotfiles/xonsh/xonshrc.py ~/.xonshrc")

@task
def screenrc(c):
    c.run("cp ~/dotfiles/screenrc/screenrc ~/.screenrc")

@task
def istio(c):
    print("## istio")
    d = f"{HOME}/OSS/istio"
    if not os.path.exists(d):
        c.run(f"mkdir -p {d}")
    with c.cd(d):
        c.run("rm -rf istio-*")
        c.run("curl -L https://git.io/getLatestIstio | sh -")
        ds = glob.glob(f"{d}/istio-*")
        d = ds[0]
        c.run(f"ln -fs {d}/bin/* {HOME}/bin/")

@task(default=True)
def install(c):
    c: invoke.Context
    update_package_manager(c)
    create_basic_dir(c)
    homebrew.default(c)
    checkout_dotfiles(c)
    rehash_pyenv(c)
    bashrc(c)
    vscode(c)
    git_config.set_config(c)
    if os == "macos":
        macos(c)
    vimrc(c)
    pypi(c)
    xonsh(c)
    # istio(c)
    # TODO: golang
    # TODO: aws cli
    # TODO: gcloud

@task()
def install_small(c):
    c: invoke.Context
    create_basic_dir(c)
    bashrc(c)
    vimrc(c)
