# -- .bashrc for devcontainer -
export EDITOR=code
export CLICOLOR=1

# vimっぽい
set -o vi

alias ll="ls -alh"
alias g="git"
alias gt="git status"

git config --global core.editor 'code --wait'

function __show_exitcode() {
    _EXITCODE=$?
    if [ $_EXITCODE -ne 0 ]; then echo -e "\e[31m$_EXITCODE\e[m "; fi
}

function __show_relative_path() {
    local current_dir=$(pwd)
    local workspace_dir="${WORKSPACE_DIR%/}"

    # $WORKSPACE_DIR配下では、ワークスペースからの相対パスを表示する
    # $WORKSPACE_DIR             -> .
    # $WORKSPACE_DIR/sub/path    -> ./sub/path
    if [[ -n "$workspace_dir" && ( "$current_dir" == "$workspace_dir" || "$current_dir" == "$workspace_dir"/* ) ]]; then
        local relative_path="${current_dir#"$workspace_dir"}"
        if [[ -z "$relative_path" ]]; then
            echo "."
        else
            echo ".${relative_path}"
        fi
    else
        # $WORKSPACE_DIRが未設定、またはその配下ではない場合は通常のパス表示
        echo "$current_dir"
    fi
}

PS1='$(__show_exitcode)$(__show_relative_path) $ '

# 人間らしいgitコマンド
declare -A humanize_aliases=(
    [branches]="git branch -a"
    [add-line]="git add -p"
    [add-line-edit]="git add -e"
    [stashes]="git stash list"
    [stash-all]="git stash -u"
    [unstage]="git reset"
    [unstage-all]="git reset -q HEAD --"
    [discard]="git checkout --"
    [discard-all]="git reset --hard && git clean -fd"
    [uncommit]="git reset --mixed HEAD~"
    [commit-first]="git commit --allow-empty -m 'first commit'"
    [amend]="git commit --amend"
    [delete-branch]="git branch -d"
    [tags]="git tag"
    [push-with-tags]="git push && git push --tags"
    [push-with-tags-and-follow]="git push -u && git push --tags"
    [follow]='git branch --set-upstream-to=origin/$(git symbolic-ref --short HEAD)'
    [graph]="git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative"
    [unmerged]="git diff --name-only --diff-filter=U"
    [history]="git log -10 --format=format:'%Cgreen%h %Creset• %s (%cN, %ar)'"
    [swdev]="git fetch origin && git switch -m -C develop origin/develop"
    [swmain]="git fetch origin && git switch -m -C main origin/main"
    [swmaster]="git fetch origin && git switch -m -C main origin/master"
)

# 省略形
declare -A easy_aliases=(
    [cm]="commit"
    [pu]="push-with-tags-and-follow"
    [sw]="switch"
    [st]="status"
    [swp]="switch-peco"
    [swf]="switch-origin"
    [swcf]="switch-create-from"
    [pt]="push-with-tags"
)

for alias_name in "${!humanize_aliases[@]}"; do
    git config --global "alias.${alias_name}" "!set -x && ${humanize_aliases[$alias_name]}"
done

for alias_name in "${!easy_aliases[@]}"; do
    git config --global "alias.${alias_name}" "${easy_aliases[$alias_name]}"
done
unset alias_name
