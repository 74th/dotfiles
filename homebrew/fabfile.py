# -*- coding: utf-8 -*-
from fabric import task
import invoke

my_list = """
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

# docker & kubernetes
homebrew/cask/docker
kubernetes-helm
kubectx
stern
kubespy

# python
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

# Libre Office
caskroom/cask/libreoffice

# redis
redis
""" # type:str


def setHome(c: invoke.Context) -> dict:
    env = {}
    if len(c.run("echo $HOME", hide=True).stdout.strip()) == 0:
        env["HOME"] = c.run("cd ~;pwd", hide=True).stdout.strip()
    return env


@task(default=True)
def default(c):
    install_java(c)
    update(c)
    install(c)


@task
def install_java(c):
    env = setHome(c)
    c.run("brew install homebrew/cask/java", env=env)


@task
def update(c):
    c: invoke.Context
    env = setHome(c)
    c.run("brew update", env=env)
    c.run("brew upgrade", env=env)


@task
def install(c):
    c: invoke.Context
    env = setHome(c)
    lines = my_list.split("\n")
    install_list = ""
    for l in lines:
        if len(l) == 0:
            continue
        if l.startswith("#"):
            continue
        install_list += " " + l
    c.run("brew install" + install_list, env=env)
