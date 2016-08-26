import json

from bcycle import app
from bcycle.models import Trip, Rider


def serialize(datetime):
    return datetime.isoformat()


@app.route('/trip')
def get_trips():
    trips_result = [dict(bike_id=trip.bike_id,
                         duration=trip.duration,
                         checkout_kiosk=trip.checkout_kiosk,
                         checkout_datetime=serialize(trip.checkout_datetime),
                         return_kiosk=trip.return_kiosk,
                         return_datetime=serialize(trip.return_datetime))
                    for trip in Trip.query.all()]

    return json.dumps(trips_result)


@app.route('/trip/<int:trip_id>')
def get_trip(trip_id):
    pass


@app.route('/rider')
def get_riders():
    pass


@app.route('/rider/<int:rider_id>')
def get_rider(rider_id):
    pass

@app.errorhandler(404)
def not_found(error):
    return json.dumps({'error': 'not found'}), 404
