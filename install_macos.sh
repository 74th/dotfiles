#!/bin/bash
set -xe
if ! type brew >/dev/null 2>&1; then
    # https://brew.sh/
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    export PATH=$PATH:/opt/homebrew/bin
    brew update
    brew install python
fi
/opt/homebrew/bin/python3 -u -m pip install invoke detect pyyaml
/opt/homebrew/bin/python3 -u -m invoke install-small
