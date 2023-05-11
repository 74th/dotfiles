#!env bash
set -xe

ghq get https://github.com/pymumu/fan-control-rock5b
cd ~/ghq/github.com/pymumu/fan-control-rock5b
make package
sudo dpkg -i fan-control*.deb
sudo cp /home/nnyn/ghq/github.com/74th/dotfiles/rock5b/fan_control.json /etc/
sudo systemctl enable fan-control
sudo systemctl start fan-control
