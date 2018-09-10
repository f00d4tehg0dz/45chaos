import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pymysql
import csv
from itertools import islice
from datetime import datetime
import pandas as pd
conn = pymysql.connect(host = "127.0.0.1",
                       user = "root",
                       passwd = "",
                       db = "mooches",
                       charset='utf8')

#conn = pymysql.connect(host = "185.21.216.192",
                      #unix_socket = "/media/sde1/home/stargatesga/private/mysql/socket",
                      #user = "root",
                      #passwd = "elNpWb0Nr7YkUuAV",
                      #db = "schoolshooting",
                      #charset='utf8')


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("Departures and Nominations").sheet1
#worksheet = wks.worksheet('Copy of Resignations and Nominations')
cell_list = wks.range('A4:Q641')

for i, worksheet in enumerate(cell_list):
    filename = '-worksheet' + '.csv'
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(wks.get_all_values())

# Start DB connection
cursor = conn.cursor()
# If data exists before, delete
cursor.execute("SELECT id, Name, Department, Position, DatesHired, DatesLeft, TotalTimes, TimesunderTrump, TimesMooches, FiredResign, Notes, Img FROM mooches_table")
#rows = cursor.fetchall()
cursor.execute('Truncate `mooches_table` ')
#clean and remove top row

#test = pd.read_csv("-worksheet.csv", encoding='latin-1', parse_dates=[4], dayfirst=True)

#print (test)
dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')

df = pd.read_csv("-worksheet.csv", encoding='latin-1', error_bad_lines=False, warn_bad_lines=False, parse_dates=[4], date_parser=dateparse)
#df = pd.read_csv("-worksheet.csv", encoding='latin-1', error_bad_lines=False,


# Changing datatype
df['Date Hired'] = pd.to_datetime(df['Date Hired'])
with open("-worksheet.csv", "rt") as infile, open("cleaned.csv", "w") as outfile:
   reader = csv.reader(infile)

   writer = csv.writer(outfile)
   # for column in islice(reader, 4, None):
   #     print(column[4])
   for row in islice(reader, 4, None):
       # process each row
       #writer.writerow(row)

        #new_row = [' '.join([row[0], row[1]])]


        #print(row[])
        #help = [' '.join([row[0], row[1]])], row[2].strip(),row[3].strip(), row[4].strip(), row[6].strip(), row[7].strip(), row[8].strip(), row[9].strip(), row[10].strip(), row[11].strip(), row[16].strip()
        #print (new_row)
        #print (help)
        #sql = "INSERT INTO mooches_table(Name, Department, Position, DatesHired, DatesLeft, TotalTimes, TimesunderTrump, TimesMooches, FiredResign, Notes, Img) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        #cursor.execute(sql, help)

        conn.commit()
        cursor.close()
print ("Done")
