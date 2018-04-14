# -*- coding: utf-8 -*-

import bs4 as bs
import urllib.request
from datetime import datetime
import logging
from collections import OrderedDict


from config import WHITELIST

logger = logging.getLogger(__name__)


def generate_url(country='uk', region='london',
                 date_time=datetime.now()):
    """ Generates event page url
    Args:
        country (str): 2 letter ISO country code
        region (str): city or region  as specified by RA
            eg: london or midlands
        date_time (datetime.datetime): datetime of request, defaults to current
    """
    date_str = str(date_time.date())

    base_url = 'https://www.residentadvisor.net/events/{}/{}/day/{}'
    return base_url.format(country, region, date_str)


def get_and_parse_events(url):
    """gets event details
    Args:
        url (str): RA event page URL
    Returns:
        dict: dict with venues as keys and event name,
            lineup and number attending
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
                logger.debug('got - event: {}, venue: {}, lineup {}'.format(event_name,
                                                                            event_venue,
                                                                            event_lineup)
                             )

                if number_attending_html is not None:
                    number_attending = int(number_attending_html.text.split(' ')[0])
                else:
                    number_attending = 0

                output[event_venue] = {'event_name': event_name,
                                       'event_lineup': event_lineup,
                                       'number_attending': number_attending}

    output = OrderedDict(sorted(output.items(),
                            key=lambda x: x[1]['number_attending'],
                            reverse=True
                            )
                     )
    return output


def choose_events(events_dict, region='london', max_num=5):
    """ chooses max_num events in order of preference, or sorted
    by number attending if there are not enough preferences.
    Args:
        events_dict (OrderedDict): dict with venues as keys and event name,
            lineup and number attending, corresponding to the output
            of get_and_parse_events
        max_num (int): maximum number of events to display

    Returns:
        events: truncated dict of events
    """

    preferred_venues = WHITELIST.get(region.lower())

    events = list(events_dict.items())

    # in case of no preferences for region, just take top by # attending
    if preferred_venues is None:
        logger.info('no config for {}, taking top {} events'.format(region, max_num))
        return events[:max_num]

    # iterate through preferences and find valid listings
    chosen_cntr = 0
    output = []
    for venue in preferred_venues:
        if chosen_cntr >= max_num:
            logger.info('found sufficient events at preferred venues')
            return output

        if events_dict.get(venue) is not None:
            chosen_cntr += 1
            output.append((venue, events_dict.get(venue)))

    # if we still do not have max_num events in total, get more
    # by taking top events which are not in preferences
    logger.info('appending additional events, not enough events in preferences')
    for event in events:
        if chosen_cntr >= max_num:
            return output

        if event[0] not in preferred_venues:
            chosen_cntr += 1
            output.append((event[0], event[1]))

    return output


def parse_events_to_speech(events):
    """takes list of events in format output by
    choose_events and parses them into alexa speakable text
    Args:
        events (list): list of events and details.
    Returns:
        list[str]: list of speakable text strings.
    """
    def _speak_event(event):
        template = '{} at {}, featuring {} . There are {} people attending'
        return template.format(event[1]['event_name'],
                               event[0],
                               event[1]['event_lineup'],
                               event[1]['number_attending']
                               )

    return [_speak_event(event) for event in events]


if __name__ == '__main__':
    # offline testing
    url = 'https://www.residentadvisor.net/events/uk/london/day/2018-04-13'

    # region = 'london'

    events = get_and_parse_events(url)

    chosen_events = choose_events(events, region='london')

    a = parse_events_to_speech(chosen_events)