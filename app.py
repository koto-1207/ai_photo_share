from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from peewee import IntegrityError, fn
from werkzeug.security import check_password_hash, generate_password_hash

from config import Config
from forms import LoginForm, LogoutForm, RegisterForm
from models import User, create_tables, db

app = Flask(__name__)
app.config.from_object(Config)

# SECRET_KEY がないとセッションとCSRFトークンを安全に扱えないため、起動を止める
if not app.config["SECRET_KEY"]:
    raise RuntimeError(".env に SECRET_KEY を設定してください")

login_manager = LoginManager(app)
# 未ログインで @login_required のページを開いたときの移動先
login_manager.login_view = "login"
login_manager.login_message = "ログインしてください"

create_tables()


@login_manager.user_loader
def load_user(user_id):
    # セッションに保存された id から User を取り出す
    return User.get_or_none(User.id == int(user_id))


# リクエストごとにDBへ接続し、終わったら閉じる
@app.before_request
def before_request():
    db.connect(reuse_if_open=True)


@app.teardown_request
def teardown_request(exc):
    if not db.is_closed():
        db.close()


# すべてのテンプレートでヘッダーのログアウトボタンを使えるようにする
@app.context_processor
def inject_logout_form():
    return {"logout_form": LogoutForm()}


def find_user_by_username(username):
    # 大文字と小文字を区別せずに探す（Taro と taro は同じユーザー名とみなす）
    return User.get_or_none(fn.LOWER(User.username) == username.lower())


@app.route("/")
def index():
    return render_template("posts/index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        has_error = False
        if find_user_by_username(form.username.data):
            form.username.errors.append("このユーザー名は使われています")
            has_error = True
        if User.get_or_none(User.email == email):
            form.email.errors.append("このメールアドレスは登録済みです")
            has_error = True

        if not has_error:
            try:
                user = User.create(
                    username=form.username.data,
                    email=email,
                    password_hash=generate_password_hash(form.password.data),
                )
            except IntegrityError:
                # 確認してから保存するまでの間に、同じ名前で登録された場合
                form.username.errors.append("このユーザー名またはメールアドレスは使われています")
            else:
                login_user(user)
                flash("登録しました")
                return redirect(url_for("index"))

    return render_template("auth/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = find_user_by_username(form.username.data)
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("ログインしました")
            return redirect(url_for("index"))
        # どちらが違うかは伝えない（登録済みのユーザー名を知られないため）
        flash("ユーザー名またはパスワードが違います")

    return render_template("auth/login.html", form=form)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        flash("ログアウトしました")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=8000)
