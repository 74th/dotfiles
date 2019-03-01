# -*- coding: utf-8 -*-
import os
import json
import tempfile
import prompt_toolkit
from .lib import run, x_execer, HOSTNAME
from .xonsh_builtin import x_env
from collections import OrderedDict
from operator import itemgetter


def select_history(buf: prompt_toolkit.buffer.Buffer):
    '''
    履歴検索
    '''
    with tempfile.NamedTemporaryFile() as tmp:
        o = x_execer.eval(f"history show all -r | peco > {tmp.name}")
        o.end()
        with open(tmp.name) as f:
            cmd = f.read().strip()
    buf.insert_text(cmd)



def select_git(buf):
    line :str = buf.document.current_line
    if line.startswith("git checkout"):
        '''
        git status と ブランチを表示
        '''
        with tempfile.NamedTemporaryFile() as inputs:
            run(f"git branch -a --no-color > {inputs.name}")
            run(f"git status --short >> {inputs.name}")
            with tempfile.NamedTemporaryFile() as tmp:
                run(f"cat {inputs.name} | peco > {tmp.name}")
                with open(tmp.name) as f:
                    peco: str = f.readline().strip()
        if len(peco) > 0:
            branch = peco.split(" ")[-1]
            buf.insert_text(" "+branch)
    if line.startswith("git add") or line.startswith("git reset"):
        '''
        git status で表示されるファイルを選択
        '''
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

def select_command_bookmark(buf: prompt_toolkit.buffer.Buffer):
    if HOSTNAME.startswith("o-"):
        filename = "work"
    else:
        filename = "home"
    with tempfile.NamedTemporaryFile() as tmp:
        run(f"cat  ~/mycheatsheets/CmdBookmark/{filename} | peco > {tmp.name}")
        with open(tmp.name) as f:
            line = f.readline()
    if not line:
        return
    name = line.strip()
    if name[0] == "[":
        name = name[name.find("]")+1:]
    buf.reset()
    buf.insert_text(name)

def select_peco(buf: prompt_toolkit.buffer.Buffer, command:str):
    with tempfile.NamedTemporaryFile() as tmp:
        run(f"{command} | peco > {tmp.name}")
        with open(tmp.name) as f:
            line = f.readline()
            if not line:
                return
    buf.insert_text(" " + line.strip())


def select(buf: prompt_toolkit.buffer.Buffer):
    line :str = buf.document.current_line
    if len(line) == 0:
        select_history(buf)
    if line.startswith("git"):
        select_git(buf)
    if line.startswith("kubectx"):
        select_peco(buf, "kubectx")
    if line.startswith("kubens"):
        select_peco(buf, "kubens")
    if line.startswith("cb"):
        select_command_bookmark(buf)
    if line.startswith("inv"):
        select_peco(buf, "inv --complete")
    if line.startswith("fab"):
        select_peco(buf, "fab --complete")
