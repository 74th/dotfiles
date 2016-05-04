# MSYS2用PATHの追加設定

# golang
if [ -e /c/tools/go/bin ];then
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
	alias node='winpty node'
	alias npm='winpty npm'
fi

# vim
if [ -e /c/Program\ Files\ \(x86\)/vim/vim74/ ];then
	alias vi='winpty /c/Program\ Files\ \(x86\)/vim/vim74/vim.exe'
	alias vim='winpty /c/Program\ Files\ \(x86\)/vim/vim74/vim.exe'
	alias gvim='/c/Program\ Files\ \(x86\)/vim/vim74/gvim.exe'
fi
