# Comrade Resident Advisor

Alexa Skill for reading electronic music event listings for a given city and date.

## Example Usage

Open app with:

> "Alexa, start comrade resident advisor"

Directly get events for a region/date:

> "Alexa, ask comrade resident advisor what events are on in London on May 27th"

Use default location eg:

> "Alexa, ask comrade resident advisor whats on this Friday "

If no date is specified, events for the nearest friday/saturday will be returned by default

> "Alexa, ask comrade resident advisor what events are in London"

## Developer

RA does not provide a public events API, this app scrapes the event pages for listings for a given region/date pair and selects top N events based on number of attendees or configuration settings.

Preferred/default venues for each city can be configured via `config.py`, if there are no configuration settings for a city, top events sorted by number of atendees will be spoken.

App can be hosted locally with ngrok and the endpoint can be configured on the Amazon Developer Console. Deployment to AWS lambda can be done via CLI with something like [zappa](https://github.com/Miserlou/Zappa). Zappa requires you to work in a virtualenv: 

```
>>> git clone https://github.com/varunbalupuri/alexa-RA-events-reader.git
>>> cd alexa-RA-events-reader

>>> virtualenv env
>>> source env/bin/activate
>>> pip install requirements.txt
```

After setting initial configuration for zappa with `zappa init`, modify `zappa_settings.json` with your own AWS details:

```
>>> zappa deploy dev
```


## Contributing

PR's welcome.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details