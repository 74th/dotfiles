sudo apt-get update

if [ $# = 0 ] || [ $1 = "git" ];then
	sudo apt-get install git git-flow bash-completion
	sudo curl -o /etc/bash_completion.d/git-flow-completion.bash https://raw.githubusercontent.com/bobthecow/git-flow-completion/master/git-flow-completion.bash
fi
