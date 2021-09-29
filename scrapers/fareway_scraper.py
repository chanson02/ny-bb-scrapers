

def execute():
    url = 'https://www.fareway.com/stores/ia/adel'
    scraper = BaseScraper('Fareway', url)

    checked = []
    while True:
        # Open the dropdown menu
        dropdown = scraper.driver.find_element_by_id('select2-cityState-container')
        dropdown.click()

        cities = scraper.driver.find_elements_by_class_name('select2-results__option')
        cities = [c for c in cities if c.text not in checked]

        if len(cities) == 0:
            # All cities checked
            break
        else:
            # Scrape city
            city = cities[0]
            checked.append(city.text)
            scraper.move(city)
            city.click()

            scrape_city(scraper)

    scraper.driver.close()
    return scraper

def scrape_city(scraper):
    addresses = scraper.driver.find_elements_by_class_name('card-subtitle')
    phones = scraper.driver.find_elements_by_class_name('store-phone')
    ids = scraper.driver.find_elements_by_class_name('card-title')

    for ndx in range(len(addresses)):
        address = addresses[ndx].text
        remote_id = scraper.strip_char(ids[ndx].text)

        try:
            phone = phones[ndx].text.split('\n')[1]
        except IndexError:
            phone = None

        scraper.add_store(address, phone, remote_id)

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
