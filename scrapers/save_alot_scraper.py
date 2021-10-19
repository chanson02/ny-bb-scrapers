from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import time

def execute():
    url = 'https://savealot.com/grocery-stores-near-me'
    scraper = BaseScraper("Save A Lot", url, 0.2)

    # ndx = scraper.postals.index('52404')
    for postal in rearrange(scraper):
        try:
            search(scraper, postal)
        except exceptions.ElementNotInteractableException:
            popup(scraper)
            search(scraper, postal)

        try:
            results = scraper.driver.find_element_by_class_name('results')
            locations = results.find_elements_by_class_name('result')
            [scrape(scraper, l) for l in locations]
        except exceptions.NoSuchElementException:
            # No locations here
            pass

    scraper.driver.close()
    return scraper

# Function to make [a, b, c, d] -> [a, d, b, c]
# so the map will update
def rearrange(scraper):
    result = []
    for i in range(int(len(scraper.postals) / 2)):
        result.append(scraper.postals[i])
        result.append(scraper.postals[-i])
    return result


def popup(scraper):
    try:
        scraper.driver.find_element_by_class_name('close').click()
    except (exceptions.NoSuchElementException, exceptions.ElementNotInteractableException):
        pass
    return

def search(scraper, postal):
    bar = scraper.driver.find_element_by_id('locate')
    bar.send_keys(Keys.BACKSPACE * 100)
    bar.send_keys(postal)
    bar.send_keys(Keys.RETURN)
    wait(scraper)
    return

# Wait for the search to compelte
# Wait n seconds or for change in map
# if change: return when hasn't changed for > 0.5 sec
def wait(scraper):
    orig = time.time()
    element = scraper.driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div/section[2]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]')
    previous_value = element.get_attribute('style')

    while time.time() - orig < 4: # Give n seconds to load
        element = scraper.driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div/section[2]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]')
        if element.get_attribute('style') != previous_value:
            change_time = time.time()
            previous_value = element.get_attribute('style')
            while time.time() - change_time < 0.5:
                element = scraper.driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div/section[2]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]')
                if element.get_attribute('style') != previous_value:
                    previous_value = element.get_attribute('style')
                    change_time = time.time()
            return True

    return False

def scrape(scraper, location):
    data = location.find_element_by_class_name('result-address').text.split('\n')
    phone = data[-1]
    address = ', '.join(data[:2])
    remote_id = location.find_element_by_class_name('primary-link').get_attribute('href').split('-')[-1]

    scraper.add_store(address, phone, remote_id, True)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper


# this thing updates?
# /html/body/div[2]/main/div/div/div/section[2]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]
