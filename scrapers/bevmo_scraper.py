def execute():
    url = 'https://www.bevmo.com/my-store/store-locator'
    scraper = BaseScraper('BevMo!', url)
    scraper.wait(10)

    table = scraper.driver.find_element_by_class_name('fp-panel-list')
    locations = table.find_elements_by_tag_name('li')[2:]
    for location in locations:
        try:
            scrape(scraper, location)
        except Exception:
            continue

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    address = location.find_element_by_class_name('fp-store-address').text
    phone = location.find_element_by_class_name('fp-store-phone').text
    remote_id = location.get_attribute('data-store-number')

    scraper.add_store(address, phone, remote_id)
    return


if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
