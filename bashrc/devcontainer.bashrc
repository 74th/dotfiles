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
    # /workspaces/で始まる場合の処理
    if [[ "$current_dir" == /workspaces/* ]]; then
        # /workspaces/projectname/sub/path -> ./sub/path のように変換
        # /workspaces/projectname -> ./ のように変換
        local relative_path=$(echo "$current_dir" | sed 's|^/workspaces/[^/]*||')
        if [[ -z "$relative_path" ]]; then
            echo "."
        else
            echo ".${relative_path}"
        fi
    else
        # /workspaces/以外の場合は通常のパス表示
        echo "$current_dir"
    fi
}

PS1='$(__show_exitcode)$(__show_relative_path) $ '
