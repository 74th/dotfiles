#!/bin/bash
set -Ceu

# homebrew https://brew.sh/index_ja.html
if ! which brew >/dev/null 2>&1; then
	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi


brew update
brew upgrade

brew install homebrew/cask/java

PKG_LIST=$(cat <<EOS
# bash
bash bash-completion

# Linuxのツールを使う
coreutils

# Java
maven

# CUIツール
wget
fish
direnv
peco
readline
imagemagick
ffmpeg
watch
rsync

# Windowsで作ったzipのファイル名でも文字化けを防ぐ
unar
# sftpのタブ補完が効くので入れる
openssh

# develop
git
node
openssl
python
sqlite
jq
gnuplot
protobuf
gcc
gdb
geos

# Golang
go

# メモリーのビジュアル化
graphviz qt qcachegrind

# docker
docker
docker-compose
kubectl

# tensorflow関連
# Java1.8がいるとかイケてないこと言うので、一旦排除
#bazel
#gpp
pyenv
pyenv-virtualenv

# wine
wine

# plantuml
plantuml

# rbenv
rbenv

# bashのデバッグ
bashdb

# font
homebrew/cask-fonts/font-source-code-pro
homebrew/cask-fonts/font-source-han-code-jp
homebrew/cask-fonts/font-sourcecodepro-nerd-font
homebrew/cask-fonts/font-fira-code
homebrew/cask-fonts/font-hasklig

# gimp
homebrew/cask/gimp

# ディスク領域可視化
homebrew/cask/disk-inventory-x

# Caffeine
homebrew/cask/caffeine

# 小さいカレンダー
homebrew/cask/day-o

# terraform
# https://github.com/hashicorp/terraform
terraform

# Libre Office
caskroom/cask/libreoffice

# MacVimはkaoriyaのエディションを入れるので、
# homebrewからは外す
EOS
)
PKG_LIST=$(echo "$PKG_LIST" | perl -pe 's/^#.*$//g')
PKG_LIST=$(echo "$PKG_LIST" | perl -pe 's/\n/ /g')

brew install $PKG_LIST

brew cleanup
