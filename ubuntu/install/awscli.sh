#!/bin/bash
set -xe
rm -rf /tmp/awscli
mkdir /tmp/awscli
cd /tmp/awscli

ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
elif [ "$ARCH" = "aarch64" ]; then
    curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

unzip awscliv2.zip
if [ -f /usr/local/bin/aws ]; then
    sudo ./aws/install --update
else
    sudo ./aws/install
fi

rm -rf /tmp/awscli