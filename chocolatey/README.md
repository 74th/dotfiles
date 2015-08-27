Chocolateyのパッケージ
=====

Windows用のコマンドラインなパッケージ管理ツール

https://chocolatey.org/

## インストール

Chocolateyのインストール
> @powershell -NoProfile -ExecutionPolicy unrestricted -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%systemdrive%\chocolatey\bin

リポジトリがないことにはなんで、gitはコマンドインストール
> chocolatey install git

gitでリポジトリをチェックアウト
> git config --global http.sslVerify false
> git clone https://g27.j74th.com/gitbucket/git/atsushi/dotfiles.git

ファイルにあるアプリを一括インストールする
> chocolatey install dotfiles\chocolatey\pakages.config
