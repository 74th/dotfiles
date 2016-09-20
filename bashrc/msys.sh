# MSYS2用PATHの追加設定

# golang
if [ -e /c/tools/go/bin ];then
	export GOROOT=/c/tools/go/
	export PATH=$PATH:/c/tools/go/bin
fi

# docker
if [ -e /c/Program\ Files/Docker/Docker/Resources/bin/ ];then
	export PATH=$PATH:/c/Program\ Files/Docker/Docker/Resources/bin
	alias docker='winpty docker'
	alias docker-compose='winpty docker-compose'
fi

# nodejs
if [ -e /c/Program\ Files/nodejs/ ];then
	export PATH=$PATH:/c/Program\ Files/nodejs
	export PATH=$PATH:/c/Users/atsushi/npm
	alias node='winpty node'
	alias npm='winpty npm.cmd'
	alias cordova='winpty cordova.cmd'
fi
