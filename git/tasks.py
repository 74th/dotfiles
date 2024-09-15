import datetime
import shlex
from invoke.tasks import task


@task(default=True)
def set_config(c):
    print("## git set configs")

    env = {}
    if len(c.run("echo $HOME", hide=True).stdout.strip()) == 0:
        env["HOME"] = c.run("cd ~;pwd", hide=True).stdout.strip()

    # 改行コード対策
    c.run("git config --global core.autocrlf false", env=env)
    # CRLFをコミットしようとしたらエラー
    c.run("git config --global core.safecrlf true", env=env)

    # pushは現在のブランチをプッシュする
    c.run("git config --global push.default current", env=env)

    # globalのGitIgnore
    c.run("git config --global core.excludesfile ~/dotfiles/git/.gitignore", env=env)

    # git diffの並列実行
    c.run("git config --global core.preloadindex true", env=env)

    # 色を付ける
    c.run("git config --global color.ui true", env=env)

    # master push時の警告
    c.run("git config --global init.templatedir ~/dotfiles/git/template/", env=env)

    # master push時の警告
    c.run("git config --global init.defaultBranch main", env=env)

    # https://zenn.dev/hiro8_hiro8/articles/d63b3bfbe2c86e
    c.run("git config --global http.postBuffer 524288000", env=env)

    # 人間らしいgitコマンド
    humanize_aliases = {
        "branches": "git branch -a",
        "add-line": "git add -p",
        "add-line-edit": "git add -e",
        "stashes": "git stash list",
        "stash-all": "git stash -u",
        "unstage": "git reset",
        "unstage-all": "git reset -q HEAD --",
        "discard": "git checkout --",
        "discard-all": "git reset --hard && git clean -fd",
        "uncommit": "git reset --mixed HEAD~",
        "commit-first": "git commit --allow-empty -m 'first commit'",
        "amend": "git commit --amend",
        "delete-branch": "git branch -d",
        "tags": "git tag",
        "push-with-tags": "git push && git push --tags",
        "push-with-tags-and-follow": "git push -u && git push --tags",
        "follow": "git branch --set-upstream-to=origin/$(git symbolic-ref --short HEAD)",
        "graph": "git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative",
        "unmerged": "git diff --name-only --diff-filter=U",
        "history": "git log -10 --format=format:'%Cgreen%h %Creset• %s (%cN, %ar)'",
    }

    for alias, command in humanize_aliases.items():
        cmd = shlex.quote(f"!set -x && {command}")
        c.run(f"git config --global alias.{alias} {cmd}", env=env)

    # 省略形
    easy_aliases = {
        "cm": "commit",
        "pu": "push-with-tags-and-follow",
        "sw": "switch",
        "st": "status",
        "swp": "switch-peco",
        "swf": "switch-origin",
        "swcf": "switch-create-from",
        "pt": "push-with-tags",
    }

    for alias, command in easy_aliases.items():
        c.run(f'git config --global alias.{alias} "{command}"', env=env)

    # vimを使用
    c.run('git config --global core.editor "vi"', env=env)

    # 日本語の文字化けを治す
    c.run("git config --global core.quotepath false", env=env)

    # pull では rebase を優先する
    c.run("git config --global pull.rebase false")
    # rebase のときに自動で stash save pop する
    c.run("git config --global rebase.autostash true")

    # ghq
    c.run("git config --global ghq.user 74th")
    c.run("git config --global commit.gpgsign true")

    # gpg key
    # gpg --import gpgkey.key
    # c.run("git config --global user.signingkey 275E8CC7AD40E892")

    # username
    c.run('git config --global user.name "Atsushi Morimoto (74th)"', env=env)
    c.run("git config --global user.email 74th.tech@gmail.com", env=env)


@task
def chmod_config(c):
    c.run("chmod 600 ~/.gitconfig")


@task
def create_gpg(c):
    c.run("which gpg")
    if not c.run("gh gpg-key list", warn=True).ok:
        print("gh auth refresh -s write:gpg_key")
        return

    c.run(
        "gpg --batch --passphrase '' --quick-gen-key \"Atsushi Morimoto (74th) <74th.tech@gmail.com>\" default default never"
    )
    stdout: list[str] = c.run("gpg  --list-keys").stdout.splitlines()
    for i, l in enumerate(stdout):
        r = l.split(" ")
        if "pub" in r and "[SC]" in r:
            key_id = stdout[i + 1].strip()
            break

    hostname = c.run("hostname").stdout.strip()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    c.run(f"gpg --armor --export {key_id} > gpg.key")
    c.run(f'gh gpg-key add ./gpg.key --title "{hostname} {current_date}"')
    c.run("rm gpg.key")

    c.run("git config --global gpg.program gpg")
    c.run("git config --global commit.gpgsign true")
    c.run(f"git config --global user.signingkey {key_id}")
