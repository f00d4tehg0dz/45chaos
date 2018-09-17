from datetime import datetime
from flask import render_template

from . import main
from .. import models

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/data", methods=["GET", "POST"])
def data():
    # db query and JSON return go here
    return "None"
