#!/bin/sh
set -xe
if [ -e /etc/debian_version ]; then
    sudo apt-get update
    sudo apt-get install -y git unzip curl
    mkdir -p ~/tmp
    rm -rf ~/tmp/*
    cd ~/tmp
    curl -OL https://github.com/x-motemen/ghq/releases/latest/download/ghq_linux_amd64.zip
    unzip ghq_linux_amd64.zip
    ./ghq_linux_amd64/ghq get 74th/dotfiles
    rm -rf $HOME/dotfiles
    ln -sf $HOME/ghq/github.com/74th/dotfiles $HOME/dotfiles
else
    mkdir -p ~/tmp
    rm -rf ~/tmp/*
    cd ~/tmp
    curl -OL https://github.com/x-motemen/ghq/releases/latest/download/ghq_darwin_amd64.zip
    unzip ghq_darwin_amd64.zip
    ./ghq_darwin_amd64/ghq get 74th/dotfiles
    rm -rf $HOME/dotfiles
    ln -sf $HOME/ghq/github.com/74th/dotfiles $HOME/dotfiles
fi
cd $HOME/dotfiles/
bash ./install.sh
