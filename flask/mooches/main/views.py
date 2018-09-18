from datetime import datetime
from flask import render_template, request
from datatables import DataTable
import json

from . import main
from .. import models, db


TRUMP_INAUGURAL = datetime.strptime("01/20/2017", "%m/%d/%Y").date()


def trumpTime(startDate, leaveDate):

    # Return the difference between their leave and either their
    # start or Trump inaugural, whichever was later

    if startDate < TRUMP_INAUGURAL:
        startDate = TRUMP_INAUGURAL
    return (leaveDate - startDate).days


@main.route("/")
def index():
    return render_template("index.html")

@main.route("/data", methods=["POST"])
def data():
    table = DataTable(
        request.form,
        models.Mooch,
        db.session.query(models.Mooch),
        [
            ("Image"),
            ("Name", "LastName", lambda i: "{}, {}".format(i.LastName, i.FirstName)),
            ("Affiliation"),
            ("Position"),
            ("Hired", "DateHired", lambda i: " {} ".format(i.DateHired.strftime("%m/%d/%Y"))),
            ("Left", "DateLeft", lambda i: " {} ".format(i.DateLeft.strftime("%m/%d/%Y"))),
            ("Total Days", lambda i: "{}".format((i.DateLeft - i.DateHired).days)),
            ("Under Trump", lambda i: "{}".format(trumpTime(i.DateHired, i.DateLeft))),
            ("Mooches", "MoochesTime"),
            ("Fired/Resign", "LeaveType"),
            ("Notes")
        ]
    )
    return json.dumps(table.json())
