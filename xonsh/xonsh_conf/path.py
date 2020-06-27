#!/usr/local/bin/python3
import os
from typing import List
import sys

import detect


def get_paths(default_paths: List[str]) -> List[str]:

    HOME = os.environ.get("HOME", "/home/nnyn/")
    _paths = [] # type: List[str]


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

    add("/usr/local/cuda/bin")
    add(HOME + "/Library/Python/2.7/bin")
    add(HOME + "/Library/Python/3.7/bin")
    add(HOME + "/google-cloud-sdk/bin")
    add(HOME + "/google-cloud-sdk/platform/google_appengine")
    add(HOME + "/npm/bin")
    add(HOME + "/npm/node_modules/.bin")
    add(HOME + "/Library/Android/sdk/platform-tools")
    add(HOME + "/.local/bin")
    add(HOME + "/.rbx_env/shims")
    add(HOME + "/.nodenv/shims")
    add(HOME + "/.pyenv/shims")
    add(HOME + "/.nodenv/shims")
    add(HOME + "/.tfenv/bin")
    add(HOME + "/go/bin")
    add(HOME + "/go/src/github.com/uber/go-torch/FlameGraph")
    add(HOME + "/Android/Sdk/platform-tools")
    add(HOME + "/Android/Sdk/tools")
    add(HOME + "/sdks/google-cloud-sdk/bin")
    add(HOME + "/sdks/android-studio/bin")
    add("/opt/X11/bin")

    add(HOME + "/bin")
    add(HOME + "/dotfiles/bin")

    if detect.linux:
        add(HOME + "/dotfiles/bin/linux")
    if detect.mac:
        add(HOME + "/dotfiles/bin/macos")


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
