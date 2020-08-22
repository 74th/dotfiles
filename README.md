# dotfiles

同梱しているプラグイン等はそれぞれのライセンスに従う。
その他 74th 作成のスクリプト等については、MIT ライセンスとする。

# 同梱

- git(git-comletion) : GNU General Public License version 2
- git flow : BSD License
- git flow completion : MIT License
- fisher : MIT
- bass : MIT

# よく忘れる Tools

- mdr https://github.com/mrchimp/mdr マークダウンをターミナル上で読みやすくする
- bat https://github.com/sharkdp/bat cat の代わりに使えるシンタックスハイライトしてくれる CUI ビューア

# paste

```sh
sudo apt-get update
sudo apt-get install -y git unzip curl
mkdir -p ~/tmp
rm -rf ~/tmp/*
cd ~/tmp
curl -OL https://github.com/x-motemen/ghq/releases/latest/download/ghq_linux_amd64.zip
unzip ghq_linux_amd64.zip
./ghq_linux_amd64/ghq get 74th/dotfiles
rm -rf $HOME/dotfiles
ln -sf $HOME/ghq/github.com/74th/dotfiles $HOME/dotfiles
cd $HOME/dotfiles
bash ./install.sh
```
