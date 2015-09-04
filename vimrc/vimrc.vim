"-----------------------------------------------------------
" おまじない系
if has('vim_starting')
    set nocompatible
endif
" 一旦filetypeを無効化する
" すべてのプラグインを読み込んでから後でONにする
filetype off
filetype plugin indent off

"-----------------------------------------------------------
" 前処理
"-----------------------------------------------------------
if !exists('g:j74Spec')
    let g:j74Spec = 'low'
endif

" Python3の有効化（Mac） 2014/09/07
"$ brew tap supermomonga/homebrew-splhack
"$ brew install cscope
"$ brew install python
"$ brew install python3
"$ brew install lua
"$ brew install --HEAD cmigemo-mk
"$ brew install --HEAD ctags-objc-ja
"$ brew install macvim-kaoriya --HEAD --with-lua --with-cscope --with-python --with-python3
"$ brew linkapps
if has('gui_macvim')
    let $PYTHON3_DLL="/usr/local/Cellar/python3/3.4.1_1/Frameworks/Python.framework/Versions/3.4/Python"
endif

"リポジトリ管理の.vim的ディレクトリ 2012/01/20
if has('vim_starting')
    "VimRepoPath/plugins下のディレクトリをruntimepathへ追加
    for path in split(glob(g:j74VimRepoPath.'plugins/*'), '\n')
        if isdirectory(path) 
            execute 'set runtimepath+=' . path
        end
    endfor
    "リポジトリルートをruntimepathへ追加
    execute 'set runtimepath+=' . g:j74VimRepoPath
    if isdirectory(expand('~/.vim/bundle/neobundle.vim/'))
        " NeoBundle
        set runtimepath+=~/.vim/bundle/neobundle.vim/
        let g:j74NeoBundleExists=1
    else
        " NeoBundleがない時の退避処理
        let g:j74NeoBundleExists=0
        command! -nargs=* NeoBundle 
    endif
    " 香り屋さんのvimを読み込む
    execute 'source ' . g:j74VimRepoPath . 'kaoriya.vim'
endif

"-----------------------------------------------------------
" NeoBundleによるプラグイン管理 2012-11-03
"-----------------------------------------------------------
" NeoBundle管理するvimディレクトリを作る
if exists('g:j74UserDirectory' . 'bundle' ) == 1
    execute '"set rtp+=' . g:j74UserDirectory . 'bundle/"'
endif
if g:j74NeoBundleExists == 1
    call neobundle#begin(expand('~/.vim/bundle/'))
endif

"プロキシ環境の場合は、githubにhttpsでアクセスする
if g:j74isProxy == 1
    let g:neobundle_default_git_protocol='https'
endif

"インストールコマンド
"NeoBundleInstall
"インストール/更新
"NeoBundleInstall!

"githubの場合、URLにあるのをそのまま書く

NeoBundle 'MultipleSearch'
"複数の検索をハイライトできる
":Search /検索条件/			"検索
":SearchReset				"ハイライトの削除

"NeoBundle 'tpope/vim-pathogen'
"不要かもしれないが、一応入ってる

NeoBundle 'matchit.zip'
"%で当たるのを増やしてくれるやつ

NeoBundle 'autofmt'
"自動整形。使ってるかわからん。


"NeoBundle 'sudo.vim'
"sudo.vim 2012/02/12

NeoBundle 'deris/columnjump'
"縦移動を便利にする 2013/09/24
nmap <c-k> <Plug>(columnjump-backward)
nmap <c-j> <Plug>(columnjump-forward)

"surround.vim
NeoBundle 'tpope/vim-surround'

"Dockerfile
NeoBundle 'ekalinin/Dockerfile.vim'
autocmd BufNewFile,BufRead Dockerfile set filetype=dockerfile

"-----------------------------------------------------------
" 2013/02/09 VimProc
" マニュアルを見て、コンパイルすること
NeoBundle 'Shougo/vimproc'

"-----------------------------------------------------------
" unite.vim
NeoBundle 'Shougo/unite.vim'
NeoBundle 'Shougo/neomru.vim'
NeoBundle 'Shougo/vimfiler'
" 2011/08/16導入
" 入力モードで開始する
let g:unite_enable_start_insert=1
" バッファ一覧
nnoremap <silent> ,ub :<C-u>Unite buffer bookmark<CR>
" ファイル一覧
nnoremap <silent> ,uf :<C-u>UniteWithBufferDir -buffer-name=files file directory file/new directory/new<CR>
" レジスタ一覧
nnoremap <silent> ,ur :<C-u>Unite -buffer-name=register register<CR>
" 最近使用したファイル一覧
nnoremap <silent> ,uu :<C-u>Unite bookmark file_mru<CR>
let g:unite_source_file_mru_long_limit = 200
" マッピングの表示
command! ShowMapping :Unite mapping
" コマンドの表示
command! ShowCommand :Unite command
" ノートディレクトリの表示
command! OpenNotes :Unite file_rec:~/Dropbox/notes/ file/new:~/Dropbox/notes/
" チートシートを引く
command! OpenCheatSheets :Unite file:~/MyCheatSheets/ file/new:~/MyCheatSheets/
nnoremap <silent> ,uc :<C-u>Unite file:~/MyCheatSheets/ file/new:~/MyCheatSheets/<CR>
"-----------------------------------------------------------
"neocomplcache 2012/01/27
if g:j74Spec == 'high'
    NeoBundle 'Shougo/neocomplcache'
    NeoBundle 'Shougo/neosnippet'
    NeoBundle 'Shougo/neosnippet-snippets'
endif
" Disable AutoComplPop.
let g:acp_enableAtStartup = 0
" 自動でON
let g:neocomplcache_enable_at_startup = 1
" 大文字が入力されるまで大文字小文字の区別を無視する
let g:neocomplcache_enable_smart_case = 1
" シンタックスをキャッシュするときの最小文字長
let g:neocomplcache_min_syntax_length = 4
" neocomplcacheを無効にするバッファ名のパターン。とりあえず使用しない。
"let g:neocomplcache_lock_buffer_name_pattern = '\*ku\*'
" 補完ウィンドウの設定
set completeopt=menuone
" _(アンスコ)区切りの補完を有効化
let g:neocomplcache_enable_underbar_completion = 1
" CamelCaseの保管は使わない
let g:neocomplcache_enable_camel_case_completion  = 0
" ポップアップメニューで表示される候補の数
let g:neocomplcache_max_list = 20

" ディクショナリ定義
let g:neocomplcache_dictionary_filetype_lists = {
            \ 'default' : '',
            \ }
if !exists('g:neocomplcache_keyword_patterns')
    let g:neocomplcache_keyword_patterns = {}
endif
" 日本語は保管対象外
"let g:neocomplcache_keyword_patterns['default'] = '\v\h\w*'
let g:neocomplcache_keyword_patterns['default'] = '\h\w*'
" 部分一致しない
"let g:neocomplcache_patternmatch = 0

" ---------- キーマップ ---------------
" <C-k> でスニペットを展開
"imap <C-k> <Plug>(neocomplcache_snippets_expand)
" 前回の保管をキャンセル
"inoremap <expr><C-g> neocomplcache#undo_completion()
" 共通部分の保管
inoremap <expr><C-l> neocomplcache#complete_common_string()
"inoremap <expr><C-h> neocomplcache#smart_close_popup()."\<C-h>"
"inoremap <expr><BS> neocomplcache#smart_close_popup()."\<C-h>"
inoremap <expr><C-y> neocomplcache#close_popup()
inoremap <expr><C-e> neocomplcache#cancel_popup()
inoremap <expr><C-e> neocomplcache#cancel_popup()
inoremap <expr><C-Space> neocomplcache#start_manual_complete()

" Enable omni completion.
autocmd FileType css setlocal omnifunc=csscomplete#CompleteCSS
autocmd FileType html,markdown setlocal omnifunc=htmlcomplete#CompleteTags
autocmd FileType javascript setlocal omnifunc=javascriptcomplete#CompleteJS
autocmd FileType python setlocal omnifunc=pythoncomplete#Complete
autocmd FileType xml setlocal omnifunc=xmlcomplete#CompleteTags

" Enable heavy omni completion.
if !exists('g:neocomplcache_omni_patterns')
    let g:neocomplcache_omni_patterns = {}
endif
let g:neocomplcache_omni_patterns.php = '[^. \t]->\h\w*\|\h\w*::'
let g:neocomplcache_omni_patterns.c = '[^.[:digit:] *\t]\%(\.\|->\)'
"let g:neocomplcache_omni_patterns.cs = '[^.[:digit:] *\t]\%(\.\|->\)'
let g:neocomplcache_omni_patterns.cs = '.*'
let g:neocomplcache_omni_patterns.cpp = '[^.[:digit:] *\t]\%(\.\|->\)\|\h\w*::'

" For perlomni.vim setting.
" https://github.com/c9s/perlomni.vim
let g:neocomplcache_omni_patterns.perl = '\h\w*->\h\w*\|\h\w*::'



"-----------------------------------------------------------
"オリジナルの取説
"-----------------------------------------------------------
"*オリジナルシンタックス
"**メモ用
"set syntax=memo74
"これで表示したいファイルに、以下を最初か最後に入れる。()は外す。
"# vi(m): set syntax=memo74 :
"ちなみにマークダウン記法の場合
"<!-- vim: set filetype=markdown : -->



"-----------------------------------------------------------
" 標準設定系
"-----------------------------------------------------------
"標準のタブ幅
set tabstop=4
set shiftwidth=4
set autoindent
set expandtab

"不可視文字の表示
" tab、trail(行末のスペース)のみ表示する
set list
if g:j74OsName == 'Win'
    set listchars=tab:>\ ,trail:-,extends:>,precedes:<,nbsp:%
else
    set listchars=tab:>\ ,trail:-,extends:>,precedes:<,nbsp:%
endif

"自動改行を抑制
set tw=0

"バックアップを自動作成しない
set nobackup

"色つける
if has("vim_starting")
    syntax on
endif

"スワップファイルはテンポラリへ
let g:j74SwapDirectory = g:j74UserDirectory . 'swp/' 
set directory=~/.vim/swp/
if !isdirectory( expand(g:j74SwapDirectory) )
    call mkdir(expand(g:j74SwapDirectory))
endif

" <C-a><C-x>で02を8進数と見なさない
set nrformats=

" Macのテンポラリディレクトリではバックアップを作成しない
" crontab -e対策
" 参考:http://d.hatena.ne.jp/yuyarin/20100225/1267084794
set backupskip=/tmp/*,/private/tmp/*

" undoファイルは一箇所に集める
let g:j74UndoDirectory = g:j74UserDirectory . 'undo/' 
execute 'set undodir=' . g:j74UndoDirectory
if !isdirectory( expand(g:j74UndoDirectory) )
    call mkdir(expand(g:j74UndoDirectory))
endif

" iterm2でマウスを使う設定
set mouse=a
set ttymouse=xterm2

" 丸数字などが1文字になってしまう
set ambiwidth=double

"-----------------------------------------------------------
" オリジナルキーマップ
"-----------------------------------------------------------
" タブ関連 → 廃止
" InsertModeの時 字下げ<c-t> 字上げ<c-d> オートフォーマット<c-f> を使う
" NormalModeの時 字下げ< 字上げ> オートフォーマット= を使う


"-----------------------------------------------------------
" オリジナルコマンド
"-----------------------------------------------------------
"Vimrcを編集 2012/02/12
function! EditVimrc()
    execute 'tabnew ' . g:j74VimRepoPath . 'vimrc.vim'
endfunction
command! EditVimrc :call EditVimrc()
"-----------------------------------------------------------
"勝手に改行されるので:tw=0を実行する 2012/04/11
function! KaigyoSuruna()
    set tw=0
endfunction
command! KaigyoSuruna :call KaigyoSuruna()
command! NoKaigyo :call KaigyoSuruna()
command! NoJidoKaigyo :call KaigyoSuruna()
"-----------------------------------------------------------
"Vimrcを再読み込み 2012/02/12
if has('vim_starting')
    function! ReloadVimrc()
        execute 'source ' . g:j74VimRepoPath . 'vimrc.vim'
    endfunction
    command! ReloadVimrc :call ReloadVimrc()
endif
"-----------------------------------------------------------
"Python最初の行 2013/09/04
command! PythonInit :1normal O#!/usr/bin/python<CR># coding: UTF-8
"-----------------------------------------------------------
"JSONフォーマット 2012/05/31
"http://wozozo.hatenablog.com/entry/2012/02/08/121504
"command! ParseJson %!python -m json.tool
"JSONフォーマットをjqの利用に変更 2014/08/09
"http://qiita.com/tekkoc/items/324d736f68b0f27680b8
command! -nargs=* ParseJson call s:Jq(<f-args>)
command! -nargs=? Jq call s:Jq(<f-args>)
function! s:Jq(...)
    if 0 == a:0
        let l:arg = "."
    else
        let l:arg = a:1
    endif
    "execute "%! jq 95fe1a73-e2e2-4737-bea1-a44257c50fc8quot;" . l:arg . "95fe1a73-e2e2-4737-bea1-a44257c50fc8quot;"
    execute "%! jq " . l:arg
endfunction
"-----------------------------------------------------------
"XMLフォーマット 2013/10/04
function! ParseXML()
    execute '%s/></>\r</g'
    execute 'normal gg=G'
endfunction
command! ParseXML :call ParseXML()
"-----------------------------------------------------------
"quickrun 2012/11/03
NeoBundle 'thinca/vim-quickrun'
let g:quickrun_config = {
\   "_" : {
\       "runner" : "vimproc",
\       "runner/vimproc/updatetime" : 500,
\   },
\}
":QuickRun <標準入力ファイル
" 今のファイルでJasmine-nodeを実行
function! QuickRunFirst(...)
    let b:quickrun_previous = ""
    for i in a:000
        let b:quickrun_previous = b:quickrun_previous . " " . i
    endfor
    execute "QuickRun " . b:quickrun_previous
endfunction
command! -nargs=* QuickRunFirst :call QuickRunFirst(<f-args>)
function! QuickRunRepeat()
    if exists("b:quickrun_previous")
        execute "QuickRun " . b:quickrun_previous
    else
        call quickrun#run()
    endif
endfunction
nnoremap <F5> :call QuickRunRepeat()<CR>
command! RunJasmineNode :QuickRun jasmine-node -cmdopt="%s"<CR>
" てか<F5>でいいよね
autocmd BufNewFile,BufRead *.spec.js nnoremap <buffer> <F5> :QuickRun jasmine-node -cmdopt="%s"<CR>
"-----------------------------------------------------------
"tabnewを楽にする 2012/11/27
command! Tn :tabnew
nnoremap <silent> gn :tabnew<CR>
nnoremap <silent> g1 :tabn 1<CR>
nnoremap <silent> g2 :tabn 2<CR>
nnoremap <silent> g3 :tabn 3<CR>
nnoremap <silent> g4 :tabn 4<CR>
nnoremap <silent> g5 :tabn 5<CR>
nnoremap <silent> g6 :tabn 6<CR>
nnoremap <silent> g7 :tabn 7<CR>
"-----------------------------------------------------------
"文字コードを指定して再オープン 2014/10/31
command! OpenUtf8 :e! ++enc=utf-8
command! OpenSjis :e! ++enc=cp932
command! OpenEucjp :e! ++enc=euc-jp
"-----------------------------------------------------------
"JavaScript系
"http://layzie.hatenablog.com/entry/20130122/1358811539

"JavaScriptのインデントをマシにしてくれる
NeoBundle 'jiangmiao/simple-javascript-indenter'
" この設定入れるとshiftwidthを1にしてインデントしてくれる
let g:SimpleJsIndenter_BriefMode = 1
" この設定入れるとswitchのインデントがいくらかマシに
let g:SimpleJsIndenter_CaseIndentLevel = -1

"JavaScriptのSyntax
"NeoBundle 'jelera/vim-javascript-syntax'
"遅くなる原因のようなので削除

"JavaScriptのメソッド保管
"NeoBundle 'teramako/jscomplete-vim'
" DOMとMozilla関連とES6のメソッドを補完
"let g:jscomplete_use = ['dom', 'moz', 'es6th']

"-----------------------------------------------------------
"シンタックスチェッカー
if g:j74Spec == 'high'
    NeoBundle 'scrooloose/syntastic'
endif
" Javascript
" 要jshintのインストール #npm install -g jshint
let g:syntastic_javascript_checkers = ["jshint"]
" java
let g:syntastic_java_javac_options = "-J-Dfile.encoding=UTF8"
"-----------------------------------------------------------
" ちょこっとマニュアル
"コマンドラインモードでの貼付け         :<C-r>{register}
"yy/ddした後を貼り付ける場合            :<C-r>"
"

" 一括置換のコマンド
" :args **/**.cs
" :args
" :argsdo %s/xxx/aaa/g | update

"-----------------------------------------------------------
"Markdown 周り

"Markdownをプレビュー
NeoBundle '74th/previm'
let g:previm_open_cmd = 'open -a Google\ Chrome'

".mdをマークダウン記法にする
autocmd BufNewFile,BufRead *.md set filetype=markdown

"-----------------------------------------------------------
" 特定ディレクトリでexpandtabをしない
"-----------------------------------------------------------

"-----------------------------------------------------------
" CUI時の色設定 2014/09/07
"-----------------------------------------------------------
if !has('gui_running')
    if g:j74OsName != 'Win'
        set t_Co=256
        "NeoBundle 'tomasr/molokai'
        colorscheme molokai
    endif
endif

"-----------------------------------------------------------
" CUIで、インサートモードを抜けた時に、IMEをオフにしたい 2014/09/07
"-----------------------------------------------------------
" http://hotolab.net/blog/vim_ime/
" GoogleIME のキー設定に以下を加える
"
" 入力文字なし  Escape  キャンセル後IMEを無効化
"
"-----------------------------------------------------------
" vimshell 2014/09/07
"-----------------------------------------------------------
NeoBundle "Shougo/vimshell.vim"
"-----------------------------------------------------------
" 日本語ヘルプ 2014/09/07
"-----------------------------------------------------------
NeoBundle 'vim-jp/vimdoc-ja'
"-----------------------------------------------------------
" コメント設定／アウト 2014/09/07
"-----------------------------------------------------------
NeoBundle "tyru/caw.vim.git"
nmap <Leader>c <Plug>(caw:i:toggle)
vmap <Leader>c <Plug>(caw:i:toggle)
" \c    コメントトグル
" gci   コメント
" gcui  コメントアウト
"-----------------------------------------------------------
" 日付も<C-A>でインクリメント 2014/09/29
NeoBundle 'tpope/vim-speeddating'
let g:speeddating_formats = [
    \    ["%Y/%m/%d%a",0,0]
    \]
"-----------------------------------------------------------
" SQLのフォーマット
NeoBundle 'SQLUtilities'
NeoBundle 'Align'
":SQLUFormat で、SQLを整形する
"Alignというマクロも必要らしい

" よく使うので:SQLで実行
command! SQL :SQLUFormatter<CR>

"カンマで改行する
let g:sqlutil_align_comma = 1
"-----------------------------------------------------------
" ディレクトリごとのvimrc設定
" .local.vimrc というファイルをディレクトリにおいておくと、見てくれる
" .local.{filetype}.vimrc でもファイルタイプごとに有効
NeoBundle 'thinca/vim-localrc'
"-----------------------------------------------------------
" おまじない最後系
"-----------------------------------------------------------
" 一旦無効化したfiletypeを最後に復活させる
" http://d.hatena.ne.jp/wiredool/20120618/1340019962
if g:j74NeoBundleExists == 1
    call neobundle#end()
endif
filetype plugin indent on
