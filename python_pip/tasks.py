import pathlib

from invoke.tasks import task


def set_poetry_config(c):
    c.run(f"~/.local/bin/poetry config virtualenvs.create true")
    c.run(f"~/.local/bin/poetry config virtualenvs.in-project true")


@task
def install_small(c):
    install_by_uv(c)
    set_poetry_config(c)


def list_packages_by_uv():
    l = [
        "poetry",
        "pre-commit",
        # "xonsh[full]",
    ]
    return l


@task
def install_by_uv(c):
    l = list_packages_by_uv()
    for p in l:
        c.run(f"uv tool install {p}")


@task
def install_uv(c):
    if pathlib.Path("~/.local/bin/uv").expanduser().exists():
        return
    c.run("curl -LsSf https://astral.sh/uv/install.sh | sh", pty=True)


@task
def install(c):
    install_uv(c)
    install_by_uv(c)
    set_poetry_config(c)


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
