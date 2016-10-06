import os
import googlemaps
import csv
from pprint import pprint

api_key = os.environ['GOOGLE_DIRECTIONS_API_KEY']
directions = googlemaps.Client(key=api_key)

api_key = os.environ['GOOGLE_API_KEY']
geolocate = googlemaps.Client(key=api_key)


def geocode(place):
    geocode_result = geolocate.geocode(place)

    formatted_address = geocode_result[0]['formatted_address']
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']

    return formatted_address, lat, lng


with open('data/subset.csv', 'r') as csvfile:
    kiosks = []
    reader = csv.DictReader(csvfile, delimiter=',')

    for row in reader:
        source = row['checkout_kiosk'] + ' Denver, CO'
        target = row['return_kiosk'] + ' Denver, CO'

        d = directions.directions(source, target, mode='bicycling')
        steps = [step['start_location'] for step in d[0]['legs'][0]['steps']]
        pprint(steps)
        break

    # for b_cycle_kiosk in set(kiosks):
    #     address, lat, lng = geocode(b_cycle_kiosk + ' Denver, CO')
    #     if address == 'Denver, CO, USA':
    #         print(b_cycle_kiosk)