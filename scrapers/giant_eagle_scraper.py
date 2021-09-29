from selenium.webdriver.common.keys import Keys

def execute():
    url = 'https://www.gianteagle.com/store-locator'
    scraper = BaseScraper('Giant Eagle', url, 2)

    table = scraper.driver.find_element_by_class_name('listing')
    scraper.scroll(table)
    locations = table.find_elements_by_class_name('row')
    location_urls = [l.find_element_by_tag_name('a').get_attribute('href') for l in locations]
    for location_url in location_urls:
        scraper.driver.get(location_url)
        scrape(scraper)

    scraper.driver.close()
    return scraper

def scrape(scraper):
    remote_id = scraper.driver.current_url.split('/')[-1]
    address_elements = []
    while address_elements == []:
        address_elements = [e.text for e in scraper.driver.find_elements_by_class_name('store-address') if e.text != '']
    address = ', '.join(address_elements)
    phone = scraper.driver.find_elements_by_class_name('icon-container')[1].text

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
