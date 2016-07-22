# font-manager
if [ $# = 0 ] || [ $1 = "font-manager" ];then
	sudo apt install -y font-manager
fi

# ICON
if [ $# = 0 ] || [ $1 = "icon" ];then
	# https://numixproject.org/
	sudo add-apt-repository ppa:numix/ppa
	sudo apt-get update
	sudo apt-get install numix-icon-theme-circle
fi

# gvim
if [ $# = 0 ] || [ $1 = "gvim" ];then
	sudo apt install -y vim-gui-common
fi

# ibus-mozc
if [ $# = 0 ] || [ $1 = "mozc" ];then
	sudo apt install -y ibus-mozc
fi
