import datetime

def parse_events_to_speech(events, eventCity, eventDate):
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

    events_list = [_speak_event(event) for event in events]
    # add 2 second break between reading of each event.
    cleaned_template = ' <break time="2s"/> '.join(events_list).replace('&','and')
    intro = 'Suggested events for {} in {}'.format(eventDate, eventCity)
    # Format into SSML - flask-ask automatically detects this.
    speech_template = '<speak> ' + intro + '<break time="2s"/>' + \
                       cleaned_template +' </speak>'

    return speech_template


def get_nearest_weekend_date(date_time):
    """ Returns the nearest friday or saturday
    Args:
        date_time: (datetime.datetime or date)
    Returns:
        (datetime.date): nearest weekend-y date
    """
    weekday = date_time.weekday()

    if (weekday == 6):
        diff = 7
    if (weekday < 5):
        diff = 4-weekday
    else:
        diff = 0

    return (date_time + datetime.timedelta(days=diff)).date()
