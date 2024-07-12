import os
from typing import Set
from invoke.tasks import task

install_script = os.path.dirname(__file__) + "/install.sh"
krew_bin = os.path.expanduser("~/.krew/bin/kubectl-krew")


def installed_plugins(c) -> Set[str]:
    lines = c.run(f"{krew_bin} list").stdout.split("\n")
    results: list[str] = []
    for line in lines:
        l = line.split(" ")
        if not l[0]:
            continue
        results.append(l[0])
    print(results)
    return set(results)


def target_plugins() -> Set[str]:
    plugins = [
        "ctx",
        "ns",
        "iexec",
        "view-secret",
    ]
    return set(plugins)


@task(default=True)
def install(c):
    if c.run("which kubectl", warn=True, hide=True).failed:
        return

    if not os.path.exists(krew_bin):
        c.run(f"bash {install_script}")

    plugins = target_plugins() - installed_plugins(c)
    if len(plugins) > 0:
        c.run(f"{krew_bin} install " + " ".join(plugins))
