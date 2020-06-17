from typing import List
import os
import tempfile

from invoke import task


@task
def update(c):
    c.run("sudo apt-get update")


@task
def install_classic_snap_pkgs(c):
    pkgs = ["google-cloud-sdk"]
    pkgs_str = " ".join(pkgs)

    c.run("sudo snap install --classic " + pkgs_str)


@task
def add_snap_path(c):
    with open("/etc/environment") as f:
        text = f.read()
    if text.find("/snap/bin") != -1:
        return
    prefix = 'PATH="'
    pos = text.find(prefix)

    if pos >= 0:
        new_text = text[:pos] + prefix + "/snap/bin:" + text[pos + len(prefix) :]
    with tempfile.NamedTemporaryFile() as tmp:
        with open(tmp.name, "w") as f:
            f.write(new_text)
        c.run("sudo cp " + tmp.name + " /etc/environment")

def _list_packages()->List[str]:
    pkgs: List[str] = []
    pkgs += [
        "apt-transport-https",
        "protobuf-compiler",
        "curl",
        "vim",
        "direnv",
    ]
    return pkgs

@task
def install(c):
    pkgs = _list_packages()
    c.run("sudo apt update")
    c.run("sudo apt install -y " + " ".join(pkgs))

def _list_desktop_packages()->List[str]:
    pkgs: List[str] = []
    pkgs += [
        "fcitx",
        "fcitx-mozc",
        "vim-gtk",
        "code",
        "code-insiders",
        "font-manager",
    ]
    return pkgs

@task
def install_vscode(c):
    if not os.path.exists("/etc/apt/sources.list.d/vscode.list"):
        c.run("curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg")
        c.run("sudo install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/")
        c.run("sudo sh -c 'echo \"deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main\" > /etc/apt/sources.list.d/vscode.list'")
        c.run("rm packages.microsoft.gpg")

@task
def desktop_install(c):
    install_vscode(c)
    pkgs = _list_desktop_packages()
    c.run("sudo apt update")
    c.run("sudo apt install -y " + " ".join(pkgs))
