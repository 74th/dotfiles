# type: ignore
from collections import OrderedDict
import builtins
import xonsh

x_env: xonsh.environ.Env = builtins.__xonsh__.env
x_execer: xonsh.execer.Execer = builtins.__xonsh__.execer
x_aliases: xonsh.aliases.Aliases = builtins.aliases
x_events: xonsh.events.EventManager = builtins.events
__xonsh__: xonsh.built_ins.XonshSession = builtins.__xonsh__
x_session: xonsh.built_ins.XonshSession = builtins.__xonsh__
x_completers: OrderedDict = builtins.__xonsh__.completers


def x_exitcode():
    if builtins.__xonsh__.history.rtns is None:
        return 0
    if len(builtins.__xonsh__.history.rtns) > 0:
        return builtins.__xonsh__.history.rtns[-1]
    return 0
