#!/bin/bash
set -xe
sudo apt-get update
export PATH=/home/linuxbrew/.linuxbrew/bin:$PATH
if ! type brew >/dev/null 2>&1; then
    sudo apt-get install -y build-essential curl file git
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
fi
brew install python3
pip3 install fabric invoke detect
if [ ! -e ~/dotfiles ]; then
    git clone https://github.com/74th/dotfiles.git ~/dotfiles
fi
cd ~/dotfiles
inv
