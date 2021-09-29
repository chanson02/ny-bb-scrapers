from selenium.webdriver.common.keys import Keys

def execute():
    url = 'https://www.lowesfoods.com/store-locator'
    scraper = BaseScraper('Lowes Foods', url, eager=True)

    scraper.wait()
    search(scraper.driver)
    scraper.wait()

    urls = [b.get_attribute('href') for b in scraper.driver.find_elements_by_link_text('Store Details')]
    for url in urls:
        scraper.driver.get(url)
        scrape(scraper)

    scraper.driver.close()
    return scraper

def search(driver):
    bar = driver.find_element_by_tag_name('input')
    bar.send_keys(Keys.BACKSPACE * 100)
    bar.send_keys(Keys.RETURN)
    return

def scrape(scraper):
    address_elements = scraper.driver.find_element_by_class_name('store-details__store-info').find_elements_by_tag_name('li')[1:4]
    address = ', '.join([e.text for e in address_elements if e.text != ''])

    phone = scraper.driver.find_element_by_class_name('store-details__store-info__phone').find_element_by_tag_name('a').text
    remote_id = scraper.strip_char(scraper.driver.current_url)

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
