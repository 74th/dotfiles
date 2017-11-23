#!/bin/bash
set -Ceu

# homebrew https://brew.sh/index_ja.html
if ! which brew >/dev/null 2>&1; then
	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi


P=
C=

brew update
brew upgrade

# bash
P="$P bash bash-completion"

# Linuxのツールを使う
P="$P coreutils"

# CUIツール
P="$P wget"
P="$P fish"
P="$P direnv"
P="$P peco"
P="$P readline"
P="$P imagemagick"
P="$P ffmpeg"
# sftpのタブ補完が効く
P="$P openssh"

# develop
P="$P git"
P="$P node"
P="$P openssl"
P="$P python"
P="$P sqlite"
P="$P jq"
P="$P gnuplot"
P="$P protobuf"

# Golang
P="$P go"
P="$P go-delve/delve/delve"

# docker
P="$P docker"
P="$P docker-compose"
P="$P docker-machine"
C="$C docker"

# tensorflow関連
P="bazel"
P="gpp"
P="pyenv"

# wine
P="wine"

# font
brew tap caskroom/fonts
C="$C font-source-han-code-jp"
C="$C font-sourcecodepro-nerd-font"

# hosts manager
C="$C hosts"

# veertu
C="$C veertu-desktop"

# vs code
C="$C visual-studio-code"

# gimp
C="$C gimp"

# gimp
C="$C qr-journal"

# ディスク領域可視化
C="$C Caskroom/cask/disk-inventory-x"

brew install $P
brew cask install $C

brew cleanup
