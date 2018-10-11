import requests
import csv

URL_FORMAT = "https://docs.google.com/spreadsheets/d/%s/export?format=csv&id=%s&gid=%s"
SPREADSHEET_ID = "1IUwAsVqNzs1TXUs3DQdQEwT8txb5MD7Yps9MGO0JV24"
DEPARTURES_GID = "0"
LEGEND_GID = "20619410"
DEPARTURE_KEYS_LINE_INDEX = 3

class Scraper(object):

    def __init__(self):
        self.key_url = URL_FORMAT % (SPREADSHEET_ID, SPREADSHEET_ID, LEGEND_GID)
        self.departures_url = URL_FORMAT % (SPREADSHEET_ID, SPREADSHEET_ID, DEPARTURES_GID)

    def get_legend(self):
        resp = requests.get(self.key_url)
        lines = resp.content.decode().split("\n")
        defs = {}
        for line in lines[2:]:
            split = line.strip().split(",")
            defs[split[0]] = split[1]
        return defs

    def get_all_departures(self):
        departures = []
        resp = requests.get(self.departures_url)
        lines = resp.content.decode().split("\n")
        reader = csv.DictReader(lines[DEPARTURE_KEYS_LINE_INDEX:])
        for row in reader:
            departures.append(row)
        return departures
