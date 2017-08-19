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
	# https://launchpad.net/~fish-shell/+archive/ubuntu/release-2
	sudo apt-add-repository ppa:fish-shell/release-2
	sudo apt-get update
	sudo apt-get install fish
fi

# go-1.8
if [ $# = 0 ] || [ $1 = "go" ];then
	sudo apt install -y golang-1.8
	sudo ln -s /usr/share/go-1.8/bin/* /usr/local/bin/
fi

# dotnet need
sudo apt install apt-transport-https
