"""Using Beautiful tree with CSS Selectors to collect UNSC Resolutions
"""

import time
import requests
from requests.compat import urljoin
from lxml import etree


def inner_text(element):
    return ''.join(element.itertext())


def get_year_urls():
    """Return a list of (year_url, year) pairs
    """
    # WARNING: the final / is very important when doing urljoin below
    base_url = 'http://www.un.org/en/sc/documents/resolutions/'
    response = requests.get(base_url)
    tree = etree.HTML(response.content)
    tables = tree.cssselect('#content > table')
    # It's a good idea to check you captured something
    # and not more than you expected
    assert len(tables) == 1

    table = tables[0]
    links = table.cssselect('a')

    out = []
    for link in links:
        year_url = urljoin(base_url, link.attrib['href'])
        year = link.text
        # As well as converting to a number, this validates the year text is
        # what we expect
        year = int(year)
        out.append((year_url, year))

    # Check we got something
    assert len(out)
    return out


def get_resolutions_for_year(year_url, year):
    """Return a list of dicts, each detailing 1 UNSC resolution from given year
    """
    response = requests.get(year_url)
    tree = etree.HTML(response.content)
    tables = tree.cssselect('#content > table')
    if year != 1960 and year != 1964:
        # 1960 and 1964 have the entire page repeated twice!
        # Let's just use the first copy in all cases...
        assert len(tables) == 1

    rows = tables[0].cssselect('tr')

    out = []
    for row in rows:
        cells = row.cssselect('td')
        if len(cells) < 2:
            # ignore the header
            continue
        symbol_cell = cells[0]
        title_cell = cells[-1]
        links = symbol_cell.cssselect('a')
        if not links:
            # http://www.un.org/en/sc/documents/resolutions/2013.shtml
            # has a row which breaks our scraper. Skip it.
            print('Found a cell that does not have a view link: ',
                  inner_text(symbol_cell))
            continue
        url = links[0].attrib['href']
        out.append({'year': year,
                    'title': inner_text(title_cell),
                    # TODO: whitespace needs cleaning in these!
                    'symbol': inner_text(symbol_cell),
                    'url': urljoin(year_url, url)})
    assert len(out) > 1 or year == 1959
    return out


def scrape_unsc_resolutions():
    # Note that for some projects you might be scraping lots of data
    # over a long time, and so might not want to store all the data in
    # memory at the same time like this code does.
    out = []
    for year_url, year in get_year_urls():
        time.sleep(0.01)
        print('Processing:', year_url)
        out += get_resolutions_for_year(year_url, year)
    return out


if __name__ == '__main__':
    import csv

    resolutions = scrape_unsc_resolutions()

    with open('unsc-resolutions.csv', 'w') as out_file:
        writer = csv.DictWriter(out_file, ['year', 'symbol', 'title', 'url'])
        writer.writeheader()
        for resolution in resolutions:
            writer.writerow(resolution)
