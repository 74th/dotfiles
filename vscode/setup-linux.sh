#!/bin/bash
if [ "$(uname)" == 'Darwin' ]; then
	CONFIG_DIR=$HOME/Library/.config/Code/User
	echo cannot setup for macos
	exit 1
else
	CONFIG_DIR=$HOME/.config/Code/User
fi
DOTFILE_DIR=$HOME/dotfiles/vscode

FILE=keybindings.json
if [ -e $CONFIG_DIR/$FILE ]; then
	rm $CONFIG_DIR/$FILE
fi
ln -s $DOTFILE_DIR/$FILE $CONFIG_DIR/$FILE

FILE=settings_mac.json
if [ -e $CONFIG_DIR/settings.json ]; then
	rm $CONFIG_DIR/settings.json
fi
ln -s $DOTFILE_DIR/settings_mac.json $CONFIG_DIR/settings.json

FILE=snippets
if [ -e $CONFIG_DIR/$FILE ]; then
	rm -rf $CONFIG_DIR/$FILE
fi
ln -s $DOTFILE_DIR/$FILE $CONFIG_DIR/$FILE
