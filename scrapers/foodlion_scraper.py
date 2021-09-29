from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def execute():
    url = 'https://www.foodlion.com/stores/'
    scraper = BaseScraper('Foodlion', url, 0.1)

    # Wait for page to load
    WebDriverWait(scraper.driver, 10).until(
        EC.presence_of_element_located((By.ID, "sidebar-content")))

    for postal in scraper.postals:
        search(scraper, postal)
        # scraper.wait()

        sidebar = scraper.driver.find_element_by_id('sidebar-content').text
        if sidebar == 'No matching search results, please try again.':
            continue
        else:
            locations = sidebar.split('\nHours/Details >\nDirections >\nWEEKLY SPECIALS\n')
            for location in locations:
                scrape(scraper, location)

    scraper.driver.close()
    return scraper

def search(scraper, postal):
    bar = scraper.driver.find_element_by_id('flStoreSearch')
    bar.send_keys(Keys.BACKSPACE * 5)
    bar.send_keys(postal)
    bar.send_keys(Keys.RETURN)

def scrape(scraper, location):
    data = location.split('\n')
    address = data[2] + ', ' + data[3]
    phone = data[4]

    scraper.add_store(address, phone)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
