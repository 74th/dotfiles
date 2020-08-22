from .lib import run, silent_run, HOSTNAME
from .xonsh_builtin import x_env, x_aliases


def load_commands():
    def open_bookmark():
        name = run("cat ~/bookmark | peco").lines[0].strip()
        run(f"cd {name}")

    x_aliases["bk"] = open_bookmark

    def edit_cheatsheets():
        d = run("pwd").lines[0].strip()
        run("cd ~/mycheatsheets/sheets/")
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
        r = run(f"cat ~/mycheatsheets/CmdBookmark/{filename} | peco")
        if len(r.lines) > 0:
            name = r.lines[0].strip()
            if name[0] == "[":
                name = name[name.find("]") + 1 :]
            run(name)

    x_aliases["cb"] = select_command_bookmark

    def cd_ghq():
        r = run("ghq list | peco").lines[0].strip()
        if r:
            r = silent_run(f"ghq list --full-path {r}").strip()
            run(f"cd {r}")

    x_aliases["cdg"] = cd_ghq

    def select_dir_bookmark():
        r = run(f"cat ~/mycheatsheets/DirBookmark/{HOSTNAME} | peco")
        if len(r.lines) > 0:
            name = r.lines[0].strip()
            if name[0] == "[":
                name = name[name.find("]") + 1 :]
            run(name)

    x_aliases["db"] = select_dir_bookmark
