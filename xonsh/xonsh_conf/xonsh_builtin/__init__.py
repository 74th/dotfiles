# -*- coding: utf-8 -*-
import builtins
import xonsh

x_env: xonsh.environ.Env = builtins.__xonsh_env__
x_execer: xonsh.execer.Execer = builtins.__xonsh_execer__
x_aliases: xonsh.aliases.Aliases = builtins.aliases
x_events: xonsh.events.EventManager = builtins.events
