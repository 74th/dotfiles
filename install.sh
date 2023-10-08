#!/bin/bash
set -xe
if [ -e /etc/debian_version ]; then
    if ! type pip3 >/dev/null 2>&1; then
        sudo apt-get update
	sudo apt-get install -y python3 python3-pip direnv pipx git-secrets
    fi
    pipx install invoke
    pipx runpip invoke install detect pyyaml
fi
if [ ! -e ~/dotfiles ]; then
    git clone https://github.com/74th/dotfiles.git ~/dotfiles
fi
cd ~/dotfiles
export PATH=$HOME/.local/bin:$PATH
invoke install-small
