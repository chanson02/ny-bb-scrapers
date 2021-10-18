from selenium.webdriver.common.keys import Keys


def execute():
    url = 'https://www.ediblearrangements.com/stores/store-locator.aspx'
    scraper = BaseScraper('Edible Arrangements', url, 2)

    for state in scraper.states:
        search(scraper, state)

        locations = scraper.driver.find_elements_by_class_name('aStore')
        locations = [l for l in locations if l.text != '']
        if len(locations) == 0:
            continue
        for location in locations:
            scrape(scraper, location)

    scraper.driver.close()
    return scraper

def search(scraper, state):
    search_bar = scraper.driver.find_element_by_id('txtSearchStore')
    scraper.move(search_bar)
    search_bar.send_keys(Keys.BACKSPACE * 50)
    search_bar.send_keys(state['name'])
    search_bar.send_keys(Keys.RETURN)
    scraper.wait()
    return

def scrape(scraper, location):
    scraper.move(location)
    address = location.find_element_by_class_name("StoreListAddress").text
    phone = location.find_element_by_class_name("StoreListPhone").text
    remote_id = scraper.strip_char(location.find_element_by_class_name("StoreListName").text)

    scraper.add_store(address, phone, remote_id, True)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
    print(f'found {len(scraper.stores)} stores')
else:
    from scrapers.base_scraper import BaseScraper
