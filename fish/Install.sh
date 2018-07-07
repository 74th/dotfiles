#!/bin/bash
set -x

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
fish -c 'fisher update'
# balias
fish -c 'fisher omf/balias'
# balias
fish -c 'fisher omf/balias'
# bass
fish -c 'fisher kedc/bass'
# aws
if type aws >/dev/null 2>&1; then
	fish -c 'fisher omf/aws'
fi
if type docker >/dev/null 2>&1; then
	fish -c 'fisher docker-completion'
fi
if type gcloud >/dev/null 2>&1; then
	fish -c 'fisher github.com/Doctusoft/google-cloud-sdk-fish-completion'
fi

