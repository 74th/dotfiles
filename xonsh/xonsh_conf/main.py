# -*- coding: utf-8 -*-
import os
from typing import cast
import os.path
import re

try:
    from . import git
    from .lib import HOSTNAME, x_run, silent_run, PTKBuffer
    from .xonsh_builtin import x_env, x_aliases, x_events, x_completers
    from xonsh.tools import register_custom_style
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

paths = x_env["PATH"]


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
    default_paths = cast(list[str], x_env["PATH"])
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


def set_keybind():
    @x_events.on_ptk_create
    def __custom_keybindings(bindings, **kw):
        handler = bindings.add
        insert_mode = ViInsertMode()

        @handler(Keys.ControlW)
        def __ctrl_w(event):
            buf = cast(PTKBuffer, event.current_buffer)
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


def load_xontrib():
    x_run("xontrib load direnv")


def color():
    mystyle = {
        "Token.PTK.CompletionMenu.Completion": "#0F0F0F",
    }
    register_custom_style("my", mystyle, base="default")
    x_env["XONSH_COLOR_STYLE"] = "my"


def add_bash_competion():
    if os.path.exists("/home/linujxbrew/.linuxbrew/etc/bash_completion.d"):
        x_env["BASH_COMPLETIONS"] = "/home/linuxbrew/.linuxbrew/etc/bash_completion.d"


def launch_ssh_agent():
    if HOSTNAME not in ["crow"]:
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

    color()

    _gcloud_config()

    __set_aliases()
    load_commands()
    x_aliases["uuid"] = _new_uuid
    set_keybind()
    apply_envs()

    x_env["VI_MODE"] = True
    if "PYENV_VERSION" in x_env:
        del x_env["PYENV_VERSION"]

    git.set_aliases()

    # detect_user_docker_for_xonsh()

    add_bash_competion()

    x_env["NNYN_DOTFILES_LOADED"] = "1"
    # load_xontrib()
    x_run(
        f"source /{HOME}/ghq/github.com/74th/dotfiles/xonsh/xonsh_conf/xonsh-direnv.xsh"
    )
