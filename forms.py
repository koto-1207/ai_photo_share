from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


def strip_filter(value):
    # 前後の空白を取り除く（未入力のときは None が来る）
    return value.strip() if value else value


class RegisterForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        filters=[strip_filter],
        validators=[
            DataRequired("ユーザー名を入力してください"),
            Length(min=3, max=30, message="ユーザー名は3〜30文字の半角英数字と _ で入力してください"),
            Regexp(r"^[A-Za-z0-9_]+$", message="ユーザー名は3〜30文字の半角英数字と _ で入力してください"),
        ],
    )
    email = EmailField(
        "メールアドレス",
        filters=[strip_filter],
        validators=[
            DataRequired("メールアドレスを入力してください"),
            Length(max=255, message="メールアドレスは255文字までです"),
            Email("メールアドレスの形式が正しくありません"),
        ],
    )
    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired("パスワードを入力してください"),
            Length(min=8, max=64, message="パスワードは8〜64文字で入力してください"),
        ],
    )
    password_confirm = PasswordField(
        "パスワード（確認）",
        validators=[
            DataRequired("パスワード（確認）を入力してください"),
            EqualTo("password", message="パスワードが一致しません"),
        ],
    )
    submit = SubmitField("登録する")


class LoginForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        filters=[strip_filter],
        validators=[DataRequired("ユーザー名を入力してください")],
    )
    password = PasswordField(
        "パスワード",
        validators=[DataRequired("パスワードを入力してください")],
    )
    submit = SubmitField("ログイン")


class LogoutForm(FlaskForm):
    # 入力欄はなく、CSRFトークンを送るためだけに使う
    submit = SubmitField("ログアウト")
