copy %USERPROFILE%\dotfiles\vimrc\defaultvimrc.vim %USERPROFILE%\.vimrc
copy %USERPROFILE%\dotfiles\vimrc\defaultGvimrc.vim %USERPROFILE%\.gvimrc

IF EXIST %USERPROFILE%\.vim\bundle GOTO SKIP
mkdir -p %USERPROFILE%\.vim\bundle
git clone https://github.com/Shougo/neobundle.vim %USERPROFILE%\.vim\bundle\neobundle.vim
:SKIP
