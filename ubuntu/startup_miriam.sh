#!/bin/bash
sleep 3
gsettings set org.gnome.desktop.interface scaling-factor 2
xrandr --output DP-0 --scale 1.5x1.5
xrandr --output HDMI-0 --scale 1.5x1.5
xinput set-prop 'Apple Inc. Magic Trackpad 2' 'libinput Tapping Drag Enabled' 0
xbindkeys -p
