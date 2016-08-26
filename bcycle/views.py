import json

from bcycle import app
from bcycle.models import Trip, Rider


def serialize(datetime):
    return datetime.isoformat()


@app.route('/trip')
def trips():
    trips_result = [dict(bike_id=trip.bike_id,
                         duration=trip.duration,
                         checkout_kiosk=trip.checkout_kiosk,
                         checkout_datetime=serialize(trip.checkout_datetime),
                         return_kiosk=trip.return_kiosk,
                         return_datetime=serialize(trip.return_datetime))
                    for trip in Trip.query.all()]

    return json.dumps(trips_result)


