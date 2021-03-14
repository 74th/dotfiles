#!/usr/local/bin/python3
import os
import subprocess
from typing import List
import sys


def get_system():
    return subprocess.run(
        ["uname", "-s"], stdout=subprocess.PIPE, text=True
    ).stdout.strip()


def get_hostname():
    return subprocess.run(
        ["hostname"], stdout=subprocess.PIPE, text=True
    ).stdout.strip()


def has_path(cmd: str):
    return subprocess.run(
        ["which", "-s", cmd], stdout=subprocess.PIPE, text=True
    ).stdout.strip()


def get_paths(default_paths: List[str]) -> List[str]:

    home = os.path.expanduser("~")
    system = get_system()
    hostname = get_hostname()
    _paths = []  # type: List[str]

    def add(path: str):
        if path not in default_paths and os.path.exists(path):
            _paths.insert(0, path)

    # Ubuntuなどで追加されてなかった時用
    add("/usr/local/bin")
    add("/usr/local/sbin")

    # for Ubuntu
    add("/snap/bin")

    # Homebrew for Linux
    add("/home/linuxbrew/.linuxbrew/bin")
    add("/home/linuxbrew/.linuxbrew/sbin")

    add("/usr/local/cuda/bin")
    add("/opt/homebrew/bin")
    add("/opt/local/bin")
    add(home + "/Library/Python/3.9/bin")
    add(home + "/google-cloud-sdk/bin")
    add(home + "/google-cloud-sdk/platform/google_appengine")
    add(home + "/npm/bin")
    add(home + "/npm/node_modules/.bin")
    add(home + "/Library/Android/sdk/platform-tools")
    add(home + "/.nix-profile/bin")
    add(home + "/.local/bin")
    add(home + "/.rbx_env/shims")
    add(home + "/.nodenv/shims")
    add(home + "/.pyenv/shims")
    add(home + "/.pyenv/bin")
    add(home + "/.nodenv/shims")
    add(home + "/.tfenv/bin")
    add(home + "/.krew/bin")
    add(home + "/.cargo/bin")
    add(home + "/.asdf/bin")
    add(home + "/.asdf/shims")
    add(home + "/go/bin")
    add(home + "/go/src/github.com/uber/go-torch/FlameGraph")
    add(home + "/Android/Sdk/platform-tools")
    add(home + "/Android/Sdk/tools")
    add(home + "/sdks/google-cloud-sdk/bin")
    add(home + "/sdks/android-studio/bin")
    add("/opt/X11/bin")

    add(home + "/bin")
    add(home + "/dotfiles/bin")
    add(home + "/ghq/github.com/74th/mycheatsheets/bin")

    if system == "Linux":
        add(home + "/dotfiles/bin/linux")
        add(home + "/ghq/github.com/74th/mycheatsheets/bin/linux")
    if system == "Darwin":
        add(home + "/dotfiles/bin/macos")
        add(home + "/ghq/github.com/74th/mycheatsheets/bin/macos")
    add(home + "/dotfiles/bin/" + hostname)
    add(home + "/ghq/github.com/74th/mycheatsheets/bin/" + hostname)

    return _paths


if __name__ == "__main__":
    # for bash
    # eval "$(python3 ~/dotfiles/xonsh/xonsh_conf/path.py)"
    if len(sys.argv) > 1:
        current_paths = sys.argv[1].split(":")
    else:
        current_paths = os.environ["PATH"].split(":")
    additional_paths = get_paths(current_paths)
    if additional_paths:
        print("export PATH=" + ":".join(additional_paths) + ":$PATH")
