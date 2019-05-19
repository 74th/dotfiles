from .lib import run, HOSTNAME
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
        run("git commit -m \"at (uname -s)\"")
        run("git push origin master")
        run(f"cd {d}")
    x_aliases["ec"] = edit_cheatsheets

    def select_command_bookmark():
        if HOSTNAME.startswith("o-"):
            filename = "work"
        else:
            filename = "home"
        r = run(f"cat ~/mycheatsheets/CmdBookmark/{filename} | peco")
        if len(r.lines) > 0:
            name = r.lines[0].strip()
            if name[0] == "[":
                name = name[name.find("]") + 1:]
            run(name)
    x_aliases["cb"] = select_command_bookmark

    def ssh_xonsh(args):
        host = args[0]
        run(f"ssh -t {host} xonsh")
    x_aliases["xssh"] = ssh_xonsh
