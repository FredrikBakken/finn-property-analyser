
import gspread

from settings import rounds, advanced

from time import strftime
from oauth2client.service_account import ServiceAccountCredentials

# Tutorial and documentation for later
# https://www.youtube.com/watch?v=vISRn5qFrkM
# https://media.readthedocs.org/pdf/gspread/latest/gspread.pdf


# Authenticate and access Google Spreadsheets
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Open the spreadsheet
if advanced:
    open = client.open("finn-property-analyser-advanced")
    map1_cell = 'I1'
    map2_cell = 'J1'
    upd1_cell = 'I2'
    upd2_cell = 'J2'
    rnd1_cell = 'I3'
    rnd2_cell = 'J3'
else:
    open = client.open("finn-property-analyser")
    map1_cell = 'F1'
    map2_cell = 'G1'
    upd1_cell = 'F2'
    upd2_cell = 'G2'
    rnd1_cell = 'F3'
    rnd2_cell = 'G3'


# Get total number of sheets
def get_number_of_sheets():
    # Counter variable
    counter = 0

    while True:
        # Get current sheet
        current_sheet = open.get_worksheet(counter)
        if current_sheet == None:
            break

        counter += 1

    return counter


# Get map url
def get_map_url(sheet_number):
    current_sheet = open.get_worksheet(sheet_number)
    map = current_sheet.acell(map2_cell).value

    print('Initializing property extraction for area: ' + current_sheet.title)

    return map


def insert_data(sheet_number, data):
    # Variables
    i = 0

    # Get current sheet
    current_sheet = open.get_worksheet(sheet_number)
    print('Opening sheet named: ' + current_sheet.title)

    # Delete existing data
    r = current_sheet.resize(rows=1)
    print('All previous entries deleted')

    # Get the map url
    map = current_sheet.acell(map2_cell).value
    print('Current map url: ' + map)

    # Delete map and time specific cells
    current_sheet.update_acell(map1_cell, '')
    current_sheet.update_acell(map2_cell, '')

    # Insert all data into sheet
    for x in range(len(data)):
        current_sheet.insert_row(data[x], 2)

    # Get all records in current sheet
    rec = current_sheet.get_all_records()

    # Get current time
    upd_time = strftime("%d-%m-%Y %H:%M:%S")

    # Re-add map url and time data
    current_sheet.update_acell(map1_cell, 'Original map')
    current_sheet.update_acell(map2_cell, map)
    current_sheet.update_acell(upd1_cell, 'Latest update')
    current_sheet.update_acell(upd2_cell, upd_time)
    current_sheet.update_acell(rnd1_cell, 'Max rounds')
    current_sheet.update_acell(rnd2_cell, rounds)

    # Increase sheet variable by 1
    i += 1
