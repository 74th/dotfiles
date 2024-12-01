# type: ignore
import os
import warnings


def __append_xonshrc_path():
    import sys

    xonsh_conf = os.path.join(
        os.environ["HOME"], "ghq", "github.com", "74th", "dotfiles", "xonsh"
    )
    sys.path.append(xonsh_conf)


__append_xonshrc_path()

import xonsh_conf

xonsh_conf.load()

machine_xonsh = os.path.join(os.environ["HOME"], ".xonshrc-machine")
if os.path.exists(machine_xonsh):
    source @ (machine_xonsh)

warnings.filterwarnings(
    "ignore",
    message="There is no current event loop",
    category=DeprecationWarning,
    # module='prompt_toolkit',
)
