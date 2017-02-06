echo 改行コード対策
git config --global core.autocrlf false
echo CRLFをコミットしようとしたらエラー
git config --global core.safecrlf true

echo pushは現在のブランチをプッシュする
git config --global push.default current

echo tagのpush
git config --global push.followTags

echo globalのGitIgnore
git config --global core.excludesfile ~/dotfiles/git/.gitignore

echo git diffの並列実行
git config --global core.preloadindex true

echo 人間らしいgitコマンド
git config --global alias.branches "branch -a"
git config --global alias.addline "add -p"
git config --global alias.tags "tag"
git config --global alias.stashes "stash list"
git config --global alias.unstage "reset -q HEAD --"
git config --global alias.discard "checkout --"
git config --global alias.uncommit "reset --mixed HEAD~"
git config --global alias.amend "commit --amend"
git config --global alias.graph "log --graph -20 --branches --remotes --tags  --format=format:'%Cgreen%h %Creset• %<(75,trunc)%s (%cN, %cr) %Cred%d' --date-order"
git config --global alias.unmerged "diff --name-only --diff-filter=U"
git config --global alias.history "log -10 --format=format:'%Cgreen%h %Creset• %s (%cN, %ar)'"
git config --global alias.deleteuntrackedfile "logi clean -f"

echo やっぱり楽なコマンドが良い
git config --global alias.st "status"

# Windowsの場合、以下も追加する
# ファイルモードを無視
# git config --global core.filemode false
