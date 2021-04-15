from pybring import BringApi
import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# read google sheet
# tuto https://towardsdatascience.com/how-to-integrate-google-sheets-and-jupyter-notebooks-c469309aacea
spreadsheet_key = r'1aTqsmCbfN8moxBcSwIp1BMXEQDIKRTG9CXWDik51ZZI'
credentials_file = r'/app//credentials/bringapi-92345de4ed45.json'
scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
gc = gspread.authorize(credentials)

book = gc.open_by_key(spreadsheet_key)
worksheet = book.worksheet("Bring!")
table = worksheet.get_all_values()
table = np.array(table)

# create DataFrame
df = pd.DataFrame(data={'item': table[:, 0], 'quantity':  table[:, 1]})
df = df[df['item'] != ''].copy()
df['quantity'] = df['quantity'].astype(float)

df['unit'] = df['item'].str.extract(r'(\(.+\))')
df['unit'] = df['unit'].str[1:-1].values

n_i = []
for i, u in zip(df['item'].tolist(), df['unit'].tolist()):
    n_i.append(i.replace(' ({unit})'.format(unit=u), ''))
df['item'] = n_i

reduced_df = df[df['quantity'] != 0]

# Connect to bring
b = BringApi(uuid='mike.claure@gmail.com', bringuuid='bringMike2021', use_login=True)

for index in range(len(reduced_df)):
    item_i = reduced_df.values[index][0]
    quantity_i = reduced_df.values[index][1]
    unit_i = reduced_df.values[index][2]
    
    b.purchase_item(item=item_i, specification='{} {}'.format(quantity_i, unit_i))



