from flask import jsonify

from bcycle.v1 import v1_blueprint
from bcycle.v1.models import Kiosk, Trip, Rider
from bcycle.v1.decorators import no_resource_error_handler


@v1_blueprint.route('/trip')
def get_trips():
    trips_result = [trip.to_dict() for trip in Trip.query.all()]
    return jsonify(trips_result)


@v1_blueprint.route('/trip/<int:trip_id>')
@no_resource_error_handler
def get_trip(trip_id):
    trip = Trip.query.get(trip_id)
    return jsonify(trip.to_dict())


@v1_blueprint.route('/rider')
def get_riders():
    riders_result = [rider.to_dict() for rider in Rider.query.all()]
    return jsonify(riders_result)


@v1_blueprint.route('/rider/<int:rider_id>')
@no_resource_error_handler
def get_rider(rider_id):
    rider = Rider.query.get(rider_id)
    return jsonify(rider.to_dict())


@v1_blueprint.route('/kiosk')
def get_kiosks():
    kiosks = [kiosk.to_dict() for kiosk in Kiosk.query.all()]
    return jsonify(kiosks)


@v1_blueprint.route('/kiosk/<int:kiosk_id>')
@no_resource_error_handler
def get_kiosk(kiosk_id):
    kiosk = Kiosk.query.get(kiosk_id)
    return jsonify(kiosk.to_dict())
