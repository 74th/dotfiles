#!/usr/bin/env -S uv run --script
import shlex
import subprocess

SOAP_VERSION = "v3.13.3"


def run(cmd: list[str]):
    print("\033[1m" + shlex.join(cmd) + "\033[0m")
    subprocess.run(cmd, check=True)


arch = subprocess.run(
    ["uname", "-m"], check=True, capture_output=True, text=True
).stdout.strip()
kernel = subprocess.run(
    ["uname", "-s"], check=True, capture_output=True, text=True
).stdout.strip()

if arch == "aarch64":
    arch = "arm64"

soap_url = f"https://github.com/getsops/sops/releases/download/{SOAP_VERSION}/sops-{SOAP_VERSION}.{kernel.lower()}.{arch}"
run(["curl", "-o/usr/local/bin/soap", "-L", soap_url])

run(["chmod", "+x", "/usr/local/bin/soap"])

if kernel == "Linux":
    run(["apt", "update"])
    run(["apt", "install", "-y", "age"])
if kernel == "Darwin":
    run(["brew", "install", "age"])
