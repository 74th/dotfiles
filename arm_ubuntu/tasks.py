from invoke.tasks import task
from invoke.context import Context

ubuntu_pkgs = [
    "python3",
    "python3-pip",
    "golang-go",
]


@task
def install(c: Context):
    c.run("sudo apt-get update")
    pkgs = " ".join(ubuntu_pkgs)
    c.run("sudo apt-get install -y " + pkgs)
