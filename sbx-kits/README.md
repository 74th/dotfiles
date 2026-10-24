# sbx kits

- `v2/`: 旧 `sbx-kit/` から内容を変更せず移動した kit。
  `bin/sbx-create-with-kit` と `bin/sbx-add-kit` は引き続きこちらを使用する。
- `v3/`: 同じ6種類の mixin を Kit v3 へ移植したもの。
  各ディレクトリの `<kit名>.yaml` が descriptor。

## v3 の利用

sbx v0.45 以降と v3 workload を使用する。組み込みの `codex` / `claude`
は v2 のため、v3 mixin と組み合わせる際は workload の OCI 参照を指定する。
リポジトリのルートで実行する例:

```sh
sbx create docker.io/docker/sbx-kit-shell:1.0.0 . \
  --name shell-v3 --kit ./sbx-kits/v3/std-74th
```

複数追加する場合は `--kit` を繰り返す。`std-74th` は `mybashrc`、
`openspec`、`pre-commit` の処理を含むため、それらを重複指定しない。
v3 は sandbox 作成時に mixin を選ぶ。既存 sandbox への `sbx kit add` は使えない。

## 移植方針

既存のインストールコマンド、実行ユーザー、実行順を維持し、`setup.install`
を `com.docker.sandbox/lifecycle@1` の `config.install` に移した。
インストールは sandbox 作成時に実行する、コンテンツを持たない宣言のみの mixin。
v3 ではトップレベルの `name` を指定せず、参照するディレクトリ名が識別名になる。

ネットワーク許可は `com.docker.sandbox/network-policy@1` に移し、
ダウンロード先を `install.allow` に宣言した。既存の許可は `runtime.allow` にも
保持している。通信を行う hook にはプロキシ環境変数を明示的に渡す。
apt の許可先は Ubuntu / Debian の標準ミラーで、独自ミラーには追加設定が必要。

従来と同様、workload 側に `apt-get`（`mybashrc` / `std-74th`）、
`npm`（`openspec` / `std-74th`）、`uv`（`pre-commit` / `std-74th`）が必要。
gcloud / tfenv の PATH 設定には `/etc/sandbox-persistent.sh` を使用する。
ツールのバージョン指定も v2 を維持しているため、取得する内容は固定されていない。

Docker / BuildKit が利用できる環境では、各 descriptor を直接ビルドして検証できる:

```sh
docker buildx build -f sbx-kits/v3/std-74th/std-74th.yaml \
  -t standard-74th:dev --load sbx-kits/v3/std-74th
```

このビルドでは descriptor を検証する。install hook の動作確認には実際の sandbox
作成が必要。手元の sbx v0.45.1 の `sbx kit validate` は v3 ソースに対して
`this load path has no kit builder configured` を返すため、このコマンドでは検証できない。

参照: [Docker Kit v3 の作成](https://docs.docker.com/ai/sandboxes/customize/author/)、
[v2 → v3 フィールド対応](https://github.com/docker/sandbox-kit-spec/blob/main/skills/migrate-kit-to-v3/FIELD-MAPPING.md)。
