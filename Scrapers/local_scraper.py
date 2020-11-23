import json
import time
import pdb

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common import exceptions

### CHAIN ###
chain = "vons"

# Setup Chromedriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# Initialize data structure
payload = {"name": chain.capitalize(), "stores": []}

driver = webdriver.Chrome(
    'D:\Programs\webdrivers\chromedriver.exe', chrome_options=options)
driver.get(f"https://local.{chain}.com/")


def get_store_data():
    global payload
    global webdriver

    # Wait for page to load
    time.sleep(4)

    # get page data
    phone = driver.find_element_by_id("phone-main").text[1:].replace(") ", "-")
    address = driver.find_element_by_id("address").text.replace("\n", ", ")
    remote_id = phone.replace("-", "")

    # Update payload
    store_object = {"address": address, "phone": phone, "id": remote_id}
    payload["stores"].append(store_object)
    print("Added", store_object)


def write_output():
    global payload
    with open(f"../Outputs/{chain}.json", "w") as f:
        json.dump(payload, f, indent=2)


# Count how many states there are
list_path = "/html/body/main/div[2]/div[2]/div[2]/ul"
state_count = 0
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, list_path)))
time.sleep(4)
try:
    while True:
        state_count += 1
        state_button_path = list_path + f"/li[{state_count}]/a"
        driver.find_element_by_xpath(state_button_path)
except exceptions.NoSuchElementException:
    state_count -= 1

# Loop through states
for state_index in range(state_count):
    print(f"State {state_index+1}/{state_count}")
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, list_path)))
    time.sleep(4)

    # Click on the state
    state_button_path = list_path + f"/li[{state_index + 1}]/a"
    state_button = driver.find_element_by_xpath(state_button_path)
    city_count = int(state_button.get_attribute('data-count')[1:-1])
    state_button.click()

    if city_count == 1:
        get_store_data()
        driver.back()
        time.sleep(4)
        continue

    city_index = 0
    while True:  # loop for cities
        city_index += 1
        # Wait for cities to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, list_path)))
        time.sleep(4)

        # select a city
        city_path = list_path + f"/li[{city_index}]/a"
        try:
            city = driver.find_element_by_xpath(city_path)
            driver.execute_script(
                "return arguments[0].scrollIntoView();", city)
            store_count = int(city.get_attribute("data-count")[1:-1])
            city.click()
        except exceptions.ElementClickInterceptedException:
            # Element was not clickable, try scrolling back up
            driver.execute_script(
                "return arguments[0].scrollIntoView(false);", city)
            city.click()
        except exceptions.NoSuchElementException:
            # No more cities
            driver.back()  # Back to states page
            break

        # If there is only 1 store, it will automatically open that store page
        if store_count == 1:
            get_store_data()
        else:
            # else store_count > 1, must manually click into store
            for store_index in range(store_count):
                # Wait for store to load
                store_path = list_path + f"/li[{store_index + 1}]/article/h2/a"
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, store_path)))
                time.sleep(4)
                driver.find_element_by_xpath(store_path).click()
                get_store_data()
                driver.back()  # Back to the stores page

        time.sleep(4)
        driver.back()  # Back to the cities page

    # Finished a state
write_output()
