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

import detect
import questionary
from print_color import print as cprint

DOTFILES_BASE = pathlib.Path(__file__).parent.parent


class Method(Enum):
    UBUNTU_INSTALL = "ubuntu-install"
    HOMEBREW = "homebrew"


def print_cmd(cmd: str | list[str]) -> None:
    if isinstance(cmd, list):
        cmd = shlex.join(cmd)
    cprint(cmd, color="green")


def install_by_ubuntu_script(items: list[str]) -> None:
    for item in items:
        bin_file = DOTFILES_BASE / "ubuntu" / "install" / f"{item}.sh"
        print_cmd(f"{bin_file}")
        subprocess.run([str(bin_file)], check=True)


def list_ubuntu_install_scripts() -> dict[str, tuple[Method, str]]:
    ubuntu_install_dir = DOTFILES_BASE / "ubuntu" / "install"
    items = {}
    for script_file in ubuntu_install_dir.glob("*.sh"):
        item = script_file.stem
        items[item] = (Method.UBUNTU_INSTALL, item)
    return items


def install_by_brew(items: list[str]) -> None:
    cmd = ["brew", "install", *items]
    print_cmd(cmd)
    subprocess.run(cmd, check=True)


def list_brew_install_items() -> dict[str, tuple[Method, str]]:
    items = {}
    brew_packages = ["volta", "fio", "herdr"]
    for package in brew_packages:
        items[package] = (Method.HOMEBREW, package)
    return items


def main() -> None:
    available_items: dict[str, tuple[Method, str]] = {}

    if detect.linux:
        available_items.update(list_ubuntu_install_scripts())
    if detect.mac:
        available_items.update(list_brew_install_items())

    available_items_keys_sorted = sorted(available_items.keys())

    selected_item_keys = questionary.checkbox(
        "Select an item to install:", choices=available_items_keys_sorted
    ).ask()

    if not selected_item_keys:
        sys.exit(1)

    selected_tag_grouped_items: dict[Method, list[str]] = {}
    for key in selected_item_keys:
        method, func = available_items[key]
        if method not in selected_tag_grouped_items:
            selected_tag_grouped_items[method] = []
        selected_tag_grouped_items[method].append(func)
    print(selected_tag_grouped_items)

    for method, items in selected_tag_grouped_items.items():
        if method == Method.UBUNTU_INSTALL:
            install_by_ubuntu_script(items)

        if method == Method.HOMEBREW:
            install_by_brew(items)


if __name__ == "__main__":
    main()
