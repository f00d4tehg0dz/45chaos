import os
import atexit
import threading
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()

from . import models, config

updateThread = threading.Thread()

def bootstrap_app(no_thread=False):

    server_config = config.load_config()

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = server_config["database_uri"]
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
        updateThread = threading.Timer(
            int(server_config["update_interval"]), runUpdate, ()
        )
        updateThread.start()

    def startUpdates():
        global updateThread
        print("Starting update thread")
        updateThread = threading.Timer(
            int(server_config["update_interval"]), runUpdate, ()
        )
        updateThread.start()

    if not no_thread:
        startUpdates()
        atexit.register(interrupt)

    with app.app_context():
        models.check_database()

    return app, server_config
