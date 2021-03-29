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
driver.get("https://www.ingles-markets.com/storelocate/")
driver.maximize_window()
chain = {"name": "Ingles Markets", "stores": []}
default_delay = 1

with open("../states.json", "r") as f:
    states = json.load(f)


def scrape():
    phone = driver.find_elements_by_tag_name("a")[-1].text
    data = driver.find_elements_by_tag_name("strong")
    remote_id = re.sub("[^0-9]", "", data[0].text)
    address = data[1].text

    store = {"address": address, "phone": phone, "id": remote_id}
    if store not in chain["stores"]:
        chain["stores"].append(store)
        print("Added", store)


search_bar = driver.find_element_by_id("addressInput")
search_button = driver.find_element_by_id("searchButton")

for state in states:
    search_bar.send_keys(Keys.BACKSPACE * 50)
    search_bar.send_keys(state["name"])
    search_button.click()
    time.sleep(default_delay)

    locations = driver.find_element_by_id("locationSelect")
    anchors = locations.find_elements_by_tag_name("a")
    for a in anchors:
        ActionChains(driver).move_to_element(a).click().perform()
        time.sleep(default_delay)
        driver.switch_to.window(driver.window_handles[-1])
        scrape()
        driver.find_element_by_link_text("Close Window").click()
        driver.switch_to.window(driver.window_handles[0])

with open("../Outputs/ingles_markets.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
