#!/bin/sh
# Mac/Linuxで最速設定するスクリプト

#bashrc
if [ -e ~/.bashrc ]; then
    rm ~/.bashrc
fi
cp ~/dotfiles/bashrc/rootbashrc ~/.bashrc

#vimrc
echo "source ~/dotfiles/vimrc/vimrc.vim">~/.vimrc
echo "source ~/dotfiles/vimrc/gvimrc.vim">~/.gvimrc

#screenrc
if [ -e ~/.screenrc ]; then
    rm ~/.screenrc ~/.screenrc_
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
