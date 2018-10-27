def __append_xonshrc_path():
    import sys
    import os
    xonsh_conf = os.path.join(os.environ["HOME"], "dotfiles", "xonsh")
    sys.path.append(xonsh_conf)


__append_xonshrc_path()

import xonsh_conf
