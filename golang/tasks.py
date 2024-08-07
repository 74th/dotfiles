import os
import tempfile

import yaml
import detect
from invoke.tasks import task


@task
def download_packages(c):
    if c.run("which go", warn=True).failed:
        install_go(c)

    if os.path.exists("packages.yaml"):
        yaml_path = "packages.yaml"
    else:
        yaml_path = "golang/packages.yaml"

    with open(yaml_path, "r") as f:
        packages = yaml.load(f, yaml.CLoader)["packages"]

    for package in packages:
        c.run("go install " + package)


@task
def install_go(c):
    version = c.run("curl https://go.dev/VERSION?m=text").stdout.splitlines()[0].strip()
    # version = "1.14.15"
    cpu = c.run("uname -p").stdout.strip()
    go_version = c.run("go version", warn=True)
    if go_version.ok and go_version.stdout.count(version) > 0:
        return
    with tempfile.TemporaryDirectory() as d:
        with c.cd(d):
            if detect.mac:
                if cpu == "arm":
                    tar_gz = f"{version}.darwin-arm64.tar.gz"
                else:
                    tar_gz = f"{version}.darwin-amd64.tar.gz"
            else:
                if cpu == "aarch64":
                    tar_gz = f"{version}.linux-arm64.tar.gz"
                else:
                    tar_gz = f"{version}.linux-amd64.tar.gz"
            c.run(f"curl -LO https://dl.google.com/go/{tar_gz}")
            c.run("sudo rm -rf /usr/local/go")
            c.run(f"sudo tar -C /usr/local -xzf {tar_gz}")
            c.run("sudo ln -fs /usr/local/go/bin/* /usr/local/bin/")
