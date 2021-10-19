from selenium.webdriver.common.keys import Keys

###
# INCOMPLETE:
# Sams club detecting selenium?
###

def execute():
    url = 'https://www.samsclub.com/locator'
    scraper = BaseScraper("Sam's Club", url, 0.1)
    scraper.wait(1)

    for postal in scraper.postals:
        # search(scraper, postal)
        import pdb; pdb.set_trace()
        # verify_human(scraper)
        import pdb; pdb.set_trace()
        # how to tell if it loaded?
        scraper.wait()

        locations = scraper.driver.find_elements_by_class_name('sc-club-card-content')
        [scrape(scraper, l) for l in locations]

    scraper.driver.close()
    return scraper

def verify_human(scraper):
    if 'no robots allowed' in scraper.driver.page_source:
        scraper.driver.find_element_by_class_name('sc-modal-close-button-gray').click()
        return True
    return False

def search(scraper, postal):
    bar = scraper.driver.find_element_by_id('inputbox2')
    bar.send_keys(Keys.BACKSPACE * 20)
    bar.send_keys(postal)
    bar.send_keys(Keys.RETURN)
    return

def scrape(scraper, location):
    remote_id = location.find_element_by_class_name('sc-club-card-club-number').text
    address = location.find_element_by_class_name('sc-club-card-club-address').text
    phone = location.find_element_by_class_name('sc-phone-link').text

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
