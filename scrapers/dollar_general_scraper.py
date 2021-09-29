

def execute():
    url = 'https://stores.dollargeneral.com/'
    scraper = BaseScraper('Dollar General', url)

    for state_ndx in range(len(get_list(scraper.driver))):
        state = get_list(scraper.driver)[state_ndx]
        scraper.move(state)
        state.click()

        table = scraper.driver.find_element_by_class_name('state_wrapper')
        for city_ndx in range(len(get_list(table))):
            table = scraper.driver.find_element_by_class_name('state_wrapper')
            city = get_list(table)[city_ndx]
            scraper.move(city)
            city.click()

            for location in scraper.driver.find_elements_by_class_name('itemlist'):
                scrape(scraper, location)

            # Back to cities view
            scraper.driver.back()

        # Back to states view
        scraper.driver.back()

    scraper.driver.close()
    return scraper

def get_list(e):
    return e.find_elements_by_class_name('ga_w2gi_lp')

def scrape(scraper, location):
    data = location.text.split('\n')
    address = ', '.join(data[1:-2])
    phone = data[-2][8:]
    remote_id = scraper.strip_char(data[0])

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
