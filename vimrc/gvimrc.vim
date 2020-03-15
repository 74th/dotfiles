colorscheme molokai

" メニューは表示しない
set guioptions=egrLt
command! ShowGuiMenu :set guioptions=egmrLtT<CR>

set lines=55
set columns=120

if has('gui_macvim')
	set guifont=Liga\ InputMono\ ExLight:h13
	set guifontwide=Hiragino\ Sans\ W1:h13
    " set noimdisableactivate
	set lsp=-1
elseif has('win32')
    set guifont=Source_Code_Pro_Light:h10:cANSI
    set guifontwide=源真ゴシック等幅_Light:h10:cSHIFTJIS
else
	set guifont=Source\ Code\ Variable\ Medium\ 12
	set guifontwide=Source\ Han\ Sans\ Semi-Light\ 10.5
endif

" GVIMではマウスが使えるように
set mouse=a
