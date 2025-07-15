#!env bash
set -xe
if [ -e /etc/debian_version ]; then
    if [ "aarch64" == "$(uname -m)" ]; then
        ARCH=arm64
    else
        ARCH=amd64
    fi
    sudo apt-get update
    sudo apt-get install -y git unzip curl
else
    if [ "arm64" == "$(uname -m)" ]; then
        ARCH=arm64
    else
        ARCH=amd64
    fi
    mkdir -p ~/tmp
fi
mkdir -p $HOME/ghq/github.com/74th
cd $HOME/ghq/github.com/74th
git clone https://github.com/74th/dotfiles.git

cd $HOME/ghq/github.com/74th/dotfiles/

source ./install_uv.sh

uv run invoke install
