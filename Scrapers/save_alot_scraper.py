import json
import time
import pdb
import re

from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions


with open("../states.json", "r") as f:
    states = json.load(f)

chain = {"name": "Save a Lot", "stores": []}
driver = webdriver.Chrome(executable_path='../chromedriver.exe')
driver.get("https://savealot.com/grocery-stores-near-me")
time.sleep(2)

search_bar = driver.find_element_by_xpath(
    "/html/body/div[2]/div/div[2]/div/div/div/div/div/div/div[1]/form/input")
for state in states:
    search_bar.send_keys(Keys.BACKSPACE * 5)
    search_bar.send_keys(state["name"])
    search_bar.send_keys(Keys.RETURN)

#     locations = driver.find_elements_by_class_name("sb-location")
#     for location in locations:
#         pass
