copy %USERPROFILE%\dotfiles\vimrc\rootvimrc.vim %USERPROFILE%\.vimrc
copy %USERPROFILE%\dotfiles\vimrc\rootgvimrc.vim %USERPROFILE%\.gvimrc

IF EXIST %USERPROFILE%\.vim\bundle GOTO SKIP
mkdir -p %USERPROFILE%\.vim\bundle
git clone https://github.com/Shougo/neobundle.vim %USERPROFILE%\.vim\bundle\neobundle.vim
:SKIP
