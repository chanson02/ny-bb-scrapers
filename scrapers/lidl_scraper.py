

def execute():
    url = 'https://www.lidl.com/stores'
    scraper = BaseScraper('Lidl', url)

    locations = scraper.driver.find_elements_by_class_name('store-search-card')
    for location in locations:
        scrape(scraper, location)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    address = location.find_element_by_class_name('address').text
    remote_id = scraper.strip_char(location.find_element_by_tag_name('a').get_attribute('href'))
    scraper.add_store(address, None, remote_id)

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
