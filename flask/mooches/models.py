from . import db
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
CREDENTIAL_FILE = "client_secret.json"
WORKSHEET_NAME = "Trump Gov Departures"
HEAD_ROW = 4

UI_HEAD = {
    "LastName": "Last Name",
    "FirstName": "First Name",
    "Affiliation": "Affiliation",
    "Position": "Position",
    "DateHired": "Date Hired",
    "DateLeft": "Date Left",
    "TotalTime": "Total Time (days)",
    "TrumpTime": "Time under Trump (days)",
    "MoochesTime": "Time in Mooches",
    "LeaveType": "Fired/Resigned /Resigned under pressure",
    "Notes": "Notes"
}

class Mooch(db.Model):
    __tablename__ = 'mooches_table'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    LastName = db.Column(db.String(64))
    FirstName = db.Column(db.String(64))
    Affiliation = db.Column(db.String(64))
    Position = db.Column(db.String(64))
    DateHired = db.Column(db.Date)
    DateLeft = db.Column(db.Date)
    TotalTime = db.Column(db.Integer)
    TrumpTime = db.Column(db.Integer)
    MoochesTime = db.Column(db.Float)
    LeaveType = db.Column(db.String(64))
    Notes = db.Column(db.Text)
    Sources = db.Column(db.Text)

def seed():
    db.drop_all()
    db.create_all()
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIAL_FILE,
        SCOPE
    )
    gc = gspread.authorize(creds)
    wks = gc.open(WORKSHEET_NAME).sheet1
    records = wks.get_all_records(head=HEAD_ROW)
    db_objects = enumerate_records(records)
    for obj in db_objects:
        db.session.add(obj)
    db.session.commit()

def enumerate_records(records):
    db_objects = []
    for record in records:
        object = Mooch()
        object.LastName = record[UI_HEAD["LastName"]]
        object.FirstName = record[UI_HEAD["FirstName"]]
        object.Affiliation = record[UI_HEAD["Affiliation"]]
        object.Position = record[UI_HEAD["Position"]]
        object.DateHired = convert_date(record[UI_HEAD["DateHired"]])
        object.DateLeft = convert_date(record[UI_HEAD["DateLeft"]])
        object.TotalTime = record[UI_HEAD["TotalTime"]]
        object.TrumpTime = record[UI_HEAD["TrumpTime"]]
        object.MoochesTime = record[UI_HEAD["MoochesTime"]]
        object.LeaveType = record[UI_HEAD["LeaveType"]]
        object.Notes = record[UI_HEAD["Notes"]]
        sources = []
        if record.get("Source 1"):
            sources.append(record["Source 1"])
        if record.get("Source 2"):
            sources.append(record["Source 2"])
        object.Sources = "\n".join(sources)
        db_objects.append(object)
    return db_objects

def convert_date(dateStr):
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
