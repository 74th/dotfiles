#!/bin/bash
set -xe
sudo apt-get update
if [ "$(uname -p)" = "x86_64" ]; then
    export PATH=/home/linuxbrew/.linuxbrew/bin:$PATH
    if ! type brew >/dev/null 2>&1; then
        sudo apt-get install -y build-essential curl file git
        sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
    fi
    brew install python3
fi
if [ "$(uname -p)" = "arrch64" ]; then
    if ! type pip3 >/dev/null 2>&1; then
        sudo apt-get install -y python3 python3-pip
    fi
fi
pip3 install invoke detect
if [ ! -e ~/dotfiles ]; then
    git clone https://github.com/74th/dotfiles.git ~/dotfiles
fi
cd ~/dotfiles
inv
