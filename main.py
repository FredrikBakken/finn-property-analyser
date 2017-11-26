
### Main file

### Important note: URL in argument has to be within "". E.g.: "www.url.com"

### Run example:
### py -3.5 main.py "https://kart.finn.no/?lng=10.93332&lat=63.47365&tab=iad&zoom=14&mapType=normap&activetab=iad&searchKey=search_id_realestate_homes&keyword=&PRICE_FROM=&PRICE_TO=&ESTATE_SIZE%2FLIVING_AREA_FROM=&ESTATE_SIZE%2FLIVING_AREA_TO=&PLOT%2FAREARANGE_FROM=&PLOT%2FAREARANGE_TO=&NUMBER_OF_BEDROOMS_FROM=&NUMBER_OF_BEDROOMS_TO=&CONSTRUCTION_YEAR_FROM=&CONSTRUCTION_YEAR_TO=&ISNEWPROPERTY=&periode=&metro_distance_TO=&tram_distance_TO=&bus_distance_TO=&train_distance_TO=&orgId="

import sys

from settings import rounds, init_value, round_increase

from web import get_map_properties, get_property_data
from properties import url_properties


# Initializing the program by formatting arguments
def init(arguments):
    # Get the provided argument
    argument = arguments[1]

    # Split the url and url variables
    url = argument.split('?')[0]
    url_variables = argument.split('?')[1].split('&')

    # Execute the program
    run(url, url_variables)


# Run
def run(url, url_variables):
    # Variables
    results = []
    min_bedrooms = 0

    # Loop through the rounds
    for x in range(rounds):
        min_bedrooms = min_bedrooms + 1
        max_amount = init_value + (round_increase * x)

        # Format the url properties
        internal_url = url_properties(url, url_variables, min_bedrooms, max_amount)
        result = [min_bedrooms, max_amount, internal_url]

        # Get properties off finn
        properties = get_map_properties(internal_url)

        # Append results to list
        for y in range(len(properties)):
            #get_property_data(properties[y])
            result.append(properties[y])

        # Append lists to list
        results.append(result)

    # Print results
    for x in range(len(results)):
        for y in range(len(results[x])):
            try:
                skip = results[x][3]

                if y == 0:
                    print('\n\nMinimum number of bedrooms: ' + str(results[x][0]) + ', maximum price: ' + str(results[x][1]) + 'kr.')
                elif y == 1:
                    pass
                elif y == 2:
                    print('Finn.no Map URL: ' + str(results[x][2]))
                else:
                    print('https://www.finn.no/' + results[x][y])
            except:
                pass

    return True


# Handle execution
if __name__ == "__main__":
    arguments = sys.argv
    init(arguments)
