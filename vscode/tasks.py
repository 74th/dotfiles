import os
import os.path
from invoke.tasks import task
import detect


@task(default=True)
def backup(c, insider=False):
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


@task
def upload_markdown_style(c):
    css_path = os.path.join(os.path.dirname(__file__), "markdown-style.css")
    c.run(f"gsutil cp {css_path} gs://74th-open/markdown-style.css")
