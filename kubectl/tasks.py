import tempfile
from urllib import request
from pathlib import Path

import detect

from task_utils import HOME, get_arch
from invoke.tasks import task
from invoke.context import Context

install_script = Path(__file__).joinpath("install.sh")
krew_bin = Path("~/.krew/bin/kubectl-krew").expanduser()

KREW_PLUGINS = {
    "ctx",
    "ns",
    "iexec",
    "view-secret",
}


@task
def install_kubectl(c: Context, force: bool = False) -> None:
    if not force:
        r = c.run("which kubectl", warn=True)
        assert r is not None
        if r.ok:
            return

    with request.urlopen("https://dl.k8s.io/release/stable.txt") as res:
        latest_version = res.read().decode("utf-8").strip()

    arch = get_arch(c)
    os_name = "linux"
    if detect.mac:
        os_name = "darwin"

    with tempfile.TemporaryDirectory() as tmpdir:
        with c.cd(tmpdir):
            c.run(
                f'curl -LO "https://dl.k8s.io/release/{latest_version}/bin/{os_name}/{arch.value}/kubectl"'
            )
            c.run("chmod +x kubectl")
            c.run(f"cp kubectl {HOME}/bin/kubectl")


def install_krew(c: Context):
    if krew_bin.exists():
        return
    c.run(f"bash {install_script}")


def installed_plugins(c: Context) -> set[str]:
    r = c.run(f"{krew_bin} list", hide=True)
    assert r

    lines = r.stdout.split("\n")
    results: list[str] = []
    for line in lines:
        l = line.split(" ")
        if not l[0]:
            continue
        results.append(l[0])
    return set(results)


def install_krew_plugins(c: Context):
    plugins = KREW_PLUGINS - installed_plugins(c)
    if len(plugins) > 0:
        c.run(f"{krew_bin} install " + " ".join(plugins))


@task(default=True)
def install(c):
    install_kubectl(c)
    install_krew(c)
    install_krew_plugins(c)
