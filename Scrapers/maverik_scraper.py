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
driver.maximize_window()
driver.get("https://loyalty.maverik.com/locations/map")
chain = {"name": "Maverik", "stores": []}
default_delay = 2
time.sleep(3)

with open("../Outputs/maverik.json", "r") as f:
    chain = json.load(f)


def write_output():
    with open("../Outputs/maverik.json", "w") as f:
        json.dump(chain, f, indent=2)


def shadow_click(element):
    shadow_root = driver.execute_script(
        'return arguments[0].shadowRoot', element)
    shadow_root.find_element_by_tag_name("button").click()


def scrape(location):
    ActionChains(driver).move_to_element(location).click().perform()
    time.sleep(default_delay)

    name = driver.find_element_by_xpath(
        "/html/body/app-root/ion-app/ion-router-outlet/app-locations/div/div[2]/app-desktop-detail/ion-header/ion-toolbar/ion-buttons/ion-title").text
    remote_id = re.sub("[^0-9]", "", name)
    data = driver.find_element_by_xpath(
        "/html/body/app-root/ion-app/ion-router-outlet/app-locations/div/div[2]/app-desktop-detail/ion-content/div/div[2]").text.split("\n")
    address = ", ".join(data[:2])
    phone = data[2][1:].replace(") ", "-")

    store = {"address": address, "phone": phone, "id": remote_id}
    if store not in chain["stores"]:
        chain["stores"].append(store)
        print("Added", store)

    back_button()


def get_clusters():
    try:
        divs = driver.find_elements_by_tag_name("div")
        cluster_url = "https://s3.us-west-2.amazonaws.com/imagesms-dev.maverik.com/media/ac/assets/cluster_markers/m1.png"
        clusters = [
            cluster for cluster in divs if cluster_url in cluster.get_attribute("style")]
        return clusters
    except Exception as e:
        print(e)
        return []


def get_locations():
    try:
        images = driver.find_elements_by_tag_name("img")
        location_images = [e for e in images if e.get_attribute("src") == "data:image/svg+xml;charset=UTF-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMyAyNyI+PHBhdGggZD0iTTE3LjQ3MSwwYzMuMDUyLDAgNS41MjksMi40ODIgNS41MjksNS41NGwwLDExLjA4YzAsMy4wNTcgLTIuNDc3LDUuNTM5IC01LjUyOSw1LjUzOWwtMi44MjEsMGwtMy4xNSw0Ljg0MWwtMy4xNSwtNC44NDFsLTIuODIxLDBjLTMuMDUyLDAgLTUuNTI5LC0yLjQ4MiAtNS41MjksLTUuNTM5bDAsLTExLjA4YzAsLTMuMDU4IDIuNDc3LC01LjU0IDUuNTI5LC01LjU0bDExLjk0MiwwWiIgc3R5bGU9ImZpbGw6I2FmMjIzMzsiLz48Zz48cGF0aCBkPSJNNy44MjgsMTEuNzY0bDIuNjIzLC00LjQ3N2wyLjU4OCw0LjQ3N2wtNS4yMTEsMFoiIHN0eWxlPSJmaWxsOiNmZmY7Ii8+PHBhdGggZD0iTTQuNDcsMTEuNzY0bDQuMjY3LC03LjQxNWwxLjE4OSwyLjA2M2wtMy4wNzgsNS4zNTJsLTIuMzc4LDBaIiBzdHlsZT0iZmlsbDojZmZmOyIvPjxwYXRoIGQ9Ik0xNC4wMTgsMTEuNzY0bC0zLjA3OCwtNS4zNTJsMi4yMzksLTMuOTE3bDUuMzUxLDkuMjY5bC00LjUxMiwwWiIgc3R5bGU9ImZpbGw6I2ZmZjsiLz48L2c+PC9zdmc+"]
        return location_images
    except:
        return []


def back_button():
    try:
        back_button = driver.find_element_by_xpath(
            "/html/body/app-root/ion-app/ion-router-outlet/app-locations/div/div[2]/app-desktop-detail/ion-header/ion-toolbar/ion-buttons/ion-button")
        shadow_click(back_button)
    except:
        print("Back failed")
    time.sleep(default_delay)


# Close popup
driver.find_element_by_class_name("alert-button-inner").click()

# Select 'Search by Store #'
store_number_type = driver.find_element_by_xpath(
    "/html/body/app-root/ion-app/ion-router-outlet/app-locations/div/div[2]/div/ion-radio-group/div/div[4]/ion-radio")
shadow_click(store_number_type)
time.sleep(3)

for i in range(694, 999):
    search_bar = driver.find_element_by_xpath(
        "/html/body/app-root/ion-app/ion-router-outlet/app-locations/div/div[2]/div/div[2]/ion-searchbar/div/input")
    search_bar.send_keys(Keys.BACKSPACE * 3)
    search_bar.send_keys(str(i))
    time.sleep(default_delay)

    for location_index in range(len(get_locations())):
        location = get_locations()[location_index]
        scrape(location)

    while len(get_clusters()) > 0:
        cluster = get_clusters()[0]
        try:
            ActionChains(driver).move_to_element(
                cluster).click().click().perform()
        except:
            pass
        time.sleep(default_delay)
        for location_index in range(len(get_locations())):
            location = get_locations()[location_index]
            scrape(location)


print("Done")
