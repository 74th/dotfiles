#!/usr/local/bin/python3
import os
import subprocess
import os.path

HOME = os.environ.get("HOME", "/home/nnyn")


def exists_command(cmd: str):
    r = subprocess.run(
        ["which", cmd],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return r.returncode == 0


def get_aliases(human: bool = False) -> dict[str, list[str]]:
    a: dict[str, list[str]] = {}
    a["g"] = ["git"]
    a["gt"] = ["git", "status"]
    a["co"] = ["git", "checkout"]
    a["commit"] = ["git", "commit", "-v"]
    a["add"] = ["git", "add"]
    a["push"] = ["git", "push"]
    a["pull"] = ["git", "pull"]

    # kubernetes
    a["k"] = ["kubectl"]
    a["kgp"] = ["eubectl", "get", "pods", "--sort-by=.metadata.creationTimestamp"]
    a["kga"] = ["kubectl", "get", "all"]
    a["kg"] = ["kubectl", "get"]
    a["kd"] = ["kubectl", "describe"]
    a["krm"] = ["kubectl", "delete"]

    # syntax_sugar
    if os.path.exists(f"{HOME}/.cargo/bin/lsd"):
        a["al"] = ["lsd", "-al"]
        a["la"] = ["lsd", "-al"]
        a["ll"] = ["lsd", "-al"]
        a["lt"] = ["lsd", "-alt"]
    else:
        a["al"] = ["ls", "-al"]
        a["la"] = ["ls", "-al"]
        a["ll"] = ["ls", "-alh"]
        a["lt"] = ["ls", "-alt"]
    a["rm"] = ["trash"]

    # java
    # a["javac"] = ["javac", "-J-Dfile.encoding=utf-8"]
    # a["java"] = ["java", "-Dfile.encoding=UTF-8"]

    if os.path.exists("/Volumes"):
        a["brew"] = ["arch", "-arm64", "brew"]

    return a


def export_bash(aliases: dict[str, list[str]]):
    output = ""
    for alias, cmd in aliases.items():
        output += "alias " + alias + "='" + " ".join(cmd) + "';"
    print(output)


if __name__ == "__main__":
    # for bash
    # eval "$(python3 ~/ghq/github.com/74th/dotfiles/xonsh/xonsh_conf/aliases.py)"
    aliases = get_aliases()
    export_bash(aliases)
