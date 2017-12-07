
import sys
import time
import schedule

from settings import rounds, init_value, round_increase, advanced

from web import get_map_properties, get_advanced_map_properties
from properties import url_properties
from spreadsheet import get_number_of_sheets, get_map_url, insert_data


# Schedule for automatic updates
def scheduler():
    schedule.every().day.at("09:00").do(initializer)
    schedule.every().day.at("12:00").do(initializer)
    schedule.every().day.at("15:00").do(initializer)
    schedule.every().day.at("18:00").do(initializer)

    while True:
        schedule.run_pending()
        time.sleep(30)

# Initializing the program by formatting arguments
def initializer():
    # Get number of sheets
    number_of_sheets = get_number_of_sheets()

    # Loop through the sheets
    for x in range(number_of_sheets):
        map = get_map_url(x)

        if not map == '':
            # Split the url and url variables
            url = map.split('?')[0]
            url_variables = map.split('?')[1].split('&')

            # Execute the program
            result = run(url, url_variables)

            # Sorting results (x[0] = bedrooms || x[1] = price)
            sorted_result = sorted(result, key=lambda x: x[1], reverse=False)

            # Insert data into the sheet
            insert_data(x, sorted_result)

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
        if advanced:
            properties = get_advanced_map_properties(internal_url)

            # Append results to list
            for y in range(len(properties)):
                exist = False
                d = [properties[y][4], properties[y][5], properties[y][1], properties[y][2], properties[y][3], properties[y][0], internal_url]
                for z in range(len(result)):
                    if result[z][0:5] == d[0:5]:
                        exist = True

                if not exist:
                    result.append(d)
                else:
                    print('This property is already included in the result list.')
        else:
            properties = get_map_properties(internal_url)

            # Append results to list
            for y in range(len(properties)):
                d = [min_bedrooms, max_amount, 'https://www.finn.no/' + properties[y], internal_url]
                result.append(d)

        # Printing status
        print('Current map progress: ' + str(x + 1) + '/' + str(rounds) + '...')

    # Return properties found for current map
    return result


# Handle execution
if __name__ == "__main__":
    argument = sys.argv
    try:
        if argument[1] == 'auto':
            scheduler()
    except:
        initializer()
