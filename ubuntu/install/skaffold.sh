#!/bin/bash
set -xe
curl -o $HOME/bin/skaffold -L https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-arm64
chmod +x $HOME/bin/skaffold
