

def execute():
    url = 'https://www.harpsfood.com/StoreLocator/'
    scraper = BaseScraper('Harps Food Stores', url)
    location_urls = []

    for url in get_state_urls(scraper):
        scraper.driver.get(url)
        table = scraper.driver.find_element_by_class_name('table')
        rows = table.find_elements_by_tag_name('tr')[1:]
        for row in rows:
            location_urls.append(row.find_elements_by_tag_name('td')[-1].find_element_by_tag_name('a').get_attribute('href'))

    for url in location_urls:
        scraper.driver.get(url)
        scrape(scraper)

    scraper.driver.close()
    return scraper

def get_state_urls(scraper):
    container = scraper.driver.find_element_by_class_name('col-md-9')
    labels = container.find_elements_by_tag_name('li')
    anchors = [l.find_element_by_tag_name('a') for l in labels]
    urls = [a.get_attribute('href') for a in anchors]
    return urls

def scrape(scraper):
    container = scraper.driver.find_elements_by_class_name('container-fluid')[1]
    address = ', '.join(container.find_element_by_class_name('Address').text.split('\n')[1:])
    phone = scraper.driver.find_element_by_class_name('PhoneNumber').text
    remote_id = scraper.strip_char(container.find_element_by_tag_name('h3').text)

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
