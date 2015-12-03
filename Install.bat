REM vim
IF EXIST %USERPROFILE%\.vimrc del %USERPROFILE%\.vimrc
copy %USERPROFILE%\dotfiles\vimrc\rootvimrc.vim %USERPROFILE%\.vimrc
IF EXIST %USERPROFILE%\.gvimrc del %USERPROFILE%\.gvimrc
copy %USERPROFILE%\dotfiles\vimrc\rootgvimrc.vim %USERPROFILE%\.gvimrc

REM bash
IF EXIST %USERPROFILE%\.bashrc del %USERPROFILE%\.bashrc
mklink /H %USERPROFILE%\.bashrc %USERPROFILE%\dotfiles\bashrc\bashrc 

REM VSCode
SET VSCODE_DIR=%USERPROFILE%\AppData\Roaming\Code\User
IF EXIST %VSCODE_DIR%\keybindings.json del %VSCODE_DIR%\keybindings.json
mklink /H %VSCODE_DIR%\keybindings.json %USERPROFILE%\dotfiles\vscode\keybindings.json
IF EXIST %VSCODE_DIR%\settings.json del %VSCODE_DIR%\settings.json
mklink /H %VSCODE_DIR%\settings.json %USERPROFILE%\dotfiles\vscode\settings.json
IF EXIST %VSCODE_DIR%\snippets rmdir /S /Q %VSCODE_DIR%\snippets
mklink /j %VSCODE_DIR%\snippets %USERPROFILE%\dotfiles\vscode\snippets
