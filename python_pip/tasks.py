from invoke import task
import invoke


def list_small_packages():
    l = []
    l += [
        "invoke",
        "poetry",
    ]
    return l

@invoke.task
def install_small(c):
    l = list_small_packages()
    l_str = " ".join(l)
    c.run(f"pip3 install --user --upgrade {l_str}")
    c.run(f"poetry config virtualenvs.create true")

def list_packages():
    l = list_small_packages()
    l += [
        "black",
        "mypy",
        "xonsh[ptk]",
        "xontrib-readable-traceback",
        "xonsh-docker-tabcomplete",
        "xontrib-z",
        "xonsh-direnv",
    ]
    return l

@invoke.task
def install(c):
    l = list_packages()
    l_str = " ".join(l)
    c.run(f"pip3 install --user --upgrade {l_str}")
    c.run(f"poetry config virtualenvs.create true")

@invoke.task
def upgrade_all(c,force=False, upgrade=False):
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
