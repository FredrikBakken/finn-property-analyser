import re
import sys
import time

from settings import set_browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Start browser driver
def start_browser():
    if set_browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        browser = webdriver.Chrome('webdriver/chromedriver.exe', chrome_options=options)
    elif set_browser == 'phantom':
        browser = webdriver.PhantomJS('webdriver/phantomjs.exe')
        browser.set_window_size(1080, 1920)

    return browser


#### BASIC
def get_map_properties(url):
    # Property list variable
    properties_list = []

    # Start browser
    browser = start_browser()
    time.sleep(2)
    browser.get(url)

    # Wait until website is loaded and open list
    time.sleep(7)
    browser.execute_script("document.getElementById('map-poi-categories').style.display = 'block';")

    # Wait until list is open and select 'hide all'
    time.sleep(1)
    element = browser.find_element_by_xpath('//*[@id="map-poi-categories"]/div/ul/li[2]')
    element.click()

    # Wait until everything is hidden and select map element
    time.sleep(3)
    map_id = browser.find_element_by_id('poiImageMap-1')

    # Split map elements
    map_elements = map_id.get_attribute('innerHTML').split('><')

    # Get finn property IDs
    for x in range(len(map_elements)):
        finn_id = ''
        result = re.search('id="poi_(.*)" class', map_elements[x])

        if result != None:
            finn_id = result.group(1)

            properties_list.append(finn_id)

    # Quit browser
    browser.quit()

    # Return property IDs
    return properties_list
####


#### ADVANCED
def get_advanced_map_properties(url):
    # Property list variable
    properties_list = []

    # Found elements
    map_elements = ''

    # Variables for issue handling
    issue_counter = 0
    extract_properties_issues = True

    while extract_properties_issues and issue_counter < 3:
        try:
            # Start browser
            browser = start_browser()
            browser.get(url)

            # Wait until website is loaded and open list
            time.sleep(15)
            browser.execute_script("document.getElementById('map-poi-categories').style.display = 'block';")

            # Wait until list is open and select 'hide all'
            time.sleep(5)
            element = browser.find_element_by_xpath('//*[@id="map-poi-categories"]/div/ul/li[2]')
            element.click()

            # Wait until everything is hidden and select map element
            time.sleep(8)
            map_id = browser.find_element_by_id('poiImageMap-1')

            # Split map elements
            map_elements = map_id.get_attribute('innerHTML').split('><')
            extract_properties_issues = False
        except:
            browser.quit()
            issue_counter += 1
            print('Issues while starting browser.')
            time.sleep(3)


    # Get finn property IDs
    for x in range(len(map_elements)):
        finn_id = ''
        property_id = ''
        map_slide_pages = ''
        number_of_slides = 0
        result = re.search('id="(.*)" class', map_elements[x])

        if result != None:
            finn_id = result.group(1)
            property_id = finn_id.replace('poi_', '')

            try:
                browser.execute_script('document.getElementById("poi_' + property_id + '").click()')
                time.sleep(3)
            except:
                print('Issues while trying get all property data. Please see the map for unlisted properties.')

            # Find how many slides of properties there are
            try:
                map_slide_pages = browser.find_element_by_xpath(
                    '//*[@id="' + property_id + 'iadPopup_contentDiv"]/div/div/div/div[4]/div[2]/span[2]')

                if not map_slide_pages == '':
                    number_of_slides = int(map_slide_pages.text)
                else:
                    number_of_slides = 1
            except:
                number_of_slides = 1

            for x in range(number_of_slides):
                close = False
                if (x + 1) == number_of_slides:
                    close = True
                else:
                    close = False

                property_data_results = get_property_details(browser, property_id, close)

                try:
                    browser.execute_script('document.querySelectorAll(".navigation.next-ad")[0].click()')
                except:
                    print('ISSUE: Trying to select property add.')

                time.sleep(3)

                if not property_data_results[0] == '':
                    properties_list.append(property_data_results)

    # Quit browser
    browser.quit()

    # Return property IDs
    return properties_list


def get_property_details(browser, property_id, close):
    complete_property_data_list = []
    property_link = ''
    property_data = ''
    property_size = ''
    property_type = ''
    property_ownership = ''
    property_bedrooms = ''
    property_price = ''

    # Get property title
    try:
        property_link = browser.find_element_by_xpath(
            '//*[@id="' + property_id + 'iadPopup_contentDiv"]/div/div/div/div[2]/span[1]/a').get_attribute(
            'href')
    except:
        print('ISSUE: Trying to get property title.')

    time.sleep(2)

    # Get property data (size, type, ownership, bedrooms)
    try:
        property_data = browser.find_element_by_xpath(
            '//*[@id="' + property_id + 'iadPopup_contentDiv"]/div/div/div/div[2]/span[2]').text.split()

        property_size = property_data[0][:-2]
        property_type = property_data[1]
        property_ownership = property_data[2] + ' ' + property_data[3]
        property_bedrooms = property_data[4]
    except:
        print('ISSUE: Trying to get property data.')

    time.sleep(2)

    # Get property price
    try:
        property_price = browser.find_element_by_xpath(
            '//*[@id="' + property_id + 'iadPopup_contentDiv"]/div/div/div/div[2]/span[4]').text.replace(
            'Prisantydning:  ', '').replace('NOK', '').replace(' ', '')[:-2]
    except:
        print('ISSUE: Trying to get property price.')

    time.sleep(2)

    if close:
        # Close the map property window
        try:
            browser.execute_script('document.querySelectorAll(".olPopupCloseBox")[0].click()')
            time.sleep(2)
        except:
            print('ISSUE: Trying to close map property window.')

    # Append all results to data list
    if property_price.isdigit():
        complete_property_data_list.append(property_link)
        complete_property_data_list.append(property_size)
        complete_property_data_list.append(property_type)
        complete_property_data_list.append(property_ownership)
        complete_property_data_list.append(property_bedrooms)
        complete_property_data_list.append(property_price)

        # Return data list
        return complete_property_data_list
    else:
        return ['']
####
