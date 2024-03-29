from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
from datetime import datetime
import logging

from utils import get_nearest_weekend_date, parse_events_to_speech
from get_listings import generate_url, get_and_parse_events, choose_events

logging.getLogger('flask_ask').setLevel(logging.DEBUG)
app = Flask(__name__)
ask = Ask(app, "/comrade_resident_advisor")


@ask.launch
def start_skill():
    logging.info('entering Comrade Resident Advisor')
    welcome_message = 'Welcome to comrade resident advisor, Which city and date would you like events information for?'
    return question(welcome_message)


@ask.intent('EventsIntent',
            convert={'eventDate': 'date'},
            default={
                     'eventCity': 'london',
                     'eventDate': get_nearest_weekend_date(datetime.now())
                     }
            )
def read_events(eventCity, eventDate):
    eventCity=eventCity.lower()
    logging.info('getting events for city: {}, date: {}'.format(eventCity, eventDate))
    url = generate_url(country='uk', region=eventCity, date_time=eventDate)
    logging.info('requesting url: {}'.format(url))

    events = get_and_parse_events(url)
    chosen_events = choose_events(events, region=eventCity)

    to_speak = parse_events_to_speech(chosen_events, eventCity, eventDate)
    return statement(to_speak)

@ask.intent('AMAZON.HelpIntent')
def help():
    help_template = 'please ask me what events are on for a city and for a date'
    return statement(help_template)

@ask.intent('AMAZON.StopIntent')
def stop():
    stop_template = 'exiting comrade resident advisor'
    return statement(stop_template)

@ask.session_ended
def session_ended():
    return '{}', 200


if __name__ == '__main__':
    app.run(debug=True)

