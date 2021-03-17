import json
import time
import pdb
import re
import traceback

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium.common import exceptions

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value,
                     OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(
    software_names=software_names, operating_systems=operating_systems, limit=100)
user_agent = user_agent_rotator.get_random_user_agent()

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome('../chromedriver.exe', options=options)
driver.get("https://www.totalwine.com/store-finder/browse")
chain = {"name": "Total Wine", "stores": []}

default_delay = 1


def state_buttons():
    state_list = driver.find_element_by_class_name("chooseStateForm__11Av-cem")
    return state_list.find_elements_by_tag_name("a")


def refresh():
    driver.get(driver.current_url)
    time.sleep(default_delay)


def human_verify():
    frame = driver.find_element_by_tag_name("iframe")
    driver.switch_to.frame(frame)
    button = driver.find_element_by_xpath("/html/body/div")
    action = ActionChains(driver)
    action.click_and_hold(button).perform()
    time.sleep(3)
    action.move_to_element(button).release().perform()
    driver.switch_to.default_content()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "chooseStateForm__11Av-cem")))
    time.sleep(default_delay)
    return


def scrape(container):
    for location in container.find_elements_by_tag_name("li"):
        # address = location.find_element_by_class_name(
        #     "sectionAddress__2q-6eD9Y").text
        address = ", ".join(
            [e.text for e in location.find_elements_by_class_name("addressLine__2zI8XkAD")])
        phone = location.find_element_by_class_name(
            "storePhoneNumber__1JSSHYWv").text[1:].replace(") ", "-")
        url = location.find_element_by_link_text(
            "View Store Info").get_attribute("href")
        remote_id = re.sub("[^0-9]", "", url)

        store = {"address": address, "phone": phone, "id": remote_id}
        chain["stores"].append(store)
        print("Added", store)


time.sleep(default_delay)
for state_index in range(len(state_buttons())):
    state = state_buttons()[state_index]
    state.click()
    time.sleep(default_delay)

    if state_index == 0:
        # Human verification :eye_roll:
        refresh()
        human_verify()
        # load all stores
        driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/main/div/div[1]/div[3]/section/div[3]/div/button").click()

    container = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div/main/div/div[1]/div[3]/section/div[3]/ol")
    scrape(container)

with open("../Outputs/total_wine.json", "w") as f:
    json.dump(chain, f, indent=2)
print("Done")
