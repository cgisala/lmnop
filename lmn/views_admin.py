import requests
from .models import Artist, Venue, Show
from django.http import HttpResponse
from django.db import IntegrityError
import os


def get_shows():

    key = os.environ.get('TICK_MASTER')
    query = {'apikey': key}
    url = 'https://app.ticketmaster.com/discovery/v2/events.json?'
    response = requests.get(url, params=query).json()
    if response.status_code == 200:
        return response
    if response.status_code == 404:
        return None
    
    response.raise_for_status()

def create_artist(response):

    if response is not None:
        try:
            artist_name = response['_embedded']['events'][0]['name']
            artist = Artist(name=artist_name).save()
            return artist
        except IntegrityError:
            pass

def create_venue(response):

    if response is not None:    
        try:
            venue_name = response['_embedded']['events'][0]['_embedded']['venues'][0]['name']
            city = response['_embedded']['events'][0]['_embedded']['venues'][0]['city']['name']
            state = response['_embedded']['events'][0]['_embedded']['venues'][0]['state']['name']
            venue = Venue(name=venue_name, city=city, state=state).save()
            return venue
        except IntegrityError:
            pass

def create_show(response, artist, venue):

    if response is not None:
        try:
            show_date = response['_embedded']['events'][0]['dates']['start']['dateTime']
            show = Show(show_date=show_date, artist=artist, venue=venue).save()
        except IntegrityError:
            pass

def admin_main(request):
    response = get_shows()
    artist = create_artist(response)
    venue = create_venue(response)
    create_show(response, artist, venue)
    return HttpResponse('ok')