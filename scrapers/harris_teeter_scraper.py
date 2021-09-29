

def execute():
    url = 'https://locations.harristeeter.com/'
    scraper = BaseScraper('Harris Teeter', url)
    state_urls = []
    city_urls = []
    location_urls = []

    state_urls = [e.get_attribute('href') for e in scraper.driver.find_element_by_id('state_list').find_elements_by_tag_name('a')]
    for url in state_urls:
        scraper.driver.get(url)
        city_urls += [e.get_attribute('href') for e in scraper.driver.find_element_by_id('cities').find_elements_by_tag_name('a')]
    for url in city_urls:
        scraper.driver.get(url)
        location_urls += [e.get_attribute('href') for e in scraper.driver.find_element_by_id('locations').find_elements_by_tag_name('a')]
    for url in location_urls:
        scraper.driver.get(url)
        scrape(scraper)

    scraper.driver.close()
    return scraper

def scrape(scraper):
    data = scraper.driver.find_element_by_class_name('addressphone').find_element_by_tag_name('div').text.split('\n')
    address = ', '.join(data[:-1])
    phone = data[-1]
    remote_id = scraper.strip_char(scraper.driver.current_url)

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
