from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

def execute():
    url = 'https://www.hannaford.com/locations/'
    scraper = BaseScraper('Hannaford', url)
    scraper.wait()

    # Remove the popup
    scraper.driver.find_element_by_class_name("tipso_close").click()

    for postal in scraper.postals:
        while True:
            try:
                search(scraper, postal)
                if results(scraper):
                    locations = scraper.driver.find_elements_by_class_name('list-unstyled')
                    for location in locations:
                        scrape(scraper, location)
                break
            except exceptions.ElementNotInteractableException:
                try:
                    scraper.driver.find_element_by_id('fsrFocusFirst').click()
                except exceptions.NoSuchElementException:
                    scraper.reload_page()
            except exceptions.NoSuchElementException:
                scraper.reload_page()

    scraper.driver.close()
    return scraper

def search(scraper, postal):
    bar = scraper.driver.find_element_by_id('cityStateZip')
    bar.send_keys(Keys.BACKSPACE * 5)
    bar.send_keys(postal)
    bar.send_keys(Keys.RETURN)
    return

def remove_popup(scraper):
    try:
        scraper.driver.find_element_by_id('fsrFocusFirst').click()
    except exceptions.NoSuchElementException:
        pass
    return

def results(scraper):
    try:
        scraper.driver.find_element_by_class_name('search-error')
        return False
    except exceptions.NoSuchElementException:
        return True

def scrape(scraper, location):
    data = location.text.split('\n')
    address = data[3] + ', ' + data[4]
    phone = data[5]
    remote_id = scraper.driver.find_elements_by_link_text(data[0])[-1].get_attribute('href')[-5:]

    scraper.add_store(address, phone, remote_id)

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
