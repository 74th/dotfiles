#!/bin/bash
set -xe
# containerd
sudo apt-get install -y containerd golang
# rootless で使うので、systemdの設定を無効化
sudo systemctl disable containerd
sudo systemctl stop containerd

# nerdctl
go install github.com/containerd/nerdctl/cmd/nerdctl@latest

# rootのcontainerdをuser権限で使えるようにするtips
# https://github.com/containerd/nerdctl/blob/main/docs/faq.md#does-nerdctl-have-an-equivalent-of-sudo-usermod--ag-docker-user-
# cp ~/go/bin/nerdctl ~/bin
# sudo chown root ~/bin/nerdctl
# sudo chmod +s ~/bin/nerdctl
# rm ~/go/bin/nerdctl

# buildkit
go install github.com/moby/buildkit/cmd/buildkitd@latest
go install github.com/moby/buildkit/cmd/buildctl@latest
sudo cp $HOME/go/bin/buildkitd /usr/local/bin/

curl -L https://raw.githubusercontent.com/containerd/nerdctl/main/extras/rootless/containerd-rootless.sh > ~/bin/containerd-rootless.sh
chmod +x ~/bin/containerd-rootless.sh
curl -L https://raw.githubusercontent.com/containerd/nerdctl/main/extras/rootless/containerd-rootless-setuptool.sh > ~/bin/containerd-rootless-setuptool.sh
chmod +x ~/bin/containerd-rootless-setuptool.sh
sudo apt-get install -y rootlesskit

~/bin/containerd-rootless-setuptool.sh install
~/bin/containerd-rootless-setuptool.sh install-buildkit

CNI_VERSION=1.4.0
if [ "$(uname -m)" = "x86_64" ]; then
    ARCH=amd64
elif [ "$(uname -m)" = "aarch64" ]; then
    ARCH=arm64
else
    echo "This system is not amd64 or aarch64."
    exit 1
fi

mkdir -p ~/tmp/cni
cd ~/tmp/cni
curl -OL https://github.com/containernetworking/plugins/releases/download/v${CNI_VERSION}/cni-plugins-linux-${ARCH}-v${CNI_VERSION}.tgz
tar -zxvf cni-plugins-linux-amd64-v1.4.0.tgz
sudo mkdir -p /opt/cni/bin
sudo mv * /opt/cni/bin/
