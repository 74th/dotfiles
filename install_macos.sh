#!/bin/bash
set -xe
if [ ! -d "/opt/homebrew" ]; then
    # https://brew.sh/
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    export PATH=$PATH:/opt/homebrew/bin
    brew update
    brew install python
fi

if [ ! -f "$HOME/.local/bin/uv" ]; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

~/.local/bin/uv sync

if ! type brew >/dev/null 2>&1; then
    export PATH=/opt/homebrew/bin:$PATH
fi

~/.local/bin/uv run invoke install-small
