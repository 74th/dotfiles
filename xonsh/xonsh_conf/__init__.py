# -*- coding: utf-8 -*-
import os
import re
import json
import tempfile
import builtins
import invoke
from . import git
from collections import OrderedDict
from operator import itemgetter
import prompt_toolkit
from .lib import HOSTNAME, run, silent_run
from .xonsh_builtin import x_env, x_aliases, x_events, x_exitcode,x_completers
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition, ViInsertMode
from .gitstatus import gitstatus_prompt
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


def _default_charsets():
    '''
    文字コードの標準設定
    '''
    x_env["LESSCHARSET"] = "UTF-8"
    x_env["LANG"] = "en_US.UTF-8"
    x_env["LC_CTYPE"] = "en_US.UTF-8"
    x_env["LC_ALL"] = "en_US.UTF-8"


def __add_paths():
    if '/usr/local/bin' not in paths:
        # 追加されてなかった時用
        _add_path_if_exists('/usr/local/bin')
    if '/usr/local/sbin' not in paths:
        _add_path_if_exists('/usr/local/sbin')
    _add_path_if_exists('/usr/local/cuda/bin')
    _add_path_if_exists(f'{HOME}/npm/bin')
    _add_path_if_exists(f'{HOME}/npm/node_modules/.bin')
    _add_path_if_exists(f'{HOME}/Library/Android/sdk/platform-tools')
    _add_path_if_exists(f'{HOME}/.rbx_env/shims')
    _add_path_if_exists(f'{HOME}/.pyenv/shims')
    _add_path_if_exists(f'{HOME}/go/bin')
    _add_path_if_exists(f'{HOME}/dotfiles/bin/darwin')
    _add_path_if_exists(f'{HOME}/go/src/github.com/uber/go-torch/FlameGraph')
    _add_path_if_exists(f'/home/linuxbrew/.linuxbrew/bin')
    _add_path_if_exists('/opt/X11/bin')
    _add_path_if_exists('/usr/local/share/dotnet')
    _add_path_if_exists('/Library/Frameworks/Mono.framework/Versions/Current/Commands')
    _add_path_if_exists('/Library/TeX/texbin')
    _add_path_if_exists('/Applications/MacVim.app/Contents/bin')
    if os.path.exists(f'{HOME}/Library/Python/2.7/bin'):
        x_env["PATH"].append(f'{HOME}/Library/Python/2.7/bin')
    if os.path.exists(f'{HOME}/Library/Python/3.7/bin'):
        x_env["PATH"].append(f'{HOME}/Library/Python/3.7/bin')

    _add_path_if_exists(f'{HOME}/google-cloud-sdk/bin')
    _add_path_if_exists(f'{HOME}/google-cloud-sdk/platform/google_appengine')

    # TODO: gcloud completion

    _add_path_if_exists(f'{HOME}/bin')
    _add_path_if_exists(f'{HOME}/dotfiles/bin')


def _set_git_alias():
    x_aliases["gt"] = ["git", "status"]
    x_aliases["commit"] = ["git", "commit", "-v"]
    x_aliases["add"] = ["git", "add"]
    x_aliases["push"] = ["git", "push"]
    x_aliases["pull"] = ["git", "pull"]

def _set_kubenetes_alias():
    x_aliases["k"] = ["kubectl"]
    x_aliases["kube-get-pods"] = ["kubectl", "get", "pods", "--sort-by=.metadata.creationTimestamp"]

def _set_xonsh_alias():
    x_aliases["gt"] = ["git", "status"]

def _xonsh_alias():
    x_aliases["xssh"] = ["ssh", "-t", "-c", "xonsh"]


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


def __bookmark():
    name = run("cat ~/bookmark | peco").lines[0].strip()
    run(f"cd {name}")


def __add_bookmark():
    run(f"pwd >> ~/bookmark")


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


def _set_syntax_sugar():
    x_aliases["al"] = ["ls", "-al"]
    x_aliases["la"] = ["ls", "-al"]
    x_aliases["ll"] = ["ls", "-al"]
    x_aliases["lt"] = ["ls", "-alt"]


def _set_java_alias():
    x_aliases['javac'] = ['javac', '-J-Dfile.encoding=utf-8']
    x_aliases['java'] = ['java', '-Dfile.encoding=UTF-8']


def _new_uuid():
    import uuid
    print(uuid.uuid1())


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


def set_keybind():
    @x_events.on_ptk_create
    def __custom_keybindings(bindings, **kw):
        handler = bindings.add
        insert_mode = ViInsertMode()

        @handler(Keys.ControlW)
        def __ctrl_w(event):
            buf = event.current_buffer  # type: prompt_toolkit.buffer.Buffer
            text = buf.text[:buf.cursor_position]  # type: str
            m = re.search(r"[/,.=\-\s][^/,.=\-\s]+[/,.=\-\s]?$", text)
            if m is not None:
                buf.delete_before_cursor(len(text) - m.start() - 1)
                return
            buf.delete_before_cursor(len(text))

        @handler(Keys.ControlK)
        def __ctrl_k(event):
            if event.current_buffer.suggestion:
                event.current_buffer.insert_text(event.current_buffer.suggestion.text)

        @handler(Keys.ControlR, filter=insert_mode)
        def __ctrl_r_event(event):
            ctrl_r.select(event.current_buffer)

def invoke_completer(prefix:str, line:str, begidx:int, endidx:int, ctx:dict):
    if not line.startswith("inv"):
        return set()
    args = line.split(" ")
    if len(args)>1 and args[-2] == "-f":
        from xonsh.completers.path import complete_path
        return complete_path(prefix, line, begidx, endidx, ctx)
    tasks = silent_run("/usr/local/bin/invoke --complete")
    return set(tasks.split("\n"))

def set_inv_completer():
    x_completers["inv"] = invoke_completer
    x_completers.move_to_end("inv", False)
    pass

def load_xontrib():
    run("xontrib load coreutils docker_tabcomplete jedi z readable-traceback")
    run("xontrib load direnv")


def load():
    from .prompt import set_prompt
    set_prompt()

    _default_charsets()

    __add_paths()
    load_xontrib()
    _xonsh_config()
    x_aliases["ec"] = __edit_cheatsheets
    x_aliases["bk"] = __bookmark
    x_aliases["AddBookmark"] = __add_bookmark
    x_aliases["cb"] = __command_bookmark

    _gcloud_config()

    _set_syntax_sugar()
    _set_git_alias()
    _set_kubenetes_alias()
    _set_java_alias()
    x_aliases["uuid"] = _new_uuid
    set_keybind()
    set_inv_completer()

    git.set_aliases()
