import os.path
from invoke import task
import detect

@task
def ln(c):
    d = os.path.expanduser("~")
    if detect.linux:
        d = f"{d}/.config"
    if detect.mac:
        d = f"{d}/Library/Application Support"
    c.run(f"mkdir -p '{d}/Code - Insiders/User'")
    c.run(f"mkdir -p '{d}/Code/'")
    c.run(f"rm -rf '{d}/Code/User'")
    c.run(f"ln -s '{d}/Code - Insiders/User' '{d}/Code/User'")

    d = os.path.expanduser("~")
    c.run(f"mkdir -p '{d}/.vscode-insiders'")
    c.run(f"rm -rf '{d}/.vscode'")
    c.run(f"ln -s '{d}/.vscode-insiders' '{d}/.vscode'")
