# -*- coding: utf-8 -*-
import invoke
import os
from xonsh.procs.pipelines import HiddenCommandPipeline
from .xonsh_builtin import x_execer, x_env


def run(command: str) -> HiddenCommandPipeline:
    return x_execer.eval(command)


def silent_run(command: str) -> str:
    return invoke.run(command, warn=True, hide=True).stdout.strip()


HOSTNAME = os.uname().nodename
HOME = x_env["HOME"]
