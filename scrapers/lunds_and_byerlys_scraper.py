def execute():
    url = 'https://lundsandbyerlys.com/our-stores/locations/'
    scraper = BaseScraper("Lunds & Byerlys", url)
    scraper.wait(3)

    container = scraper.driver.find_element_by_id('wpsl-stores')
    locations = container.find_elements_by_tag_name('li')
    [scrape(scraper, location) for location in locations]

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    data = location.find_element_by_class_name('wpsl-addressLeft').text.split('\n')
    address = ', '.join(data[1:3])
    phone = data[3]
    remote_id = location.get_attribute('data-store-id')

    scraper.add_store(address, phone, remote_id)
    return


if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
