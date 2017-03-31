P=

brew update
brew upgrade

# bash
P="$P bash bash-completion"

# Linuxのツールを使う
P="$P coreutils"

# CUIツール
P="$P wget"
P="$P fish"
P="$P peco"
P="$P readline"
P="$P imagemagick"
P="$P ffmpeg"

# develop
P="$P git"
P="$P node"
P="$P openssl"
P="$P python"
P="$P sqlite"
P="$P jq"

# Golang
P="$P go"
P="$P go-delve/delve/delve"

# docker
P="$P docker"
P="$P docker-compose"
P="$P docker-machine"

brew install $P

# font
brew tap caskroom/fonts
C="$C font-source-han-code-jp"
C="$C font-sourcecodepro-nerd-font"
brew cask install $C

brew cleanup
