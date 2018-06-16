#!/bin/bash
set -Ceux
go get -u \
	sourcegraph.com/sqs/goreturns\
	github.com/golang/lint/golint\
	github.com/jessevdk/go-assets\
	github.com/jessevdk/go-assets-builder\
	github.com/peco/peco/cmd/peco\
	github.com/golang/dep/cmd/dep\
	github.com/derekparker/delve/cmd/dlv
