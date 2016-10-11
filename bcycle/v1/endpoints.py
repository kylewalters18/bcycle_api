from flask import jsonify

from bcycle.v1 import v1_blueprint
from bcycle.v1.models import Kiosk, Trip, Rider, Route
from bcycle.v1.decorators import no_resource_error_handler, paginate


@v1_blueprint.route('/trip')
@paginate('trips')
def get_trips():
    return Trip.query


@v1_blueprint.route('/trip/<int:trip_id>')
@no_resource_error_handler
def get_trip(trip_id):
    trip = Trip.query.get(trip_id)
    return jsonify(trip.to_dict())


@v1_blueprint.route('/rider')
@paginate('riders')
def get_riders():
    return Rider.query


@v1_blueprint.route('/rider/<int:rider_id>')
@no_resource_error_handler
def get_rider(rider_id):
    rider = Rider.query.get(rider_id)
    return jsonify(rider.to_dict())


@v1_blueprint.route('/kiosk')
@paginate('kiosks')
def get_kiosks():
    return Kiosk.query


@v1_blueprint.route('/kiosk/<int:kiosk_id>')
@no_resource_error_handler
def get_kiosk(kiosk_id):
    kiosk = Kiosk.query.get(kiosk_id)
    return jsonify(kiosk.to_dict())


@v1_blueprint.route('/route')
@paginate('routes')
def get_routes():
    return Route.query


@v1_blueprint.route('/route/<int:route_id>')
@no_resource_error_handler
def get_route(route_id):
    route = Route.query.get(route_id)
    return jsonify(route.to_dict())
