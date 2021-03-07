import json
import time
import pdb
import re
import traceback

from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium.common import exceptions

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"


def gen_url(page):
    return f"https://www.richardsrainwater.com/directory-stores/?_page={page}&num=20&settings_cache_id=7932ec662f5f7534ea23a32f7e6f01a6&sort=post_title"


page = 1
driver = webdriver.Chrome('../chromedriver.exe', desired_capabilities=caps)
driver.get(gen_url(page))
chain = {"name": "The Fresh Market", "stores": []}
default_delay = 1


def scrape(location):
    address = location.find_element_by_class_name("drts-location-address").text
    phone = None
    head = location.find_element_by_class_name("directory-listing-title").text
    remote_id = re.sub("[^0-9]", "", head)

    store = {"address": address, "phone": phone, "id": remote_id}
    if store in chain["stores"]:
        raise "Repeat"
    chain["stores"].append(store)
    print("Added", store)


while True:
    try:
        locations = driver.find_elements_by_class_name("dw-panel__content")
        for location in locations:
            scrape(location)
    except Exception:
        break

    page += 1
    driver.get(gen_url(page))
    time.sleep(default_delay)

with open("../Outputs/fresh_market_ids.json", "w") as f:
    json.dump(chain, f, indent=2)

###########
### OLD ###
###########

# driver.get("https://www.thefreshmarket.com/your-market/store-locator")
# link_index = 0


# def move(element):
#     ActionChains(driver).move_to_element(element).perform()


# def scrape():
#     address = ", ".join(driver.find_element_by_class_name(
#         "store-detail-overlay-group").text.split("\n")[:-1])
#     phone = driver.find_element_by_class_name("simple-link").text
#     remote_id = phone.replace("-", "")

#     store = {"address": address.strip(), "phone": phone, "id": remote_id}
#     chain["stores"].append(store)
#     print("Added", store)


# states = driver.find_elements_by_class_name("accordion__item-title")

# for state_index in range(len(states)):
#     time.sleep(default_delay)
#     states = driver.find_elements_by_class_name("accordion__item-title")
#     state = states[state_index]
#     move(state)
#     state.click()
#     time.sleep(default_delay)

#     links = driver.find_elements_by_class_name(
#         "store-list-item-goto-details-link")
#     while True:
#         time.sleep(default_delay)
#         links = driver.find_elements_by_class_name(
#             "store-list-item-goto-details-link")
#         link = links[link_index]
#         move(link)
#         try:
#             link.click()
#         except:
#             break
#         link_index += 1
#         time.sleep(default_delay)

#         scrape()

#         # Go back to that same states directory
#         driver.back()
#         time.sleep(default_delay)
#         states = driver.find_elements_by_class_name("accordion__item-title")
#         state = states[state_index]
#         move(state)
#         try:
#             state.click()
#         except:
#             move(states[0])
#             move(state)
#             state.click()

# with open("../Outputs/fresh_market.json", "w") as f:
#     json.dump(chain, f, indent=2)
print("Done")
