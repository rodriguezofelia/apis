from flask import Flask, render_template, request

from pprint import pformat
import os
import requests

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY, 
                'postcalCode': postalcode, 
                'keyword': keyword, 
                'radius': radius, 
                'unit': unit, 
                'sort': sort}

    res = requests.get(url, params=payload)
    """Makes request to event search endpoint and passing all params"""

    data = res.json()
    """Parses and saves JSON received in the response to data"""

    events = data['_embedded']['events']
    """Accessing the dictionary at data embedded with another dictionary of events"""

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    url = f'https://app.ticketmaster.com/discovery/v2/events/{id}'
    payload = {'apikey': API_KEY}

    res = requests.get(url, params=payload)
    """Makes request to event search endpoint and passing all params"""

    event = res.json()
    """Parses and saves JSON received in the response to data"""

    if '_embedded' not in event.keys():
        """"If no venues are listed, go to /event with no venue details"""
        return render_template('event-details.html', 
                            event=event
                            )

    venues = event['_embedded']['venues']
    """Accessing the dictionary at event and accessing dictiionary at embedded"""

    return render_template('event-details.html', 
                            event=event, 
                            venues=venues
                            )

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
