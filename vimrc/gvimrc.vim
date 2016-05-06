colorscheme evening

" メニューは表示しない
set guioptions=egrLt
command! ShowGuiMenu :set guioptions=egmrLtT<CR>

set lines=55
set columns=120

if has('gui_macvim')
	set guifont=Gen\ Shin\ Gothic\ Monospace\ Light:h13
	set noimdisableactivate
	set lsp=-1
elseif has('win32')
    set guifont=源真ゴシック等幅_Normal:h10:cSHIFTJIS
endif

" GVIMではマウスが使えるように
set mouse=a
