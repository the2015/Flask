from flask import Flask

from App.settings import envs
from App.views import init_view
from ext import init_ext


def create_app(env):
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sqlite.db"
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/test"
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(envs.get("develop"))
    init_ext(app)
    init_view(app=app)
    return app
