import invoke
import git as git_config
import homebrew
from fabric import task, Connection, runners


def detect_os(c: invoke.Context):
    if c.run("test -e /etc/lsb-release", warn=True, hide=True).ok:
        return "ubuntu"
    if c.run("test -e /etc/debian_version", warn=True).ok:
        return "debian"
    if c.run("test -e /etc/redhat-release", warn=True).ok:
        return "redhat"
    r: invoke.Result = c.run("uname -o", warn=True, hide="both")
    if r.ok and r.stdout.find("Linux") >= 0:
            return "linux"
    r = c.run("uname", warn=True, hide="both")
    if r.ok and r.stdout.find("Darwin") >= 0:
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


def install_from_package_manager(c: invoke.Context, package: str):
    os = detect_os(c)
    print(f"## install {package}")
    if os == "debian" or os == "ubuntu":
        c.sudo(f"apt-get install -y {package}")
    elif os == "redhat":
        c.sudo(f"yum install -y {package}")


def has_file(c: invoke.Context, path: str):
    return c.run(f"ls {path}", warn=True, hide="both").ok


def delete_file(c: invoke.Context, path: str):
    if has_file(c, path):
        c.run(f"rm {path}")

@task
def git(c):
    c: invoke.Context
    if c.run("which git", warn=True).failed:
        install_from_package_manager(c, "git")


def checkout_dotfiles(c: invoke.Context):
    print("checkout and update dotfiles")
    if c.run("test -e ~/dotfiles", warn=True, hide="both").failed:
        c.run("git clone https://github.com/74th/dotfiles.git", echo=True)
        return
    with c.cd("~/dotfiles"):
        c.run("git pull")


@task
def curl(c):
    c: invoke.Context
    if c.run("which curl", warn=True).failed:
        install_from_package_manager(c, "curl")


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
def tmux(c):
    c: invoke.Context
    print("## ~/.tmux.conf")
    delete_file(c, "~/.tmux.conf")
    c.run("ln -s ~/dotfiles/tmux/.tmux.conf ~/.tmux.conf")


@task
def vscode(c):
    c: invoke.Context
    print("## vscode")
    os = detect_os(c)
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
def vimrc(c):
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

    c.run("mkdir -p .vim")
    if c.run("vi --version").stdout.find("Huge version") == -1 :
        install_from_package_manager(c, "vim")

    c.run(
        "curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
    )
    c.run("vi +PlugInstall +qall")


@task
def fish(c):
    c: invoke.Context
    os = detect_os(c)
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


def install_pip3(c, pkg):
    c: invoke.Context
    os: str = detect_os(c)
    if os == "macos":
        c.run(f"/usr/local/bin/pip3 install --upgrade {pkg}", env={"PYTHONPATH": "/usr/local/bin/python3"})
    else:
        c.run(f"pip3 install {pkg}")


@task
def mypy(c):
    print(f"## mypy")
    install_pip3(c, "mypy")

@task
def xonsh(c):
    print("## xonsh")
    install_pip3(c, "xonsh[ptk]")
    c.run("ln -fs ~/dotfiles/xonsh/xonshrc.py ~/.xonshrc")

@task
def fabric(c):
    print("## fabric")
    install_pip3(c, "fabric")

@task(default=True)
def install(c):
    c: invoke.Context
    os = detect_os(c)
    print(f"## detected os: {os}")
    update_package_manager(c, os)
    if os == "macos":
        homebrew.default(c)
    git(c)
    checkout_dotfiles(c)
    curl(c)
    rehash_pyenv(c)
    bashrc(c)
    tmux(c)
    vscode(c)
    git_config.set_config(c)
    if os == "macos":
        macos(c)
    vimrc(c)
    fish(c)
    xonsh(c)
    #fabric(c)
    mypy(c)
    # TODO: golang
    # TODO: aws cli
    # TODO: gcloud
