from flask import render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from datatables import DataTable
import datetime
import json

from . import main
from .. import models, db


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
            ("Name", "LastName", lambda i: " {}, {} ".format(i.LastName, i.FirstName)),
            ("Affiliation"),
            ("Position"),
            ("Hired", "DateHired", lambda i: "  {}  ".format(i.DateHired.strftime("%m/%d/%Y"))),
            ("Left", "DateLeft", lambda i: "  {}  ".format(i.DateLeft.strftime("%m/%d/%Y"))),
            ("Total Days", "TotalTime", lambda i: "  {}  ".format((i.DateLeft - i.DateHired).days)),
            ("Under Trump", "TrumpTime", lambda i: "  {}  ".format(models.trumpTime(i.DateHired, i.DateLeft))),
            ("Mooches", "MoochesTime"),
            ("Fired/Resign", "LeaveType"),
            ("Notes")
        ]
    )
    table.searchable(
        lambda queryset, user_input:
            perform_search(queryset, user_input)
    )
    return json.dumps(table.json())

def perform_search(queryset, user_input):
    return queryset.filter(
        db.or_(
            models.Mooch.LastName.like('%' + user_input + '%'),
            models.Mooch.FirstName.like('%' + user_input + '%'),
            models.Mooch.Affiliation.like('%' + user_input + '%'),
            models.Mooch.Position.like('%' + user_input + '%')
            )
        )

@main.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = db.session.query(models.Mooch.LastName, models.Mooch.FirstName).order_by(models.Mooch.FirstName, models.Mooch.LastName).all()
    return json.dumps(query)

@main.route('/search', methods=['POST'])
def searchprocess():
    search_string = request.form.get('search_term')
    query = models.Mooch.query.filter_by(LastName=search_string).first()

    #query = db.session.query(models.Mooch.LastName, models.Mooch.FirstName, models.Mooch.Affiliation, models.Mooch.Position).order_by(models.Mooch.FirstName).first()
    if not query: # no results return empty list
        return json.dumps([])
    return query.json()
    #return json.dumps(query) # return query.json()

    # use this function when you have a list of models.Mooch objects to return
def jsonify_mooches(mooches):
    return json.dumps([x.json() for x in mooches])
