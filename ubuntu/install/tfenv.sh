#!/bin/bash
set -xe
if [ -d ~/.tfenv ]; then
    cd ~/.tfenv
    git pull
else
    git clone --depth=1 https://github.com/tfutils/tfenv.git ~/.tfenv
fi

mkdir -p ~/.tfenv/versions
