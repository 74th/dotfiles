import os
from typing import cast
import detect
from .lib import run, x_run, silent_run, HOSTNAME
from .xonsh_builtin import x_env, x_aliases


def load_commands():
    def open_bookmark():
        name = run("cat ~/bookmark | peco")
        x_run(f"cd {name}")

    x_aliases["bk"] = open_bookmark

    x_aliases["ec"] = "edit-cs"

    def cd_ghq(args=[""]):
        r = ""
        if len(args) == 0:
            r = silent_run("ghq list | peco").strip()
        else:
            l: list[str] = silent_run("ghq list").split("\n")
            for p in l:
                if p.find(args[0]) >= 0:
                    if len(r) == 0 or len(p) < len(r):
                        r = p
        if r:
            r = silent_run(f"ghq list --exact --full-path {r}").strip()
            x_run(f"cd {r}")

    x_aliases["cdg"] = cd_ghq

    def select_dir_bookmark():
        name = run(
            f"cat ~/ghq/github.com/74th/mycheatsheets/DirBookmark/{HOSTNAME} | peco"
        )
        if len(name) > 0:
            if name[0] == "[":
                name = name[name.find("]") + 1 :]
            x_run(name)

    x_aliases["db"] = select_dir_bookmark

    def up_ssh_agent():
        uid = int(silent_run("id -u"))
        d = f"/run/user/{uid}/keyring"
        sock = f"{d}/ssh"
        if not os.path.exists(d):
            run(f"mkdir {d}")
        run(f"killall ssh-agent")
        if os.path.exists(sock):
            run(f"rm {sock}")
        run(f"ssh-agent -a {sock}")
        x_env["SSH_AUTH_SOCK"] = sock

    x_aliases["ssh-agent-up"] = up_ssh_agent

    def deactivate_homebrew():
        paths = cast(list[str], x_env["PATH"])
        for p in list(paths):
            if p.count("homebrew"):
                paths.remove(p)
            elif p.count("linuxbrew"):
                paths.remove(p)
            if detect.mac and p == "/usr/local/bin":
                paths.remove(p)

    x_aliases["homebrew-deactivate"] = deactivate_homebrew

    def allow_rm_toggle():
        if "rm" in x_aliases:
            print("allow rm")
            del x_aliases["rm"]
        else:
            print("use trash as rm")
            x_aliases["rm"] = "trash"

    x_aliases["allow-rm-toggle"] = allow_rm_toggle
