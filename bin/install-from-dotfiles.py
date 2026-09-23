#!/usr/bin/env -S uv run --no-project --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "questionary==2.1.1",
#     "detect==2020.12.3",
#     "print-color==0.4.8",
# ]
# ///
from __future__ import annotations

import pathlib
import shlex
import subprocess
import sys
from enum import Enum
from typing import cast

import detect
import questionary
from print_color import print as cprint
from questionary import Choice

DOTFILES_BASE = pathlib.Path(__file__).parent.parent


class Method(Enum):
    SCRIPT = "script"
    CMD = "cmd"
    HOMEBREW = "homebrew"


ChoiceValue = tuple[Method, str]


def print_cmd(cmd: str | list[str]) -> None:
    if isinstance(cmd, list):
        cmd = shlex.join(cmd)
    cprint(cmd, color="green")


def install_by_scripts(items: list[str]) -> None:
    for item in items:
        print_cmd(item)
        subprocess.run([item], check=True)


def install_by_cmd(items: list[str | list[str]]) -> None:
    for item in items:
        if isinstance(item, list):
            for cmd in item:
                print_cmd(cmd)
                subprocess.run(cmd, shell=True, check=True)
        else:
            print_cmd(item)
            subprocess.run(item, shell=True, check=True)


def list_dotfiles_ubuntu_install_scripts() -> list[Choice]:
    DOTFILES_UBUNTU_INSTALL_dir = DOTFILES_BASE / "ubuntu" / "install"
    items: list[Choice] = []
    for script_file in DOTFILES_UBUNTU_INSTALL_dir.glob("*.sh"):
        items.append(
            Choice(
                title=f"{script_file.stem} (dotfiles/ubuntu/install)",
                value=(Method.SCRIPT, script_file),
            )
        )
    return items


def list_install_scripts() -> list[Choice]:
    DOTFILES_INSTALL_dir = DOTFILES_BASE / "install"
    items: list[Choice] = []
    for script_file in DOTFILES_INSTALL_dir.glob("*.sh"):
        items.append(
            Choice(
                title=f"{script_file.stem} (dotfiles/install)",
                value=(Method.SCRIPT, script_file),
            )
        )
    for script_file in DOTFILES_INSTALL_dir.glob("*.py"):
        items.append(
            Choice(
                title=f"{script_file.stem} (dotfiles/install)",
                value=(Method.SCRIPT, script_file),
            )
        )
    return items


def install_by_brew(items: list[str]) -> None:
    cmd = ["brew", "install", *items]
    print_cmd(cmd)
    subprocess.run(cmd, check=True)


def list_brew() -> list[Choice]:
    brew_packages = ["volta", "fio", "herdr"]
    items = [
        Choice(title=f"{package} (brew)", value=(Method.HOMEBREW, package))
        for package in brew_packages
    ]
    return items


def list_mac() -> list[Choice]:
    items: list[Choice] = []

    # docker sandboxes (sbx)
    items.append(
        Choice(
            title="sbx (brew)",
            value=(
                Method.CMD,
                [
                    ["brew", "trust", "docker/tap"],
                    ["brew", "install", "docker/tap/sbx"],
                ],
            ),
        )
    )

    return items


def main() -> None:
    available_items: list[Choice] = []

    available_items.extend(list_install_scripts())
    if detect.linux:
        available_items.extend(list_dotfiles_ubuntu_install_scripts())
    if detect.mac:
        available_items.extend(list_brew())
        available_items.extend(list_mac())

    available_items.sort(key=lambda choice: choice.title)

    choiced = cast(
        list[ChoiceValue],
        questionary.checkbox(
            "Select an item to install:", choices=available_items
        ).ask(),
    )

    if not choiced:
        sys.exit(1)

    selected_tag_grouped_items: dict[Method, list[str]] = {}
    for choiced_item in choiced:
        method, item = choiced_item
        if method not in selected_tag_grouped_items:
            selected_tag_grouped_items[method] = []
        selected_tag_grouped_items[method].append(item)

    for method, items in selected_tag_grouped_items.items():
        if method == Method.SCRIPT:
            install_by_scripts(items)

        if method == Method.HOMEBREW:
            install_by_brew(items)

        if method == Method.CMD:
            install_by_cmd(items)


if __name__ == "__main__":
    main()
