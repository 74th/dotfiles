# type: ignore
import os
def __append_xonshrc_path():
    import sys

    xonsh_conf = os.path.join(os.environ["HOME"], "dotfiles", "xonsh")
    sys.path.append(xonsh_conf)


__append_xonshrc_path()

import xonsh_conf

xonsh_conf.load()

machine_xonsh = os.path.join(os.environ["HOME"], ".xonshrc-machine")
if os.path.exists(machine_xonsh):
    source @(machine_xonsh)
