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

brew install caskroom/cask/java

#brew cask install xquartz

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
P="$P watch"
# sftpのタブ補完が効くので入れる
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
P="$P gcc"

# Golang
P="$P go"
#P="$P go-delve/delve/delve"

# メモリーのビジュアル化
P="$P graphviz qt qcachegrind"

# docker
P="$P docker"
P="$P docker-compose"
P="$P docker-machine"
C="$C docker"

# tensorflow関連
#P="$P bazel" # バージョンが古いものが必要なため自前で入れる必要がある
P="$P gpp"
P="$P pyenv"
P="$P pyenv-virtualenv"

# plantuml
P="$P plantuml"

# plantuml
P="$P rbenv"

# font
brew tap caskroom/fonts
C="$C font-source-code-pro"
C="$C font-source-han-code-jp"
C="$C font-sourcecodepro-nerd-font"
C="$C font-fira-code"
C="$C font-hasklig"

# vs code
C="$C visual-studio-code"

# gimp
C="$C gimp"

# QE
C="$C qr-journal"

# ディスク領域可視化
C="$C Caskroom/cask/disk-inventory-x"

# Caffeine
C="$C caskroom/cask/caffeine"

# Libre Office
C="$C caskroom/cask/libreoffice"

# MacVim
#C="$C macvim"

echo $P
brew install $P

brew cask install $C

brew cleanup
