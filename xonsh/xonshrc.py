def __append_xonshrc_path():
    import sys
    import builtins
    from os import path
    ENV = builtins.__xonsh_env__
    xonsh_conf = path.join(ENV["HOME"],"dotfiles","xonsh")
    sys.path.append(xonsh_conf)

__append_xonshrc_path()

import xonsh_conf
