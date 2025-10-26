#!/bin/bash
if ! grep -q "source ~/dotfiles/bashrc/devcontainer.bashrc" ~/.bashrc; then
    echo "source ~/dotfiles/bashrc/devcontainer.bashrc" >> ~/.bashrc
fi
