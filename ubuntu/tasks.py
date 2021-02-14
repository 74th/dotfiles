from typing import List
import os
import tempfile

from invoke import task


def add_source_list(c):
    # gh
    # https://github.com/cli/cli/blob/trunk/docs/install_linux.md
    c.run(
        "sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0"
    )
    c.run("sudo apt-add-repository https://cli.github.com/packages")
    # nodejs
    # https://github.com/nodesource/distributions
    # if not os.path.exists("/etc/apt/sources.list.d/nodesource.list"):
    #     c.run("curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -")


def add_source_list_desktop(c):
    # vscode
    # https://code.visualstudio.com/docs/setup/linux#_debian-and-ubuntu-based-distributions
    c.run(
        "curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg"
    )
    c.run(
        "sudo install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/"
    )
    c.run(
        "sudo sh -c 'echo \"deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main\" > /etc/apt/sources.list.d/vscode.list'"
    )
    c.run("rm packages.microsoft.gpg")


def is_ubuntu():
    if not os.path.exists("/etc/lsb-release"):
        return False
    with open("/etc/lsb-release") as f:
        body = f.read()
    return body.count("Ubuntu") >= 0


@task
def update(c):
    c.run("sudo apt-get update")


@task
def install_classic_snap_pkgs(c):
    pkgs = ["google-cloud-sdk"]
    pkgs_str = " ".join(pkgs)

    c.run("sudo snap install --classic " + pkgs_str)


def _list_packages() -> List[str]:
    pkgs: List[str] = []
    pkgs += [
        "jq",
        "peco",
        "xclip",
        "bat",
        "ripgrep",
        "docker-compose",
        "readline-common",
        "git",
        "bzip2",
        "unar",
        "nodejs",
        "apt-transport-https",
        "protobuf-compiler",
        "curl",
        "vim",
        "direnv",
        "cargo",
        "python-is-python3",
    ]
    return pkgs


@task
def install(c):
    add_source_list(c)
    pkgs = _list_packages()
    c.run("sudo apt update")
    c.run("sudo apt install -y " + " ".join(pkgs))


def _list_desktop_packages() -> List[str]:
    pkgs: List[str] = []
    pkgs += [
        "guake",
        "fcitx",
        "fcitx-mozc",
        "xbindkeys",
        "vim-gtk",
        "font-manager",
        "libinput-tools",
        "wmctrl",
        "xdotool",
        "gnome-tweaks",
        "code",
        "code-insiders",
        # desktop tools
        "gimp",
        "inkscape",
        "easytag",
        # system monitor
        "gir1.2-gtop-2.0",
        "gir1.2-nm-1.0",
        "gir1.2-clutter-1.0",
        # grub
        "grub-customizer",
        # gtk theme
        "gtk2-engines-murrine",
        "gtk2-engines-pixbuf",
    ]
    return pkgs


@task
def zfs_auto_snapshot(c):
    c.run("sudo cp ./zfs-auto-snapshot/frequency.crontab /etc/cron.d/zfs-auto-snapshot")
    c.run("sudo cp ./zfs-auto-snapshot/hourly.sh /etc/cron.hourly/zfs-auto-snapshot")
    c.run("sudo cp ./zfs-auto-snapshot/daily.sh /etc/cron.daily/zfs-auto-snapshot")
    c.run("sudo cp ./zfs-auto-snapshot/weekly.sh /etc/cron.weekly/zfs-auto-snapshot")
    c.run("sudo cp ./zfs-auto-snapshot/monthly.sh /etc/cron.monthly/zfs-auto-snapshot")


@task
def desktop_install(c):
    add_source_list_desktop(c)
    pkgs = _list_desktop_packages()
    c.run("sudo apt update")
    c.run("ln -sf ~/dotfiles/ubuntu/.xbindkeysrc ~/.xbindkeysrc")
    c.run("sudo apt install -y " + " ".join(pkgs))
    c.run("ln -sf ~/dotfiles/ubuntu/_config/libinput-gestures.conf ~/.config/")
