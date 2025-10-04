#!/bin/bash
if ! grep -q "source ~/dotfiles/bashrc/devcontainer.sh" ~/.bashrc; then
    echo "source ~/dotfiles/bashrc/devcontainer.sh" >> ~/.bashrc
fi
