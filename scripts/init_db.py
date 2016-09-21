import sys
import os
import csv

from datetime import datetime

# Add the top level of the repo so this script can import application modules
sys.path.insert(0, os.path.dirname('..'))

from bcycle import db
from bcycle.models import Kiosk, Rider, Trip


Trip.query.delete()
Rider.query.delete()


def format_datetime(date, time):
    as_string = '{} {}'.format(date, time)
    date_time = datetime.strptime(as_string, '%m/%d/%y %I:%M:%S %p')
    return date_time


def add_trip(row):
    checkout_kiosk = Kiosk.query.filter_by(kiosk_name=row['checkout_kiosk']).first()
    return_kiosk = Kiosk.query.filter_by(kiosk_name=row['return_kiosk']).first()

    trip = Trip(bike_id=row['bike'],
                checkout_kiosk=checkout_kiosk,
                checkout_datetime=format_datetime(row['checkout_date'], row['checkout_time']),
                return_kiosk=return_kiosk,
                return_datetime=format_datetime(row['return_date'], row['return_time']),
                duration=row['duration_minutes'])
    db.session.add(trip)
    return trip


class RiderCollection:
    def __init__(self):
        self.riders = {}

    def get_rider(self, rider_id):
        if rider_id in self.riders:
            rider = self.riders[rider_id]
        else:
            rider = Rider(id=rider_id,
                          program=row['users_program'],
                          zip_code=row['zip'] or 0,
                          membership_type=row['membership_type'])
            self.riders[rider_id] = rider
            db.session.add(rider)
        return rider


with open('data/subset.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')

    rider_collection = RiderCollection()
    for row in reader:
        trip = add_trip(row)
        rider = rider_collection.get_rider(row['user_id'])

        rider.trips.append(trip)

    db.session.commit()
