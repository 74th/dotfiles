#!/bin/bash
sleep 3
echo 2 | sudo tee /sys/module/hid_apple/parameters/fnmode
echo 1 | sudo tee /sys/module/hid_apple/parameters/swap_opt_cmd
xinput set-prop 'bcm5974' 'libinput Tapping Drag Enabled' 0
