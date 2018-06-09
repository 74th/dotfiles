#!/bin/bash
set -Ceu

# homebrew https://brew.sh/index_ja.html
if ! which brew >/dev/null 2>&1; then
	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi


P=

brew update
brew upgrade

brew install homebrew/cask/java

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

# メモリーのビジュアル化
P="$P graphviz qt qcachegrind"

# docker
P="$P docker"
P="$P docker-compose"
P="$P docker-machine"

# tensorflow関連
# Java1.8がいるとかイケてないこと言うので、一旦排除
#P="$P bazel"
P="$P gpp"
P="$P pyenv"
P="$P pyenv-virtualenv"

# wine
#P="$P wine"

# plantuml
P="$P plantuml"

# rbenv
P="$P rbenv"

# font
P="$P homebrew/cask-fonts/font-source-code-pro"
P="$P homebrew/cask-fonts/font-source-han-code-jp"
P="$P homebrew/cask-fonts/font-sourcecodepro-nerd-font"
P="$P homebrew/cask-fonts/font-fira-code"
P="$P homebrew/cask-fonts/font-hasklig"

# gimp
P="$P homebrew/cask/gimp"

# ディスク領域可視化
P="$P homebrew/cask/disk-inventory-x"

# Caffeine
P="$P homebrew/cask/caffeine"

# 小さいカレンダー
P="$P homebrew/cask/day-o"

# Libre Office
#C="$C caskroom/cask/libreoffice"

# MacVim
#C="$C macvim"

echo $P
brew install $P

brew cleanup
