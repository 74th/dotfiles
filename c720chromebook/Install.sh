#!/bin/bash
if [ -e ~/.xmodmap ]; then
	rm ~/.xmodmap
fi
ln -s ~/dotfiles/c720chromebook/_xmodmap ~/.xmodmap

if [ -e ~/.xbindkeysrc ]; then
	rm ~/.xbindkeysrc
fi
ln -s ~/dotfiles/c720chromebook/_xbindkeysrc ~/.xbindkeysrc
