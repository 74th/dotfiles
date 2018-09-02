import invoke
import git
from fabric2 import task, Connection


def detect_os(c: invoke.Context):
    if c.run("test -e /etc/lsb-release", warn=True).ok:
        return "ubuntu"
    if c.run("test -e /etc/debian_version", warn=True).ok:
        return "debian"
    if c.run("test -e /etc/redhat-release", warn=True).ok:
        return "redhat"
    r: invoke.Result = c.run("uname -o", warn=True, hide="both")
    if r.ok:
        if r.stdout.find("Linux"):
            return "linux"
        if r.stdout.find("Darwin"):
            return "macos"
    return "unknown"


def is_linux(os: str) -> bool:
    return os == "ubuntu" or \
        os == "debian" or \
        os == "redhat" or \
        os == "linux"


def update_package_manager(c: invoke.Context, os: str):
    print("update package manager")
    if os == "ubuntu" or os == "debian":
        c.sudo("apt-get update")
    elif os == "redhat":
        c.sudo("yum update")
    elif os == "macos":
        c.run("brew update", echo=True)


def install_from_package_manager(c: invoke.Context, os: str, package: str):
    print(f"## install {package}")
    if os == "debian" or os == "ubuntu":
        c.sudo(f"apt-get install -y {package}")
    elif os == "redhat":
        c.sudo(f"yum install -y {package}")


def install_git(c: invoke.Context, os: str):
    if c.run("which git", warn=True).failed:
        install_from_package_manager(c, os, "git")


def checkout_dotfiles(c: invoke.Context):
    print("checkout and update dotfiles")
    if c.run("test -e ~/dotfiles", warn=True, hide="both").failed:
        c.run("git clone https://github.com/74th/dotfiles.git", echo=True)
        return
    with c.cd("~/dotfiles"):
        c.run("git pull")


def install_curl(c: invoke.Context, os: str):
    if c.run("which curl", warn=True).failed:
        install_from_package_manager(c, os, "curl")


def rehash_pyenv(c: invoke.Context):
    if c.run("which pyenv", warn=True).ok:
        print("## rehash pyenv")
        c.run("pyenv rehash")


def has_file(c: invoke.Context, path: str):
    return c.run(f"ls {path}", warn=True, hide="both").ok


def delete_file(c: invoke.Context, path: str):
    if has_file(c, path):
        c.run(f"rm {path}")


def bashrc(c: invoke.Context):
    print("## ~/.bashrc")
    delete_file(c, "~/.bashrc")
    c.run('echo "source ~/dotfiles/bashrc/bashrc" >> ~/.bashrc')


def tmux(c: invoke.Context):
    print("## ~/.tmux.conf")
    delete_file(c, "~/.tmux.conf")
    c.run("ln -s ~/dotfiles/tmux/.tmux.conf ~/.tmux.conf")


def vscode(c: invoke.Context, os: str):
    print("## vscode")
    if is_linux(os):
        vscode_dir = "~/.config/Code/User"
    else:
        vscode_dir = "~/Library/Application\\ Support/Code/User"

    c.run(f"mkdir -p {vscode_dir}")

    delete_file(c, f"{vscode_dir}/keybindings.json")
    c.run(f"ln -s ~/dotfiles/vscode/keybindings.json {vscode_dir}/keybindings.json")

    delete_file(c, f"{vscode_dir}/settings.json")
    c.run(f"ln -s ~/dotfiles/vscode/settings.json {vscode_dir}/settings.json")

    c.run(f"rm -rf {vscode_dir}/snippets")
    c.run(f"ln -s ~/dotfiles/vscode/snippets {vscode_dir}/snippets")


def macos(c: invoke.Context):
    print("## MacOS")
    c.run("mkdir -p ~/.config")
    c.run("defaults write -g ApplePressAndHoldEnabled -bool false")
    c.run("mkdir -p ~/bin")

    # macvim-kaoriya用のmvim
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


def vimrc(c: invoke.Context):
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

    c.run("mkdir -p .vim")
    # TODO: ubuntuの場合vim-hugeをインストールする

    c.run("curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim")
    c.run("vi +PlugInstall +qall")


@task(default=True)
def install(c):
    c: invoke.Context
    os = detect_os(c)
    print(f"## detected os: {os}")
    update_package_manager(c, os)
    install_git(c, os)
    checkout_dotfiles(c)
    install_curl(c, os)
    rehash_pyenv(c)
    bashrc(c)
    tmux(c)
    vscode(c, os)
    git.set_config(c)
    if os == "macos":
        macos(c)
    # vimrc(c)
    # TODO: fish
    # TODO: golang
    # TODO: aws cli
    # TODO: gcloud