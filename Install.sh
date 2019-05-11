#!/bin/bash
set -xe
sudo apt-get update
sudo apt-get install -y python3 python3-pip git
sudo pip3 install invoke fabric detect
if [ ! -e ~/dotfiles ]; then
    git clone https://github.com/74th/dotfiles.git ~/dotfiles
fi
cd ~/dotfiles
inv
