import os
import json
import os.path
import subprocess

hock_path = os.environ.get("VSCODE_IPC_HOOK_CLI", "")

code_path = ""
for p in os.environ.get("PATH", "").split(":"):
    if p.find("/.vscode-remote/bin/") >= 0:
        code_path = p

if not hock_path or not code_path:
    os._exit(0)

home = os.environ.get("HOME", "")
info_file = os.path.join(home, ".vscode-remote", "latest-info.json")
with open(info_file, "w") as f:
    j = {
        "hock": hock_path,
        "code": code_path,
    }
    json.dump(j,f)
