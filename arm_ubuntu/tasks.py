from invoke import task

ubuntu_pkgs = [
    "direnv",
    "python3",
    "python3-pip",
    "peco",
    "nodejs",
    "vim",
]

@task
def install(c):
    c.run("sudo apt update")
    pkgs = " ".join(ubuntu_pkgs)
    c.run(f"sudo apt install {pkgs}")

    if c.run("which pyenv", warn=True).failed:
        c.run("git clone https://github.com/pyenv/pyenv.git ~/.pyenv")
