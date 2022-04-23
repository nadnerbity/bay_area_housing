#!/usr/bin/env python
"""Data collection methods and data storage.
version 0.0 - 2019 version that scrapes Zillow
Version 0.1 - 2022 update that downloads data from Redfin
"""

# Because this file uses Firefox via selenium you may need to install
# geckodriver.  If you have homebrew install 'brew install geckodriver' will
# sort it out for you.  You can also download it from the github repo.  It
# needs to be added to your path:
# 'export PATH=$PATH:/path/to/geckodriver/'
# See here for more details:
# https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path
#
# Version 0.0: Original version from 2019
# Version 0.1: Re-written 3 years later to switch to Redfin which has a more permissive API


__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"


# Set up the imports to run the scrape.
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import shared_res
import pandas as pd
import numpy as np
import time
import datetime


def create_browser(path_to_save_loc):
    options = Options()
    options.set_preference("browser.download.folderList", 2)  # the custom location specified browser.download.dir is
    # enabled when browser.download.folderList equals 2
    options.set_preference('browser.download.dir', path_to_save_loc)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference('browser.helperApps.neverAsk.saveToDisk', "text/csv")
    options.set_preference("webdriver_enable_native_events", False)
    options.set_preference("browser.download.manager.scanWhenDone", False)
    options.set_preference("browser.download.manager.useWindow", False)
    options.set_preference("browser.helperApps.alwaysAsk.force", False)

    driver_loc = webdriver.Firefox(options=options)
    return driver_loc


def load_a_page_and_save_data(driver_loc, zipcode_in):
    page_to_load = 'https://www.redfin.com/zipcode/' + zipcode_in
    driver_loc.get(page_to_load)
    t = np.abs(np.random.normal(4, 1))
    print("Pausing for %3.2f seconds" % (t))
    time.sleep(t)

    try:
        temp = driver_loc.find_element(by='id', value="download-and-save")
        # Save the data
        temp.click()
    except NoSuchElementException:
        print('Element does not exist, skipping download')

    except:
        print('Some other error occurred')

    t = np.abs(np.random.normal(8, 1))
    print("Pausing for %3.2f seconds" % (t))
    time.sleep(t)


# Select the zipcodes to search
zip_list = shared_res.santa_clara_county_zip
path_to_save = '/Users/brendan/Documents/Coding/RedfinTravelTime/data'

driver = create_browser(path_to_save)

N = len(zip_list)
print("Grabbing data for %3i zipcodes" % N)
for i in range(N):
    search_zip = zip_list[i]

    print("Searching zipcode " + search_zip + ' which is %3i of %3i' % (i, N-1))
    load_a_page_and_save_data(driver, search_zip)
