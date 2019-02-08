# -*- coding: utf-8 -*-
# copy from https://github.com/xonsh/xonsh/blob/master/xonsh/prompt/gitstatus.py
"""Informative git status prompt formatter"""

from . import xonsh_builtin
import collections
import os
import subprocess

import xonsh.lazyasd as xl

GitStatus = collections.namedtuple(
    "GitStatus",
    [
        "branch",
        "num_ahead",
        "num_behind",
        "untracked",
        "changed",
        "conflicts",
        "staged",
        "stashed",
        "operations",
    ],
)


def _check_output(*args, **kwargs):
    kwargs.update(
        dict(
            env=xonsh_builtin.__xonsh__.env.detype(),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
        ))
    timeout = xonsh_builtin.__xonsh__.env["VC_BRANCH_TIMEOUT"]
    # See https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate
    with subprocess.Popen(*args, **kwargs) as proc:
        try:
            out, err = proc.communicate(timeout=timeout)
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(
                    proc.returncode, proc.args, output=out,
                    stderr=err)  # note err will always be empty as we redirect stderr to DEVNULL abvoe
            return out
        except subprocess.TimeoutExpired:
            # We use `.terminate()` (SIGTERM) instead of `.kill()` (SIGKILL) here
            # because otherwise we guarantee that a `.git/index.lock` file will be
            # left over, and subsequent git operations will fail.
            # We don't want that.
            # As a result, we must rely on git to exit properly on SIGTERM.
            proc.terminate()
            # We wait() to ensure that git has finished before the next
            # `gitstatus` prompt is rendered (otherwise `index.lock` still exists,
            # and it will fail).
            # We don't technically have to call `wait()` here as the
            # `with subprocess.Popen()` context manager above would do that
            # for us, but we do it to be explicit that waiting is being done.
            proc.wait()  # we ignore what git says after we sent it SIGTERM
            raise


def _get_tag_or_hash():
    tag_or_hash = _check_output(["git", "describe", "--always"]).strip()
    hash_ = _check_output(["git", "rev-parse", "--short", "HEAD"]).strip()
    have_tag_name = tag_or_hash != hash_
    return tag_or_hash if have_tag_name else _get_def("HASH") + hash_


def _get_stash(gitdir):
    try:
        with open(os.path.join(gitdir, "logs/refs/stash")) as f:
            return sum(1 for _ in f)
    except IOError:
        return 0


def _gitoperation(gitdir):
    files = (
        ("rebase-merge", "REBASE"),
        ("rebase-apply", "AM/REBASE"),
        ("MERGE_HEAD", "MERGING"),
        ("CHERRY_PICK_HEAD", "CHERRY-PICKING"),
        ("REVERT_HEAD", "REVERTING"),
        ("BISECT_LOG", "BISECTING"),
    )
    return [f[1] for f in files if os.path.exists(os.path.join(gitdir, f[0]))]


def gitstatus():
    """Return namedtuple with fields:
    branch name, number of ahead commit, number of behind commit,
    untracked number, changed number, conflicts number,
    staged number, stashed number, operation."""
    status = _check_output(["git", "status", "--porcelain", "--branch"])
    branch = ""
    num_ahead, num_behind = 0, 0
    untracked, changed, conflicts, staged = 0, 0, 0, 0
    for line in status.splitlines():
        if line.startswith("##"):
            line = line[2:].strip()
            if "Initial commit on" in line:
                branch = line.split()[-1]
            elif "no branch" in line:
                branch = _get_tag_or_hash()
            elif "..." not in line:
                branch = line
            else:
                branch, rest = line.split("...")
                if " " in rest:
                    divergence = rest.split(" ", 1)[-1]
                    divergence = divergence.strip("[]")
                    for div in divergence.split(", "):
                        if "ahead" in div:
                            num_ahead = int(div[len("ahead "):].strip())
                        elif "behind" in div:
                            num_behind = int(div[len("behind "):].strip())
        elif line.startswith("??"):
            untracked += 1
        else:
            if len(line) > 1 and line[1] == "M":
                changed += 1

            if len(line) > 0 and line[0] == "U":
                conflicts += 1
            elif len(line) > 0 and line[0] != " ":
                staged += 1

    gitdir = _check_output(["git", "rev-parse", "--git-dir"]).strip()
    stashed = _get_stash(gitdir)
    operations = _gitoperation(gitdir)

    return GitStatus(
        branch,
        num_ahead,
        num_behind,
        untracked,
        changed,
        conflicts,
        staged,
        stashed,
        operations,
    )


def gitstatus_prompt():
    """Return str `BRANCH|OPERATOR|numbers`"""
    try:
        s = gitstatus()
    except subprocess.SubprocessError:
        return None

    ret = "{YELLOW}" + s.branch
    if s.branch == "master":
        ret += "🌟"
    if s.num_ahead > 0:
        ret += "{GREEN}>" + str(s.num_ahead)
    if s.num_behind > 0:
        ret +='{RED}<'  + str(s.num_behind)
    if s.operations:
        ret += "{CYAN}" + "|" + "|".join(s.operations)
    ret += " "
    if s.staged > 0:
        ret += "{GREEN}" + str(s.staged) + "{NO_COLOR}"
    if s.conflicts > 1:
        ret += "{BOLD_RED}" + str(s.conflicts) + "{NO_COLOR}"
    if s.changed > 0:
        ret += "{RED}+" + str(s.changed) + "{NO_COLOR}"
    if s.untracked > 0:
        ret += "{YELLOW}+" + str(s.untracked) + "{NO_COLOR}"
    if s.stashed > 0:
        ret += "s" + str(s.stashed) + "{NO_COLOR}"
    if s.staged + s.conflicts + s.changed + s.untracked + s.stashed == 0:
        ret += "🦉{BOLD_GREEN}CLEAN!{NO_COLOR}"
    ret += "{NO_COLOR}"

    return ret
