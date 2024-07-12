import os
import tempfile

from invoke.tasks import task


def add_source_list(c):
    # gh -> miniconda を使おう
    if os.path.exists("/etc/apt/sources.list.d/github-cli.list"):
        return

    # https://github.com/cli/cli/blob/trunk/docs/install_linux.md
    # c.run(
    #    "curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg"
    # )
    # c.run(
    #    """echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null"""
    # )
    # c.run("sudo apt-add-repository https://cli.github.com/packages")


def add_source_list_desktop(c):
    # vscode
    # https://code.visualstudio.com/docs/setup/linux#_debian-and-ubuntu-based-distributions
    c.run(
        "curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg"
    )
    c.run(
        "sudo install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/"
    )
    c.run(
        "sudo sh -c 'echo \"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main\" > /etc/apt/sources.list.d/vscode.list'"
    )
    c.run("rm packages.microsoft.gpg")


def is_ubuntu():
    if not os.path.exists("/etc/lsb-release"):
        return False
    with open("/etc/lsb-release") as f:
        body = f.read()
    return body.count("Ubuntu") >= 0


@task
def update(c):
    c.run("sudo apt-get update")


@task
def install_classic_snap_pkgs(c):
    pkgs = ["google-cloud-sdk"]
    pkgs_str = " ".join(pkgs)

    c.run("sudo snap install --classic " + pkgs_str)


def _list_packages() -> list[str]:
    pkgs: list[str] = []
    pkgs += [
        "jq",
        "peco",
        "xclip",
        "docker-compose",
        "readline-common",
        "git",
        "git-secrets",
        "bzip2",
        "unar",
        # "nodejs",
        # "npm",
        "apt-transport-https",
        "protobuf-compiler",
        "curl",
        "vim",
        "direnv",
        "cargo",
        "python3-venv",
        "python-is-python3",
        "pipx",
        "trash-cli",
    ]
    return pkgs


@task
def install(c):
    add_source_list(c)
    pkgs = _list_packages()
    c.run("sudo apt-get update")
    c.run("sudo apt-get install -y " + " ".join(pkgs))


def _list_desktop_packages() -> list[str]:
    pkgs: list[str] = []
    pkgs += [
        "guake",
        "fcitx",
        "fcitx-mozc",
        "xbindkeys",
        "vim-gtk",
        "font-manager",
        "libinput-tools",
        "wmctrl",
        "xdotool",
        "gnome-tweaks",
        "code",
        "code-insiders",
        "shutter",
        "python3-packaging",
        # desktop tools
        "gimp",
        "inkscape",
        "easytag",
        # system monitor
        "gir1.2-gtop-2.0",
        "gir1.2-nm-1.0",
        "gir1.2-clutter-1.0",
        # grub
        "grub-customizer",
        # gtk theme
        "gtk2-engines-murrine",
        "gtk2-engines-pixbuf",
    ]
    return pkgs


@task
def libinput_gestures(c):
    if c.run("which libinput-gestures-setup", warn=True).ok:
        return
    with tempfile.TemporaryDirectory() as tmp:
        with c.cd(tmp):
            c.run("git clone https://github.com/bulletmark/libinput-gestures.git")
            with c.cd("libinput-gestures"):
                c.run("sudo ./libinput-gestures-setup install")
    c.run("libinput-gestures autostart start")


@task
def zfs_auto_snapshot(c):
    c.run("sudo cp ./zfs-auto-snapshot/frequency.crontab /etc/cron.d/zfs-auto-snapshot")
    c.run("sudo cp ./zfs-auto-snapshot/hourly.sh /etc/cron.hourly/zfs-auto-snapshot")
    c.run("sudo cp ./zfs-auto-snapshot/daily.sh /etc/cron.daily/zfs-auto-snapshot")
    c.run("sudo cp ./zfs-auto-snapshot/weekly.sh /etc/cron.weekly/zfs-auto-snapshot")
    c.run("sudo cp ./zfs-auto-snapshot/monthly.sh /etc/cron.monthly/zfs-auto-snapshot")


@task
def desktop_install(c):
    c.run("sudo add-apt-repository ppa:shutter/ppa -y")
    add_source_list_desktop(c)
    pkgs = _list_desktop_packages()
    c.run("sudo apt-get update")
    c.run("ln -sf ~/dotfiles/ubuntu/.xbindkeysrc ~/.xbindkeysrc")
    c.run("sudo apt-get install -y " + " ".join(pkgs))
    c.run("ln -sf ~/dotfiles/ubuntu/_config/libinput-gestures.conf ~/.config/")
    libinput_gestures(c)
