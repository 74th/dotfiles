#!/bin/bash
# https://qiita.com/mkiken/items/af5c40ce0d0c6d3530c7

while read local_ref local_sha1 remote_ref remote_sha1
do
  if [[ "${remote_ref##refs/heads/}" = "master" ]]; then
    echo "Warning: push to remote master, continue? [y/N]"

    exec < /dev/tty
    read ANSWER

    case $ANSWER in
      "Y" | "y" | "yes" | "Yes" | "YES" ) echo "OK. push start.";;
      * ) echo "push failed.";exit 1;;
    esac
    exit 0
  fi
done
