#!/usr/local/bin/python3
import os
from typing import List

def get_paths(default_paths : List[str]) -> List[str]:

    HOME = os.environ.get("HOME", "/home/nnyn/")
    _paths: List[str] = []

    def add(path: str):
        if path not in default_paths and os.path.exists(path):
            _paths.insert(0, path)

    # Ubuntuなどで追加されてなかった時用
    add("/usr/local/bin")
    add("/usr/local/sbin")

    # for Ubuntu
    add("/snap/bin")

    # Homebrew for Linux
    add(f"/home/linuxbrew/.linuxbrew/bin")

    add("/usr/local/cuda/bin")
    add(f"{HOME}/Library/Python/2.7/bin")
    add(f"{HOME}/Library/Python/3.7/bin")
    add(f"{HOME}/google-cloud-sdk/bin")
    add(f"{HOME}/google-cloud-sdk/platform/google_appengine")
    add(f"{HOME}/npm/bin")
    add(f"{HOME}/npm/node_modules/.bin")
    add(f"{HOME}/Library/Android/sdk/platform-tools")
    add(f"{HOME}/.rbx_env/shims")
    add(f"{HOME}/.pyenv/shims")
    add(f"{HOME}/.pyenv/bin")
    add(f"{HOME}/.tfenv/bin")
    add(f"{HOME}/go/bin")
    add(f"{HOME}/go/src/github.com/uber/go-torch/FlameGraph")
    add(f"{HOME}/Android/Sdk/platform-tools")
    add(f"{HOME}/Android/Sdk/tools")
    add(f"{HOME}/sdks/google-cloud-sdk/bin")
    add(f"{HOME}/sdks/android-studio/bin")
    add("/opt/X11/bin")
    add("/usr/local/share/dotnet")
    add("/Library/Frameworks/Mono.framework/Versions/Current/Commands")
    add("/Library/TeX/texbin")

    add(f"{HOME}/bin")
    add(f"{HOME}/dotfiles/bin")

    return _paths

if __name__ == "__main__":
    # for bash
    # eval "$(python3 ~/dotfiles/xonsh/xonsh_conf/path.py)"
    current_paths = os.environ["PATH"].split(":")
    additional_paths = get_paths(current_paths)
    if additional_paths:
        print("export PATH=" + ":".join(additional_paths) + ":$PATH")
