#!/bin/bash
set -xe
if [ -e /etc/debian_version ]; then
    if [ ! -f "$HOME/.local/bin/uv" ]; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    fi

    if ! type uv >/dev/null 2>&1; then
        export PATH=$HOME/.local/bin:$PATH
    fi
fi

if [ ! -e ~/ghq/github.com/74th/dotfiles ]; then
    mkdir -p ~/ghq/github.com/74th/dotfiles
    git clone https://github.com/74th/dotfiles.git ~/ghq/github.com/74th/dotfiles
fi
cd ~/ghq/github.com/74th/dotfiles

~/.local/bin/uv sync

~/.local/bin/uv run invoke install
