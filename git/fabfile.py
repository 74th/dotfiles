# -*- coding: utf-8 -*-
import invoke
from invoke import task

@task(default=True)
def set_config(c):
    print("## git set configs")

    # 改行コード対策
    c.run('git config --global core.autocrlf false')
    # CRLFをコミットしようとしたらエラー
    c.run('git config --global core.safecrlf true')

    # pushは現在のブランチをプッシュする
    c.run('git config --global push.default current')

    # globalのGitIgnore
    c.run('git config --global core.excludesfile ~/dotfiles/git/.gitignore')

    # git diffの並列実行
    c.run('git config --global core.preloadindex true')

    # 色を付ける
    c.run('git config --global color.ui true')

    # 人間らしいgitコマンド
    c.run('git config --global alias.branches "branch -a"')
    c.run('git config --global alias.addline "add -p"')
    c.run('git config --global alias.addlineedit "add -e"')
    c.run('git config --global alias.addremove "reset"')
    c.run('git config --global alias.tags "tag"')
    c.run('git config --global alias.stashes "stash list"')
    c.run('git config --global alias.unstage "reset -q HEAD --"')
    c.run('git config --global alias.discard "checkout --"')
    c.run('git config --global alias.uncommit "reset --mixed HEAD~"')
    c.run('git config --global alias.amend "commit --amend"')
    c.run("git config --global alias.graph \"log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative\"")
    c.run('git config --global alias.unmerged "diff --name-only --diff-filter=U"')
    c.run("git config --global alias.history \"log -10 --format=format:'%Cgreen%h %Creset• %s (%cN, %ar)'\"")
    c.run('git config --global alias.deleteuntrackedfile "logi clean -f"')

    # やっぱり楽なコマンドが良い
    c.run('git config --global alias.st "status"')

    # やっぱり楽なコマンドが良い
    c.run('git config --global alias.upstreamtomaster "branch --set-upstream-to=origin/master master"')

    # vimを使用
    c.run('git config --global core.editor "vi"')

    # 日本語の文字化けを治す
    c.run('git config --global core.quotepath false')


    # Windowsの場合、以下も追加する
    # ファイルモードを無視
    # git config --global core.filemode false
