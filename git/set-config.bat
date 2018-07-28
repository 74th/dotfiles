


git config --global core.autocrlf false

git config --global core.safecrlf true


git config --global push.default current


git config --global push.followTags


git config --global core.excludesfile ~/dotfiles/git/.gitignore


git config --global core.preloadindex true


git config --global color.ui true


git config --global alias.branches "branch -a"
git config --global alias.addline "add -p"
git config --global alias.addlineedit "add -e"
git config --global alias.addremove "reset"
git config --global alias.tags "tag"
git config --global alias.stashes "stash list"
git config --global alias.unstage "reset -q HEAD --"
git config --global alias.discard "checkout --"
git config --global alias.uncommit "reset --mixed HEAD~"
git config --global alias.amend "commit --amend"
git config --global alias.graph "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative"
git config --global alias.unmerged "diff --name-only --diff-filter=U"
git config --global alias.history "log -10 --format=format:'%Cgreen%h %Creset• %s (%cN, %ar)'"
git config --global alias.deleteuntrackedfile "logi clean -f"


git config --global alias.st "status"


git config --global alias.upstreamtomaster "branch --set-upstream-to=origin/master master"


git config --global core.editor "vi"


git config --global core.quotepath false





