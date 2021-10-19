def execute():
    url = 'https://www.rosauers.com/store-locations/'
    scraper = BaseScraper("Rosauers Supermarkets", url)

    locations = scraper.driver.find_elements_by_class_name('location')
    [scrape(scraper, l) for l in locations]

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    data = location.text.split('\n')
    address = data[1][9:]
    phone = data[3]

    scraper.add_store(address, phone)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
