# config.fish

#--------------------------------------
# OS判定
if test (uname) = 'Darwin'
	set OSNAME 'Mac'
	set OSDISTRO 'Mac'
else if test (uname -o) = 'Cygwin'
	set OSNAME 'Windows'
	set OSDISTRO 'Cygwin'
else if test (uname -o) = 'Msys'
	set OSNAME 'Windows'
	set OSDISTRO 'Msys'
else if test -e "/etc/debian_version"
	set OSNAME 'Linux'
	set OSDISTRO 'Debian'
else if test -e "/etc/redhat-release"
	set OSNAME 'Linux'
	set OSDISTRO 'Redhat'
else
	set OSNAME 'Linux'
	set OSDISTRO 'unknown'
end

#--------------------------------------
# fish
# viキーバインド
fish_vi_key_bindings
# viキーバインドのモードは表示しない
function fish_mode_prompt; end
# プロンプトのディレクトリを省略しない
set -U fish_prompt_pwd_dir_length 0

# 色設定
# fished.xxx からコピー
SET fish_color_command:ffffff
SET fish_color_comment:990000
SET fish_color_cwd:green
SET fish_color_cwd_root:red
SET fish_color_end:009900
SET fish_color_error:ff0000
SET fish_color_escape:bryellow\x1e\x2d\x2dbold
SET fish_color_history_current:\x2d\x2dbold
SET fish_color_host:normal
SET fish_color_match:\x2d\x2dbackground\x3dbrblue
SET fish_color_normal:normal
SET fish_color_operator:bryellow
SET fish_color_param:00afff
SET fish_color_quote:999900
SET fish_color_redirection:00afff
SET fish_color_search_match:bryellow\x1e\x2d\x2dbackground\x3dbrblack
SET fish_color_selection:white\x1e\x2d\x2dbold\x1e\x2d\x2dbackground\x3dbrblack
SET fish_color_status:red
SET fish_color_user:brgreen
SET fish_color_valid_path:\x2d\x2dunderline

#--------------------------------------
# 文字コードの標準設定
set -x LESSCHARSET UTF-8
set -x LANG en_US.UTF-8
set -x LC_CTYPE en_US.UTF-8
set -x LC_ALL en_US.UTF-8

#--------------------------------------
# PATH
if test -e $HOME/go
	set -x PATH $HOME/go/bin $PATH
end
if test -e $HOME/npm
	set -x PATH $HOME/npm/bin $PATH
end
if test -e $HOME/bin
	set -x PATH $HOME/bin $PATH
end
set PATH $HOME/dotfiles/bin $PATH
if test $OSNAME = 'Mac'
	set -x PATH /usr/local/bin ~/dotfiles/bin/darwin $PATH
end
if test -e ~/dotfiles/dotfile/bin
	set -x PATH ~/dotfiles/dotfile/bin $PATH
end


#--------------------------------------
# MacVim
if test $OSNAME = "Mac"
	alias gvim='env LANG=ja_JP.UTF-8 /Applications/MacVim.app/Contents/MacOS/gvim'
end

#--------------------------------------
# エディターはVim
set -x EDITOR vi

#--------------------------------------
# コマンド簡単化
alias FreezeTargz='tar zcvf'
alias OpenTargz='tar zxvf'
alias FreezeTarbz2='tar jcvf'
alias OpenTarbz2='tar jxvf'
alias ShowListenPorts='netstat -lnptua'
alias df='df -h'
alias ":q"=exit
alias ConvertLfAll='find . -type f | xargs -n 10 nkf -Lu --overwrite'
alias m=make
alias s7l='sudo systemctl'
alias sl=ls

#--------------------------------------
# Javacの文字コード
alias javac='javac -J-Dfile.encoding=utf-8'
alias java='java -Dfile.encoding=UTF-8'

#--------------------------------------
# ImageMagic関連
alias ConvertToJpg='mogrify -format jpg'
alias ConvertToPng='mogrify -format png'

#--------------------------------------
# git周り
function pushpush --description 'git commit and push'
	git add -A
	git commit -m "at $HOSTNAME"
	git push origin master
end
alias g=git
alias commit='git commit -v'
alias commita='git commit -av'
alias add='git add'
alias push='git push'
alias pull='git pull'
alias gt='git status'

# Fish git prompt
set __fish_git_prompt_showdirtystate 'yes'
set __fish_git_prompt_showstashstate 'yes'
set __fish_git_prompt_showuntrackedfiles 'yes'
set __fish_git_prompt_showupstream 'yes'
set __fish_git_prompt_color_branch yellow
set __fish_git_prompt_color_upstream_ahead green
set __fish_git_prompt_color_upstream_behind red

#--------------------------------------
# golang
if test -e $HOME/go
	set -x GOPATH $HOME/go
	set -x PATH $GOPATH/bin $PATH
end
if test $OSNAME = "Mac"
	set -x GOROOT /usr/local/opt/go/libexec
else if test $OSNAME = "Windows"
	set -x GOROOT C:\\tools\\go
	set -x GOPATH C:\\Users\\$USERNAME\\go
else if test -e $HOME/goroot/go/bin
	set -x GOROOT $HOME/goroot/go
	set -x PATH $HOME/goroot/go/bin $PATH
else if test -e $HOME/goroot/bin
	set -x GOROOT $HOME/goroot
	set -x PATH $HOME/goroot/bin $PATH
end
alias golinux='env GOOS=linux GOARCH=amd64 go'
alias goarm='env GOOS=linux GOARCH=arm go'
alias gowindows='env GOOS=windows GOARCH=amd64 go'
alias gomac='env GOOS=darwin GOARCH=amd64 go'

# デバッグ
if type dlv 2>/dev/null 1>/dev/null
	function dlv_test --description 'debug golang test'
		dlv test --headless --listen "0.0.0.0:2345" --log=true
		eval $GOPATH/bin/dlv test --headless --listen "0.0.0.0:2345" --log=true
	end
end

# GOPATHへの移動
if test -e $GOPATH/src/github.com/74th
	function CDGOPATH --description 'change directory to GOPATH'
		cd $GOPATH/src/github.com/74th
	end
end

#--------------------------------------
# vscode
if test $OSNAME = "Mac"
	function code --description 'VSCode'
	env VSCODE_CWD="$PWD" open -n -b "com.microsoft.VSCode" --args $argv
	end
end

