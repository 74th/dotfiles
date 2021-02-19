import os
import invoke
import yaml
import tempfile
from invoke import task, Context


@task
def download_packages(c):
    if os.path.exists("packages.yaml"):
        yaml_path = "packages.yaml"
    else:
        yaml_path = "golang/packages.yaml"

    with open(yaml_path, "r") as f:
        packages = yaml.load(f)["packages"]

    for package in packages:
        c.run("go get -u " + package)


@task
def install_ubuntu(c):
    version = c.run("curl https://golang.org/VERSION?m=text").stdout.strip()
    #version = "1.14.15"
    if c.run("go version", warn=True).stdout.count(version) > 0:
        return
    with tempfile.TemporaryDirectory() as d:
        with c.cd(d):
            tar_gz = f"{version}.linux-amd64.tar.gz"
            c.run(f"wget https://dl.google.com/go/{tar_gz}")
            c.run(f"sudo rm -rf /usr/local/go")
            c.run(f"sudo tar -C /usr/local -xzf {tar_gz}")
            c.run(f"sudo ln -fs /usr/local/go/bin/* /usr/local/bin/")
