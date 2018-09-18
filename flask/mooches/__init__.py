import os
import atexit
import threading
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()

from . import models

updateThread = threading.Thread()

def bootstrap_app(no_thread=False):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % (
        os.path.join(basedir, "data.sqlite")
    )
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    def interrupt():
        global updateThread
        print("Stopping updates")
        updateThread.cancel()

    def runUpdate():
        global updateThread
        print("Running mooch update")
        with app.app_context():
            models.update()
        updateThread = threading.Timer(60, runUpdate, ())
        updateThread.start()

    def startUpdates():
        global updateThread
        print("Starting update thread")
        updateThread = threading.Timer(60, runUpdate, ())
        updateThread.start()

    if not no_thread:
        startUpdates()
        atexit.register(interrupt)

    with app.app_context():
        models.check_database()

    return app
