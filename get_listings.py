# -*- coding: utf-8 -*-

import bs4 as bs
import urllib.request
from datetime import datetime
import logging

from config import WHITELIST

logger = logging.getLogger(__name__)

def generate_url(region='uk', city='london',
                 date_time=datetime.now()):
    """
    Args:
        country (str): 2 letter ISO country code
        region (str): city or region  as specified by RA
            eg: london or midlands
        date_time (datetime.datetime): datetime of request, defaults to current
    """
    date_str = str(date_time.date())

    base_url = 'https://www.residentadvisor.net/events/{}/{}/day/{}'
    return base_url.format(region, city, date_str)


def get_and_parse_events(url):
    """ gets event details
    """


    sauce = urllib.request.urlopen(url)
    soup = bs.BeautifulSoup(sauce, 'lxml').body

    events_div = soup.find("div", {"id": "event-listing"})
    listo = events_div.find_all('li')

    output = {}

    for el in listo:
        bbox = el.find('div', attrs={'class': 'bbox'})

        if bbox is not None:
            event_details_html = bbox.find('h1', attrs={'class': 'event-title'})
            event_lineup_html = bbox.find('div', attrs={'class': 'grey event-lineup'})
            number_attending_html = bbox.find('p', attrs={'class': 'attending'})

            if (event_details_html is not None) and (event_lineup_html is not None):
                event_name, event_venue = event_details_html.text.lower().rsplit(' at ', 1)
                event_lineup = event_lineup_html.text
                logger.debug('got - event: {}, venue: {}, lineup {}'.format(event_name, event_venue, event_lineup))
                
                if number_attending_html is not None:
                    number_attending = number_attending_html.text
                else:
                    number_attending = 0

                output[event_venue] = {'event_name': event_name,
                                       'event_lineup': event_lineup,
                                       'number_attending': number_attending}
    return output


if __name__ == '__main__':
    # offline testing
    url = 'https://www.residentadvisor.net/events/uk/london/day/2018-04-13'

    events = get_and_parse_events(url)

    region = 'london'

    preferred_venues = WHITELIST.get(region.lower())
    
    if preferred_venues is not None:
        for venue in preferred_venues:
            if events.get(venue) is not None:
                print(venue, events.get(venue))

    # if preferred venues is None -> sort venues by # attending and print top N
