from . import db
from .spreadsheets import Scraper
from datetime import datetime, date
from sqlalchemy.engine.reflection import Inspector
import json

scraper = Scraper()
TRUMP_INAUGURAL = datetime.strptime("01/20/2017", "%m/%d/%Y").date()

# Mapping of Database Columns to their spreadsheet equivalent
UI_HEAD = {
    "LastName": "Last Name",
    "FirstName": "First Name",
    "Affiliation": "Affiliation",
    "Position": "Position",
    "DateHired": "Date Hired",
    "DateLeft": "Date Left",
    "MoochesTime": "Time in Mooches",
    "LeaveType": "Fired/Resigned /Resigned under pressure",
    "Notes": "Notes",
    "Image": "Technical stuff for the website (coming soon)"
}


FAILED_NOMINATIONS_HEAD = {}

VACANCIES_HEAD = {}


class Definition(db.Model):

    """
    Table definition for the mooches legend scraper
    """

    __tablename__ = "definitions"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    Name = db.Column(db.String(64))
    Definition = db.Column(db.Text)

    def to_json():

        """
        Dumps all definitions to a single dict in json
        Usage: return models.Definition.to_json()
        """

        legend_dict = {}
        defs = Definition.query.all()
        for item in defs:
            legend_dict[item.Name] = item.Definition
        return json.dumps(legend_dict)


class Mooch(db.Model):

    """
    Table definition for mooches scraper
    """

    __tablename__ = "mooches_table"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    LastName = db.Column(db.String(64))
    FirstName = db.Column(db.String(64))
    Affiliation = db.Column(db.String(64))
    Position = db.Column(db.Text)
    DateHired = db.Column(db.Date)
    DateLeft = db.Column(db.Date)
    TotalTime = db.Column(db.Integer)
    TrumpTime = db.Column(db.Integer)
    MoochesTime = db.Column(db.Float)
    LeaveType = db.Column(db.String(64))
    Notes = db.Column(db.Text)
    Image = db.Column(db.String(64))
    Sources = db.Column(db.Text)

    def json(self):

        """
        Dumps a single moocher row to json
        Usage: query = models.Mooch.query.first()
               return query.json()
        """

        mooch_dict = {}
        for k, v in vars(self).items():
            if k != "_sa_instance_state":
                if isinstance(v, date):
                    mooch_dict[k] = v.strftime("%m/%d/%Y")
                else:
                    mooch_dict[k] = v
        return json.dumps(mooch_dict)


class FailedNomination(db.Model):

    __tablename__ = "failed_nominations"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    LastName = db.Column(db.String(64))
    FirstName = db.Column(db.String(64))
    Affiliation = db.Column(db.String(64))
    Position = db.Column(db.Text)
    DateNominated = db.Column(db.Date)
    DateRejected = db.Column(db.Date)
    ReasonRejected = db.Column(db.Text)
    Notes = db.Column(db.Text)
    Sources = db.Column(db.Text)

    @property
    def TotalTime(self):
        return (self.DateRejected - self.DateNominated).days

    @property
    def MoochesTime(self):
        return float(round((self.TotalTime / 10), 2))

def check_database():

    """
    Check if the table exists, and seed the database if it doesn't
    """

    inspector = Inspector.from_engine(db.engine)
    tables = inspector.get_table_names()
    if "mooches_table" not in tables or "definitions" not in tables \
            or "failed_nominations" not in tables:
        print("Detected missing tables, running seed")
        seed()


def seed():

    """
    Drop and recreate tables, scrape spreadsheet, and populate the db
    """

    db.drop_all()
    db.create_all()
    for obj in enumerate_departures():
        db.session.add(obj)
    for obj in enumerate_legend():
        db.session.add(obj)
    db.session.commit()


def update():

    """
    Scrape the spreadsheet, and if the entry does not already exist then add it
    """

    check_database()
    new_records = []
    for obj in enumerate_departures():
        if not mooch_exists(obj):
            new_records.append(obj)
    for obj in enumerate_legend():
        if not definition_exists(obj):
            new_records.append(obj)
    if len(new_records) > 0:
        for obj in new_records:
            db.session.add(obj)
        db.session.commit()
    else:
        print("No mooches to update")


def enumerate_legend():

    """
    Parse scraped legend into database objects
    """

    db_objects = []
    for key, value in scraper.get_legend().items():
        object = Definition()
        object.Name = key
        object.Definition = value.replace('"', '')
        db_objects.append(object)
    return db_objects


def enumerate_departures():

    """
    Parse scraped records into database objects
    """

    db_objects = []
    for record in scraper.get_all_departures():
        object = Mooch()
        object.LastName = record[UI_HEAD["LastName"]]
        object.FirstName = record[UI_HEAD["FirstName"]]
        object.Affiliation = record[UI_HEAD["Affiliation"]]
        object.Position = record[UI_HEAD["Position"]]
        object.DateHired = convert_date(record[UI_HEAD["DateHired"]])
        object.DateLeft = convert_date(record[UI_HEAD["DateLeft"]])
        object.MoochesTime = record[UI_HEAD["MoochesTime"]]
        object.LeaveType = record[UI_HEAD["LeaveType"]]
        object.TrumpTime = trumpTime(object.DateHired, object.DateLeft)
        object.TotalTime = (object.DateLeft- object.DateHired).days
        object.Notes = record[UI_HEAD["Notes"]]
        object.Image = record[UI_HEAD["Image"]]
        sources = []
        if record.get("Source 1"):
            sources.append(record["Source 1"])
        if record.get("Source 2"):
            sources.append(record["Source 2"])
        object.Sources = "\n".join(sources)
        db_objects.append(object)
    return db_objects


def definition_exists(definition):

    """
    check if a definition already exists in the database
    """

    query = Definition.query.filter_by(
        Name=definition.Name,
        Definition=definition.Definition
    ).first()
    if query:
        return True
    else:
        return False


def mooch_exists(mooch):

    """
    Check if an entry already exists in the database
    """

    query = Mooch.query.filter_by(
        LastName=mooch.LastName,
        FirstName=mooch.FirstName,
        Position=mooch.Position
    ).first()
    if query:
        return True
    else:
        return False


def convert_date(dateStr):

    """
    Handle date inconsistencies
    """

    if len(str(dateStr)) == 4:
        date = datetime.strptime(str(dateStr), "%Y").date()
    else:
        try:
            date = datetime.strptime(dateStr, "%m/%d/%Y").date()
        except ValueError:
            if len(dateStr.split("/")) == 3:
                fmt = "%m/%d/%y"
            else:
                fmt = "%Y"
            date = datetime.strptime(dateStr.split("-")[-1], fmt).date()
    return date


def get_top_leave_dates():
    moochers = Mooch.query.all()
    leaveDates = {}
    for mooch in moochers:
        if not leaveDates.get(mooch.DateLeft):
            leaveDates[mooch.DateLeft] = 1
        else:
            leaveDates[mooch.DateLeft] += 1
    s = [(k, leaveDates[k]) for k in sorted(leaveDates, key=leaveDates.get, reverse=True)]
    return s[0:5]


def get_affiliation_stats():
    moochers = Mooch.query.all()
    affiliations = {}
    for mooch in moochers:
        if not affiliations.get(mooch.Affiliation):
            affiliations[mooch.Affiliation] = 1
        else:
            affiliations[mooch.Affiliation] += 1
    return affiliations


def get_leave_type_stats():
    moochers = Mooch.query.all()
    leaveTypes = {}
    for mooch in moochers:
        if not leaveTypes.get(mooch.LeaveType):
            leaveTypes[mooch.LeaveType] = 1
        else:
            leaveTypes[mooch.LeaveType] += 1
    return leaveTypes


def get_average_trump_time():
    moochers = Mooch.query.all()
    total = 0
    for mooch in moochers:
        total += mooch.TrumpTime
    return round(float(total/len(moochers)), 2)


def get_average_trump_hire_time():
    moochers = Mooch.query.all()
    total = 0
    moochCount = 0
    for mooch in moochers:
        if mooch.DateHired >= TRUMP_INAUGURAL:
            total += mooch.TrumpTime
            moochCount += 1
    return round(float(total/moochCount), 2)


def get_average_rollover_time():
    moochers = Mooch.query.all()
    total = 0
    moochCount = 0
    for mooch in moochers:
        if mooch.DateHired < TRUMP_INAUGURAL:
            total += mooch.TrumpTime
            moochCount += 1
    return round(float(total/moochCount), 2)


def trumpTime(startDate, leaveDate):

    """
    Return the difference between their leave and either their
    start or Trump inaugural, whichever was later
    """

    if startDate < TRUMP_INAUGURAL:
        startDate = TRUMP_INAUGURAL
    return (leaveDate - startDate).days
