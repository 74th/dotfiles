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

# tmux
if [ $# = 0 ] || [ $1 = "tmux" ];then
	sudo apt install -y tmux
fi

# dotnet need
sudo apt install apt-transport-https
