import csv

from datetime import datetime

from bcycle import db
from bcycle.models import Rider, Trip


Trip.query.delete()
Rider.query.delete()


def format_datetime(date, time):
    as_string = '{} {}'.format(date, time)
    date_time = datetime.strptime(as_string, '%m/%d/%y %I:%M:%S %p')
    return date_time


with open('data/subset_2015denverbcycletripdata_public.csv', 'r') as csvfile:
    riders = {}
    reader = csv.DictReader(csvfile, delimiter=',')

    for row in reader:
        trip = Trip(bike_id=row['bike'],
                    checkout_kiosk=row['checkout_kiosk'],
                    checkout_datetime=format_datetime(row['checkout_date'], row['checkout_time']),
                    return_kiosk=row['return_kiosk'],
                    return_datetime=format_datetime(row['return_date'], row['return_time']),
                    duration=row['duration_minutes'])
        db.session.add(trip)

        rider_id = row['user_id']
        if rider_id in riders:
            rider = riders[rider_id]
        else:
            rider = Rider(id=rider_id,
                          program=row['users_program'],
                          zip_code=row['zip'],
                          membership_type=row['membership_type'])
            riders[rider_id] = rider
            db.session.add(rider)

        rider.trips.append(trip)

    db.session.commit()
