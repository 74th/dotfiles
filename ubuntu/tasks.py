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
        "xclip",
        "bat",
        "docker-compose",
        "readline-common",
        "git",
        "bzip2",
        "nodejs",
        "apt-transport-https",
        "protobuf-compiler",
        "curl",
        "vim",
        "direnv",
        "gh",
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
        "vim-gtk",
        "font-manager",
        "code",
        "code-insiders",
    ]
    return pkgs


@task
def desktop_install(c):
    add_source_list_desktop(c)
    pkgs = _list_desktop_packages()
    c.run("sudo apt update")
    c.run("sudo apt install -y " + " ".join(pkgs))
