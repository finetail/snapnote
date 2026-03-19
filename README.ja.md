# snapnote

ターミナルからプレーンテキストのメモを素早く記録・検索するCLIツール — アイデアをメモし、タグを付けて、すぐに見つけ出せます。

[![CI](https://github.com/demo-user/snapnote/actions/workflows/ci.yml/badge.svg)](https://github.com/demo-user/snapnote/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 機能

- **即時メモ** — コマンド一つでターミナルからメモを追加
- **タグ付け** — 1つ以上のタグでメモにラベルを付けてフィルタリングを容易に
- **全文検索** — 全メモを対象とした大文字小文字を区別しない部分文字列検索
- **時系列一覧** — タグフィルターや件数制限を指定して最近のメモを表示
- **安全な削除** — 確認プロンプト付きでIDプレフィックスによりメモを削除
- **永続ストレージ** — プラットフォームに適したユーザーデータディレクトリにJSONで保存
- **リッチ出力** — [Rich](https://github.com/Textualize/rich) によるカラーハイライト付きターミナル出力

---

## 技術スタック

| レイヤー | ライブラリ |
|---|---|
| CLIフレームワーク | [Click](https://click.palletsprojects.com/) >= 8.1 |
| ターミナル出力 | [Rich](https://github.com/Textualize/rich) >= 13.0 |
| データディレクトリ | [platformdirs](https://github.com/platformdirs/platformdirs) >= 4.0 |
| ビルドバックエンド | [setuptools](https://setuptools.pypa.io/) >= 68 |
| リンター | [Ruff](https://docs.astral.sh/ruff/) >= 0.3 |
| 型チェック | [mypy](https://mypy-lang.org/) >= 1.8 |
| テスト | [pytest](https://docs.pytest.org/) >= 7.4 + pytest-cov >= 4.1 |

---

## インストール

PyPIからインストール：

```bash
pip install snapnote
```

またはリポジトリをクローンして開発用依存関係込みで編集可能モードでインストール：

```bash
git clone https://github.com/demo-user/snapnote.git
cd snapnote
pip install -e ".[dev]"
```

インストール後、`snapnote` コマンドが `PATH` 上で使用可能になります。

---

## 使い方

### メモを追加する

```bash
# プレーンテキストのメモ
snapnote add 牛乳とバナナを買う

# タグ付きメモ
snapnote add 四半期報告書を仕上げる -t 仕事

# 複数タグ付きメモ
snapnote add "データ指向アプリケーションデザイン" を読む -t 読書 -t 技術
```

`-t` / `--tag` フラグは繰り返し使用可能です。複数回指定することで1つのメモに複数のタグを付けられます。

### メモを一覧表示する

```bash
# 直近20件のメモを表示（デフォルト）
snapnote list

# 5件に制限して表示
snapnote list -n 5

# タグでフィルタリング
snapnote list --tag 仕事

# タグフィルターと件数制限を組み合わせる
snapnote list -t 読書 -n 10
```

> 注意：一覧出力では各メモのIDプレフィックス、日付、本文が表示されます。タグはインラインで表示されませんが、`-t` でフィルターとして使用できます。

### メモを検索する

```bash
# 全文検索（大文字小文字を区別しない）
snapnote search 牛乳

snapnote search "四半期報告書"
```

### メモを削除する

```bash
# 一覧/検索結果に表示されるメモIDの先頭8文字で削除
snapnote delete a1b2c3d4
# 確認プロンプトが表示されます: "Delete this note? [y/N]"
```

### グローバルオプション

```bash
# インストール済みバージョンを表示
snapnote --version

# 各コマンドのヘルプを表示
snapnote --help
snapnote add --help
snapnote list --help
snapnote search --help
snapnote delete --help
```

---

## テストの実行

```bash
# カバレッジレポート付きでテストスイート全体を実行
pytest

# 特定のテストファイルを実行
pytest tests/test_store.py

# 詳細出力で実行
pytest -v
```

カバレッジはターミナルに自動で表示されます。CIパイプラインではリンターと型チェックも実行されます：

```bash
ruff check .
mypy src
```

---

## プロジェクト構成

```
snapnote/
├── src/
│   └── snapnote/
│       ├── __init__.py     # パッケージバージョン定義 (__version__ = "0.1.0")
│       ├── cli.py          # Clickコマンド定義 (add, list, search, delete)
│       ├── models.py       # シリアライズヘルパー付き Note データクラス
│       └── store.py        # JSONバックの NoteStore (save, list, search, delete)
├── tests/
│   ├── __init__.py
│   ├── test_models.py      # Noteモデルのユニットテスト
│   └── test_store.py       # NoteStore の統合テスト
├── pyproject.toml          # プロジェクトメタデータ、依存関係、ツール設定
└── README.md
```

---

## データの保存場所

メモはプラットフォームに適したユーザーデータディレクトリにJSONファイルとして保存されます：

| プラットフォーム | パス |
|---|---|
| Linux | `~/.local/share/snapnote/notes.json` |
| macOS | `~/Library/Application Support/snapnote/notes.json` |
| Windows | `%LOCALAPPDATA%\snapnote\snapnote\notes.json` |

ディレクトリは初回使用時に自動作成されます。

---

## コントリビューション

1. リポジトリをフォークしてフィーチャーブランチを作成する。
2. 開発用依存関係をインストールする：`pip install -e ".[dev]"`
3. 変更を加え、`tests/` 配下にテストを追加する。
4. プルリクエストを開く前にチェックスイート全体が通ることを確認する：

```bash
ruff check .
mypy src
pytest
```

---

## ライセンス

このプロジェクトは [MITライセンス](https://opensource.org/licenses/MIT) のもとで公開されています。
