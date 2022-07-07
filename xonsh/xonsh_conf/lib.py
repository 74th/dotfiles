# -*- coding: utf-8 -*-
import os
import subprocess
from xonsh.procs.pipelines import HiddenCommandPipeline
from .xonsh_builtin import x_execer, x_env


def run(command: str) -> str:
    pwd = x_env["PWD"]
    r = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=pwd)
    return r.stdout.strip()


def peco(input: str) -> str:
    r = subprocess.run("peco", shell=True, capture_output=True, text=True, input=input)
    return r.stdout.strip()


def x_run(command: str) -> HiddenCommandPipeline:
    return x_execer.eval(command)


def silent_run(command: str) -> str:
    # return invoke.run(command, warn=True, hide=True).stdout.strip()
    return x_execer.eval(f"$({command})")


HOSTNAME = os.uname().nodename
HOME = x_env["HOME"]
