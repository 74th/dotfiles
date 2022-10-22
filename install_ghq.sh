#! env python3
set -xe
if [ -e /etc/debian_version ]; then
    if [ "aarch64" == "$(uname -m)" ]; then
        ARCH=arm64
    else
        ARCH=amd64
    fi
    sudo apt-get update
    sudo apt-get install -y git unzip curl
    mkdir -p ~/tmp
    rm -rf ~/tmp/*
    cd ~/tmp
    curl -OL https://github.com/x-motemen/ghq/releases/latest/download/ghq_linux_$ARCH.zip
    unzip ghq_linux_$ARCH.zip
    ./ghq_linux_$ARCH/ghq get 74th/dotfiles
    mkdir -p ~/bin
    cp ./ghq_linux_$ARCH/ghq ~/bin/
    rm -rf $HOME/dotfiles
    ln -sf $HOME/ghq/github.com/74th/dotfiles $HOME/dotfiles
else
    if [ "arm64" == "$(uname -m)" ]; then
        ARCH=arm64
    else
        ARCH=amd64
    fi
    mkdir -p ~/tmp
    rm -rf ~/tmp/*
    cd ~/tmp
    curl -OL https://github.com/x-motemen/ghq/releases/latest/download/ghq_darwin_$ARCH.zip
    unzip ghq_darwin_$ARCH.zip
    ./ghq_darwin_$ARCH/ghq get 74th/dotfiles
    mkdir -p ~/bin
    cp ./ghq_darwin_$ARCH/ghq ~/bin/
    rm -rf $HOME/dotfiles
    ln -sf $HOME/ghq/github.com/74th/dotfiles $HOME/dotfiles
fi
cd $HOME/dotfiles/
bash ./install.sh
