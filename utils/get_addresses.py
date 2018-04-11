import bs4 as bs
import urllib.request
import logging

logger = logging.getLogger(__name__)


def get_club_addresses(html_source):
    """
    Args:
        html_source (str): html representation of webpage

    Returns:
        list: list of tuples containing club name and address.

    """

    soup = bs.BeautifulSoup(sauce, 'lxml').body

    div = soup.find_all('div', attrs={'class': 'fl col4-6'})

    listo = div[0].find_all('li')

    addresses_list = []

    for d in listo:
        if d is not None:
            address_html = d.find('div', attrs={'class': 'fl grey mobile-off'})
            name_html = d.find('a', href=True)

            if address_html and name_html:
                name = name_html.text.lstrip()
                address = address_html.text

                logger.debug('name:', name)
                logger.debug('address:', address)

                addresses_list.append((name, address))

    return list(set(addresses_list))


if __name__ == '__main__':
    i = 13
    url = 'https://www.residentadvisor.net/clubs.aspx?ai={}'.format(i)

    sauce = urllib.request.urlopen(url)

    # TO DO: implement
    region = get_region(sauce)

    if region:
        addrs = get_club_addresses(sauce)

        # TO DO: implement
        save_addrs(region, filepath)