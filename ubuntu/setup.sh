sudo apt update

# git
if [ $# = 0 ] || [ $1 = "git" ];then
	sudo apt install -y git git-flow bash-completion
	sudo curl -o /etc/bash_completion.d/git-flow-completion.bash https://raw.githubusercontent.com/bobthecow/git-flow-completion/master/git-flow-completion.bash
fi

# tmux
if [ $# = 0 ] || [ $1 = "tmux" ];then
	sudo apt install -y tmux
fi

# mozc
if [ $# = 0 ] || [ $1 = "mozc" ];then
	sudo apt install -y ibus-mozc
fi

# dotnet need
sudo apt install apt-transport-https

# font-manager
if [ $# = 0 ] || [ $1 = "font-manager" ];then
	sudo apt install -y font-manager
fi

# ICON
if [ $# = 0 ] || [ $1 = "icon" ];then
	# https://numixproject.org/
	sudo add-apt-repository ppa:numix/ppa
	sudo apt-get update
	sudo apt-get install numix-icon-theme-shine
fi

