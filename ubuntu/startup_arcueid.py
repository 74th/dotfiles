#!/usr/local/bin/system-python
import time
import re
import subprocess


def setup_trackpad():
    settings = [
        ("libinput Tapping Drag Enabled", "0"),
        ("libinput Tapping Enabled", "1"),
        ("libinput Natural Scrolling Enabled", "1"),
        ("libinput Accel Speed", "1.0"),
    ]

    r = subprocess.run(
        ["xinput", "list", "--short"], check=True, capture_output=True, text=True
    )
    lines = r.stdout.splitlines()
    for line in lines:
        if not line.count("Apple Inc. Magic Trackpad"):
            continue
        device_id = list(re.findall(r"id=(\d+)", line))[0]
        for s in settings:
            subprocess.run(["xinput", "set-prop", device_id, s[0], s[1]])


def reload_xbindkeys():
    subprocess.run(["xbindkeys", "-p"], check=True, capture_output=True)


time.sleep(3)
setup_trackpad()
reload_xbindkeys()
