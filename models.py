from datetime import datetime

from flask_login import UserMixin
from peewee import CharField, DateTimeField, ForeignKeyField, Model, SqliteDatabase

from config import Config

# foreign_keys を有効にしないと、SQLiteでは外部キーの制約が効かない
db = SqliteDatabase(Config.DATABASE_PATH, pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


# UserMixin を継承すると、Flask-Login が必要とする is_authenticated などが使えるようになる
class User(UserMixin, BaseModel):
    username = CharField(max_length=30, unique=True)
    email = CharField(max_length=255, unique=True)
    password_hash = CharField(max_length=255)
    # datetime.now() と書くと起動時刻で固定されるため、関数そのものを渡す
    created_at = DateTimeField(default=datetime.now)


class Post(BaseModel):
    user = ForeignKeyField(User, backref="posts")
    image_filename = CharField(max_length=255, unique=True)
    caption = CharField(max_length=200, default="")
    created_at = DateTimeField(default=datetime.now, index=True)


def create_tables():
    with db:
        db.create_tables([User, Post])
