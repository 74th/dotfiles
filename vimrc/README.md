vimセットアップ手順
=====

* Gvimを用意する
    * Windowsの場合、**32bit版**香り屋さんGVim
    * Macの場合、MacVim
    * Linuxの場合、yum install gvim、apt-get install gvim

* vimrcを開き、OSの判定を、きちんと書く

* git管理の.vim的ディレクトリを、きちんと書く

* NeoBundleをインストールする

```
$ curl https://raw.githubusercontent.com/Shougo/neobundle.vim/master/bin/install.sh | sh
```

Windows版の場合、既にRapidSettingsForWin.batに入っている

* vimを起動して、:NeoBundleInstallを実行して暫く待つ

* Rictyのインストールを忘れずに
    * Windowsの場合、gdi++を導入する
    * http://74th.hateblo.jp/entry/2012/11/17/002213
    * gdi++Helium版の対応が32bitのみのため、32bitのvimを導入した
