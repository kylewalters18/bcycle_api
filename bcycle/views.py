import json

from bcycle import app
from bcycle.models import Trip, Rider


def serialize_date(datetime):
    return datetime.isoformat()


def format_trip(trip):
    formatted_trip = dict(id=trip.id,
                          bike_id=trip.bike_id,
                          duration=trip.duration,
                          checkout_kiosk=trip.checkout_kiosk,
                          checkout_datetime=serialize_date(trip.checkout_datetime),
                          return_kiosk=trip.return_kiosk,
                          return_datetime=serialize_date(trip.return_datetime))
    return formatted_trip


def format_rider(rider):
    formatted_rider = dict(id=rider.id,
                           program=rider.program,
                           zip_code=rider.zip_code,
                           membership_type=rider.membership_type,
                           trips=[format_trip(trip) for trip in rider.trips])
    return formatted_rider


@app.route('/trip')
def get_trips():
    trips_result = [format_trip(trip) for trip in Trip.query.all()]
    return json.dumps(trips_result)


@app.route('/trip/<int:trip_id>')
def get_trip(trip_id):
    trip_result = Trip.query.get(trip_id)
    if trip_result:
        trip = format_trip(trip_result)
        return json.dumps(trip)
    else:
        return json.dumps({'error': 'no such trip'})


@app.route('/rider')
def get_riders():
    riders_result = [format_rider(rider) for rider in Rider.query.all()]
    return json.dumps(riders_result)


@app.route('/rider/<int:rider_id>')
def get_rider(rider_id):
    rider_result = Rider.query.get(rider_id)
    if rider_result:
        rider = format_rider(rider_result)
        return json.dumps(rider)
    else:
        return json.dumps({'error': 'no such rider'})


@app.errorhandler(404)
def not_found(error):
    return json.dumps({'error': 'not found'}), 404
