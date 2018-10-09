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

@main.route('/search', methods=['GET'])
def searchs():
    query = db.session.query(models.Mooch.LastName, models.Mooch.FirstName).order_by(models.Mooch.FirstName).all()
    return json.dumps(query)

@main.route('/process', methods=['GET', 'POST'])
def searchprocess():
    search_string = request.args.get('search_term')
    query = models.Mooch.query.filter_by(LastName=search_string).first()
    def jsonify_mooches(mooches,query):
        jsonified = []
        for mooch in mooches:
            data = vars(mooch)
            mooch_dict = {}
            for k, v in data.items():
                if k != "_sa_instance_state":
                    if isinstance(v, datetime.date):
                        mooch_dict[k] = v.strftime("%m/%d/%Y")
                    else:
                        mooch_dict[k] = v
            jsonified.append(mooch_dict)
        return json.dumps(jsonified)
    #return json.dumps(query)
    #return jsonify(query)

    return jsonify_mooches(query)
