#!/bin/bash
set -Ceux

OUTPUT_DIR=/Volumes/HDD/Backup/

function backup_dir() {
	rm -rf ${OUTPUT_DIR}/${NAME}
	if [ -e ${DIR} ]; then
		tar -zcvf ${OUTPUT_DIR}/${NAME}.tar.gz ${DIR}
	fi
}

#NAME=Documents
#DIR=~/Documents
#backup_dir
#
#NAME=Desktop
#DIR=~/Desktop
#backup_dir
#
#NAME=go
#DIR=~/go
#backup_dir
#
#NAME=npm
#DIR=~/npm
#backup_dir
#
#NAME=vscode
#DIR=~/.vscode
#backup_dir
#
#NAME=.config
#DIR=~/.config
#backup_dir
#
#NAME=.ssh
#DIR=~/.ssh
#backup_dir

#brew list > ${OUTPUT_DIR}/homebrew.txt

ls -1 /Applications/ > ${OUTPUT_DIR}/Applications.txt
