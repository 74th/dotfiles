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
set fish_color_autosuggestion 875f00
set fish_color_command ffffff
set fish_color_comment 990000
set fish_color_cwd green
set fish_color_cwd_root red
set fish_color_end 009900
set fish_color_error ff0000
set fish_color_escape bryellow\x1e\x2d\x2dbold
set fish_color_history_current \x2d\x2dbold
set fish_color_host normal
set fish_color_match \x2d\x2dbackground\x3dbrblue
set fish_color_normal normal
set fish_color_operator bryellow
set fish_color_param 00afff
set fish_color_quote 999900
set fish_color_redirection 00afff
set fish_color_search_match bryellow\x1e\x2d\x2dbackground\x3dbrblack
set fish_color_selection white\x1e\x2d\x2dbold\x1e\x2d\x2dbackground\x3dbrblack
set fish_color_status red
set fish_color_user brgreen
set fish_color_valid_path \x2d\x2dunderline

#--------------------------------------
# 文字コードの標準設定
set -x LESSCHARSET UTF-8
set -x LANG en_US.UTF-8
set -x LC_CTYPE en_US.UTF-8
set -x LC_ALL en_US.UTF-8

#--------------------------------------
# PATH
if test $OSNAME = 'Mac'
	set -x PATH /usr/local/bin ~/dotfiles/bin/darwin $PATH
end
if test $OSNAME = 'Linux'
	set -x PATH ~/dotfiles/bin/linux $PATH
end
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
if test -e ~/dotfiles/dotfile/bin
	set -x PATH ~/dotfiles/dotfile/bin $PATH
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

function ShowCheatSheets --description 'show my cheat sheets'
	ls ~/mycheatsheets/ | peco | read sheet
	less ~/mycheatsheets/$sheet
end

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

#--------------------------------------
# peco
function peco_ls
	commandline|read CMD
	if test $CMD = ""
		# なにもないときはhistory
		history|peco $peco_flags|read foo
		if [ $foo ]
			commandline $foo
		else
			commandline ''
		end
	else
		echo $CMD|pecols|read foo
		if [ $foo ]
			commandline -r $foo
		end
	end
end

function OpenBookmark
	cat ~/bookmark | peco | read DIR
	if [ $DIR ]
		cd $DIR
	end
end
alias bk=OpenBookmark
function AddBookmark
	pwd >> ~/bookmark
end

#--------------------------------------
# Cheat Sheets
function fish_user_key_bindings
	# peco
	bind -M insert \cr 'peco_ls'
	# 第一候補を確定
	bind -M insert \ck forward-char
end

#--------------------------------------
# Cheat Sheets
if test -e $HOME/mycheatsheets
	function OpenCheatSheets
		ls $HOME/mycheatsheets|peco|read sheet
		vim $HOME/mycheatsheets/$sheet
	end
	alias ShowCheatSheets=OpenCheatSheets
	alias oc=OpenCheatSheets
	function EditCheatSheets
		cd ~/mycheatsheets/
		git pull origin master
		ls $HOME/mycheatsheets|peco|read sheet
		vim ~/mycheatsheets/$sheet
		git add -A
		git commit -m "at $HOSTNAME"
		git push origin master
		cd -
	end
	alias ec=EditCheatSheets
end

#--------------------------------------
# ローカル設定
if test -e $HOME/.config.fish
	source $HOME/.config.fish
end
