#!/bin/bash

if [ $(uname) == 'Darwin' ]; then
	OSNAME='Mac'
elif [ $(uname -o) == 'Cygwin' ]; then
	OSNAME='Cygwin'
elif [ $(uname -o) == 'Msys' ]; then
	OSNAME='Msys'
else
	OSNAME='Linux'
fi

# bashrc
if [ $(grep dotfiles ~/.bashrc | wc -l ) -eq 0 ]; then
	echo "source ~/dotfiles/bashrc/bashrc" >> ~/.bashrc
fi

# vimrc
if [ $(grep dotfiles ~/.vimrc | wc -l ) -eq 0 ]; then
	echo "source ~/dotfiles/vimrc/vimrc.vim" >>~/.vimrc
fi
if [ $(grep dotfiles ~/.gvimrc | wc -l ) -eq 0 ]; then
	echo "source ~/dotfiles/vimrc/gvimrc.vim" >>~/.gvimrc
fi
# vim-plug
curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

# screenrc
if [ -e ~/.screenrc ]; then
	rm ~/.screenrc
fi
if [ ! OSNAME = "Linux" ]; then
	ln -s ~/dotfiles/screenrc/screenrc ~/.screenrc
fi

# tmux
if [ -e ~/.tmux.conf ]; then
	rm ~/.tmux.conf
fi
ln -s ~/dotfiles/tmux/.tmux.conf ~/.tmux.conf

# vscode
if [ $OSNAME = "Linux" ]; then
	if [ -e ~/.config/Code ];then
		VSCODE_DIR=~/.config/Code/User
	fi
fi
if [ $OSNAME = 'Mac' ]; then
	if [ -e ~/Library/Application\ Support/Code/User ];then
		VSCODE_DIR=~/Library/Application\ Support/Code/User
	fi
fi
echo $VSCODE_DIR
if [ -e "$VSCODE_DIR" ]; then

	if [ -e "$VSCODE_DIR/keybindings.json" ]; then
		rm "$VSCODE_DIR/keybindings.json"
	fi
	ln -s ~/dotfiles/vscode/keybindings.json "$VSCODE_DIR"

	if [ -e "$VSCODE_DIR/settings.json" ]; then
		rm "$VSCODE_DIR/settings.json"
	fi
	ln -s ~/dotfiles/vscode/settings.json "$VSCODE_DIR/settings.json"

	if [ -e "$VSCODE_DIR/snippets" ]; then
		rm -rf "$VSCODE_DIR/snippets"
	fi
	ln -s ~/dotfiles/vscode/snippets "$VSCODE_DIR"

fi

# git
sh ~/dotfiles/git/set-config.sh

# xfce4
if [ -e ~/.config/xfce4/terminal/terminalrc ];then
	rm ~/.config/xfce4/terminal/terminalrc 
	ln -s ~/dotfiles/xfce4terminal/terminalrc ~/.config/xfce4/terminal/terminalrc 
fi

# fish
if [ ! -e ~/.config/fish ]; then
	mkdir -p ~/.config/fish
fi
if [ -e ~/.config/fish/config.fish ]; then
	rm ~/.config/fish/config.fish
fi
ln -s ~/dotfiles/fish/config.fish ~/.config/fish/config.fish
if [ -e ~/.config/fish/functions ]; then
	rm -rf ~/.config/fish/functions
fi
ln -s ~/dotfiles/fish/functions ~/.config/fish/functions
rm -rf ~/.config/fish/fishd.*; true
ln -s ~/dotfiles/fish/fishd.784f4359182f ~/.config/fish/
# fisherman
curl -Lo ~/.config/fish/functions/fisher.fish --create-dirs git.io/fisherman

# Macの環境設定
if [ $OSNAME = 'Mac' ]; then
	# キーリピート
	defaults write -g ApplePressAndHoldEnabled -bool false

	# homebrew
	~/dotfiles/homebrew/install.sh
fi
