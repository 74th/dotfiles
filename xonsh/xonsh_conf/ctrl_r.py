# -*- coding: utf-8 -*-
import json
import subprocess
import tempfile

from .lib import run, silent_run, x_execer, HOSTNAME
from .xonsh_builtin import x_env


class Buffer:
    text: str

    def reset(self):
        pass

    def insert_text(self, text: str):
        pass

def select_history(buf: Buffer):
    """
    履歴検索
    """
    with tempfile.NamedTemporaryFile() as tmp:
        o = x_execer.eval(f"history show all -r | peco > {tmp.name}")
        o.end()
        with open(tmp.name) as f:
            cmd = f.read().strip()
    buf.insert_text(cmd)


def select_git(buf):
    line: str = buf.document.current_line
    if line.startswith("git checkout"):
        """
        git status と ブランチを表示
        """
        with tempfile.NamedTemporaryFile() as inputs:
            run(f"git branch -a --no-color > {inputs.name}")
            run(f"git status --short >> {inputs.name}")
            with tempfile.NamedTemporaryFile() as tmp:
                run(f"cat {inputs.name} | peco > {tmp.name}")
                with open(tmp.name) as f:
                    peco: str = f.readline().strip()
        if len(peco) > 0:
            branch = peco.split(" ")[-1]
            buf.insert_text(" " + branch)
    if line.startswith("git add") or line.startswith("git reset"):
        """
        git status で表示されるファイルを選択
        """
        selected = ""
        with tempfile.NamedTemporaryFile() as tmp:
            run(f"git status --short | peco > {tmp.name}")
            with open(tmp.name) as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    file = line.strip().split(" ")[-1]
                    selected += " " + file
        if len(selected) > 0:
            buf.insert_text(selected)


def select_command_bookmark(buf: Buffer):
    if HOSTNAME.startswith("o-"):
        filename = "work"
    else:
        filename = "home"
    with tempfile.NamedTemporaryFile() as tmp:
        run(f"cat  ~/ghq/github.com/74th/mycheatsheets/CmdBookmark/{filename} | peco > {tmp.name}")
        with open(tmp.name) as f:
            line = f.readline()
    if not line:
        return
    name = line.strip()
    if name[0] == "[":
        name = name[name.find("]") + 1 :]
    buf.reset()
    buf.insert_text(name)


def select_dir_bookmark(buf: Buffer):
    with tempfile.NamedTemporaryFile() as tmp:
        run(f"cat  ~/ghq/github.com/74th/mycheatsheets/DirBookmark/{HOSTNAME} | peco > {tmp.name}")
        with open(tmp.name) as f:
            line = f.readline()
    if not line:
        return
    name = line.strip()
    if name[0] == "[":
        name = name[name.find("]") + 1 :]
    buf.reset()
    buf.insert_text(name)


def select_peco(buf: Buffer, command: str):
    with tempfile.NamedTemporaryFile() as tmp:
        run(f"{command} | peco > {tmp.name}")
        with open(tmp.name) as f:
            line = f.readline()
            if not line:
                return
    buf.insert_text(" " + line.strip())


def select_k8s_list(buf: Buffer, list_command: str, replace: str):
    j = json.loads(silent_run(list_command))
    l = []
    for item in j["items"]:
        l.append(item["kind"] + "/" + item["metadata"]["name"])
    with tempfile.NamedTemporaryFile() as input_file:
        with open(input_file.name, "w") as f:
            f.write("\n".join(l))
        with tempfile.NamedTemporaryFile() as output_file:
            run(f"peco {input_file.name} > {output_file.name}")
            with open(output_file.name) as f:
                lines = f.read().splitlines()
                if not lines:
                    return
    buf.reset()
    buf.insert_text(replace + " ".join(lines))


def comp_branch(buf: Buffer):
    with tempfile.NamedTemporaryFile() as tmp:
        run(f"git branch -a --no-color | peco > {tmp.name}")
        with open(tmp.name) as f:
            peco = f.readline()
            if not peco:
                return
            branch = peco.split(" ")[-1]
    text = buf.document.current_line
    text = text[:-1]

    # buf.reset()
    # buf.insert_text(text + branch.strip())
    buf.text = text + branch.strip()
    buf.text

def comp_ls(buf: Buffer):
    with tempfile.NamedTemporaryFile() as tmp:
        run(f"ls --color=never -1 | peco > {tmp.name}")
        with open(tmp.name) as f:
            peco = f.readline()
            if not peco:
                return
    text = buf.document.current_line
    text = text[:-1]
    buf.reset()
    buf.insert_text(text + peco.strip())

def comp_test(buf: Buffer):
    pwd = x_env["PWD"]
    r = subprocess.run(f"ls --color=never -1 | peco", shell=True, capture_output=True, text=True, cwd=pwd)
    peco = r.stdout.strip()
    text = buf.document.current_line
    text = text[:-1]
    buf.reset()
    buf.insert_text(text + peco)

def select(buf: Buffer):
    line: str = buf.document.current_line
    if len(line) == 0:
        select_history(buf)
        return
    if line.endswith(" B"):
        comp_branch(buf)
        return
    if line.endswith(" L"):
        comp_ls(buf)
        return
    if line.endswith(" T"):
        comp_test(buf)
        return
    if line.startswith("git"):
        select_git(buf)
        return
    if line.startswith("kubectx"):
        select_peco(buf, "kubectx")
        return
    if line.startswith("kubens"):
        select_peco(buf, "kubens")
        return
    if line.startswith("kdp"):
        select_k8s_list(buf, "kubectl get pods --output json", "kubectl describe ")
        return
    elif line.startswith("kd"):
        tail = line[3:].strip()
        if len(tail):
            select_k8s_list(buf, "kubectl get " + tail + " --output json", "kubectl describe ")
        else:
            select_k8s_list(buf, "kubectl get all --output json", "kubectl describe ")
        return
    if line.startswith("klp"):
        select_k8s_list(buf, "kubectl get pods --output json", "kubectl logs ")
        return
    elif line.startswith("kl") or line.startswith("k logs"):
        select_k8s_list(buf, "kubectl get all --output json", "kubectl logs ")
        return
    if line.startswith("k exec"):
        select_k8s_list(buf, "kubectl get pods --output json", "kubectl exec ")
        return
    if line.startswith("krm") or line.startswith("k delete"):
        select_k8s_list(buf, "kubectl get all --output json", "kubectl delete ")
        return
    if line.startswith("cb"):
        select_command_bookmark(buf)
        return
    if line.startswith("db"):
        select_dir_bookmark(buf)
        return
    if line.startswith("inv"):
        select_peco(buf, "inv --complete")
        return
    if line.startswith("fab"):
        select_peco(buf, "fab --complete")
        return
