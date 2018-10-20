from flask import render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from datatables import DataTable
from titlecase import titlecase
import datetime
import json

from . import main
from .. import models, db, stats

collector = stats.StatCollector()


@main.route("/api/departures")
def api_departures():
    return jsonify_mooches(models.Mooch.query.all())

@main.route("/api/definitions")
def api_definitions():
    return models.Definition.to_json()

@main.route("/api/stats")
def api_stats():
    return json.dumps(collector.get_all_stats())

@main.route("/api/stats/affiliations")
def affiliation_stats():
    return json.dumps(collector.get_affiliation_stats())

@main.route("/api/stats/perday")
def perday_string():
    return collector.get_average_per_day_str()

@main.route("/api/stats/avgtrumptime")
def avg_trump_time():
    return str(collector.get_average_trump_time())

@main.route("/api/stats/avgtrumphiretime")
def avg_trump_hire_time():
    return str(collector.get_average_trump_hire_time())

@main.route("/api/stats/avgrollovertime")
def avg_rollover_time():
    return str(collector.get_average_rollover_time())

@main.route("/api/stats/leavetypes")
def leave_types():
    return json.dumps(collector.get_leave_type_stats())

@main.route("/departures")
def departures():
    return jsonify_mooches(models.Mooch.query.all())


@main.route("/")
def index():
    totalDepartures = len(models.Mooch.query.all())
    return render_template("index.html", total=totalDepartures)


@main.route("/keys")
def keys():
    definitions = models.Definition.query.order_by(models.Definition.Name).all()
    return render_template("keys.html", definitions=definitions)


@main.route("/mooches")
def mooches():
    return render_template("mooches.html")


@main.route("/stats")
def stats():
    return render_template(
        "stats.html",
        definitions=models.Definition.to_dict(),
        affiliations=collector.get_affiliation_stats(),
        leave_types=collector.get_leave_type_stats(),
        avg_trump_hire_time=collector.get_average_trump_hire_time(),
        avg_rollover_time=collector.get_average_rollover_time(),
        avg_per_day=collector.get_average_per_day_str()
    )


@main.route("/data.php", methods=["POST"])
def mooch_calc():
    today = datetime.datetime.today()
    calcDate = datetime.datetime.strptime(
        request.form.get("df"),
        "%Y-%m-%d"
    )
    totalMooches = str(round(float((today - calcDate).days / 10), 2))
    return '<h3 class="mooches-title">That was %s Mooches ago!</h3>' % totalMooches


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
            ("Hired", "DateHired", lambda i: "{}".format(i.DateHired.strftime("%m/%d/%Y"))),
            ("Left", "DateLeft", lambda i: "{}".format(i.DateLeft.strftime("%m/%d/%Y"))),
            ("Total Days", "TotalTime", lambda i: "{:,}".format((i.DateLeft - i.DateHired).days)),
            ("Under Trump", "TrumpTime", lambda i: "{:,}".format(models.trumpTime(i.DateHired, i.DateLeft))),
            ("Mooches", "MoochesTime"),
            ("Fired/Resign", "LeaveType"),
            ("Notes", lambda i: "{}".format(titlecase(i.Notes))),
            ("Sources")
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
    query = db.session.query(
            models.Mooch.LastName, models.Mooch.FirstName
        ).order_by(
            models.Mooch.FirstName, models.Mooch.LastName
        ).all()
    return json.dumps(query)


@main.route('/search', methods=['POST'])
def searchprocess():
    search_string = request.form.get('search_term')
    query = models.Mooch.query.filter_by(LastName=search_string).first()
    if not query: # no results return empty list
        return json.dumps([])
    return json.dumps(query.dict())


# use this function when you have a list of models.Mooch objects to return
def jsonify_mooches(mooches):
    return json.dumps([x.dict() for x in mooches])
