#!/bin/bash
# nodejsのバージョンマネージャー
set -ux

curl https://get.volta.sh | bash
export VOLTA_HOME="$HOME/.volta"
export PATH="$VOLTA_HOME/bin:$PATH"
volta install node
