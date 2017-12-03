import gspread

from oauth2client.service_account import ServiceAccountCredentials

# Good tutorial and documentation
# https://www.youtube.com/watch?v=vISRn5qFrkM
# https://media.readthedocs.org/pdf/gspread/latest/gspread.pdf


# Authenticate and access Google Spreadsheets
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Open the spreadsheet
open = client.open("finn-property-analyser")


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
    map = current_sheet.acell('G1').value

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
    map = current_sheet.acell('G1').value
    print('Current map url: ' + map)

    # Delete map specific cells
    current_sheet.update_acell('F1', '')
    current_sheet.update_acell('G1', '')

    # Insert all data into sheet
    for x in range(len(data)):
        current_sheet.insert_row(data[x], 2)

    # Get all records in current sheet
    rec = current_sheet.get_all_records()

    # Re-add map url data
    current_sheet.update_acell('F1', 'MAP URL')
    current_sheet.update_acell('G1', map)

    # Increase sheet variable by 1
    i += 1
