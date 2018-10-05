# -*- coding: utf-8 -*-
import os
import re
import json
import tempfile
import builtins
import invoke as _invoke
from collections import OrderedDict
from operator import itemgetter
import prompt_toolkit
from xonsh.environ import Env
from xonsh.execer import Execer
from xonsh.proc import HiddenCommandPipeline
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition, ViInsertMode

ENV = builtins.__xonsh_env__  # type: Env
ENV["XONSH_SHOW_TRACEBACK"] = True

execer = builtins.__xonsh_execer__ # type: Execer

def silent_run(command: str) -> str:
    return _invoke.run(command, warn=True, hide=True).stdout.strip()

def run(command: str)->HiddenCommandPipeline:
    return execer.eval(command)


c = _invoke.Context({
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
    _add_path_if_exists(f'{HOME}/npm/bin')
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
        ENV["PATH"].append(f'{HOME}/Library/Python/2.7/bin')
    if os.path.exists(f'{HOME}/Library/Python/3.7/bin'):
        ENV["PATH"].append(f'{HOME}/Library/Python/3.7/bin')

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
    d = run("pwd").lines[0].strip()
    run("cd ~/mycheatsheets/")
    run("git pull origin master")
    name = run("ls | peco").lines[0].strip()
    run(f"vim {name}")
    run("git add -A")
    run("git commit -m \"at (uname -s)\"")
    run("git push origin master")
    run(f"cd {d}")
aliases["ec"] = __edit_cheatsheets

def __bookmark():
    name = run("cat ~/bookmark | peco").lines[0].strip()
    run(f"cd {name}")
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

def _add_syntax_suger():
    aliases["al"] = ["ls", "-al"]
    aliases["ll"] = ["ls", "-al"]
_add_syntax_suger()

def _new_uuid():
    import uuid
    print(uuid.uuid1())
aliases["uuid"] = _new_uuid

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
        if event.current_buffer.suggestion:
            event.current_buffer.insert_text(event.current_buffer.suggestion.text)

    @handler(Keys.ControlR, filter=insert_mode)
    def select_history(event):
        sess_history = run("history").lines
        sess_history = [h.strip() for h in sess_history]
        hist = _get_history(sess_history)
        with tempfile.NamedTemporaryFile() as tmp:
            with open(tmp.name,"w") as f:
                f.write(hist)
            selected = run(f"cat {tmp.name} | peco").lines[0].strip()
        event.current_buffer.insert_text(selected)

xontrib load autoxsh bashisms coreutils distributed docker_tabcomplete jedi mpl prompt_ret_code free_cwd scrapy_tabcomplete vox vox_tabcomplete xo xonda z
#xontrib load autoxsh bashisms coreutils distributed docker_tabcomplete jedi mpl prompt_ret_code free_cwd scrapy_tabcomplete vox vox_tabcomplete xo xonda avox z powerline prompt_vi_mode click_tabcomplete

# vim: expandtab ts=4 sw=4 :
