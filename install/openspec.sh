#!/bin/bash
set -xe

if ! command -v volta > /dev/null 2>&1; then
	export PATH="$HOME/.volta/bin:$PATH"
fi

volta install @fission-ai/openspec@latest
