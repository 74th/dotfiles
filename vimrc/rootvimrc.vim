"~/.vimrcにこれを上書きしよう！

"OS名
if has('gui_macvim') == 1 
    let g:j74OsName = 'Mac'
elseif has('win32')
    let g:j74OsName = 'Win'
else
    let g:j74OsName = 'Linux'
endif

"Specにより読み込むプラグインを制御する
"let g:j74Spec = 'high'

"git管理の.vim的ディレクトリ
let g:j74VimRepoPath = '~/dotfiles/vimrc/'

"ユーザディレクトリの.vimの場所（ほぼBundle用）
let g:j74UserDirectory = '~/.vim/'

"プロキシの有無
let g:j74isProxy = 0

"vimrcを開く
execute 'source ' . g:j74VimRepoPath . 'vimrc.vim'
