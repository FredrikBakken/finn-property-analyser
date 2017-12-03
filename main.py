
### Main file

### Important note: URL in argument has to be within "". E.g.: "www.url.com"

### Run example:
### py -3.5 main.py "https://kart.finn.no/?lng=10.93332&lat=63.47365&tab=iad&zoom=14&mapType=normap&activetab=iad&searchKey=search_id_realestate_homes&keyword=&PRICE_FROM=&PRICE_TO=&ESTATE_SIZE%2FLIVING_AREA_FROM=&ESTATE_SIZE%2FLIVING_AREA_TO=&PLOT%2FAREARANGE_FROM=&PLOT%2FAREARANGE_TO=&NUMBER_OF_BEDROOMS_FROM=&NUMBER_OF_BEDROOMS_TO=&CONSTRUCTION_YEAR_FROM=&CONSTRUCTION_YEAR_TO=&ISNEWPROPERTY=&periode=&metro_distance_TO=&tram_distance_TO=&bus_distance_TO=&train_distance_TO=&orgId="

import sys

from settings import rounds, init_value, round_increase

from web import get_map_properties
from properties import url_properties
from spreadsheet import get_number_of_sheets, get_map_url, insert_data


# Initializing the program by formatting arguments
def initializer():
    # Get number of sheets
    number_of_sheets = get_number_of_sheets()

    # Loop through the sheets
    for x in range(number_of_sheets):
        map = get_map_url(x)

        # Split the url and url variables
        url = map.split('?')[0]
        url_variables = map.split('?')[1].split('&')

        # Execute the program
        result = run(url, url_variables)

        insert_data(x, result)

    return True


# Run
def run(url, url_variables):
    # Variables
    result = []
    min_bedrooms = 0

    # Loop through the rounds
    for x in range(rounds):
        min_bedrooms = min_bedrooms + 1
        max_amount = init_value + (round_increase * x)

        # Format the url properties
        internal_url = url_properties(url, url_variables, min_bedrooms, max_amount)

        # Get properties off finn
        properties = get_map_properties(internal_url)

        # Append results to list
        for y in range(len(properties)):
            d = [min_bedrooms, max_amount, 'https://www.finn.no/' + properties[y], internal_url]
            result.append(d)

        print('Program progress: ' + str(x + 1) + '/' + str(rounds) + '...')

    return result

# Handle execution
if __name__ == "__main__":
    arguments = sys.argv
    initializer()
