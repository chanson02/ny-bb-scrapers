def execute():
    url = 'https://www.rulerfoods.com/locations'
    scraper = BaseScraper("Ruler Foods", url)
    scraper.wait()

    next_button = scraper.driver.find_element_by_class_name('next_link')
    current_page = int(scraper.driver.find_elements_by_class_name('active')[1].text)
    while True:
        locations = scraper.driver.find_elements_by_class_name('location_secondary')
        loc_ndx = (current_page - 1) * 5 # 5 locations per page
        for location in locations[loc_ndx: loc_ndx + 4]:
            scrape(scraper, location)


        next_button.click()
        new_page = int(scraper.driver.find_elements_by_class_name('active')[1].text)
        if new_page == current_page:
            break
        else:
            current_page = new_page


    scraper.driver.close()
    return scraper

def scrape(scraper, location):
    parts = location.find_elements_by_class_name('slp_result_address')[:-1]
    parts = [p.text for p in parts if p.text != '']
    phone = parts[-1]
    address = ', '.join(parts[:-1])

    scraper.add_store(address, phone, debug=True)
    return

if __name__ == '__main__':
    from base_scraper import BaseScraper
    scraper = execute()
else:
    from scrapers.base_scraper import BaseScraper
