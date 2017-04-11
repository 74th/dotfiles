#!/bin/bash
set -Ceux

launchctl unload ~/Library/LaunchAgents/setenv.plist
launchctl load ~/Library/LaunchAgents/setenv.plist
