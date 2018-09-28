from invoke import task
import invoke

@invoke.task
def upgrade_all(c,force=False, upgrade=False):
    c: invoke.Context
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
        c.run(f"pip3 install {flg} {pkg}")
