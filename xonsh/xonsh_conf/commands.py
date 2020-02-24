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
        if HOSTNAME.startswith("o-") or HOSTNAME.startswith("violet-gopher"):
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

    def ssh_xonsh(args):
        host = args[0]
        run(f"ssh -t {host} xonsh")

    x_aliases["xssh"] = ssh_xonsh

    def docker_delete_all_containers():
        lines = silent_run('docker ps -a --format "{{.ID}}"').split("\n")
        ids = [line.strip() for line in lines]
        " ".join(ids)
        cmd = "docker rm -f " + " ".join(ids)
        run(cmd)

    x_aliases["docker-delete-all-containers"] = docker_delete_all_containers

    def docker_delete_all_images():
        lines = silent_run('docker images --format "{{.ID}}"').split("\n")
        ids = [line.strip() for line in lines]
        ids = list(set(ids))
        " ".join(ids)
        cmd = "docker rmi " + " ".join(ids)
        run(cmd)

    x_aliases["docker-delete-all-images"] = docker_delete_all_images
