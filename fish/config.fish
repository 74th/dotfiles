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
# Git周り
alias g=git

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
	set PATH ~/dotfiles/bin/darwin /usr/local/bin $PATH
end

