#!/usr/local/bin/python3
import os
import subprocess
import sys
import shlex
import pathlib


def get_system():
    system_name = subprocess.run(
        ["uname", "-s"], stdout=subprocess.PIPE, text=True
    ).stdout.strip()
    if system_name == "Darwin":
        return "macos"
    return "linux"


def get_hostname() -> str:
    return subprocess.run(
        ["hostname"], stdout=subprocess.PIPE, text=True
    ).stdout.strip()


def has_path(cmd: str) -> str:
    return subprocess.run(
        ["which", "-s", cmd], stdout=subprocess.PIPE, text=True
    ).stdout.strip()


def get_arch(system: str) -> str:
    if system == "macos":
        return "arm64"
    arch = subprocess.run(
        ["uname", "--processor"], stdout=subprocess.PIPE, text=True
    ).stdout.strip()
    if arch == "aarch64":
        return "arm64"
    if arch == "x86_64":
        return "amd64"
    return "unknown"


def get_paths(default_paths: list[str]) -> list[str]:
    home = os.path.expanduser("~")
    system = get_system()  # Linux, Darwin
    hostname = get_hostname()
    arch = get_arch(system)  # arm64, amd64
    _paths = []  # type: list[str]

    def add(path: str):
        if path not in default_paths and os.path.exists(path):
            _paths.insert(0, path)

    # --- OS のパッケージマネージャ ---

    # Ubuntuなどで追加されてなかった時用
    add("/usr/local/bin")
    add("/usr/local/sbin")

    # for Ubuntu
    add("/snap/bin")

    # Homebrew
    add("/home/linuxbrew/.linuxbrew/bin")
    add("/home/linuxbrew/.linuxbrew/sbin")
    add("/opt/homebrew/bin")

    add("/usr/local/cuda/bin")
    add("/opt/X11/bin")

    # optは強め
    add("/opt/local/bin")

    # --- アプリケーション ---
    add("/Applications/WezTerm.app/Contents/MacOS")
    add("/opt/riscv-gnu-toolchain/bin")
    add("/Applications/Rancher Desktop.app/Contents/Resources/resources/darwin/bin")
    add("/usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin")

    # --- ユーザのパッケージ ---
    add(home + "/.local/bin")

    # Cloud
    add(home + "/Library/Python/3.9/bin")
    add(home + "/google-cloud-sdk/bin")
    add(home + "/google-cloud-sdk/platform/google_appengine")
    add(home + "/sdks/google-cloud-sdk/bin")
    add(home + "/sdks/android-studio/bin")

    # JS
    add(home + "/.deno/bin")
    add(home + "/npm/bin")
    add(home + "/npm/node_modules/.bin")

    # 環境選択系
    add(home + "/.asdf/bin")
    add(home + "/.asdf/shims")
    add(home + "/.nodenv/bin")
    add(home + "/.nodenv/shims")
    add(home + "/.rbx_env/shims")
    add(home + "/.pyenv/shims")

    # Lang
    add(home + "/go/bin")
    add(home + "/.nix-profile/bin")
    add(home + "/.rye/shims")
    add(home + "/.pyenv/bin")
    add(home + "/.cargo/bin")

    # Tool
    add(home + "/.tfenv/bin")
    add(home + "/.krew/bin")
    add(
        home
        + "/.local/xPacks/@xpack-dev-tools/riscv-none-elf-gcc/12.2.0-3.1/.content/bin"
    )
    add(home + "/miniconda3/bin")
    add(home + "/go/src/github.com/uber/go-torch/FlameGraph")

    # Espressif
    # add(home + "/.platformio/penv/bin") # 余計なアイテムも引き込んでしまうので、必要に応じてシンボリックリンクをする
    add(home + "/libraries/espressif/esp-idf/components/esptool_py/esptool")
    add(home + "/libraries/espressif/esp-idf/components/espcoredump")
    add(home + "/libraries/espressif/esp-idf/components/partition_table")
    add(home + "/libraries/espressif/esp-idf/components/app_update")
    # add(home + "/.espressif/python_env/idf4.4_py3.9_env/bin")
    add(home + "/libraries/espressif/esp-idf/tools")

    # Android
    add(home + "/Library/Android/sdk/platform-tools")
    add(home + "/Library/AndroidIntel/platform-tools")  # 会社PC用
    add(home + "/Library/AndroidIntel/tools")  # 会社PC用
    add(home + "/Android/Sdk/platform-tools")
    add(home + "/Android/Sdk/tools")

    # --- 個人管理最優先系 ---
    add(home + "/ghq/github.com/74th/dotfiles/bin")
    add(home + "/ghq/github.com/74th/mycheatsheets/bin")
    if system == "linux":
        add(home + "/ghq/github.com/74th/dotfiles/bin/linux")
        add(home + "/ghq/github.com/74th/mycheatsheets/bin/linux")
        if arch == "amd64":
            add(home + "/ghq/github.com/74th/dotfiles/bin/linux/amd64")
        if arch == "arm64":
            add(home + "/ghq/github.com/74th/dotfiles/bin/linux/arm64")
    if system == "macos":
        add(home + "/ghq/github.com/74th/dotfiles/bin/macos")
        add(home + "/ghq/github.com/74th/mycheatsheets/bin/macos")
    add(home + "/ghq/github.com/74th/dotfiles/bin/" + hostname)
    add(home + "/ghq/github.com/74th/mycheatsheets/bin/" + hostname)
    add(home + "/bin")

    # --- ローカル ---
    if "VIRTUAL_ENV" in os.environ:
        _bin_path = pathlib.Path(os.environ["VIRTUAL_ENV"]) / "bin"
        if _bin_path.exists():
            add(_bin_path.as_posix())

    return _paths


if __name__ == "__main__":
    # for bash
    # eval "$(python3 ~/ghq/github.com/74th/dotfiles/xonsh/xonsh_conf/path.py)"
    if len(sys.argv) > 1:
        current_paths = sys.argv[1].split(":")
    else:
        current_paths = os.environ["PATH"].split(":")
    additional_paths = get_paths(current_paths)
    if additional_paths:
        print("export PATH=" + shlex.quote(":".join(additional_paths)) + ":$PATH")
