if g:j74NeoBundleExists == 1
    neobundle#append()
endif
"カラースキーマ---------------------------------------------
NeoBundle 'desert.vim'
NeoBundle 'w0ng/vim-hybrid'
NeoBundle 'jpo/vim-railscasts-theme'
NeoBundle 'vim-scripts/Wombat'
NeoBundle 'altercation/vim-colors-solarized'
"desert 2012/12/18
colorscheme molokai
"-----------------------------------------------------------
"フォント設定
if g:j74OsName == 'Mac'
    set guifont=Ricty\ Regular:h13
elseif g:j74OsName == 'Win'
    set guifont=Ricty\ Regular:h11
endif
"-----------------------------------------------------------
"vim-indent-guides インデントをハイライト表示する
NeoBundle 'nathanaelkane/vim-indent-guides'
let g:indent_guides_enable_on_vim_startup = 1
"設定した入りしなかったりは、以下でやる
":set IndentGuidesToggle
"-----------------------------------------------------------
"MacVimではIMEの自動オンオフをオン
" 2013/02/10
if g:j74OsName == 'Mac'
    set noimdisableactivate
endif
"-----------------------------------------------------------
"GVimrcを編集 2012/12/18
function! EditGVimrc()
    execute 'tabnew ' . g:j74VimRepoPath . 'gvimrc.vim'
endfunction
command! EditGVimrc :call EditGVimrc()
"-----------------------------------------------------------
"起動時サイズを大きくする
set lines=55
set columns=120
"-----------------------------------------------------------
"起動時サイズを大きくする
" ツールバー、メニューバーは表示しない
set guioptions=egrLt
"-----------------------------------------------------------
"メニューを表示する
command! ShowGuiMenu :set guioptions=egmrLtT<CR>
command! HideGuiMenu :set guioptions=egrLt<CR>
"-----------------------------------------------------------
if g:j74NeoBundleExists == 1
    call neobundle#end()
endif
