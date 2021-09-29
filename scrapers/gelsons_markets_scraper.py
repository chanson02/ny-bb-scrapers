

def execute():
    url = 'https://www.gelsons.com/stores.html'
    scraper = BaseScraper('Gelsons Markets', url)

    table = scraper.driver.find_element_by_id('store-search-results')
    locations = table.find_elements_by_tag_name('li')
    locations = [l for l in locations if len(l.text) > 30]
    for location in locations:
        scrape(scraper, location)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    remote_id = location.get_attribute('data-storeid')
    address = location.find_element_by_class_name("store-address").text + ', ' + location.find_element_by_class_name("store-city-state-zip").text
    phone = location.find_element_by_class_name("store-main-phone').text[13:]

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
