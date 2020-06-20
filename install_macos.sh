#!/bin/bash
set -xe
if ! type brew >/dev/null 2>&1; then
    # https://brew.sh/
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    brew update
    brew install python
fi
/usr/local/bin/python3 -u -m pip install invoke detect pyyaml
/usr/local/bin/python3 -u -m invoke install-small
