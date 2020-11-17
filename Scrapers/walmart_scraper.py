import pdb
import time
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions

# Load in postal data
with open('../postals.json', 'r') as file:
    postals = json.load(file)["Postal Codes"]

# Load in previously found walmarts
file = "../Outputs/walmarts.json"
with open(file, "r") as f:
    chain = json.load(f)

# Open webdriver and wait for page to load
driver = webdriver.Chrome('../chromedriver.exe')
driver.get("https://walmart.com/store/finder?location=00501&distance=10")
base_path = "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div/"

nearby_stores = base_path + "div[2]/div/div/span/div/div/ol"
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, nearby_stores)))

# To change the zipcode
location_button_path = base_path + \
    "div[1]/div/div[2]/section/div[1]/p[1]/span"
# when clicking on the info button
details_path = base_path + "div/div/div/div/div/div[2]"
# Find stores in each postal code
for postal_code in postals:
    # Click on location (to change it)
    location_button = driver.find_element_by_xpath(location_button_path)
    location_button.click()

    # Empty / Fill zipcode area
    text_input_path = base_path + "div[1]/div/div[2]/div/span/form/label/input"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, text_input_path)))
    text_input = driver.find_element_by_xpath(text_input_path)
    time.sleep(0.3)
    text_input.send_keys(Keys.BACKSPACE * 5)
    time.sleep(0.3)
    text_input.send_keys(postal_code)
    time.sleep(0.3)
    text_input.send_keys(Keys.RETURN)
    time.sleep(0.3)

    try:
        # Wait for nearby to appear
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, nearby_stores)))
    except exceptions.TimeoutException:
        # No stores at this location
        continue

    # Look for all nearby stores
    store_index = 0
    while True:
        store_index += 1

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, nearby_stores)))

        store_path = nearby_stores + f"/li[{store_index}]"
        try:
            time.sleep(0.3)
            driver.find_element_by_xpath(store_path).click()
        except exceptions.NoSuchElementException:
            break

        # Click to see store info
        info_button_path = store_path + "/div/div[2]/span[2]/span"
        driver.find_element_by_xpath(info_button_path).click()

        # Looking at store info. Grab data
        id_path = details_path + \
            "/div[3]/div/div[2]/div/div[1]/div/div[1]/span[2]"
        phone_path = details_path + "/div[3]/div/div[3]/div/div/div[3]/a/div"
        city_path = details_path + "/div[2]/div/h3/span[1]"
        address_path = details_path + \
            "/div[3]/div/div[2]/div/div[1]/div/div[2]"

        # Wait for page to load
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, id_path)))

        # Pulling text data from elements
        remote_id = driver.find_element_by_xpath(id_path).text[2:]
        phone = driver.find_element_by_xpath(phone_path).text
        city = driver.find_element_by_xpath(city_path).text
        address = driver.find_element_by_xpath(
            address_path).text.replace(",  ", f", {city}, ")

        # Creating store object
        store = {"address": address, "phone": phone, "id": remote_id}

        # Check for redundancy
        if store not in chain["stores"]:
            chain["stores"].append(store)
            print("Added", store)

        # Go back to nearby stores list
        back_button_path = base_path + "div/div/div/div/div/div[1]/button"
        driver.find_element_by_xpath(back_button_path).click()

    print(f"{round(postals.index(postal_code) / len(postals) * 100, 2)}%")

    # After each postal code, backup to file
    with open(file, "w") as f:
        json.dump(chain, f, indent=2)

driver.quit()
