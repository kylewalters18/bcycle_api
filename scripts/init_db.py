import csv

from bcycle import db
from bcycle.models import Rider, Trip

Trip.query.delete()
Rider.query.delete()

with open('data/subset_2015denverbcycletripdata_public.csv', 'rb') as csvfile:
    riders = {}
    reader = csv.DictReader(csvfile, delimiter=',')

    for row in reader:
        trip = Trip(bike_id=row['bike'],
                    checkout_kiosk=row['checkout_kiosk'],
                    return_kiosk=row['return_kiosk'],
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
