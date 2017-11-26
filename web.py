
import re
import time

from selenium import webdriver


def get_map_properties(url):
    # Property list variable
    properties_list = []

    # Setting webdriver options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Starting browser and open url
    browser = webdriver.Chrome('webdriver/chromedriver.exe', chrome_options=options)
    browser.get(url)

    # Wait until website is loaded and open list
    time.sleep(7)
    browser.execute_script("document.getElementById('map-poi-categories').style.display = 'block';")

    # Wait until list is open and select 'hide all'
    time.sleep(1)
    element = browser.find_element_by_xpath('//*[@id="map-poi-categories"]/div/ul/li[2]')
    element.click()

    # Wait until everything is hidden and select map element
    time.sleep(2)
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
