# ルーティング設計

- ルートはすべて `app.py` に書く。設定値は `config.py` から読み込む
- テンプレートは画面の種類ごとにフォルダを分ける（投稿は `posts/`、認証は `auth/`）
- 画面は [screens.md](screens.md) を参照する
- ログインの管理には Flask-Login を使う。ログインが必要なルートには `@login_required` を付ける

## ルート一覧

| URL | メソッド | 関数名（endpoint） | ログイン | テンプレート | 処理内容 |
|---|---|---|---|---|---|
| `/` | GET | `index` | 不要 | `posts/index.html` | 投稿を新しい順に取得して表示する |
| `/posts/<int:post_id>` | GET | `post_detail` | 不要 | `posts/detail.html` | 投稿を1件取得して表示する。ない場合は404 |
| `/posts/new` | GET | `post_new` | 必要 | `posts/new.html` | 投稿フォームを表示する |
| `/posts/new` | POST | `post_new` | 必要 | `posts/new.html`（エラー時） | 画像を保存して投稿を作成し、`index` へリダイレクトする |
| `/register` | GET | `register` | 不要 | `auth/register.html` | 登録フォームを表示する |
| `/register` | POST | `register` | 不要 | `auth/register.html`（エラー時） | ユーザーを作成し、自動でログインして `index` へリダイレクトする |
| `/login` | GET | `login` | 不要 | `auth/login.html` | ログインフォームを表示する |
| `/login` | POST | `login` | 不要 | `auth/login.html`（エラー時） | 認証して `index` へリダイレクトする |
| `/logout` | POST | `logout` | 必要 | なし | ログアウトして `index` へリダイレクトする |
| `/uploads/<filename>` | GET | `uploaded_file` | 不要 | なし | アップロードした画像を返す（`send_from_directory`） |

GETとPOSTが同じURLの画面は、1つの関数で `methods=["GET", "POST"]` を指定してまとめる。

## リダイレクトのルール
- POSTが成功したら、必ず `redirect(url_for(...))` で移動する（PRGパターン。再読み込みで二重送信されるのを防ぐ）
- POSTでエラーになったら、リダイレクトせずに同じテンプレートを表示する（入力値とエラーを残すため）
- 未ログインで `@login_required` のURLを開いたら、Flask-Loginが `login` へ移動させる（`login_manager.login_view = "login"`）
- ログイン中に `/login` や `/register` を開いたら `index` へリダイレクトする

## テンプレート構成

```
templates/
├── base.html          共通レイアウト（ヘッダー、flashメッセージ）
├── posts/
│   ├── index.html     投稿一覧
│   ├── detail.html    投稿詳細
│   └── new.html       投稿作成
└── auth/
    ├── login.html     ログイン
    └── register.html  ユーザー登録
```

## 追加機能を入れるときのURL（参考・今は作らない）
| URL | メソッド | 内容 |
|---|---|---|
| `/posts/<id>/delete` | POST | 投稿の削除（本人のみ） |
| `/posts/<id>/edit` | GET / POST | キャプションの編集（本人のみ） |
| `/posts/<id>/like` | POST | いいね / 取り消し |
| `/posts/<id>/comments` | POST | コメントの投稿 |
