#!/bin/bash
set -Ceux

if [ $# -ne 1 ]; then
   echo "Install_remote.sh <HOSTNAME>"
   exit 1
fi

ssh $1 mkdir .ssh/ \; true
scp ~/.ssh/id_rsa.pub $1:.ssh/authorized_keys
scp ~/.ssh/server_id_rsa $1:.ssh/id_rsa
scp ~/.ssh/server_id_rsa.pub $1:.ssh/id_rsa.pub

ssh -t $1 "[ -e /etc/debian_version ] && sudo apt install git curl"

ssh -t $1 "git clone git@github.com:74th/dotfiles.git
ssh $1 cd dotfiles\;./Install.sh
