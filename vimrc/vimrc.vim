syntax on

" いらんファイルを作らない
set nobackup
set noundofile

" TAB
set tabstop=4
set shiftwidth=4
set autoindent
set noexpandtab

" 自動改行を抑制
set textwidth=0

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

" マウスの利用
set mouse=a
set ttymouse=xterm2
