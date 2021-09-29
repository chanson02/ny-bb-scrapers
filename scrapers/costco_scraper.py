

def execute():
    url = 'https://www.costco.com/WarehouseListByStateDisplayView'
    scraper = BaseScraper('Costco', url, 1)

    state_buttons = scraper.driver.find_elements_by_class_name('warehouse-title-link')
    state_buttons = [b for b in state_buttons if b.text != '']
    for state_button in state_buttons:
        scraper.move(state_button)
        state_button.click()
        scraper.wait()
        locations = scraper.driver.find_elements_by_class_name('warehouse-item')
        for location in locations:
            scrape(scraper, location)

    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    address = location.find_element_by_class_name('h6-style-guide').text
    phone = location.find_element_by_class_name('body-copy-link').text
    url = location.find_element_by_link_text('Store Details').get_attribute('href')
    remote_id = scraper.strip_char(url)
    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
