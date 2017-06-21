"""Using Beautiful Soup with CSS Selectors to collect UNSC Resolutions
"""

import time
from selenium import webdriver


def get_year_urls(driver):
    """Return a list of (year_url, year) pairs
    """
    # WARNING: the final / is very important when doing urljoin below
    base_url = 'http://www.un.org/en/sc/documents/resolutions/'
    driver.get(base_url)
    tables = driver.find_elements_by_css_selector('#content > table')
    # It's a good idea to check you captured something
    # and not more than you expected
    assert len(tables) == 1

    table = tables[0]
    links = table.find_elements_by_css_selector('a')

    out = []
    for link in links:
        # Note that the webdriver returns a resolved URL: not 1977.shtml
        # as in the HTML, rather http://www.un.org/en/sc/documents/resolutions/1977.shtml
        year_url = link.get_attribute('href')
        year = link.text
        # As well as converting to a number, this validates the year text is
        # what we expect
        year = int(year)
        out.append((year_url, year))

    # Check we got something
    assert len(out)
    return out


def get_resolutions_for_year(driver, year_url, year):
    """Return a list of dicts, each detailing 1 UNSC resolution from given year
    """
    driver.get(year_url)
    tables = driver.find_elements_by_css_selector('#content > table')
    if year != 1960 and year != 1964:
        # 1960 and 1964 have the entire page repeated twice!
        # Let's just use the first copy in all cases...
        assert len(tables) == 1

    rows = tables[0].find_elements_by_css_selector('tr')

    out = []
    for row in rows:
        cells = row.find_elements_by_css_selector('td')
        if len(cells) < 2:
            # ignore the header
            continue
        symbol_cell = cells[0]
        title_cell = cells[-1]
        links = symbol_cell.find_elements_by_css_selector('a')
        if not links:
            # http://www.un.org/en/sc/documents/resolutions/2013.shtml
            # has a row which breaks our scraper. Skip it.
            print('Found a cell that does not have a view link: ',
                  symbol_cell.text)
            continue
        url = links[0].get_attribute('href')
        out.append({'year': year,
                    'title': title_cell.text,
                    'symbol': symbol_cell.text,
                    'url': url})
    assert len(out) > 1 or year == 1959
    return out


def scrape_unsc_resolutions():
    # Note that for some projects you might be scraping lots of data
    # over a long time, and so might not want to store all the data in
    # memory at the same time like this code does.
    # driver = selenium.webdriver.PhantomJS(service_args=['--load-images=no'])

    options = webdriver.ChromeOptions()
    # Don't show web browser visually
    options.add_argument('headless')
    # Don't download images
    options.add_experimental_option("prefs",
                                    {"profile.managed_default_content_settings.images": 2})
    driver = webdriver.Chrome(chrome_options=options)

    out = []
    for year_url, year in get_year_urls(driver):
        print('Processing:', year_url)
        out += get_resolutions_for_year(driver, year_url, year)
    return out


if __name__ == '__main__':
    import csv

    resolutions = scrape_unsc_resolutions()

    with open('unsc-resolutions.csv', 'w') as out_file:
        writer = csv.DictWriter(out_file, ['year', 'symbol', 'title', 'url'])
        writer.writeheader()
        for resolution in resolutions:
            writer.writerow(resolution)
