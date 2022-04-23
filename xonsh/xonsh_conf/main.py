# -*- coding: utf-8 -*-
import os
import os.path
import re
import json
try:
    import invoke
    from . import git
    from collections import OrderedDict
    from operator import itemgetter
    import prompt_toolkit
    from .lib import HOSTNAME, run, silent_run
    from .xonsh_builtin import x_env, x_aliases, x_events, x_completers
    from prompt_toolkit.keys import Keys
    from prompt_toolkit.filters import ViInsertMode
    from .commands import load_commands
    from .path import get_paths
    from .aliases import get_aliases
    from .env import apply_envs
    from . import ctrl_r
except ModuleNotFoundError:
    from .xonsh_builtin import x_execer
    command = "xpip install invoke prompt_toolkit detect pyyaml xonsh-direnv"
    print(command)
    x_execer.eval(f"$({command})")
    command = "xpip uninstall pyperclip"
    print(command)
    raise Exception("restart")


# from .detect_user_docker import detect_user_docker_for_xonsh

x_env["XONSH_SHOW_TRACEBACK"] = True

c = invoke.Context({"run": {"echo": True, "warn": True, "hide": False}})

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
    """
    文字コードの標準設定
    """
    x_env["LESSCHARSET"] = "UTF-8"
    x_env["LANG"] = "en_US.UTF-8"
    x_env["LC_CTYPE"] = "en_US.UTF-8"
    x_env["LC_ALL"] = "en_US.UTF-8"


def __add_paths():
    default_paths = x_env["PATH"]
    x_env["PATH"] = get_paths(default_paths) + default_paths


def __set_aliases():
    for alias, cmd in get_aliases(human=True).items():
        x_aliases[alias] = cmd


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


def _new_uuid():
    import uuid

    print(uuid.uuid1())


def _get_history(session_history=None, return_list=False):
    """
    https://qiita.com/riktor/items/4a90b4e125cd091a9d07
    TODO: 時々お掃除いる？
    """
    hist_dir = x_env["XONSH_DATA_DIR"]
    files = [
        os.path.join(hist_dir, f)
        for f in os.listdir(hist_dir)
        if f.startswith("xonsh-") and f.endswith(".json")
    ]
    file_hist = [json.load(open(f))["data"]["cmds"] for f in files]
    cmds = [
        (c["inp"].replace("\n", ""), c["ts"][0])
        for cmds in file_hist
        for c in cmds
        if c
    ]
    cmds.sort(key=itemgetter(1))
    cmds = [c[0] for c in cmds[::-1]]
    if session_history:
        cmds.extend(session_history)
    zip_with_dummy = list(zip(cmds, [0] * len(cmds)))[::-1]
    cmds = list(OrderedDict(zip_with_dummy).keys())[::-1]
    if return_list:
        return cmds
    else:
        return "\n".join(cmds)


def set_keybind():
    @x_events.on_ptk_create
    def __custom_keybindings(bindings, **kw):
        handler = bindings.add
        insert_mode = ViInsertMode()

        @handler(Keys.ControlW)
        def __ctrl_w(event):
            buf = event.current_buffer  # type: prompt_toolkit.buffer.Buffer
            text = buf.text[: buf.cursor_position]  # type: str
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


def invoke_completer(prefix: str, line: str, begidx: int, endidx: int, ctx: dict):
    if not line.startswith("inv"):
        return set()
    args = line.split(" ")
    if len(args) > 1 and args[-2] == "-f":
        from xonsh.completers.path import complete_path

        return complete_path(prefix, line, begidx, endidx, ctx)
    tasks = silent_run("invoke --complete")
    return set(tasks.split("\n"))


def set_inv_completer():
    x_completers["inv"] = invoke_completer
    x_completers.move_to_end("inv", False)
    pass


def load_xontrib():
    # run("xontrib load coreutils readable-traceback")
    run("xontrib load direnv")


def add_bash_competion():
    if os.path.exists("/home/linujxbrew/.linuxbrew/etc/bash_completion.d"):
        x_env["BASH_COMPLETIONS"] = "/home/linuxbrew/.linuxbrew/etc/bash_completion.d"


def launch_ssh_agent():
    if HOSTNAME not in ["violet-gopher"]:
        return
    sock = os.environ.get("XDG_RUNTIME_DIR", "/run/user/1000") + "/keyring/.ssh"
    if os.path.exists(sock):
        return
    silent_run(f"ssh-agent -a {sock}")


def load():
    from .prompt import set_prompt

    launch_ssh_agent()

    __add_paths()
    set_prompt()

    _default_charsets()

    load_xontrib()

    _gcloud_config()

    __set_aliases()
    load_commands()
    x_aliases["uuid"] = _new_uuid
    set_keybind()
    set_inv_completer()
    apply_envs()

    x_env["VI_MODE"] = True
    if "PYENV_VERSION" in x_env:
        del x_env["PYENV_VERSION"]

    git.set_aliases()

    # detect_user_docker_for_xonsh()

    add_bash_competion()

    x_env["NNYN_DOTFILES_LOADED"] = "1"
