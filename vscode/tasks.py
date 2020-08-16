import os
import os.path
from invoke import task
import detect


@task
def backup(c, insider=True):
    home = os.path.expanduser("~")
    if detect.linux:
        d = f"{home}/.config"
    else:
        d = f"{home}/Library/Application Support"
    if insider:
        d = f"{d}/Code - Insiders/User"
        cmd = "code-insiders"
    else:
        d = f"{d}/Code/User"
        cmd = "code"
    b = f"{home}/dotfiles/vscode"
    c.run(f"cp '{d}/keybindings.json' {b}/")
    for s in os.listdir(f"{d}/snippets"):
        c.run(f"cp '{d}/snippets/{s}' {b}/snippets/")

    rejects = ["hediet.vscode-drawio.local-storage", "codespaces.planFilter"]
    with open(f"{d}/settings.json") as f:
        with open(f"{home}/dotfiles/vscode/settings.json", "w") as w:
            for l in f.readlines():
                rejected = False
                for reject in rejects:
                    if l.count(reject):
                        rejected = True
                if not rejected:
                    w.write(l)

    c.run(f"{cmd} --list-extensions > {b}/list-extensions.txt")
