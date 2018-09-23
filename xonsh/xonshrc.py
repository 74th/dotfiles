# -*- coding: utf-8 -*-
import os
import re
import builtins
import invoke
import prompt_toolkit
from xonsh.environ import Env
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition, ViInsertMode

env = builtins.__xonsh_env__  # type: Env
env["XONSH_SHOW_TRACEBACK"] = True


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


paths = env["PATH"]


def _add_path_if_exists(path: str, if_path: str = None):
    if if_path:
        exist = os.path.exists(if_path)
    else:
        exist = os.path.exists(path)
    if exist:
        paths.insert(0, path)


HOME = env["HOME"]


def _set_prompt():

    prompt = ""

    # user
    root = False
    if "USER" in env and env["USER"] == "root":
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

    prompt += "{cwd}{branch_color}{curr_branch: {}}{NO_COLOR} {cwd_dir}\n$"

    env["PROMPT"] = prompt


_set_prompt()


def _default_charsets():
    '''
    文字コードの標準設定
    '''
    env["LESSCHARSET"] = "UTF-8"
    env["LANG"] = "en_US.UTF-8"
    env["LC_CTYPE"] = "en_US.UTF-8"
    env["LC_ALL"] = "en_US.UTF-8"
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
        env["PATH"].append(f'{HOME}/Library/Python/2.7/bin')

    _add_path_if_exists(f'{HOME}/google-cloud-sdk/bin')
    _add_path_if_exists(f'{HOME}/google-cloud-sdk/platform/google_appengine')
    # TODO: gcloud completion

    _add_path_if_exists(f'{HOME}/bin')
    _add_path_if_exists(f'{HOME}/dotfiles/bin')

__add_paths()


def _xonsh_config():
    env["VI_MODE"] = True
    # 補完中に Enter を押すと決定のみ
    env["COMPLETIONS_CONFIRM"] = True
    # ディレクトリ名を入力すればcdできる
    env["AUTO_CD"] = True

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


@events.on_ptk_create
def custom_keybindings(bindings, **kw):
    handler = bindings.add

    @handler(Keys.ControlW)
    def ctrl_w(event):
        buf = event.current_buffer # type: prompt_toolkit.buffer.Buffer
        text = buf.text[:buf.cursor_position] # type:str
        m = re.search("[/\s][^/\s]+[/\s]?$", text)
        if m is not None:
            buf.delete_before_cursor(len(text) - m.start() - 1)
            return
        buf.delete_before_cursor(len(text))


# vim: expandtab ts=4 sw=4 :
