from typing import List
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
        "protobuf-compiler",
    ]
    return pkgs

@task
def install(c):
    pkgs = _list_packages()
    c.run("sudo apt install " + " ".join(pkgs))