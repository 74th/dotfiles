#!/usr/local/bin/system-python
"""
~/bin/ 以下のサブディレクトリにある実行ファイルを ~/bin/ にシンボリックリンクを貼る
ディレクトリで区切るので、セットで導入、リムーブが簡単にできる
"""

import os
import pathlib
import shlex
import subprocess

bin_dir = pathlib.Path("~", "bin").expanduser()

for d in bin_dir.iterdir():
    if not d.is_dir():
        continue
    if d.name.startswith("_") or d.name.endswith("_"):
        continue
    print(f"Processing {d.name}")
    for f in d.iterdir():
        symlink = bin_dir.joinpath(f.name)
        if (
            symlink.exists()
            and symlink.is_symlink()
            and symlink.resolve() == f.resolve()
        ):
            continue
        if f.is_file() and os.access(f, os.X_OK):
            cmd = [
                "ln",
                "-sf",
                f.resolve().as_posix(),
                bin_dir.as_posix() + "/",
            ]
            print(shlex.join(cmd))
            subprocess.run(cmd, check=True, text=True)

for f in bin_dir.iterdir():
    if not f.is_symlink():
        continue
    if f.resolve().exists():
        continue

    cmd = [
        "rm",
        f.as_posix(),
    ]
    print(shlex.join(cmd))
    subprocess.run(cmd, check=True, text=True)
