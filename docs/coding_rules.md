# コーディングルール

## ファイルの役割
| ファイル | 書くもの | 書かないもの |
|---|---|---|
| `app.py` | Flaskアプリの作成、Flask-Login の設定、すべてのルート | 設定値、モデル、フォームの定義 |
| `config.py` | 設定値（`SECRET_KEY`、DBのパス、`UPLOAD_FOLDER`、`MAX_CONTENT_LENGTH`） | 処理 |
| `models.py` | DB接続、PeeWeeのモデル | Flaskのルート |
| `forms.py` | Flask-WTFのフォームとバリデータ | DBへの保存処理 |
| `templates/base.html` | 共通レイアウト | 画面ごとの内容 |
| `templates/posts/*.html` `templates/auth/*.html` | 各画面の表示 | 複雑な処理 |
| `static/css/style.css` | 自作のCSS | 投稿画像 |
| `uploads/` | ユーザーが投稿した画像だけ | それ以外のファイル |

## 命名
- URL、関数名（endpoint）、テンプレート名は、[routes.md](routes.md) のとおりにする
- モデル名とカラム名は、[database.md](database.md) のとおりにする
- 変数名と関数名は `snake_case`、クラス名は `PascalCase`
- リンクとリダイレクトには必ず `url_for()` を使う（URLを直接書かない）

## 設定
- 設定値は `config.py` の `Config` クラスにまとめ、`app.py` で `app.config.from_object(Config)` で読み込む
- `SECRET_KEY` は `.env` から読む（`os.environ`）。コードに直接書かない
- 画像の保存先は、`config.py` があるフォルダを基準にした絶対パスで指定する
  - 例: `UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")`
- 投稿画像の保存先は **プロジェクト直下の `uploads/`**。`static/` には保存しない
- `MAX_CONTENT_LENGTH = 5 * 1024 * 1024`

## ルートの書き方
- GETとPOSTが同じURLの画面は、1つの関数で `methods=["GET", "POST"]` を指定する
- POSTが成功したら `redirect(url_for(...))` で移動する（PRG）
- POSTでエラーになったら、リダイレクトせずに同じテンプレートを表示する
- 状態を変える操作（ログアウト、削除、いいね）はPOSTだけで受け付ける
- ログインが必要なルートには `@login_required` を付ける
- 見つからないデータは `abort(404)` で返す
- 本人しかできない操作は、サーバー側で `post.user.id == current_user.id` を確認する。違ったら `abort(403)`

## セキュリティ
- パスワードは `werkzeug.security` の `generate_password_hash` / `check_password_hash` で扱う
- すべてのフォームで `{{ form.hidden_tag() }}` を出力する（CSRF対策）
- 画像は次の順番で処理する
  1. 拡張子を確認する
  2. Pillow で開けるか確認する
  3. ファイル名を `uuid4().hex + 拡張子` に作り直す
  4. `uploads/` に保存する
- 画像を返すときは `send_from_directory(UPLOAD_FOLDER, filename)` を使う
- テンプレートで `|safe` を使わない（Jinja2の自動エスケープを効かせる）

## DB（PeeWee）
- [database.md](database.md) の「4. PeeWeeで実装する場合の注意点」に従う
- ユーザー名の重複チェックとログインでは、大文字と小文字を区別しない
  - 例: `User.get_or_none(fn.LOWER(User.username) == username.lower())`
- メールアドレスは `.lower()` してから保存する
- リクエストごとにDBに接続し、終わったら閉じる（`before_request` で `db.connect()`、`teardown_request` で `db.close()`）

## テンプレートとCSS
- すべてのテンプレートで `{% extends "base.html" %}` を使う
- flashメッセージは `base.html` でまとめて表示する
- CSSは `static/css/style.css` だけに書く。スマホで見られるように、幅は `max-width` と `%` で指定する
- 外部のCSSやJSは読み込まない

## コメントと報告
- コメントは日本語で書く。処理の理由が分かりにくいところにだけ付ける
- 実装後の報告は、[ai_context.md](ai_context.md) の「AIの作業ルール」の形式に従う
- 設計資料にない小さなことを決めたら、報告の中で「決めたこと」として書く
