from flask import jsonify

from bcycle import app
from bcycle.models import Kiosk, Trip, Rider
from bcycle.decorators import no_resource_error_handler


@app.route('/trip')
def get_trips():
    trips_result = [trip.to_dict() for trip in Trip.query.all()]
    return jsonify(trips_result)


@app.route('/trip/<int:trip_id>')
@no_resource_error_handler
def get_trip(trip_id):
    trip = Trip.query.get(trip_id)
    return jsonify(trip.to_dict())


@app.route('/rider')
def get_riders():
    riders_result = [rider.to_dict() for rider in Rider.query.all()]
    return jsonify(riders_result)


@app.route('/rider/<int:rider_id>')
@no_resource_error_handler
def get_rider(rider_id):
    rider = Rider.query.get(rider_id)
    return jsonify(rider.to_dict())


@app.route('/kiosk')
def get_kiosks():
    kiosks = [kiosk.to_dict() for kiosk in Kiosk.query.all()]
    return jsonify(kiosks)


@app.route('/kiosk/<int:kiosk_id>')
@no_resource_error_handler
def get_kiosk(kiosk_id):
    kiosk = Kiosk.query.get(kiosk_id)
    return jsonify(kiosk.to_dict())


@app.errorhandler(404)
def not_found():
    return jsonify({'error': 'endpoint does not exist'}), 404
