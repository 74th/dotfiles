# -*- coding: utf-8 -*-
import os
import json
import tempfile
import builtins
import prompt_toolkit
from collections import OrderedDict
from operator import itemgetter
from xonsh.proc import HiddenCommandPipeline

execer = builtins.__xonsh_execer__ # type: Execer

def run(command: str)->HiddenCommandPipeline:
    return execer.eval(command)

def _get_history(session_history=None, return_list=False):
    '''
    https://qiita.com/riktor/items/4a90b4e125cd091a9d07
    TODO: 時々お掃除いる？
    '''
    hist_dir = __xonsh_env__['XONSH_DATA_DIR']
    files = [ os.path.join(hist_dir,f) for f in os.listdir(hist_dir)
              if f.startswith('xonsh-') and f.endswith('.json') ]
    file_hist = [ json.load(open(f))['data']['cmds'] for f in files ]
    cmds = [ ( c['inp'].replace('\n', ''), c['ts'][0] )
                 for cmds in file_hist for c in cmds if c]
    cmds.sort(key=itemgetter(1))
    cmds = [ c[0] for c in cmds[::-1] ]
    if session_history:
        cmds.extend(session_history)
    zip_with_dummy = list(zip(cmds, [0] * len(cmds)))[::-1]
    cmds = list(OrderedDict(zip_with_dummy).keys())[::-1]
    if return_list:
        return cmds
    else:
        return '\n'.join(cmds)

def select_history(buf: prompt_toolkit.buffer.Buffer):
    '''
    履歴検索
    '''
    sess_history = run("history").lines
    sess_history = [h.strip() for h in sess_history]
    hist = _get_history(sess_history)
    with tempfile.NamedTemporaryFile() as input_tmp:
        with tempfile.NamedTemporaryFile() as output_tmp:
            with open(input_tmp.name,"w") as f:
                f.write(hist)
            run(f"cat {input_tmp.name} | peco > {output_tmp.name}")
            with open(output_tmp.name) as f:
                peco = f.readline().strip()
            if len(peco) > 0:
                buf.insert_text(peco)


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
    with tempfile.NamedTemporaryFile() as tmp:
        run(f"cat  ~/mycheatsheets/CmdBookmark/work | peco > {tmp.name}")
        with open(tmp.name) as f:
            line = f.readline()
            if not line:
                return
    buf.reset()
    buf.insert_text(line.strip())

def select_invoke(buf: prompt_toolkit.buffer.Buffer):
    commands = []
    with tempfile.NamedTemporaryFile() as tmp:
        run(f"invoke --complete | peco > {tmp.name}")
        with open(tmp.name) as f:
            line = f.readline()
            if not line:
                return
    buf.insert_text(" " + line.strip())

def select_fabric(buf: prompt_toolkit.buffer.Buffer):
    commands = []
    with tempfile.NamedTemporaryFile() as tmp:
        run(f"fabric --complete | peco > {tmp.name}")
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
    if line.startswith("cb"):
        select_command_bookmark(buf)
    if line.startswith("inv"):
        select_invoke_command(buf)
    if line.startswith("fab"):
        select_invoke_command(buf)
