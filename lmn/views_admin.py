import requests
from .models import Artist, Venue, Show
from django.http import HttpResponse
from django.db import IntegrityError
import os


def get_shows():

    key = os.environ.get('TICK_MASTER')
    c_name = 'music'
    query = {'classificationName': c_name, 'apikey': key}
    url = 'https://app.ticketmaster.com/discovery/v2/events.json?'
    request = requests.get(url, params=query)
    response = request.json()
    if request.status_code == 200:
        return response
    if request.status_code == 404:
        return None
    
    request.raise_for_status()

def create_artist(response, i):

    if response is not None:
        try:
            artist_name = response['_embedded']['events'][i]['name']
            artist = Artist(name=artist_name).save()
            return artist
        except IntegrityError:
            pass

def create_venue(response, i):

    if response is not None:    
        try:
            venue_name = response['_embedded']['events'][i]['_embedded']['venues'][0]['name']
            city = response['_embedded']['events'][i]['_embedded']['venues'][0]['city']['name']
            state = response['_embedded']['events'][i]['_embedded']['venues'][0]['state']['name']
            venue = Venue(name=venue_name, city=city, state=state).save()
            return venue
        except IntegrityError:
           pass

def create_show(response, artist, venue, i):

    if response is not None:
        try:
            show_date = response['_embedded']['events'][i]['dates']['start']['dateTime']
            show = Show(show_date=show_date, artist=artist, venue=venue).save()
            return show
        except IntegrityError:
            pass

def admin_main(request):
    response = get_shows()
    for i in range(0, 10):
        artist = create_artist(response,  i)
        venue = create_venue(response, i)
        create_show(response, artist, venue, i)
    return HttpResponse('ok')