#!/bin/bash
sleep 3
xinput set-prop 'Apple Inc. Magic Trackpad 2' 'libinput Tapping Drag Enabled' 0
xinput set-prop "Apple Inc. Magic Trackpad 2" "libinput Tapping Enabled" 1
xinput set-prop "Apple Inc. Magic Trackpad 2" "libinput Natural Scrolling Enabled" 1
xinput set-prop "Apple Inc. Magic Trackpad 2" "libinput Accel Speed" 0.683824

xbindkeys -p
