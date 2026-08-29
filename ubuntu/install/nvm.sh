#!/bin/bash
# nodejsのバージョンマネージャー
# ただし最近はvoltaを使いたい

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.6/install.sh | bash

export NVM_DIR="$HOME/.nvm"

[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

# ltsをインストール
nvm use --lts
nvm alias default lts/*
