#!/bin/bash
set -xe
if [ -e /etc/debian_version ]; then
    if [ ! -d "/home/nnyn/.rye" ]; then
        RYE_INSTALL_OPTION="--yes" curl -sSf https://rye.astral.sh/get | bash
    fi

    if ! type rye >/dev/null 2>&1; then
        export PATH=$HOME/.rye/shims:$PATH
    fi
fi

if [ ! -e ~/ghq/github.com/74th/dotfiles ]; then
    mkdir -p ~/ghq/github.com/74th/dotfiles
    git clone https://github.com/74th/dotfiles.git ~/ghq/github.com/74th/dotfiles
fi
cd ~/ghq/github.com/74th/dotfiles

~/.rye/shims/rye sync

~/.rye/shims/python -u -m invoke install
