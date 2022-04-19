#!/bin/sh
sleep 7
killall NotificationCenter; true
/Users/atsushi.morimoto/go/bin/rcode -command /usr/local/bin/code -server -addr 10.37.129.2:5450
