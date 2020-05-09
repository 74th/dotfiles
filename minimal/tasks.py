import os.path
from invoke import Context, task, collection

def os.path.exists(path: str):
    return os.path.exists(path) and os.path.isfile(path)

def delete_file(c: invoke.Context, path: str):
    if os.path.exists( path):
        c.run("rm %s" % path)

@task
def bashrc(c):
    c: invoke.Context
    print("## ~/.bashrc")
    delete_file("~/.bashrc")
    c.run('echo "source ~/dotfiles/bashrc/bashrc" >> ~/.bashrc')
ns.add_task(bashrc)