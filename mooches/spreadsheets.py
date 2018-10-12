import requests
import csv

URL_FORMAT = "https://docs.google.com/spreadsheets/d/%s/export?format=csv&id=%s&gid=%s"
SPREADSHEET_ID = "1IUwAsVqNzs1TXUs3DQdQEwT8txb5MD7Yps9MGO0JV24"
DEPARTURES_GID = "0"
LEGEND_GID = "20619410"
VACANCIES_GID = "769168722"
FAILURES_GID = "355920076"

DEPARTURE_KEYS_LINE_INDEX = 3
VACANCY_KEYS_LINE_INDEX = 2
FAILURES_KEYS_LINE_INDEX = 2

class Scraper(object):

    def __init__(self):
        self.key_url = URL_FORMAT % (SPREADSHEET_ID, SPREADSHEET_ID, LEGEND_GID)
        self.departures_url = URL_FORMAT % (SPREADSHEET_ID, SPREADSHEET_ID, DEPARTURES_GID)
        self.vacancies_url = URL_FORMAT % (SPREADSHEET_ID, SPREADSHEET_ID, VACANCIES_GID)
        self.failed_noms_url = URL_FORMAT % (SPREADSHEET_ID, SPREADSHEET_ID, FAILURES_GID)

    def _spread_to_dicts(self, url, index):
        objects = []
        resp = requests.get(url)
        lines = resp.content.decode().split("\n")
        reader = csv.DictReader(lines[index:])
        for row in reader:
            objects.append(row)
        return objects

    def get_legend(self):
        resp = requests.get(self.key_url)
        lines = resp.content.decode().split("\n")
        defs = {}
        for line in lines[2:]:
            split = line.strip().split(",")
            defs[split[0]] = split[1]
        return defs

    def get_all_departures(self):
        return self._spread_to_dicts(
            self.departures_url,
            DEPARTURE_KEYS_LINE_INDEX
        )

    def get_all_vacancies(self):
        return self._spread_to_dicts(
            self.vacancies_url,
            VACANCY_KEYS_LINE_INDEX
        )

    def get_all_failed_noms(self):
        return self._spread_to_dicts(
            self.failed_noms_url,
            FAILURES_KEYS_LINE_INDEX
        )
