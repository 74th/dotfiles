import os
from typing import List, cast
import detect
from .lib import run, silent_run, HOSTNAME
from .xonsh_builtin import x_env, x_aliases


def load_commands():
    def open_bookmark():
        name = run("cat ~/bookmark | peco").lines[0].strip()
        run(f"cd {name}")

    x_aliases["bk"] = open_bookmark

    def edit_cheatsheets():
        d = run("pwd").lines[0].strip()
        run("cd ~/ghq/github.com/74th/mycheatsheets/sheets/")
        run("git pull origin master")
        name = run("ls | peco").lines[0].strip()
        run(f"vim {name}")
        run("git add -A")
        run('git commit -m "at (uname -s)"')
        run("git push origin master")
        run(f"cd {d}")

    x_aliases["ec"] = edit_cheatsheets

    def select_command_bookmark():
        if (
            HOSTNAME.startswith("o-")
            or HOSTNAME.startswith("O-")
            or HOSTNAME.startswith("violet-gopher")
        ):
            filename = "work"
        else:
            filename = "home"
        r = run(
            f"cat ~/ghq/github.com/74th/mycheatsheets/CmdBookmark/{filename} | peco"
        )
        if len(r.lines) > 0:
            name = r.lines[0].strip()
            if name[0] == "[":
                name = name[name.find("]") + 1 :]
            run(name)

    x_aliases["cb"] = select_command_bookmark

    def cd_ghq():
        r = run("ghq list | peco").lines[0].strip()
        if r:
            r = silent_run(f"ghq list --exact --full-path {r}").strip()
            run(f"cd {r}")

    x_aliases["cdg"] = cd_ghq

    def select_dir_bookmark():
        r = run(
            f"cat ~/ghq/github.com/74th/mycheatsheets/DirBookmark/{HOSTNAME} | peco"
        )
        if len(r.lines) > 0:
            name = r.lines[0].strip()
            if name[0] == "[":
                name = name[name.find("]") + 1 :]
            run(name)

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
        paths = cast(List[str], x_env["PATH"])
        for p in list(paths):
            if p.count("homebrew"):
                paths.remove(p)
            elif p.count("linuxbrew"):
                paths.remove(p)
            if detect.mac and p == "/usr/local/bin":
                paths.remove(p)

    x_aliases["homebrew-deactivate"] = deactivate_homebrew
