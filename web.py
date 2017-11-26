
import re
import time

from selenium import webdriver


def get_map_properties(url):
    properties_list = []

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    browser = webdriver.Chrome('webdriver/chromedriver.exe', chrome_options=options)
    browser.get(url)

    time.sleep(7)

    browser.execute_script("document.getElementById('map-poi-categories').style.display = 'block';")

    time.sleep(2)
    element = browser.find_element_by_xpath('//*[@id="map-poi-categories"]/div/ul/li[2]')
    element.click()

    time.sleep(3)

    map_id = browser.find_element_by_id('poiImageMap-1')

    map_elements = map_id.get_attribute('innerHTML').split('><')

    for x in range(len(map_elements)):
        finn_id = ''
        result = re.search('id="poi_(.*)" class', map_elements[x])

        if result != None:
            finn_id = result.group(1)

            properties_list.append(finn_id)

    browser.quit()

    return properties_list
