import pathlib

from invoke.tasks import task


def set_poetry_config(c):
    c.run(f"~/.local/bin/poetry config virtualenvs.create true")
    c.run(f"~/.local/bin/poetry config virtualenvs.in-project true")


def install_packages_by_pipx(c, l: list[str]):
    l_str = " ".join(l)
    c.run(f"pipx install {l_str}")


@task
def install_small(c):
    install_by_pipx(c)
    set_poetry_config(c)


def list_packages_by_pipx():
    l = [
        "poetry",
        "xonsh[full]",
        "pre-commit",
    ]
    return l


@task
def install_by_pipx(c):
    l = list_packages_by_pipx()
    for p in l:
        c.run(f"pipx install {p}")
    c.run(
        f"pipx runpip xonsh install invoke prompt_toolkit detect pyyaml xonsh-direnv",
        warn=True,
    )
    c.run(f"pipx runpip xonsh uninstall pyperclip -y", warn=True)


@task
def install_rye(c):
    if pathlib.Path("~/.rye/shims/rye").expanduser().exists():
        return
    c.run("curl -sSf https://rye.astral.sh/get | bash", pty=True)


@task
def install(c):
    install_by_pipx(c)
    set_poetry_config(c)
    install_rye(c)


@task
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
