import csv
import time

from geopy.geocoders import Nominatim

geolocator = Nominatim()


class LocationNotFoundException(Exception):
    pass


def geocode(name, address):
    geocode_location = geolocator.geocode(address, timeout=10)

    if geocode_location is None:
        geocode_location = geolocator.geocode(name + ' Denver Bcycle', timeout=10)
    if geocode_location is None:
        geocode_location = geolocator.geocode(name + ' Denver B-Cycle Station', timeout=10)
    if geocode_location is None:
        geocode_location = geolocator.geocode(name + ' Denver, CO')
    if geocode_location:
        return geocode_location.latitude, geocode_location.longitude
    else:
        raise LocationNotFoundException(address)


with open('data/stations.csv', 'r') as csvfile:
    kiosks = []
    reader = csv.DictReader(csvfile, delimiter=',')

    geocode_rows = []
    for row in reader:
        try:
            lat, lng = geocode(row['name'], row['address'])
            geocode_rows.append(dict(
                name=row['name'],
                address=row['address'],
                lat=lat,
                lng=lng
            ))
        except LocationNotFoundException as e:
            print(row['name'])
            print(row['address'])
            print("\n")

        time.sleep(2)

    with open('data/geocode_stations.csv', 'w') as csvout:
        fieldnames = ['name', 'address', 'lat', 'lng']
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(geocode_rows)
