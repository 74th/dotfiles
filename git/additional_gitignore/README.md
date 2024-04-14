# Git でコミットせずに gitignore を追加するときに使うファイル

.git/config

```
[core]
  excludesfile = ~/ghq/github.com/74th/dotfiles/git/additional_gitignore/vscode-settings.gitignore
```

### .vscode/

```
excludesfile = ~/ghq/github.com/74th/dotfiles/git/additional_gitignore/vscode-settings.gitignore
```

### .env / .envrc

```
excludesfile = ~/ghq/github.com/74th/dotfiles/git/additional_gitignore/dotenv.gitignore
```
