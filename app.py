from flask import Flask, render_template

from config import Config
from models import create_tables, db

app = Flask(__name__)
app.config.from_object(Config)

create_tables()


# リクエストごとにDBへ接続し、終わったら閉じる
@app.before_request
def before_request():
    db.connect(reuse_if_open=True)


@app.teardown_request
def teardown_request(exc):
    if not db.is_closed():
        db.close()


@app.route("/")
def index():
    return render_template("posts/index.html")


if __name__ == "__main__":
    app.run(port=8000)
