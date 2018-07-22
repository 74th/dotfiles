#!/bin/bash
sudo apt update

# fish
if [ type fish 2>/dev/null 1>/dev/null ]; then
	# https://launchpad.net/~fish-shell/+archive/ubuntu/release-2
	sudo apt-add-repository ppa:fish-shell/release-2
	sudo apt-get update
	sudo apt-get -y install fish
fi

# dotnet need
PKG_LIST=$(cat <<EOS
# dotnetのインストールに必要だったりする
apt-transport-https

vim
peco

gcc
make
automake
gdb

EOS
)
PKG_LIST=$(echo "$PKG_LIST" | perl -pe 's/^#.*$//g')
PKG_LIST=$(echo "$PKG_LIST" | perl -pe 's/\n/ /g')

sudo apt install -y $PKG_LIST
