#!/usr/bin/python3
import os
import subprocess
from typing import List, Optional, Tuple


home = os.environ.get("HOME", "/home/nnyn")


def current_tty():
    return subprocess.run(["tty"], stdout=subprocess.PIPE, text=True).stdout.strip()


def ssh_agent() -> Optional[Tuple[str, str]]:
    d = os.environ.get("XDG_RUNTIME_DIR", "")
    if d:
        d += "/keyring/.ssh"
        if os.path.exists(d):
            return ("SSH_AUTH_SOCK", d)
    return None


def pico_sdk_paths() -> List[Tuple[str, str]]:
    paths: List[Tuple[str, str]] = []
    p = f"{home}/pico/pico-sdk"
    if os.path.exists(p):
        paths.append(("PICO_SDK_PATH", p))
    p = f"{home}/pico/pico-examples"
    if os.path.exists(p):
        paths.append(("PICO_EXAMPLES_PATH", p))
    p = f"{home}/pico/pico-extras"
    if os.path.exists(p):
        paths.append(("PICO_EXTRAS_PATH", p))
    p = f"{home}/pico/pico-playground"
    if os.path.exists(p):
        paths.append(("PICO_PLAYGROUND_PATH", p))
    return paths


def gpg_agent() -> Tuple[str, str]:
    return "GPG_TTY", current_tty()


def build_envs() -> List[Tuple[str, str]]:
    envs: List[Tuple[str, str]] = []
    env = ssh_agent()
    if env:
        envs.append(env)
    envs += pico_sdk_paths()
    envs.append(gpg_agent())
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
