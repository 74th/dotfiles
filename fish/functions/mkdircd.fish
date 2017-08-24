function mkdircd --description 'mkdir and cd'
	if test (count $argv) = 0 
		echo 'mkdircd <dir>'
	else
		mkdir $argv[1]
		cd $argv[1]
	end
end

