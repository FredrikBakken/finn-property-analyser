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
    map1_cell = 'J1'
    map2_cell = 'K1'
    upd1_cell = 'J2'
    upd2_cell = 'K2'
    rnd1_cell = 'J3'
    rnd2_cell = 'K3'
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
    num_sheets = 0

    # Login to make sure the token is refreshed
    client.login()

    while True:
        # Get current worksheet
        current_sheet = open.get_worksheet(num_sheets)
        
        # Check if sheet exists
        if current_sheet == None:
            return num_sheets
        
        # Add to counter
        num_sheets += 1


# Get map url
def get_map_url(sheet_number):
    # Login to make sure the token is refreshed
    client.login()

    current_sheet = open.get_worksheet(sheet_number)
    current_map = current_sheet.acell(map2_cell).value

    print('Initializing property extraction for area: ' + current_sheet.title)
    return current_map


# Insert extracted properties into spreadsheet
def insert_data(sheet_number, data):
    try:
        # Login to make sure the token is refreshed
        client.login()

        # Get current sheet
        current_sheet = open.get_worksheet(sheet_number)
        print('Opening sheet named: ' + current_sheet.title)

        # Delete existing data
        r = current_sheet.resize(rows=1)
        print('All previous entries deleted!')

        # Get the map url
        current_map = current_sheet.acell(map2_cell).value
        print('Current map url: ' + current_map)

        # Insert all data into sheet
        for x in range(len(data)):
            current_sheet.insert_row(data[x], 2)

        # Get current time
        upd_time = strftime("%d-%m-%Y %H:%M:%S")

        # Re-add map url and time data
        current_sheet.update_acell(upd1_cell, 'Latest update')
        current_sheet.update_acell(upd2_cell, upd_time)
        current_sheet.update_acell(rnd1_cell, 'Max rounds')
        current_sheet.update_acell(rnd2_cell, rounds)
    except:
        print('ISSUE: Inserting data into spreadsheet.')
