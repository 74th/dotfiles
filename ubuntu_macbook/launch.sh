#!/bin/bash
echo 2 | sudo tee /sys/module/hid_apple/parameters/fnmode
echo 1 | sudo tee /sys/module/hid_apple/parameters/swap_opt_cmd
