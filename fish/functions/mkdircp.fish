function mkdircp --description 'mkdir and cp'
	if test (count $argv) = 0 
		echo 'mkdircp file... dir'
		return 1
	else
		if not test -e $argv[-1]
			mkdir -p $argv[-1]
		end
		cp $argv
	end
end


