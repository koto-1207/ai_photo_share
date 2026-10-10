# AIコンテキスト

このプロジェクトで実装を始める前に、最初にこのファイルを読むこと。

## アプリの概要
友人同士で写真を見せ合う、インスタグラム風の写真共有Webアプリ。写真1枚と短いキャプションを投稿し、新しい順に一覧で見る。
実装するのは初学者。ローカル環境（Windows）で動けばよい。

## 固定の技術（変更しない）
- Python / **Flask** / **PeeWee** / SQLite
- 使うパッケージは [requirements.txt](../requirements.txt) にあるものだけ: Flask, peewee, Flask-Login, Flask-WTF, WTForms, email-validator, Pillow, python-dotenv
- SQLAlchemy などのほかのORM、ほかのフレームワーク、JSフレームワーク、CSSフレームワークは使わない
- 新しいパッケージが必要だと思ったら、追加する前に質問する

## ディレクトリ構成

```
ai_photo_share/
├── app.py            Flaskアプリ本体。ルートはすべてここに書く
├── models.py         PeeWeeのモデルとDB接続
├── forms.py          Flask-WTFのフォーム
├── templates/        Jinja2テンプレート（base.html を継承する）
├── static/css/       自作のCSS（style.css）だけを置く
├── uploads/          ユーザーが投稿した画像の保存先（プロジェクト直下）
├── docs/             設計資料
├── .env              SECRET_KEY など（Gitに入れない）
├── requirements.txt
└── app.db            SQLiteのDB（自動で作られる。Gitに入れない）
```

- **投稿画像の保存先は、プロジェクト直下の `uploads/`**。`static/` には置かない
- 画像は `/uploads/<filename>` のルートから `send_from_directory` で返す
- フォルダやファイルは、そのタスクで必要になったものだけ作る

## 設計資料（実装の根拠）

| ファイル | 内容 | 使う場面 |
|---|---|---|
| [requirements.md](requirements.md) | 機能、非機能要件、入力ルール | 何を作るか、入力チェックの内容 |
| [screens.md](screens.md) | 画面ごとの表示項目と画面遷移 | テンプレートを作るとき |
| [routes.md](routes.md) | URL、メソッド、関数名、テンプレート名 | ルートを作るとき |
| [database.md](database.md) | テーブル、カラム、制約、PeeWeeの注意点 | モデルを作るとき |
| [tasks.md](tasks.md) | 実装タスクの順番と完成の条件 | 次に何をするか |
| [coding_rules.md](coding_rules.md) | コードの書き方 | すべてのタスク |

設計資料と矛盾するコードは書かない。

## やらないこと
- 検索、フォロー、Comment テーブル（今回は作らない）
- Blueprint への分割、アプリファクトリ（`create_app`）
- 確認メールの送信、パスワードのリセット
- デプロイの設定

## AIの作業ルール
1. **1回に1タスクだけ実装する**: [tasks.md](tasks.md) の指定されたタスクだけを実装して止まる。次のタスクには進まない
2. **小さいことは決めて報告する**: 日時の表示形式など、設計資料にない小さなことはAIが決めて、報告に書く。設計の変更（URL、テーブル、画面、パッケージ）に関わることは、実装する前に質問する
3. **報告する**: 実装が終わったら、次の3つを短く日本語で書く
   - 変更したファイル
   - 何をしたか
   - ユーザーがブラウザで確認する手順
4. **テストは後回し**: 自動テスト（pytest）は、必須機能がすべてできてから追加する
