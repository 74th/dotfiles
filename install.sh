#!/bin/bash
set -xe
if [ -e /etc/debian_version ]; then
    if ! type pip3 >/dev/null 2>&1; then
        sudo apt-get update
	sudo apt-get install -y python3 python3-pip direnv
    fi
    pip3 install invoke detect pyyaml
fi
if [ ! -e ~/dotfiles ]; then
    git clone https://github.com/74th/dotfiles.git ~/dotfiles
fi
cd ~/dotfiles
python3 -u -m invoke install-small
