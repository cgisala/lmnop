import requests
from .models import Artist, Venue, Show
from django.http import HttpResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import os


def get_shows():

    # Parameters for API request
    key = os.environ.get('TICK_MASTER')
    c_name = 'music'    # Filter events to music
    num_shows = 200     # Number of upcoming shows
    countryCode = 'US'
    
    query = {'classificationName': c_name, 'countryCode': countryCode, 'size':num_shows, 'apikey': key}
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
        # Get artist name from response
        artist_name = response['_embedded']['events'][i]['name']

        try:
            # Check if data is in database already
            artist = Artist.objects.get(name=artist_name)
        
        except ObjectDoesNotExist:
            # If artist isn't in database, create
            artist = Artist(name=artist_name)
            artist.save()
            
        except IntegrityError:
            pass
            
        return artist

def create_venue(response, i):

    if response is not None:   
        # Get venue details from response
        venue_name = response['_embedded']['events'][i]['_embedded']['venues'][0]['name']
        city = response['_embedded']['events'][i]['_embedded']['venues'][0]['city']['name']
        state = response['_embedded']['events'][i]['_embedded']['venues'][0]['state']['name']

        try:
            # Check if data is in database already
            venue = Venue.objects.get(name=venue_name, city=city, state=state)

        except ObjectDoesNotExist:
            # If venue isn't in database, create
            venue = Venue(name=venue_name, city=city, state=state)    
            venue.save()
        
        except IntegrityError:
            pass
        
        return venue

def create_show(response, artist, venue, i):

    if response is not None:
        show_date_time = response['_embedded']['events'][i]['dates']['start']
        
        # Check if scheduled date is TBA or no specific time, if either ignore
        if show_date_time['timeTBA']:
            return
        if show_date_time['noSpecificTime']:
            return
        # If show has valid dateTime field, create show
        if show_date_time['dateTime']:
            show_date = show_date_time['dateTime']
        else:
            return

        try:    
            show = Show.objects.get(show_date=show_date, artist=artist, venue=venue)

        except ObjectDoesNotExist:
            show = Show(show_date=show_date, artist=artist, venue=venue)
            show.save()

        except IntegrityError:
            pass

def admin_main(request):
    response = get_shows()

    for i in range(0, len(response['_embedded']['events'])):
        artist = create_artist(response,  i)
        venue = create_venue(response, i)
        create_show(response, artist, venue, i)
    return HttpResponse('ok')