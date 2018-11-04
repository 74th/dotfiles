# -*- coding: utf-8 -*-
import os
import re
import json
import tempfile
import builtins
import invoke
from collections import OrderedDict
from operator import itemgetter
import prompt_toolkit
from .lib import HOSTNAME, run, silent_run
from .xonsh_builtin import x_env, x_aliases, x_events
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition, ViInsertMode
from . import ctrl_r

x_env["XONSH_SHOW_TRACEBACK"] = True

c = invoke.Context({
    "run": {
        "echo": True,
        "warn": True,
        "hide": False,
    }
})

paths = x_env["PATH"]


def _add_path_if_exists(path: str, if_path: str = None):
    if if_path:
        exist = os.path.exists(if_path)
    else:
        exist = os.path.exists(path)
    if exist:
        paths.insert(0, path)


HOME = x_env["HOME"]


def _set_prompt():

    prompt = ""

    # user
    root = False
    if x_env.get("USER", "nnyn") == "root":
        root = True
        prompt += "{RED}"
    else:
        prompt += "{GREEN}"
    prompt += "{user}{WHITE}@"

    if HOSTNAME in ["nagisa", "methyl", "mini", "patty"]:
        prompt += "{CYAN}"
    elif HOSTNAME in ["mbp"]:
        prompt += "{YELLOW}"
    else:
        prompt += "{WHITE}"
    prompt += "{hostname}"

    prompt += " "

    prompt += "{cwd}{branch_color}{curr_branch: {}}{NO_COLOR}\n$"

    x_env["PROMPT"] = prompt


_set_prompt()


def _default_charsets():
    '''
    文字コードの標準設定
    '''
    x_env["LESSCHARSET"] = "UTF-8"
    x_env["LANG"] = "en_US.UTF-8"
    x_env["LC_CTYPE"] = "en_US.UTF-8"
    x_env["LC_ALL"] = "en_US.UTF-8"


_default_charsets()


def __add_paths():
    if '/usr/local/bin' not in paths:
        # 追加されてなかった時用
        _add_path_if_exists('/usr/local/bin')
    if '/usr/local/sbin' not in paths:
        _add_path_if_exists('/usr/local/sbin')
    _add_path_if_exists('/usr/local/cuda/bin')
    _add_path_if_exists(f'{HOME}/npm/bin')
    _add_path_if_exists(f'{HOME}/Library/Android/sdk/platform-tools')
    _add_path_if_exists(f'{HOME}/.rbx_env/shims')
    _add_path_if_exists(f'{HOME}/.pyenv/shims')
    _add_path_if_exists(f'{HOME}/go/bin')
    _add_path_if_exists(f'{HOME}/dotfiles/bin/darwin')
    _add_path_if_exists(f'{HOME}/go/src/github.com/uber/go-torch/FlameGraph')
    _add_path_if_exists('/opt/X11/bin')
    _add_path_if_exists('/usr/local/share/dotnet')
    _add_path_if_exists('/Library/Frameworks/Mono.framework/Versions/Current/Commands')
    _add_path_if_exists('/Library/TeX/texbin')
    if os.path.exists(f'{HOME}/Library/Python/2.7/bin'):
        x_env["PATH"].append(f'{HOME}/Library/Python/2.7/bin')
    if os.path.exists(f'{HOME}/Library/Python/3.7/bin'):
        x_env["PATH"].append(f'{HOME}/Library/Python/3.7/bin')

    _add_path_if_exists(f'{HOME}/google-cloud-sdk/bin')
    _add_path_if_exists(f'{HOME}/google-cloud-sdk/platform/google_appengine')

    # TODO: gcloud completion

    _add_path_if_exists(f'{HOME}/bin')
    _add_path_if_exists(f'{HOME}/dotfiles/bin')


__add_paths()


def _set_gitalias():
    x_aliases["gt"] = ["git", "status"]
    x_aliases["commit"] = ["git", "commit", "-v"]
    x_aliases["add"] = ["git", "add"]
    x_aliases["push"] = ["git", "push"]
    x_aliases["pull"] = ["git", "pull"]


_set_gitalias()


def _xonsh_config():
    x_env["VI_MODE"] = True
    # 補完中に Enter を押すと決定のみ
    x_env["COMPLETIONS_CONFIRM"] = True
    # ディレクトリ名を入力すればcdできる
    x_env["AUTO_CD"] = True


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


x_aliases["ec"] = __edit_cheatsheets


def __bookmark():
    name = run("cat ~/bookmark | peco").lines[0].strip()
    run(f"cd {name}")


x_aliases["bk"] = __bookmark


def __command_bookmark():
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


x_aliases["cb"] = __command_bookmark


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
            x_env["CLOUDSDK_PYTHON"] = path
        return


_gcloud_config()


def _add_syntax_sugar():
    x_aliases["al"] = ["ls", "-al"]
    x_aliases["la"] = ["ls", "-al"]
    x_aliases["ll"] = ["ls", "-al"]
    x_aliases["lt"] = ["ls", "-alt"]


_add_syntax_sugar()


def _new_uuid():
    import uuid
    print(uuid.uuid1())


x_aliases["uuid"] = _new_uuid


def _get_history(session_history=None, return_list=False):
    '''
    https://qiita.com/riktor/items/4a90b4e125cd091a9d07
    TODO: 時々お掃除いる？
    '''
    hist_dir = x_env['XONSH_DATA_DIR']
    files = [os.path.join(hist_dir, f) for f in os.listdir(hist_dir) if f.startswith('xonsh-') and f.endswith('.json')]
    file_hist = [json.load(open(f))['data']['cmds'] for f in files]
    cmds = [(c['inp'].replace('\n', ''), c['ts'][0]) for cmds in file_hist for c in cmds if c]
    cmds.sort(key=itemgetter(1))
    cmds = [c[0] for c in cmds[::-1]]
    if session_history:
        cmds.extend(session_history)
    zip_with_dummy = list(zip(cmds, [0] * len(cmds)))[::-1]
    cmds = list(OrderedDict(zip_with_dummy).keys())[::-1]
    if return_list:
        return cmds
    else:
        return '\n'.join(cmds)


@x_events.on_ptk_create
def custom_keybindings(bindings, **kw):
    handler = bindings.add
    insert_mode = ViInsertMode()

    @handler(Keys.ControlW)
    def ctrl_w(event):
        buf = event.current_buffer  # type: prompt_toolkit.buffer.Buffer
        text = buf.text[:buf.cursor_position]  # type: str
        m = re.search(r"[/,.\s][^/,.\s]+[/,.\s]?$", text)
        if m is not None:
            buf.delete_before_cursor(len(text) - m.start() - 1)
            return
        buf.delete_before_cursor(len(text))

    @handler(Keys.ControlK)
    def ctrl_k(event):
        if event.current_buffer.suggestion:
            event.current_buffer.insert_text(event.current_buffer.suggestion.text)

    @handler(Keys.ControlR, filter=insert_mode)
    def ctrl_r_event(event):
        ctrl_r.select(event.current_buffer)


#run("xontrib load autoxsh bashisms coreutils distributed docker_tabcomplete jedi mpl prompt_ret_code free_cwd scrapy_tabcomplete vox vox_tabcomplete xo xonda z")
run("xontrib load autoxsh bashisms coreutils distributed docker_tabcomplete jedi mpl prompt_ret_code free_cwd vox xo xonda z")
