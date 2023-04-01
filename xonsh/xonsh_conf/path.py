#!/usr/local/bin/python3
import os
import subprocess
import sys
import shlex


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


def get_paths(default_paths: list[str]) -> list[str]:

    home = os.path.expanduser("~")
    system = get_system()
    hostname = get_hostname()
    _paths = []  # type: list[str]

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
    add("/opt/X11/bin")
    add("/Applications/WezTerm.app/Contents/MacOS")
    add(home + "/Library/Python/3.9/bin")
    add(home + "/google-cloud-sdk/bin")
    add(home + "/google-cloud-sdk/platform/google_appengine")
    add(home + "/npm/bin")
    add(home + "/npm/node_modules/.bin")
    add(home + "/Library/Android/sdk/platform-tools")
    add(home + "/.nix-profile/bin")
    add(home + "/.local/bin")
    add(home + "/.rbx_env/shims")
    add(home + "/.nodenv/bin")
    add(home + "/.nodenv/shims")
    add(home + "/.pyenv/shims")
    add(home + "/.pyenv/bin")
    add(home + "/.tfenv/bin")
    add(home + "/.krew/bin")
    add(home + "/.cargo/bin")
    add(home + "/.asdf/bin")
    add(home + "/.asdf/shims")
    add(home + "/miniconda3/bin")
    add(home + "/go/bin")
    add(home + "/go/src/github.com/uber/go-torch/FlameGraph")
    add(home + "/Library/AndroidIntel/platform-tools")  # 会社PC用
    add(home + "/Library/AndroidIntel/tools")  # 会社PC用
    add(home + "/Android/Sdk/platform-tools")
    add(home + "/Android/Sdk/tools")
    add(home + "/sdks/google-cloud-sdk/bin")
    add(home + "/sdks/android-studio/bin")
    # add(home + "/.platformio/penv/bin") # 余計なアイテムも引き込んでしまうので、必要に応じてシンボリックリンクをする
    add(home + "/libraries/espressif/esp-idf/components/esptool_py/esptool")
    add(home + "/libraries/espressif/esp-idf/components/espcoredump")
    add(home + "/libraries/espressif/esp-idf/components/partition_table")
    add(home + "/libraries/espressif/esp-idf/components/app_update")
    add("/Applications/Rancher Desktop.app/Contents/Resources/resources/darwin/bin")
    add(
        home
        + "/.espressif/tools/xtensa-esp32-elf/esp-2020r3-8.4.0/xtensa-esp32-elf/bin"
    )
    add(
        home
        + "/.espressif/tools/xtensa-esp32s2-elf/esp-2020r3-8.4.0/xtensa-esp32s2-elf/bin"
    )
    add(
        home
        + "/.espressif/tools/xtensa-esp32s3-elf/esp-2020r3-8.4.0/xtensa-esp32s3-elf/bin"
    )
    add(
        home
        + "/.espressif/tools/riscv32-esp-elf/1.24.0.123_64eb9ff-8.4.0/riscv32-esp-elf/bin"
    )
    add(
        home
        + "/.espressif/tools/esp32ulp-elf/2.28.51-esp-20191205/esp32ulp-elf-binutils/bin"
    )
    add(
        home
        + "/.espressif/tools/esp32s2ulp-elf/2.28.51-esp-20191205/esp32s2ulp-elf-binutils/bin"
    )
    add(
        home
        + "/.espressif/tools/openocd-esp32/v0.10.0-esp32-20210401/openocd-esp32/bin"
    )
    add("/usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin")
    # add(home + "/.espressif/python_env/idf4.4_py3.9_env/bin")
    add(home + "/libraries/espressif/esp-idf/tools")
    add("/opt/riscv-gnu-toolchain/bin")

    add(home + "/bin")
    add(home + "/dotfiles/bin")
    add(home + "/ghq/github.com/74th/mycheatsheets/bin")
    add(home + "/ghq/github.com/74th/mycheatsheets/bin/" + hostname)

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
        print("export PATH=" + shlex.quote(":".join(additional_paths)) + ":$PATH")
