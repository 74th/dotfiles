# -*- coding: utf-8 -*-
import os
import re
import json
import builtins
import invoke
from collections import OrderedDict
from operator import itemgetter
import prompt_toolkit
from xonsh.environ import Env
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition, ViInsertMode

ENV = builtins.__xonsh_env__  # type: Env
ENV["XONSH_SHOW_TRACEBACK"] = True


def silent_run(command: str) -> str:
    return invoke.run(command, warn=True, hide=True).stdout.strip()

def run(command: str) ->str:
    return invoke.run(command, warn=True, hide=False, echo=True).stdout.strip()


c = invoke.Context({
    "run": {
        "echo": True,
        "warn": True,
        "hide": False,
    }
})


paths = ENV["PATH"]


def _add_path_if_exists(path: str, if_path: str = None):
    if if_path:
        exist = os.path.exists(if_path)
    else:
        exist = os.path.exists(path)
    if exist:
        paths.insert(0, path)


HOME = ENV["HOME"]


def _set_prompt():

    prompt = ""

    # user
    root = False
    if "USER" in ENV and ENV["USER"] == "root":
        root = True
        prompt += "{RED}"
    else:
        prompt += "{GREEN}"
    prompt += "{user}{WHITE}@"

    hostname = silent_run("hostname -s")
    if hostname in ["nagisa", "methyl", "mini", "patty"]:
        prompt += "{CYAN}"
    elif hostname in ["mbp"]:
        prompt += "{YELLOW}"
    else:
        prompt += "{WHITE}"
    prompt += "{hostname}"

    prompt += " "

    prompt += "{cwd}{branch_color}{curr_branch: {}}{NO_COLOR}\n$"

    ENV["PROMPT"] = prompt


_set_prompt()


def _default_charsets():
    '''
    文字コードの標準設定
    '''
    ENV["LESSCHARSET"] = "UTF-8"
    ENV["LANG"] = "en_US.UTF-8"
    ENV["LC_CTYPE"] = "en_US.UTF-8"
    ENV["LC_ALL"] = "en_US.UTF-8"
_default_charsets()

def __add_paths():
    if '/usr/local/bin' not in paths:
        # 追加されてなかった時用
        _add_path_if_exists('/usr/local/bin')
    _add_path_if_exists('/usr/local/cuda/bin')
    _add_path_if_exists(f'{HOME}/Library/Android/sdk/platform-tools')
    _add_path_if_exists(f'{HOME}/.rbenv/shims')
    _add_path_if_exists(f'{HOME}/.pyenv/shims')
    _add_path_if_exists(f'{HOME}/go/bin')
    _add_path_if_exists(f'{HOME}/dotfiles/bin/darwin')
    _add_path_if_exists(f'{HOME}/go/src/github.com/uber/go-torch/FlameGraph')
    _add_path_if_exists('/opt/X11/bin')
    _add_path_if_exists('/usr/local/share/dotnet')
    _add_path_if_exists('/Library/Frameworks/Mono.framework/Versions/Current/Commands')
    _add_path_if_exists('/Library/TeX/texbin')
    if os.path.exists(f'{HOME}/Library/Python/2.7/bin'):
        # OS 標準の Python は優先度低めに
        ENV["PATH"].append(f'{HOME}/Library/Python/2.7/bin')

    _add_path_if_exists(f'{HOME}/google-cloud-sdk/bin')
    _add_path_if_exists(f'{HOME}/google-cloud-sdk/platform/google_appengine')
    # TODO: gcloud completion

    _add_path_if_exists(f'{HOME}/bin')
    _add_path_if_exists(f'{HOME}/dotfiles/bin')

__add_paths()

def _set_gitalias():
    aliases["gt"] = ["git", "status"]
    aliases["commit"] = ["git", "commit", "-v"]
    aliases["add"] = ["git", "add"]
    aliases["push"] = ["git", "push"]
    aliases["pull"] = ["git", "pull"]
_set_gitalias()


def _xonsh_config():
    ENV["VI_MODE"] = True
    # 補完中に Enter を押すと決定のみ
    ENV["COMPLETIONS_CONFIRM"] = True
    # ディレクトリ名を入力すればcdできる
    ENV["AUTO_CD"] = True

_xonsh_config()

def __edit_cheatsheets():
    cd ~/mycheatsheets/
    run("git pull origin master")
    name = $(ls | peco).strip()
    vim @(name)
    run("git add -A")
    run("git commit -m \"at (uname -s)\"")
    run("git push origin master")
    cd -
aliases["ec"] = __edit_cheatsheets

def __bookmark():
    name = $(cat ~/bookmark | peco).strip()
    cd @(name)
aliases["bk"] = __bookmark


def _gcloud_config():
    paths = [
        "/usr/local/bin/python2.7",
        "/usr/local/bin/python2",
        "/usr/local/bin/python",
        "/usr/bin/python2.7",
        "/usr/bin/python2",
        "/usr/bin/python",
    ]
    for path in paths:
        if os.path.exists(path):
            ENV["CLOUDSDK_PYTHON"] = path
        return
_gcloud_config()

# https://qiita.com/riktor/items/4a90b4e125cd091a9d07
def _get_history(session_history=None, return_list=False):
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
    # dedupe
    zip_with_dummy = list(zip(cmds, [0] * len(cmds)))[::-1]
    cmds = list(OrderedDict(zip_with_dummy).keys())[::-1]
    if return_list:
        return cmds
    else:
        return '\n'.join(cmds)


@events.on_ptk_create
def custom_keybindings(bindings, **kw):
    handler = bindings.add
    insert_mode = ViInsertMode()

    @handler(Keys.ControlW)
    def ctrl_w(event):
        buf = event.current_buffer # type: prompt_toolkit.buffer.Buffer
        text = buf.text[:buf.cursor_position] # type:str
        m = re.search("[/\s][^/\s]+[/\s]?$", text)
        if m is not None:
            buf.delete_before_cursor(len(text) - m.start() - 1)
            return
        buf.delete_before_cursor(len(text))

    @handler(Keys.ControlK)
    def ctrl_k(event):
        buf = event.current_buffer # type: prompt_toolkit.buffer.Buffer
        buf.apply_completion()

    @handler(Keys.ControlR, filter=insert_mode)
    def select_history(event):
        sess_history = $(history).split('\n')
        hist = _get_history(sess_history)
        selected = $(echo @(hist) | peco)
        event.current_buffer.insert_text(selected.strip())

# vim: expandtab ts=4 sw=4 :
