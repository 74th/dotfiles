#!/usr/bin/python3
import os
import subprocess
from typing import Optional


home = os.environ.get("HOME", "/home/nnyn")


def current_tty():
    if os.path.exists("/Applications"):
        return ""
    return subprocess.run(["tty"], stdout=subprocess.PIPE, text=True).stdout.strip()


def ssh_agent() -> Optional[tuple[str, str]]:
    d = os.environ.get("XDG_RUNTIME_DIR", "")
    if d:
        d += "/keyring/.ssh"
        if os.path.exists(d):
            return ("SSH_AUTH_SOCK", d)
    return None


def pico_sdk_paths() -> list[tuple[str, str]]:
    paths: list[tuple[str, str]] = []
    p = f"{home}/libs/pico/pico-sdk"
    if os.path.exists(p):
        paths.append(("PICO_SDK_PATH", p))
    p = f"{home}/libs/pico/pico-examples"
    if os.path.exists(p):
        paths.append(("PICO_EXAMPLES_PATH", p))
    p = f"{home}/libs/pico/pico-extras"
    if os.path.exists(p):
        paths.append(("PICO_EXTRAS_PATH", p))
    p = f"{home}/libs/pico/pico-playground"
    if os.path.exists(p):
        paths.append(("PICO_PLAYGROUND_PATH", p))
    return paths


def esp_tools_path() -> list[tuple[str, str]]:
    paths: list[tuple[str, str]] = []
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


def gpg_agent() -> Optional[tuple[str, str]]:
    tty = current_tty()
    if not tty:
        return None
    return "GPG_TTY", tty


def misc() -> list[tuple[str, str]]:
    d = {
        # https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
        "USE_GKE_GCLOUD_AUTH_PLUGIN": "True"
    }
    return list(d.items())


def build_envs() -> list[tuple[str, str]]:
    envs: list[tuple[str, str]] = []
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

    gpg_agent_env = gpg_agent()
    if gpg_agent_env:
        envs.append(gpg_agent_env)
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
