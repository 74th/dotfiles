function mkdircd --description 'mkdir and cd'
	if test (count $argv) = 0 
		echo 'mkdircd dir'
		return 1
	else
		if not test -e $argv[1]
			mkdir -p $argv[1]
		end
		cd $argv[1]
	end
end

