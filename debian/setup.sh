sudo apt update

# vim
if [ $# = 0 ] || [ $1 = "vim" ];then
	sudo apt install -y vim
fi

# git
if [ $# = 0 ] || [ $1 = "git" ];then
	sudo apt install -y git git-flow bash-completion
	sudo curl -o /etc/bash_completion.d/git-flow-completion.bash https://raw.githubusercontent.com/bobthecow/git-flow-completion/master/git-flow-completion.bash
fi

# fish
if [ $# = 0 ] || [ $1 = "fish" ];then
	sudo echo 'deb http://download.opensuse.org/repositories/shells:/fish:/release:/2/Debian_9.0/ /' | sudo tee /etc/apt/sources.list.d/shells:fish:release:2.list
	sudo apt-get update
	sudo apt-get install fish
fi
