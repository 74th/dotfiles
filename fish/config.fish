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
# プロンプトのディレクトリを省略しない
set -U fish_prompt_pwd_dir_length 0

#--------------------------------------
# 文字コードの標準設定
set LESSCHARSET UTF-8
set LANG en_US.UTF-8
set LC_CTYPE en_US.UTF-8
set LC_ALL en_US.UTF-8

#--------------------------------------
# PATH
if test -e $HOME/go
	set PATH $HOME/go/bin $PATH
end
if test -e $HOME/npm
	set PATH $HOME/npm/bin $PATH
end
if test -e $HOME/bin
	set PATH $HOME/bin $PATH
end
set PATH $HOME/dotfiles/bin $PATH
if test $OSNAME = 'Mac'
	set PATH /usr/local/bin ~/dotfiles/bin/darwin $PATH
end
if test -e ~/dotfiles/dotfile/bin
	set PATH ~/dotfiles/dotfile/bin $PATH
end


#--------------------------------------
# MacVim
if test $OSNAME = "Mac"
	alias vi='env LANG=ja_JP.UTF-8 /Applications/MacVim.app/Contents/MacOS/Vim "$argv"'
	alias vim='env LANG=ja_JP.UTF-8 /Applications/MacVim.app/Contents/MacOS/Vim "$argv"'
	alias gvim='env LANG=ja_JP.UTF-8 /Applications/MacVim.app/Contents/MacOS/gvim "$argv"'
	alias vimless='/Applications/MacVim.app/Contents/Resources/vim/runtime/macros/less.sh'
end

#--------------------------------------
# エディターはVim
if test $OSNAME = "Mac"
	set EDITOR /Applications/MacVim.app/Contents/MacOS/Vim
else
	set EDITOR vi
end

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
alias g=git
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
alias commit='git commit -v'
alias commita='git commit -av'
alias add='git add'
alias push='git push'
alias pull='git pull'
alias gt='git status'

#--------------------------------------
# golang
if test -e $HOME/go
	set GOPATH $HOME/go
	set PATH $GOPATH/bin $PATH
end
if test $OSNAME = "Mac"
	set GOROOT /usr/local/opt/go/libexec
else if test $OSNAME = "Windows"
	set GOROOT C:\\tools\\go
	set GOPATH C:\\Users\\$USERNAME\\go
else if test -e $HOME/goroot/go/bin
	set GOROOT $HOME/goroot/go
	set PATH $HOME/goroot/go/bin $PATH
else if test -e $HOME/goroot/bin
	set GOROOT $HOME/goroot
	set PATH $HOME/goroot/bin $PATH
end
alias golinux='env GOOS=linux GOARCH=amd64 go'
alias goarm='env GOOS=linux GOARCH=arm go'
alias gowindows='env GOOS=windows GOARCH=amd64 go'
alias gomac='env GOOS=darwin GOARCH=amd64 go'

#--------------------------------------
# vscode
if test $OSNAME = "Mac"
	function code --description 'VSCode'
	env VSCODE_CWD="$PWD" open -n -b "com.microsoft.VSCode" --args $argv
	end
end

