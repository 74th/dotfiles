from typing import List
from invoke import task
import invoke


def set_poetry_config(c):
    c.run(f"~/.local/bin/poetry config virtualenvs.create true")
    c.run(f"~/.local/bin/poetry config virtualenvs.in-project true")


def install_packages(c, l: list[str]):
    l_str = " ".join(l)
    c.run(f"pip3 install --upgrade {l_str}")


def install_packages_by_pipx(c, l: list[str]):
    l_str = " ".join(l)
    c.run(f"pipx install {l_str}")


def list_small_packages():
    l = []
    l += [
        "invoke",
        "pyyaml",
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
        "xonsh-direnv",
    ]
    return l


def list_packages_by_pipx():
    l = [
        "poetry",
        "xonsh[full]",
    ]
    return l


@invoke.task
def install_by_pipx(c):
    l = list_packages_by_pipx()
    for p in l:
        c.run(f"pipx install {p}")


@invoke.task
def install(c):
    l = list_packages()
    install_packages(c, ["pipx"])
    install_packages(c, l)
    install_by_pipx(c)
    set_poetry_config(c)


@invoke.task
def upgrade_all(c, force=False, upgrade=True, pip="pip3"):
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
