import invoke
from invoke import task, Context, Result


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
    c.run('git config --global alias.unstage "reset -q HEAD --"', env=env)
    c.run('git config --global alias.discard "checkout --"', env=env)
    c.run('git config --global alias.uncommit "reset --mixed HEAD~"', env=env)
    c.run('git config --global alias.amend "commit --amend"', env=env)
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

    # vimを使用
    c.run('git config --global core.editor "vi"', env=env)

    # 日本語の文字化けを治す
    c.run("git config --global core.quotepath false", env=env)

    # オープンソース用の名前を適用する
    c.run(
        'git config --global alias.setnnyn "!git config --local user.name 74th && git config --local user.email site@74th.tech"',
        env=env,
    )

    # pull では rebase を優先する
    c.run("git config --global pull.rebase false")
    # rebase のときに自動で stash save pop する
    c.run("git config --global rebase.autostash true")

    # ghq
    c.run("git config --global ghq.user 74th")
    c.run("git config --global commit.gpgsign true")

    # gpg key
    # gpg --import gpgkey.key
    c.run("git config --global user.signingkey 275E8CC7AD40E892")

    # username
    c.run('git config --global user.name "Atsushi Morimoto (74th)"', env=env)
    c.run("git config --global user.email site@74th.tech", env=env)


@task
def chmod_config(c):
    c.run("chmod 600 ~/.gitconfig")
