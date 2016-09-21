import os
import sys
import googlemaps
import csv

# Add the top level of the repo so this script can import application modules
sys.path.insert(0, os.path.dirname('..'))

from bcycle import db
from bcycle.models import Kiosk, Trip


api_key = os.environ['GOOGLE_API_KEY']
gmaps = googlemaps.Client(key=api_key)

Trip.query.delete()
Kiosk.query.delete()


def geocode(place):
    geocode_result = gmaps.geocode(place)

    formatted_address = geocode_result[0]['formatted_address']
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']

    return formatted_address, lat, lng


with open('data/subset.csv', 'r') as csvfile:
    kiosks = []
    reader = csv.DictReader(csvfile, delimiter=',')

    for row in reader:
        kiosks.append(row['checkout_kiosk'])
        kiosks.append(row['return_kiosk'])

    for b_cycle_kiosk in set(kiosks):
        address, lat, lng = geocode(b_cycle_kiosk + ' Denver, CO')

        kiosk = Kiosk(kiosk_name=b_cycle_kiosk,
                      geocoded_name=address,
                      lat=lat,
                      lng=lng)

        db.session.add(kiosk)

    db.session.commit()
