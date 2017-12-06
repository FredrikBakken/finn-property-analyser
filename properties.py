

from settings import freeholder

# Setting URL properties
def url_properties(url, url_variables, min_bedrooms, max_amount):
    internal_url = url + '?'

    # Setting the max price and min bedrooms
    for x in range(len(url_variables)):
        if x == 0:
            internal_url += url_variables[x]
        elif url_variables[x] == 'PRICE_TO=':
            tmp_url_variables = url_variables[x] + str(max_amount)
            internal_url += '&' + tmp_url_variables
        elif url_variables[x] == 'NUMBER_OF_BEDROOMS_FROM=':
            tmp_url_variables = url_variables[x] + str(min_bedrooms)
            internal_url += '&' + tmp_url_variables
        else:
            split_utl_variables = url_variables[x].split('=')

            if not split_utl_variables[1] == '':
                internal_url += '&' + url_variables[x]

    if freeholder:
        internal_url += '&OWNERSHIP_TYPE=3'

    # Return updated url
    return internal_url
