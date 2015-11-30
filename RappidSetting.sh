#!/bin/sh
# Mac/Linuxで最速設定するスクリプト

#bashrc
if [ -e ~/.bashrc ]; then
    rm ~/.bashrc
fi
if [ -e ~/.bash_profile ]; then
    rm ~/.bash_profile
fi
cp ~/dotfiles/bashrc/rootbashrc ~/.bashrc
cp ~/dotfiles/bashrc/rootbashrc ~/.bash_profile

#vimrc
if [ -e ~/.vimrc ]; then
    mv ~/.vimrc ~/.vimrc_
fi
if [ -e ~/.gvimrc ]; then
    mv ~/.gvimrc ~/.gvimrc_
fi
cp ~/dotfiles/vimrc/rootvimrc.vim ~/.vimrc
cp ~/dotfiles/vimrc/rootgvimrc.vim ~/.gvimrc
if [ ! -d ~/.vim ]; then
    mkdir ~/.vim
fi

#screenrc
if [ -e ~/.screenrc ]; then
    mv ~/.screenrc ~/.screenrc_
fi
ln -s ~/dotfiles/screenrc/screenrc ~/.screenrc

#vscoderc
if [ "$(uname)" == 'Darwin' ]; then
    rm ~/Library/Application\ Support/Code/User/keybindings.json
    rm ~/Library/Application\ Support/Code/User/settings.json
    rm -rf ~/Library/Application\ Support/Code/User/snippets
    ln -s ~/dotfiles/vscode/keybindings.json ~/Library/Application\ Support/Code/User/keybindings.json
    ln -s ~/dotfiles/vscode/settings.json ~/Library/Application\ Support/Code/User/settings.json
    ln -s ~/dotfiles/vscode/snippets ~/Library/Application\ Support/Code/User/snippets
fi
