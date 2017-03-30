# windowsのgit表示
function __parse_git_branch_windows
	set _GITBRANCH (git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \\(.*\\)/\\1/')
	if not test "$_GITBRANCH" = "" 
		echo -n ' '
		echo -n $_GITBRANCH
	end
end
function fish_prompt --description 'Write out the prompt'

	set -l last_status $status

	if not test $last_status -eq 0
		set_color $fish_color_error
		echo -n $last_status
		echo -n " "
		set_color normal
	end

	# User
	set_color $fish_color_user
	echo -n (whoami)
	set_color normal

	echo -n '@'

	# Host
	set_color $fish_color_host
	echo -n (prompt_hostname)
	set_color normal

	echo -n ' '

	# PWD
	set_color $fish_color_cwd
	echo -n (prompt_pwd)
	set_color normal

	if test $OSNAME = 'Windows'
		__parse_git_branch_windows
	else
		__fish_git_prompt
	end
	__fish_hg_prompt
	echo

	if test $TERM = 'screen' -o $TERM = 'screen-bce'
		hostname|read HOSTNAME
		expr $HOSTNAME : '\(...\).*'|read h3
		pwd|read PWD
		basename $PWD|read PWD2
		echo -ne "\033k$h3@$PWD2\033\\"
	end

	if not test $last_status -eq 0
		set_color $fish_color_error
	end

	echo -n '$'
	set_color normal

end
