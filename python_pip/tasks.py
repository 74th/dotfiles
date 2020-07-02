from invoke import task
import invoke

@invoke.task
def install(c):
    pkgs += [
        "poetry",
        "xonsh[ptk]"
    ]
    pkgs_str = " ".join(pkgs)
    c.run(f"pip3 install --user --upgrade {pkgs_str}")
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
