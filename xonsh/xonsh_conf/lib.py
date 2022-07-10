# -*- coding: utf-8 -*-
from abc import ABCMeta
import os
import subprocess
from typing import cast
from .xonsh_builtin import x_execer, x_env


class PTKDocument(ABCMeta):
    current_line: str


class PTKBuffer(ABCMeta):
    text: str
    document: PTKDocument
    cursor_position: int

    def delete_before_cursor(self, n: int = 1):
        pass

    def reset(self):
        pass

    def insert_text(self, text: str):
        pass


def run(command: str) -> str:
    pwd = x_env["PWD"]
    r = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=pwd)
    return r.stdout.strip()


def peco(input: str) -> str:
    r = subprocess.run("peco", shell=True, capture_output=True, text=True, input=input)
    return r.stdout.strip()


def x_run(command: str):
    return x_execer.eval(command)


def silent_run(command: str) -> str:
    pwd = x_env["PWD"]
    r = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True, cwd=pwd)
    return r.stdout


HOSTNAME = os.uname().nodename
HOME = cast(str, x_env["HOME"])
