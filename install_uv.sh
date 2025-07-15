#!/bin/bash
set -xe
if [ ! -f "$HOME/.local/bin/uv" ]; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

if ! type uv >/dev/null 2>&1; then
    export PATH=$HOME/.local/bin:$PATH
fi