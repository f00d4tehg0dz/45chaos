from . import models, bootstrap_app
from datetime import datetime

TRUMP_INAUGURAL = datetime.strptime("01/20/2017", "%m/%d/%Y").date()

class StatCollector(object):

    def __init__(self):
        self.localContext, self.config = bootstrap_app(no_thread=True)

    def get_all_stats(self):
        statDict = {}
        statDict['Affiliations'] = self.get_affiliation_stats()
        statDict['AverageTrumpTime'] = self.get_average_trump_time()
        statDict['LeaveTypes'] = self.get_leave_type_stats()
        statDict['AverageTrumpHireTime'] = self.get_average_trump_hire_time()
        statDict['AverageRolloverTime'] = self.get_average_rollover_time()
        statDict['AveragePerDayStr'] = self.get_average_per_day_str()
        return statDict

    def get_average_per_day_str(self):
        totalTrumpDays = (datetime.today().date() - TRUMP_INAUGURAL).days
        totalDepartures = len(models.Mooch.query.all())
        perDay = 0
        dayUnit = 1
        while perDay < 1:
            perDay = round(
                float(
                    (totalDepartures / totalTrumpDays) * dayUnit
                ), 2)
            if perDay < 1:
                dayUnit += 1
        if dayUnit == 1:
            return "%s people per day" % perDay
        else:
            return "%s people every %s days" % (perDay, dayUnit)

    def get_affiliation_stats(self):
        affiliations = {}
        with self.localContext.app_context():
            for mooch in models.Mooch.query.all():
                if not affiliations.get(mooch.Affiliation):
                    affiliations[mooch.Affiliation] = 1
                else:
                    affiliations[mooch.Affiliation] += 1
        return affiliations

    def get_average_trump_time(self):
        with self.localContext.app_context():
            moochers = models.Mooch.query.all()
            total = 0
            for mooch in moochers:
                total += mooch.TrumpTime
        return round(float(total/len(moochers)), 2)

    def get_leave_type_stats(self):
        with self.localContext.app_context():
            moochers = models.Mooch.query.all()
            leaveTypes = {}
            for mooch in moochers:
                if not leaveTypes.get(mooch.LeaveType):
                    leaveTypes[mooch.LeaveType] = 1
                else:
                    leaveTypes[mooch.LeaveType] += 1
        return leaveTypes

    def get_average_trump_hire_time(self):
        with self.localContext.app_context():
            moochers = models.Mooch.query.filter(
                models.Mooch.DateHired >= TRUMP_INAUGURAL
            ).all()
            total = 0
            for mooch in moochers:
                total += mooch.TrumpTime
        return round(float(total/len(moochers)), 2)

    def get_average_rollover_time(self):
        with self.localContext.app_context():
            moochers = models.Mooch.query.filter(
                models.Mooch.DateHired < TRUMP_INAUGURAL
            ).all()
            total = 0
            for mooch in moochers:
                total += mooch.TrumpTime
        return round(float(total/len(moochers)), 2)
