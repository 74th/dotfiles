#!/bin/sh

# Only call zfs-auto-snapshot if it's available
which zfs-auto-snapshot > /dev/null || exit 0

exec zfs-auto-snapshot --quiet --syslog --label=monthly --keep=12 rpool/USERDATA
