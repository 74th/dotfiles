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


def esp_tools_path() -> List[Tuple[str, str]]:
    paths: List[Tuple[str, str]] = []
    if os.path.exists(f"{home}/.espressif"):
        paths.append(
            ("IDF_PYTHON_ENV_PATH", "/home/nnyn/.espressif/python_env/idf4.4_py3.9_env")
        )
        paths.append(
            (
                "OPENOCD_SCRIPTS",
                f"{home}/.espressif/tools/openocd-esp32/v0.10.0-esp32-20210401/openocd-esp32/share/openocd/scripts",
            )
        )
    if os.path.exists(f"{home}/libraries/espressif/esp-idf"):
        paths.append(("IDF_PATH", f"{home}/libraries/espressif/esp-idf"))
        paths.append(
            ("IDF_TOOLS_EXPORT_CMD", f"{home}/libraries/espressif/esp-idf/export.sh")
        )
        paths.append(
            ("IDF_TOOLS_INSTALL_CMD", f"{home}/libraries/espressif/esp-idf/install.sh")
        )
    return paths


def gpg_agent() -> Tuple[str, str]:
    return "GPG_TTY", current_tty()

def misc() -> List[Tuple[str, str]]:
    d = {
        # https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
        "USE_GKE_GCLOUD_AUTH_PLUGIN": "True"
    }
    return list(d.items())


def build_envs() -> List[Tuple[str, str]]:
    envs: List[Tuple[str, str]] = []
    env = ssh_agent()
    if env:
        envs.append(env)
    envs += pico_sdk_paths()
    envs += esp_tools_path()
    envs += misc()

    # gcloud の CLI では固定インストールのPythonを使う
    if os.path.exists("/etc/lsb-release"):
        envs.append(("CLOUDSDK_PYTHON", "/bin/python3"))
    elif os.path.exists("/usr/local/bin/python3"):
        envs.append(("CLOUDSDK_PYTHON", "/usr/local/bin/python3"))

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
