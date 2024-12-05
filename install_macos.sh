#!/bin/bash
set -xe
if [ ! -d "/opt/homebrew" ]; then
    # https://brew.sh/
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    export PATH=$PATH:/opt/homebrew/bin
    brew update
    brew install python
fi

if [ ! -d "/Users/nnyn/.rye" ]; then
    RYE_INSTALL_OPTION="--yes" curl -sSf https://rye.astral.sh/get | bash
fi

~/.rye/shims/rye sync

if ! type brew >/dev/null 2>&1; then
    export PATH=/opt/homebrew/bin:$PATH
fi

~/.rye/shims/python -u -m invoke install-small
