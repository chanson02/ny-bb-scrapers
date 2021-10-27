from selenium.common.exceptions import NoSuchElementException

def execute():
    url = 'https://www.shoppersfood.com/stores/search-stores.html'
    scraper = BaseScraper("Shoppers Food", url)

    states = scraper.driver.find_element_by_id('find-view-states')
    state_urls = [s.get_attribute('href') for s in states.find_elements_by_tag_name('a')]
    for url in state_urls:
        scraper.reload_page(url)
        scraper.wait()

        scrape_table(scraper)
        nxt = next_button(scraper)
        while nxt is not None:
            scrape_table(scraper)
            nxt.click()
            scraper.wait()
            nxt = next_button(scraper)


    scraper.driver.close()
    return scraper

def next_button(scraper):
    try:
        return scraper.driver.find_element_by_link_text("Next")
    except NoSuchElementException:
        return None

def scrape_table(scraper):
    table = scraper.driver.find_element_by_id('store-search-results')
    locations = [l for l in table.find_elements_by_tag_name('li') if len(l.text) > 50]
    [scrape(scraper, l) for l in locations]
    return

def scrape(scraper, location):
    address = ', '.join([
        location.find_element_by_class_name('store-address').text,
        location.find_element_by_class_name('store-city-state-zip').text
    ])
    phone = location.find_element_by_class_name('store-main-phone').text
    remote_id = location.get_attribute('data-storeid')

    scraper.add_store(address, phone, remote_id, True)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
    print(f'found {len(scraper.stores)} stores')
else:
    from scrapers.base_scraper import BaseScraper
