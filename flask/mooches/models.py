from . import db

class Mooches(db.Model):
    __tablename__ = 'mooches_table'
    id = db.Column(db.Integer, primary_key=True)
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
