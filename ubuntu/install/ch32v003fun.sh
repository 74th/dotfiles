#!/bin/bash
set -xe
sudo apt-get install -y build-essential libnewlib-dev gcc-riscv64-unknown-elf libusb-1.0-0-dev libudev-dev gdb-multiarch
ghq get github.com/cnlohr/ch32v003fun
cd ~/ghq/github.com/cnlohr/ch32v003fun/minichlink
make clean all
cp minichlink ~/bin/
