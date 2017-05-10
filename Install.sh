#!/bin/bash

if [ "$(uname)" == 'Darwin' ]; then
	OSNAME='Mac'
	OSDISTRO='Mac'
elif [ "$(uname -o)" == 'Cygwin' ]; then
	OSNAME='Windows'
	OSDISTRO='Cygwin'
elif [ "$(uname -o)" == 'Msys' ]; then
	OSNAME='Windows'
	OSDISTRO='Msys'
elif [ -e "/etc/debian_version" ]; then
	OSNAME='Linux'
	OSDISTRO='Debian'
elif [ -e "/etc/redhat-release" ]; then
	OSNAME='Linux'
	OSDISTRO='Redhat'
else
	OSNAME='Linux'
	OSDISTRO='unknown'
fi

# コマンドのチェック
if ! type curl >/dev/null 2>&1; then
	if [ $OSDISTRO = "Debian" ]; then
		sudo apt -y install curl
	elif [ $OSDISTRO = "Redhat" ]; then
		sudo yum -y install curl
	else
		echo "please install curl"
		exit 1
	fi
fi

# fish shell のインストール
if ! type fish >/dev/null 2>&1; then
	if [ $OSDISTRO = "Debian" ]; then
		sudo bash -c "echo 'deb http://download.opensuse.org/repositories/shells:/fish:/release:/2/Debian_8.0/ /' > /etc/apt/sources.list.d/fish.list "
		sudo apt-get update
		sudo apt-get install -y fish
	elif [ $OSDISTRO = "Redhat" ]; then
		sudo bash -c "cd /etc/yum.repos.d/;wget http://download.opensuse.org/repositories/shells:fish:release:2/CentOS_7/shells:fish:release:2.repo"
		sudo yum install -y fish
	fi
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
# balias

# Macの環境設定
if [ $OSNAME = 'Mac' ]; then
	# キーリピート
	defaults write -g ApplePressAndHoldEnabled -bool false

	# homebrew
	~/dotfiles/homebrew/install.sh

	# macvim-kaoriya用のmvim
	if [ ! -e ~/bin ]; then
		mkdir ~/bin
	fi
	curl https://raw.githubusercontent.com/splhack/macvim/master/src/MacVim/mvim > ~/bin/mvim
	chmod 755 ~/bin/mvim

	# 環境変数
	if [ ! -e ~/Library/LaunchAgents/setenv.plist ]; then
		ln -s ~/dotfiles/mac_env/setenv.plist ~/Library/LaunchAgents/setenv.plist
	else
		launchctl unload ~/Library/LaunchAgents/setenv.plist
	fi
	launchctl load ~/Library/LaunchAgents/setenv.plist
fi
