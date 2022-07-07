# -*- coding: utf-8 -*-
from abc import ABCMeta
import json
import subprocess
import tempfile

from .lib import run, silent_run, HOSTNAME, peco
from .xonsh_builtin import x_session


class Buffer(ABCMeta):
    text: str

    def delete_before_cursor(self):
        pass

    def reset(self):
        pass

    def insert_text(self, text: str):
        pass


def select_history(buf: Buffer):
    """
    履歴検索
    """
    cmds = [item["inp"] for item in x_session.history.all_items()]
    cmds.reverse()
    input_text = "\n".join(cmds)
    result = subprocess.run("peco", input=input_text, text=True, capture_output=True)
    if result.returncode == 0:
        cmd = result.stdout.strip()
        buf.reset()
        buf.insert_text(cmd)


def select_git(buf):
    line: str = buf.document.current_line
    if line.startswith("git checkout"):
        """
        git status と ブランチを表示
        """
        inputs = run("git branch -a --no-color").strip()
        inputs += "\n" + run("git status --short").strip()
        r = peco(inputs)
        if r:
            branch = r.split(" ")[-1]
            buf.insert_text(" " + branch)
    if line.startswith("git add") or line.startswith("git reset"):
        """
        git status で表示されるファイルを選択
        """
        inputs = run("git status --short").strip()
        r = peco(inputs)
        if r:
            buf.insert_text(" " + " ".join([l.split(" ")[-1] for l in r.splitlines()]))


def select_command_bookmark(buf: Buffer):
    if HOSTNAME.startswith("o-"):
        filename = "work"
    else:
        filename = "home"
    name = run(
        f"cat  ~/ghq/github.com/74th/mycheatsheets/CmdBookmark/{filename} | peco "
    )
    if not name:
        return
    if name[0] == "[":
        name = name[name.find("]") + 1 :]
    buf.reset()
    buf.insert_text(name)


def select_dir_bookmark(buf: Buffer):
    name = run(
        f"cat  ~/ghq/github.com/74th/mycheatsheets/DirBookmark/{HOSTNAME} | peco "
    )
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
    item = run(f"git branch -a --no-color | peco")
    if not item:
        return
    branch = item.split(" ")[-1]
    buf.delete_before_cursor()
    buf.insert_text(branch)


def comp_ls(buf: Buffer):
    item = run(f"ls --color=never -1 | peco ")
    if not item:
        return
    buf.delete_before_cursor()
    buf.insert_text(item)


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
            select_k8s_list(
                buf, "kubectl get " + tail + " --output json", "kubectl describe "
            )
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
