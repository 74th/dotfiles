#!/bin/sh
sleep 7
killall NotificationCenter; true
/Users/atsushi.morimoto/go/bin/rcode -command code -server -addr 10.37.129.2:5450
