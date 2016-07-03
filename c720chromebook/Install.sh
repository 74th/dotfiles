#!/bin/bash
if [ -e ~/Desktop/xmodmap.sh ]; then
	rm ~/Desktop/xmodmap.sh
fi
cp ~/dotfiles/c720chromebook/xmodmap.sh ~/Desktop/xmodmap.sh

if [ -e ~/.xbindkeysrc ]; then
	rm ~/.xbindkeysrc
fi
ln -s ~/dotfiles/c720chromebook/_xbindkeysrc ~/.xbindkeysrc
