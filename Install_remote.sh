#!/bin/bash
set -Ceux

if [ $# -ne 1 ]; then
   echo "Install_remote.sh <HOSTNAME>"
   exit 1
fi

ssh $1 "mkdir -p .ssh/"
scp ~/.ssh/id_rsa.pub $1:.ssh/authorized_keys
scp ~/.ssh/server/id_rsa* $1:.ssh/

ssh -t $1 <<EOS
if [ -e /etc/debian_version ] ;then
	sudo apt-get install -y git curl;
elif [ -e "/etc/redhat-release" ]; then
	sudo yum install -y git curl;
fi
git clone git@github.com:74th/dotfiles.git
cd dotfiles;
./Install.sh
EOS
echo "done"
