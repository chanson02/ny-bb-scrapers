import json
import time
import pdb
import re
import traceback

from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium.common import exceptions

driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://www.aldi.us/stores/")
chain = {"name": "Aldi", "stores": []}

## NO PHONE OR ID ##

with open("../postals.json", "r") as f:
    postals = json.load(f)["Postal Codes"]

for postal in postals:
    search_bar = driver.find_element_by_id("SingleSlotGeo")
    search_bar.send_keys(Keys.BACKSPACE * 5)
    search_bar.send_keys(postal)
    search_bar.send_keys(Keys.RETURN)

    locations = driver.find_elements_by_class_name("row")
    for location in locations:
        exit()
