#!/bin/bash
set -xe
xcode-select --install

if [ ! -d "/opt/homebrew" ]; then
    # https://brew.sh/
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    export PATH=$PATH:/opt/homebrew/bin
    brew update
    brew install python git
fi

curl -L https://raw.githubusercontent.com/74th/dotfiles/master/install_ghq.sh | bash -