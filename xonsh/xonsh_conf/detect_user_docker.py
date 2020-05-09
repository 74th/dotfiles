from typing import Optional
import os
import subprocess

def detect_user_docker() -> Optional[str]:
    rootless_docker = os.path.expanduser("~/bin/dockerd-rootless.sh")
    if not os.path.exists(rootless_docker):
        return None

    subprocess.run(["systemctl", "--user", "start", "docker"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    uid = os.getuid()
    home = os.environ.get("HOME", "/home/nnyn")

    sock_paths = [
        "/run/user/{uid}/docker.sock".format(uid=uid),
        f"unix:///tmp/docker-{uid}/docker.sock".format(uid=uid),
        f"unix://{home}/var/run/docker.sock".format(home=home),
    ]
    for sock_path in sock_paths:
        if os.path.exists(sock_path):
        return sock_path
    return None

def detect_user_docker_for_xonsh():
    docker_host = detect_user_docker()
    if docker_host:
        from .xonsh_builtin import x_env
        x_env["DOCKER_HOST"] = docker_host

if __name__ == "__main__":
    # for bash
    # eval "$(python3 ~/dotfiles/xonsh/xonsh_conf/path.py)"
    docker_host = detect_user_docker()
    if docker_host:
        print("export DOCKER_HOST=" + docker_host)
