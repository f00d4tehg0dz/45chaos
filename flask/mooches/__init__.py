import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()

def bootstrap_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % (
        os.path.join(basedir, "data.sqlite")
    )
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
