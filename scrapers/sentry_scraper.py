from selenium.common import exceptions

def execute():
    url = 'https://www.sentryfoods.com/my-store/store-locator'
    scraper = BaseScraper("Sentry Foods", url)

    # Wait for locations to load in
    locations = scraper.driver.find_elements_by_class_name('fp-store-info')
    while len(locations) == 0:
        locations = scraper.driver.find_elements_by_class_name('fp-store-info')
    while True:
        locations = scraper.driver.find_elements_by_class_name('fp-store-info')
        try:
            [l.text for l in locations]
            break
        except exceptions.StaleElementReferenceException:
            continue

    # Scrape locations
    [scrape(scraper, l) for l in locations]

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    address = location.find_element_by_class_name('fp-store-address').text
    phone = location.find_element_by_class_name('fp-store-phone').text
    scraper.add_store(address, phone, debug=True)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
    print(f'found {len(scraper.stores)} stores')
else:
    from scrapers.base_scraper import BaseScraper
