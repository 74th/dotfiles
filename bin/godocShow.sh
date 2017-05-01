#!/bin/bash
set -Ceux

open -a "/Applications/Google Chrome.app" http://localhost:6060/pkg/
godoc -http :6060 -play
