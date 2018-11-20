# -*- coding: utf-8 -*-
import builtins
import xonsh

x_env: xonsh.environ.Env = builtins.__xonsh__.env
x_execer: xonsh.execer.Execer = builtins.__xonsh__.execer
x_aliases: xonsh.aliases.Aliases = builtins.aliases
x_events: xonsh.events.EventManager = builtins.events

def x_exitcode():
    if builtins.__xonsh__.history.rtns is None:
        return 0
    if len(builtins.__xonsh__.history.rtns) > 0:
        return builtins.__xonsh__.history.rtns[-1]
    return 0
