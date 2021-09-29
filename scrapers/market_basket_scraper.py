from selenium.webdriver.common.action_chains import ActionChains

def execute():
    url = 'https://www.shopmarketbasket.com/store-locations'
    scraper = BaseScraper("Market Basket", url, 3)
    scraper.driver.maximize_window()

    for image_index in range(len(refresh_images(scraper))):
        for _ in range(5):
            image = refresh_images(scraper)[image_index]
            scrape_image(scraper, image)
            zoom_in(scraper)
        image = refresh_images(scraper)[image_index]
        scrape_image(scraper, image)

        for _ in range(5):
            zoom_out(scraper)

    scraper.driver.close()
    return scraper

def scrape_image(scraper, image):
    ActionChains(scraper.driver).move_to_element(image).click().perform()
    scraper.wait()

    data = scraper.driver.find_element_by_class_name('textholder').find_element_by_tag_name('p').text.split('\n')
    remote_id = scraper.strip_char(data[0])
    phone = data[-1]
    address = ', '.join(data[1:-1])
    scraper.add_store(address, phone, remote_id)

    close_popup(scraper)
    return

def refresh_images(scraper):
    scraper.wait()
    try:
        images = [
            e for e in
            scraper.driver.find_elements_by_tag_name('img')
            if e.get_attribute('src') == "https://www.shopmarketbasket.com/themes/custom/marketbasket/images/map-pins/mb-pin.png"
        ]
        return images
    except Exception:
        print('failed')
        return refresh_images(scraper)

def close_popup(scraper):
    scraper.driver.find_element_by_id('closebutton').click()
    scraper.wait()

def zoom_in(scraper):
    zoomer = [
        e for e in
        scraper.driver.find_elements_by_tag_name("button")
        if e.get_attribute("title") == "Zoom in"
    ][0]
    zoomer.click()
    scraper.wait()
    return

def zoom_out(scraper):
    zoomer = [
        e for e in
        scraper.driver.find_elements_by_tag_name("button")
        if e.get_attribute("title") == "Zoom out"
    ][0]
    zoomer.click()
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
