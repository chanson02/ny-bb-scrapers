from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

def execute():
    url = 'https://lowesmarket.com/find-store/'
    scraper = BaseScraper("Lowe's Market", url, 10)

    radius_selector = Select(scraper.driver.find_element_by_id('radiusSelect'))
    radius_selector.select_by_index(len(radius_selector.options) - 1)

    for state in scraper.states:
        search(scraper.driver, state['name'])
        scraper.wait()

        table = scraper.driver.find_element_by_id('map_sidebar')
        while table.text == '':
            table = scraper.driver.find_element_by_id('map_sidebar')
            print('scraper is empty')
        scraper.wait()
        if table.text == 'No locations found.':
            print('no locations')
            continue
        else:
            # import pdb; pdb.set_trace()
            print('locations')

        locations = table.find_elements_by_class_name('location_primary')
        for location in locations:
            scrape(scraper, location)

    scraper.driver.close()
    return scraper

def search(driver, state):
    bar = driver.find_element_by_id('addressInput')
    bar.send_keys(Keys.BACKSPACE * 50)
    bar.send_keys(state)
    bar.send_keys(Keys.RETURN)
    return

def scrape(scraper, location):
    ActionChains(scraper.driver).move_to_element(location).click().perform()
    scraper.wait()

    try:
        address_ids = ['address', 'city', 'state', 'zip']
        address_elements = [scraper.driver.find_element_by_id(f'slp_bubble_{id}').text.replace(',', '').strip() for id in address_ids]
        address = ', '.join(address_elements)
    except Exception:
        # import pdb; pdb.set_trace()
        print('error')
        return

    phone = scraper.driver.find_element_by_id('slp_bubble_phone').text
    remote_id = scraper.strip_char(scraper.driver.find_element_by_id('slp_bubble_name').text)

    scraper.add_store(address, phone, remote_id)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
