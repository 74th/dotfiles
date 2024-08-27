import datetime
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

    # 人間らしいgitコマンド
    c.run('git config --global alias.branches "branch -a"', env=env)
    c.run('git config --global alias.addline "add -p"', env=env)
    c.run('git config --global alias.addlineedit "add -e"', env=env)
    c.run('git config --global alias.addremove "reset"', env=env)
    c.run('git config --global alias.tags "tag"', env=env)
    c.run('git config --global alias.stashes "stash list"', env=env)
    c.run('git config --global alias.stash-all "stash -u"', env=env)
    c.run('git config --global alias.unstage "reset -q HEAD --"', env=env)
    c.run('git config --global alias.discard "checkout --"', env=env)
    c.run('git config --global alias.uncommit "reset --mixed HEAD~"', env=env)
    c.run('git config --global alias.amend "commit --amend"', env=env)
    c.run('git config --global alias.reset-all "!git reset --hard && git clean -fd"', env=env)
    c.run(
        "git config --global alias.graph \"log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative\"",
        env=env,
    )
    c.run(
        'git config --global alias.unmerged "diff --name-only --diff-filter=U"', env=env
    )
    c.run(
        "git config --global alias.history \"log -10 --format=format:'%Cgreen%h %Creset• %s (%cN, %ar)'\"",
        env=env,
    )
    c.run('git config --global alias.deleteuntrackedfile "logi clean -f"', env=env)

    # めんどくなってきた
    c.run('git config --global alias.c "checkout"', env=env)
    c.run('git config --global alias.b "branch"', env=env)
    c.run('git config --global alias.p "push"', env=env)
    c.run('git config --global alias.sw "switch"', env=env)
    c.run('git config --global alias.swp "switch-peco"', env=env)
    c.run('git config --global alias.swf "switch-origin"', env=env)
    c.run('git config --global alias.pt "push-with-tags"', env=env)

    # やっぱり楽なコマンドが良い
    c.run('git config --global alias.st "status"', env=env)

    # masterを追う
    c.run(
        'git config --global alias.upstreamtomaster "branch --set-upstream-to=origin/master master"',
        env=env,
    )

    # 最初の空コミット
    c.run(
        "git config --global alias.firstcommit \"commit --allow-empty -m 'first commit'\"",
        env=env,
    )

    # ブランチをpecoでswitch
    c.run(
        'git config --global alias.switchp "!git-switch-peco"',
        env=env,
    )

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
