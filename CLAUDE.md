# 写真共有アプリ（Flask + PeeWee）

友人同士で写真を見せ合う、インスタグラム風のWebアプリ。初学者が学びながら実装する。

## 必ず守ること
- **技術枠は Flask と PeeWee（SQLite）**。ほかのフレームワークやORM（Django、FastAPI、SQLAlchemy など）に勝手に変えない。新しいパッケージは追加する前に質問する
- **1回に1タスクだけ実装する**。[docs/tasks.md](docs/tasks.md) の指定されたタスクだけを実装して止まる。依頼の範囲外の機能やファイルを一気に追加しない
- **秘密情報をコードに書かない**。`SECRET_KEY` などは `.env` から読む。`.env` はGitに入れない
- **投稿画像はプロジェクト直下の `uploads/` に保存する**。`static/` の下には置かない。表示は `/uploads/<filename>` のルートから `send_from_directory` で返す

## 詳細
実装の前に、次の2つを必ず読む。
- [docs/ai_context.md](docs/ai_context.md): 全体の前提、ディレクトリ構成、作業ルール、報告の形式
- [docs/coding_rules.md](docs/coding_rules.md): コードの書き方、セキュリティ、PeeWeeの注意点

設計の詳細（要件・画面・URL・DB）は、上の2つから参照されている docs/ の各ファイルを見る。

## 起動
```
python app.py   # http://localhost:8000 で開く
```
