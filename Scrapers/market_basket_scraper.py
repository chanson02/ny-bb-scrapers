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
driver.get("https://www.shopmarketbasket.com/store-locations")
driver.maximize_window()
chain = {"name": "Market Basket", "stores": []}
default_delay = 3

time.sleep(default_delay)


def refresh_images():
    try:
        images = [e for e in driver.find_elements_by_tag_name("img") if e.get_attribute(
            "src") == "https://www.shopmarketbasket.com/themes/custom/marketbasket/images/map-pins/mb-pin.png"]
    except Exception:
        time.sleep(default_delay)
        images = [e for e in driver.find_elements_by_tag_name("img") if e.get_attribute(
            "src") == "https://www.shopmarketbasket.com/themes/custom/marketbasket/images/map-pins/mb-pin.png"]
    return images


def scrape_image(image):
    ActionChains(driver).move_to_element(image).click().perform()
    time.sleep(default_delay)

    data = driver.find_element_by_class_name(
        "textholder").find_element_by_tag_name("p").text.split("\n")
    remote_id = re.sub("[^0-9]", "", data[0])
    phone = data[-1][7:].replace(".", "-")
    if "(" in phone:
        phone = phone[1:].replace(") ", "-")
    address = ", ".join(data[1:-1])

    store = {"address": address, "phone": phone, "id": remote_id}
    if store not in chain["stores"]:
        chain["stores"].append(store)
        print("Added", store)

    close_popup()


def close_popup():
    driver.find_element_by_id("closebutton").click()
    time.sleep(default_delay)


def zoom_in():
    zoomer = [e for e in driver.find_elements_by_tag_name(
        "button") if e.get_attribute("title") == "Zoom in"][0]
    zoomer.click()
    time.sleep(default_delay)


def zoom_out():
    zoomer = [e for e in driver.find_elements_by_tag_name(
        "button") if e.get_attribute("title") == "Zoom out"][0]
    zoomer.click()
    # time.sleep(default_delay)


zoom_out()
time.sleep(default_delay)
for image_index in range(len(refresh_images())):
    for _ in range(5):
        image = refresh_images()[image_index]
        scrape_image(image)
        zoom_in()
    image = refresh_images()[image_index]
    scrape_image(image)

    for _ in range(5):
        zoom_out()

with open("../Outputs/market_basket.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
