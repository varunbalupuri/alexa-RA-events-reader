from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time

from get_data 

app = Flask(__name__)
ask = Ask(app, "/comrade_resident_advisor")

def get_headlines():
    titles = 'haha'
    return titles

'''
@app.route('/')
def homepage():
    return "hi there, how ya doin?"
'''

@ask.launch
def start_skill():
    welcome_message = 'What is your region?'
    return question(welcome_message)


@ask.intent("LondonIntent")
def get_london_events(region):
    pass



@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'this has not been implemented yet... {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug=True)
