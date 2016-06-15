sudo apt update

if [ $# = 0 ] || [ $1 = "git" ];then
	sudo apt install -y git git-flow bash-completion
	sudo curl -o /etc/bash_completion.d/git-flow-completion.bash https://raw.githubusercontent.com/bobthecow/git-flow-completion/master/git-flow-completion.bash
fi
if [ $# = 0 ] || [ $1 = "tmux" ];then
	sudo apt install -y tmux
fi
if [ $# = 0 ] || [ $1 = "mozc" ];then
	sudo apt install -y ibus-mozc
fi
