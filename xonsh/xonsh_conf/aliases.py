#!/usr/local/bin/python3
import os
from typing import Dict, List


def get_aliases() -> Dict[str, List[str]]:
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
    a["al"] = ["ls", "-al"]
    a["la"] = ["ls", "-al"]
    a["ll"] = ["ls", "-al"]
    a["lt"] = ["ls", "-alt"]

    # java
    #a["javac"] = ["javac", "-J-Dfile.encoding=utf-8"]
    #a["java"] = ["java", "-Dfile.encoding=UTF-8"]

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
