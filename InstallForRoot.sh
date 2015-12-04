#!/bin/sh
# Linuxで最速設定するスクリプト

#ユーザ名を尋ねる
echo -n "repository username:"
read repuser
repdir=/home/$repuser/dotfiles

#bashrc
if [ -e ~/.bashrc ]; then
    rm ~/.bashrc
fi
if [ -e ~/.bash_profile ]; then
    rm ~/.bash_profile
fi
cp $repdir/bashrc/rootbashrc ~/.bashrc
cp $repdir/bashrc/rootbashrc ~/.bash_profile

#vimrc
if [ -e ~/.vimrc ]; then
    rm ~/.vimrc
fi
if [ -e ~/.gvimrc ]; then
    rm ~/.gvimrc
fi
cp $repdir/vimrc/rootvimrc.vim ~/.vimrc
cp $repdir/vimrc/rootgvimrc.vim ~/.gvimrc

#MySettings
if [ -e ~/dotfiles ]; then
    echo "Fail: directory ~/dotfiles is exists."
else
    ln -s /home/$repuser/dotfiles ~/dotfiles
fi
