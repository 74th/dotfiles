#!/usr/local/bin/python3
import subprocess

from typing import Dict, List


def exists_command(cmd: str):
    r = subprocess.run(
        ["which", cmd],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return r.returncode == 0


def get_aliases(human: bool = False) -> Dict[str, List[str]]:
    a: Dict[str, List[str]] = {}
    a["gt"] = ["git", "status"]
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
    if exists_command("lsd"):
        a["al"] = ["lsd", "-al"]
        a["la"] = ["lsd", "-al"]
        a["ll"] = ["lsd", "-al"]
        a["lt"] = ["lsd", "-alt"]
    else:
        a["al"] = ["ls", "-al"]
        a["la"] = ["ls", "-al"]
        a["ll"] = ["ls", "-al"]
        a["lt"] = ["ls", "-alt"]
    a["rm"] = ["trash"]

    # java
    # a["javac"] = ["javac", "-J-Dfile.encoding=utf-8"]
    # a["java"] = ["java", "-Dfile.encoding=UTF-8"]

    return a


def export_bash(aliases: Dict[str, List[str]]):
    output = ""
    for alias, cmd in aliases.items():
        output += "alias " + alias + "='" + " ".join(cmd) + "';"
    print(output)


if __name__ == "__main__":
    # for bash
    # eval "$(python3 ~/dotfiles/xonsh/xonsh_conf/aliases.py)"
    aliases = get_aliases()
    export_bash(aliases)
