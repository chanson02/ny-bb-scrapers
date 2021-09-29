from selenium.common import exceptions

def execute():
    url = 'https://www.cub.com/stores/search-stores.html'
    scraper = BaseScraper('Cub', url)

    for url in get_state_urls(scraper):
        scraper.driver.get(url)
        while True:
            container = scraper.driver.find_element_by_id('store-search-results')
            location_list = container.find_element_by_tag_name('ul')
            locations = location_list.find_elements_by_tag_name('li')
            locations = [l for l in locations if len(l.text) > 30]
            for location in locations:
                scrape(scraper, location)

            try:
                # Go to the next page
                scraper.driver.find_element_by_link_text('Next').click()
            except exceptions.NoSuchElementException:
                break

    scraper.driver.close()
    return scraper

def get_state_urls(scraper):
    container = scraper.driver.find_element_by_id('find-view-states')
    labels = container.find_elements_by_class_name('cell')
    return [l.find_element_by_tag_name('a').get_attribute('href') for l in labels]

def scrape(scraper, location):
    address = location.find_element_by_class_name('store-address').text + ', ' + location.find_element_by_class_name('store-city-state-zip').text
    phone = location.find_element_by_class_name('store-main-phone').text
    remote_id = scraper.strip_char(location.find_element_by_link_text("See Store Details").get_attribute("href"))
    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
