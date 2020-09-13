#!/usr/bin/python3
import os
import subprocess
from typing import List, Optional, Tuple
import sys


def ssh_agent() -> Optional[Tuple[str, str]]:
    d = os.environ.get("XDG_RUNTIME_DIR", "")
    if d:
        d += "/keyring/.ssh"
        if os.path.exists(d):
            return ("SSH_AUTH_SOCK", d)
    return None


def build_envs() -> List[Tuple[str, str]]:
    envs: List[Tuple[str, str]] = []
    env = ssh_agent()
    if env:
        envs.append(env)
    return envs


def apply_envs():
    from .xonsh_builtin import x_env

    envs = build_envs()
    for env in envs:
        x_env[env[0]] = env[1]


if __name__ == "__main__":
    # for bash
    # eval "$(python3 ~/dotfiles/xonsh/xonsh_conf/env.py)"
    envs = build_envs()
    for env in envs:
        print(f"""export {env[0]}="{env[1]}"\n""")
