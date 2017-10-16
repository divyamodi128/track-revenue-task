import json
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

with open('permission.json') as json_data:
    d = json.load(json_data)


res = {}
for key in d:
    res[key] = {}
    for value in d[key]:
        res[key][value] = 1

pprint(res)

df = pd.DataFrame(res).fillna(0).astype(int).T
print(df)

# To convert to .csv 
df.to_csv()

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('google_api_secretkey.json', scope)
client = gspread.authorize(creds)


# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Result.csv").sheet1
print('Row count before inserting', sheet.row_count)
sheet.insert_row(df.columns.insert(0, ''), 1)
for row in df.iterrows():
    lst = [row[0]]
    lst.extend(row[1].tolist())
    sheet.insert_row(lst, 2)
print('Row count after inserting:', sheet.row_count)