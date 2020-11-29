from typing import List
from invoke import task
import invoke


def set_poetry_config(c):
    c.run(f"poetry config virtualenvs.create true")
    c.run(f"poetry config virtualenvs.in-project true")


def install_packages(c, l: List[str]):
    l_str = " ".join(l)
    c.run(f"pip3 install --user --upgrade {l_str}")


def list_small_packages():
    l = []
    l += [
        "invoke",
        "poetry",
        "xonsh[full,ptk]",
        "xonsh-direnv",
        # "xontrib-readable-traceback",
    ]
    return l


@invoke.task
def install_small(c):
    l = list_small_packages()
    install_packages(c, l)
    set_poetry_config(c)


def list_packages():
    l = list_small_packages()
    l += [
        "black",
        "mypy",
        "xonsh[full,ptk]",
        "xonsh-direnv",
        # "docker-compose",
        "awscli",
    ]
    return l


@invoke.task
def install(c):
    l = list_packages()
    install_packages(c, l)
    set_poetry_config(c)


@invoke.task
def upgrade_all(c, force=False, upgrade=True):
    out = c.run("pip3 list").stdout
    lines = out.split("\n")
    for line in lines[2:]:
        pkg = line.split(" ")[0]
        print(pkg)
        flg = ""
        if force:
            flg += " --force-reinstall"
        if upgrade:
            flg += " --upgrade"
        c.run("pip3 install --user {flg} {pkg}".format(flg=flg, pkg=pkg))
