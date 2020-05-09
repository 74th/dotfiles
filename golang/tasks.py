import os
import invoke
import yaml
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
