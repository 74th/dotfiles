#!/bin/bash
gsettings set org.gnome.desktop.interface scaling-factor 2
xrandr --output DP-0 --scale 1.5x1.5
xinput set-prop 'Logitech Rechargeable Touchpad T650' 'Trackpad Scroll Buttons' 5 4 6 7
xinput set-prop 'Logitech Rechargeable Touchpad T650' 'Trackpad Drag Settings' 0 350 40 200
xinput set-prop 'Logitech Rechargeable Touchpad T650' 'Trackpad Scroll Distance' 30
