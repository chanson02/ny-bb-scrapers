from selenium.webdriver.common.action_chains import ActionChains

def execute():
    url = 'https://local.biglots.com/'
    scraper = BaseScraper('Big Lots', url)

    for state_ndx in range(len(get_list(scraper.driver))):
        select_elem(scraper, state_ndx)

        for city_ndx in range(len(get_list(scraper.driver))):
            location_count = int(get_list(scraper.driver)[city_ndx].get_attribute('data-count')[1:-1])
            select_elem(scraper, city_ndx)

            if location_count == 1:
                scrape(scraper)
            else:
                for loc_ndx in range(location_count):
                    locations = scraper.driver.find_elements_by_class_name('Teaser-titleLink')
                    location = locations[loc_ndx]
                    scraper.move(location)
                    location.click()
                    scrape(scraper)

                    # Back to locations view
                    scraper.driver.back()

            # Back to cities view
            scraper.driver.back()

        # Back to states view
        scraper.driver.back()

    scraper.driver.close()
    return scraper

def get_list(element):
    return element.find_elements_by_class_name('Directory-listLink')

def select_elem(scraper, ndx):
    elem = get_list(scraper.driver)[ndx]
    scraper.move(elem)
    elem.click()

def scrape(scraper):
    address = ', '.join(scraper.driver.find_element_by_class_name('c-address').text.split('\n'))
    phone = scraper.driver.find_element_by_class_name('Phone-display').text
    scraper.add_store(address, phone)


if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
