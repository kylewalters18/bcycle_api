from flask import jsonify

from bcycle import app
from bcycle.models import Kiosk, Trip, Rider


@app.route('/trip')
def get_trips():
    trips_result = [trip.to_dict() for trip in Trip.query.all()]
    return jsonify(trips_result)


@app.route('/trip/<int:trip_id>')
def get_trip(trip_id):
    trip_result = Trip.query.get(trip_id)
    if trip_result:
        trip = trip_result.to_dict()
        return jsonify(trip)
    else:
        return jsonify({'error': 'no such trip'})


@app.route('/rider')
def get_riders():
    riders_result = [rider.to_dict() for rider in Rider.query.all()]
    return jsonify(riders_result)


@app.route('/rider/<int:rider_id>')
def get_rider(rider_id):
    rider_result = Rider.query.get(rider_id)
    if rider_result:
        rider = rider_result.to_dict()
        return jsonify(rider)
    else:
        return jsonify({'error': 'no such rider'})


@app.route('/kiosk')
def get_kiosks():
    kiosks = [kiosk.to_dict() for kiosk in Kiosk.query.all()]
    return jsonify(kiosks)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'not found'}), 404
