# 実装タスク

- 上から順に、1回に1タスクずつ実装する
- 完成の条件をすべて満たしたら `[x]` にする
- 起動コマンドは `flask --app app run --debug`

## フェーズ1: 準備

### T1. アプリの土台
- 作るもの: `app.py`（`/` で仮の文字を表示）、`.env.example`、`templates/base.html`、`static/css/style.css`
- `.env` から `SECRET_KEY` を読み込む
- 完成の条件:
  - [ ] `flask --app app run --debug` で起動し、`/` が表示される
  - [ ] `SECRET_KEY` がコードに直接書かれていない

### T2. DB接続と User モデル
- 作るもの: `models.py`（DB接続、User モデル）。起動時に `create_tables([User])` を呼ぶ
- [database.md](database.md) の 3-1 と 4 の注意点に従う
- 完成の条件:
  - [ ] 起動すると `app.db` が作られ、User テーブルがある
  - [ ] `foreign_keys` が有効になっている

## フェーズ2: ユーザー

### T3. ユーザー登録
- 作るもの: `forms.py`（RegisterForm）、`/register`（GET / POST）、`register.html`
- 入力ルールは [requirements.md](requirements.md) の「8. 入力ルール」に従う
- 登録に成功したら、まだ一覧へは移動せず、flashメッセージを表示する（自動でログインする処理は T4 で作る）
- 完成の条件:
  - [ ] 登録すると User が保存され、パスワードはハッシュになっている
  - [ ] ユーザー名の重複（大文字と小文字の違いも含む）、メールアドレスの重複、形式エラー、パスワードの不一致で、それぞれエラーが表示される

### T4. ログイン / ログアウト
- 作るもの: Flask-Login の設定（User に `UserMixin` を継承させる、`user_loader` を作る）、LoginForm、`/login`、`/logout`（POST）、`login.html`
- 共通ヘッダーをログイン状態で切り替える（[screens.md](screens.md) の「共通ヘッダー」）
- 登録に成功したら自動でログインし、`index` へ移動するように T3 を直す
- 完成の条件:
  - [ ] ログインに成功すると一覧へ移動し、ヘッダーにユーザー名が出る
  - [ ] 失敗すると「ユーザー名またはパスワードが違います」と表示される
  - [ ] ログアウトはPOSTで受け付け、一覧へ戻る
  - [ ] ログイン中に `/login` や `/register` を開くと一覧へ移動する

## フェーズ3: 投稿

### T5. Post モデルと uploads/
- 作るもの: Post モデル（`create_tables` に追加する）、`uploads/.gitkeep`
- `.gitignore` に `uploads/*` と `!uploads/.gitkeep` があることを確認する
- 完成の条件:
  - [ ] Post テーブルが作られる
  - [ ] `uploads/` フォルダがプロジェクト直下にある

### T6. 投稿作成
- 作るもの: PostForm、`/posts/new`（GET / POST、`@login_required`）、`post_new.html`、`/uploads/<filename>`
- 画像は、名前を UUID に作り直してから、**プロジェクト直下の `uploads/` に保存する**。DBにはファイル名だけを保存する
- `MAX_CONTENT_LENGTH` を5MBにする。Pillow の `verify()` で画像かどうかを確認する
- DBへの保存に失敗したら、保存した画像ファイルを削除する
- 完成の条件:
  - [ ] 投稿すると `uploads/` に画像が保存され、一覧へ移動する
  - [ ] 未ログインで `/posts/new` を開くとログイン画面へ移動する
  - [ ] 写真なし、jpg / png 以外、偽の画像、5MB超えでエラーが表示される

### T7. 投稿一覧
- `/` を投稿一覧にする（`index.html`）。JOINを使って新しい順に取得する
- 完成の条件:
  - [ ] 写真、キャプション、投稿者名、投稿日時が新しい順に表示される
  - [ ] 投稿が0件のときに「まだ投稿がありません」と表示される

### T8. 投稿詳細
- 作るもの: `/posts/<int:post_id>`、`post_detail.html`
- 完成の条件:
  - [ ] 一覧の投稿をクリックすると詳細が表示される
  - [ ] 存在しないIDだと404になる
  - [ ] 「一覧へ戻る」リンクがある

ここまでで必須機能は完成。

## フェーズ4: 余裕があれば（上から優先）
- [ ] T9. 自分の投稿の削除（POST、本人のみ。`uploads/` の画像ファイルも削除する）
- [ ] T10. キャプションの編集（本人のみ）
- [ ] T11. いいね（Like モデル、1人1回、取り消せる、件数を表示する）
- [ ] T12. 自動テスト（pytest を追加する。登録、ログイン、投稿作成の主なケース）

コメント、サムネイル、アイコン画像は、T12 が終わってから検討する。
