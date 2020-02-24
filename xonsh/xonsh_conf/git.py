from .lib import run, silent_run
from .xonsh_builtin import x_aliases


def show_merged_branch():
    run("git branch --format '%(refname:short)' --merged")


def delete_merged_branch():
    branches = silent_run("git branch --format '%(refname:short)' --merged").split("\n")
    for branch in branches:
        run(f"git branch -d {branch}")


def set_aliases():
    x_aliases["git-show-merged-branch"] = show_merged_branch
    x_aliases["git-delete-merged-branch"] = delete_merged_branch
