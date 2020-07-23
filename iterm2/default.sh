#!/bin/bash
if [ "$(hostname)" == "kukrushka.local" ]; then
    /usr/local/bin/python3 -u -m xonsh
else
    /usr/bin/ssh -t violet xonsh
fi
