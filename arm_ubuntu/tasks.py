from typing import cast
from invoke import task, Context

ubuntu_pkgs = [
    "direnv",
    "python3",
    "python3-pip",
    "peco",
    "nodejs",
    "vim",
    "golang-go",
]


@task
def install(c):
    c.run("sudo apt-get update")
    pkgs = " ".join(ubuntu_pkgs)
    c.run("sudo apt-get install -y " + pkgs)

    if c.run("which pyenv", warn=True).failed:
        c.run("git clone https://github.com/pyenv/pyenv.git ~/.pyenv")
