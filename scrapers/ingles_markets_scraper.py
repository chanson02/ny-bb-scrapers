from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions

def execute():
    url = 'https://www.ingles-markets.com/storelocate/'
    scraper = BaseScraper('Ingles Markets', url)

    scraper.driver.maximize_window()
    for state in scraper.states:
        search(scraper, state['name'])
        scraper.wait(3)

        # Close 'No Locations Found' popup
        try:
            WebDriverWait(scraper.driver, 1).until(EC.alert_is_present())
            alert = scraper.driver.switch_to.alert
            alert.accept()
            continue
        except exceptions.TimeoutException:
            pass

        locations = scraper.driver.find_element_by_id('locationSelect')
        anchors = locations.find_elements_by_tag_name('a')
        for a in anchors:
            ActionChains(scraper.driver).move_to_element(a).click().perform()
            scraper.wait()

            scraper.driver.switch_to.window(scraper.driver.window_handles[-1])
            scrape(scraper)
            scraper.driver.find_element_by_link_text("Close Window").click()
            scraper.driver.switch_to.window(scraper.driver.window_handles[0])

    scraper.driver.close()
    return scraper

def scrape(scraper):
    data = scraper.driver.find_elements_by_tag_name('strong')
    address = data[1].text
    phone = scraper.driver.find_elements_by_tag_name('a')[-1].text
    remote_id = scraper.strip_char(data[0].text)

    scraper.add_store(address, phone, remote_id)
    return

def search(scraper, state):
    bar = scraper.driver.find_element_by_id('addressInput')
    bar.send_keys(Keys.BACKSPACE * 50)
    bar.send_keys(state)
    scraper.driver.find_element_by_id('searchButton').click()
    return


if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
