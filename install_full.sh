#!/bin/bash
set -xe
if [ -e /etc/debian_version ]; then
    if ! type pip3 >/dev/null 2>&1; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
    fi
    pip3 install invoke detect
fi
if [ ! -e ~/ghq/github.com/74th/dotfiles ]; then
    mkdir -p ~/ghq/github.com/74th/dotfiles
    git clone https://github.com/74th/dotfiles.git ~/ghq/github.com/74th/dotfiles
fi
cd ~/ghq/github.com/74th/dotfiles
python3 -u -m invoke install
