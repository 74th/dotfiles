#!/bin/bash
if ! grep -q ".bashrc for devcontainer" ~/.bashrc; then
    cat ~/dotfiles/bashrc/devcontainer.sh >> ~/.bashrc
fi
