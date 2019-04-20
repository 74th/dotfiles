" Windowsでもutf-8に設定しておく
set encoding=utf-8

syntax on

" 不要なファイルを作らない
set nobackup
set noundofile

" TAB
set tabstop=4
set shiftwidth=4
set autoindent
set expandtab
autocmd BufRead,BufNewFile *.go setlocal noexpandtab

" 自動改行を抑制
set textwidth=0

" Ctrl+aで常に10進数扱いにする
set nrformats=

" ルーラーを表示
set ruler

" CUIの場合
set background=dark

" 制御文字の表示
set list
set listchars=tab:>\ ,trail:-,extends:>,precedes:<,nbsp:%

" 文字コードを指定して再オープン
command! OpenUtf8 :e! ++enc=utf-8
command! OpenSjis :e! ++enc=cp932
command! OpenEucjp :e! ++enc=euc-jp

" 日本語表示
set ambiwidth=double

" マウスの利用 初期値は無効にしておく
set mouse=
set ttymouse=xterm2

" LFとutf-8を標準にする
set fileformats=unix,dos,mac
set fileencodings=utf-8,cp932

" jj でノーマルモードに戻る
inoremap <silent> jj <ESC>
" 覚えたいインサートモードのコマンド
" Ctrl-H BS
" Ctrl-J Enter 
" Ctrl-W BSの単語版

" プラグインマネージャ vim-plug https://github.com/junegunn/vim-plug
" 追加したら :PlugInstall を実行
if has('win32')
	call plug#begin('$HOME/vimfiles/plugged')
else
	call plug#begin('$HOME/.vim/plugged')
endif

" golang
Plug 'fatih/vim-go'

" markdown
"Plug 'godlygeek/tabular'
"Plug 'plasticboy/vim-markdown'
"let g:vim_markdown_folding_disabled = 2

" ティラノスクリプト
Plug 'bellflower2015/vim-syntax-tyranoscript'

" fish shell
Plug 'dag/vim-fish'

" type script
" npm install -g typescript
Plug 'Quramy/tsuquyomi'
" syntax
Plug 'leafgarland/typescript-vim'

" molokai
Plug 'tomasr/molokai'

" Re:View
Plug '74th/vim-review'

" Plantuml
Plug 'aklt/plantuml-syntax'

" python
Plug 'davidhalter/jedi-vim'

call plug#end()

" CUIでも256colorならmolokaiを使う
if &term == "xterm-256color"
    colorscheme molokai
    hi Comment ctermfg=102
    hi Visual  ctermbg=236
endif

autocmd BufRead,BufNewFile *.md set nolist
