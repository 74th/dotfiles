import invoke
import git
from fabric2 import task, Connection


def run(c: invoke.Context, command: str, **kwargs) -> invoke.Result:
    print(f"- {command}")
    return c.run(command, **kwargs)


def detect_os(c: invoke.Context):
    if run(c, "test -e /etc/lsb-release", warn=True).ok:
        return "ubuntu"
    if run(c, "test -e /etc/debian_version", warn=True).ok:
        return "debian"
    if run(c, "test -e /etc/redhat-release", warn=True).ok:
        return "redhat"
    r: invoke.Result = run(c, "uname -o", warn=True, hide="both")
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
        run(c, "brew update", echo=True)


def install_from_package_manager(c: invoke.Context, os: str, package: str):
    print(f"## install {package}")
    if os == "debian" or os == "ubuntu":
        c.sudo(f"apt-get install -y {package}")
    elif os == "redhat":
        c.sudo(f"yum install -y {package}")


def install_git(c: invoke.Context, os: str):
    if run(c, "which git", warn=True).failed:
        install_from_package_manager(c, os, "git")


def checkout_dotfiles(c: invoke.Context):
    print("checkout and update dotfiles")
    if run(c, "test -e ~/dotfiles", warn=True, hide="both").failed:
        run(c, "git clone https://github.com/74th/dotfiles.git", echo=True)
        return
    with c.cd("~/dotfiles"):
        run(c, "git pull")


def install_curl(c: invoke.Context, os: str):
    if run(c, "which curl", warn=True).failed:
        install_from_package_manager(c, os, "curl")


def rehash_pyenv(c: invoke.Context):
    if run(c, "which pyenv", warn=True).ok:
        print("## rehash pyenv")
        run(c, "pyenv rehash")


def has_file(c: invoke.Context, path: str):
    return run(c, f"ls {path}", warn=True, hide="both").ok


def delete_file(c: invoke.Context, path: str):
    if has_file(c, path):
        run(c, f"rm {path}")


def bashrc(c: invoke.Context):
    print("## ~/.bashrc")
    delete_file(c, "~/.bashrc")
    run(c, 'echo "source ~/dotfiles/bashrc/bashrc" >> ~/.bashrc')


def tmux(c: invoke.Context):
    print("## ~/.tmux.conf")
    delete_file(c, "~/.tmux.conf")
    run(c, "ln -s ~/dotfiles/tmux/.tmux.conf ~/.tmux.conf")


def vscode(c: invoke.Context, os: str):
    print("## vscode")
    if is_linux(os):
        vscode_dir = "~/.config/Code/User"
    else:
        vscode_dir = "~/Library/Application\\ Support/Code/User"

    run(c, f"mkdir -p {vscode_dir}")

    delete_file(c, f"{vscode_dir}/keybindings.json")
    run(c, f"ln -s ~/dotfiles/vscode/keybindings.json {vscode_dir}/keybindings.json")

    delete_file(c, f"{vscode_dir}/settings.json")
    run(c, f"ln -s ~/dotfiles/vscode/settings.json {vscode_dir}/settings.json")

    run(c, f"rm -rf {vscode_dir}/snippets")
    run(c, f"ln -s ~/dotfiles/vscode/snippets {vscode_dir}/snippets")


def macos(c: invoke.Context):
    print("## MacOS")
    run(c, "mkdir -p ~/.config")
    run(c, "defaults write -g ApplePressAndHoldEnabled -bool false")
    run(c, "mkdir -p ~/bin")

    # macvim-kaoriya用のmvim
    if has_file(c, "/Applications/MacVim.app/Contents/bin/"):
        run(c, "ln -sf /Applications/MacVim.app/Contents/bin/* ~/bin/")
        run(c, "ln -sf /Applications/MacVim.app/Contents/bin/vim ~/bin/vi")

    # karabiner-elements
    run(c, "rm -rf ~/.config/karabiner")
    run(c, "ln -s ~/dotfiles/karabiner-elements ~/.config/karabiner")

    # 環境変数
    run(c, "mkdir -p ~/Library/LaunchAgents")
    if has_file(c, "~/Library/LaunchAgents/setenv.plist"):
        run(c, "launchctl unload ~/Library/LaunchAgents/setenv.plist")
    else:
        run(c, "ln -s ~/dotfiles/mac_env/setenv.plist ~/Library/LaunchAgents/setenv.plist")
    run(c, "launchctl load ~/Library/LaunchAgents/setenv.plist")


def vimrc(c: invoke.Context):
    print("## vimrc")
    has = False
    if has_file(c, "~/.vimrc"):
        r: invoke.Result = run(c, "cat ~/.vimrc")
        has = r.stdout.find("dotfiles") > 0
    if not has:
        run(c, 'echo "source ~/dotfiles/vimrc/vimrc.vim" >>~/.vimrc')

    has = False
    if has_file(c, "~/.gvimrc"):
        r = run(c, "cat ~/.gvimrc")
        has = r.stdout.find("dotfiles") > 0
    if not has:
        run(c, 'echo "source ~/dotfiles/vimrc/gvimrc.vim" >>~/.gvimrc')

    run(c, "mkdir -p .vim")
    # TODO: ubuntuの場合vim-hugeをインストールする

    run(
        c,
        "curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
    )
    run(c, "vi +PlugInstall +qall")


def fish_shell(c: invoke.Context, os: str):
    print("## fish shell")
    if os == "ubuntu" or os == "debian":
        if os == "ubuntu":
            c.sudo("apt-add-repository ppa:fish-shell/release-2")
        else:
            c.sudo(
                "echo 'deb http://download.opensuse.org/repositories/shells:/fish:/release:/2/Debian_8.0/ /' > /etc/apt/sources.list.d/fish.list"
            )
        c.sudo("apt-get update")
        c.sudo("apt-get install -y fish")
    if os == "redhat":
        c.sudo(
            'bash -c "cd /etc/yum.repos.d/;wget http://download.opensuse.org/repositories/shells:fish:release:2/CentOS_7/shells:fish:release:2.repo"'
        )
        c.sudo("sudo yum install -y fish")


@task
def mypy(c, os):
    c: invoke.Context
    os: str
    print("## mypy")
    if os == "macos":
        run(c, "/usr/local/bin/pip3 install mypy", env={"PYTHONPATH": "/usr/local/bin/python3"})


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
    mypy(c, os)
