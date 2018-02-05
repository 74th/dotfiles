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

function OpenBookmark --description 'open bookmark'
	cat ~/bookmark | peco | read DIR
	if [ $DIR ]
		cd $DIR
	end
end
alias bk=OpenBookmark
function AddBookmark --description 'add bookmark'
	pwd >> ~/bookmark
end

