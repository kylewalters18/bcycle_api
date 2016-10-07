import unittest
import json

from collections import namedtuple
from datetime import datetime
from unittest import mock

from bcycle import app


MockTrip = namedtuple('trip', ['id', 'bike_id', 'duration', 'checkout_kiosk', 'checkout_datetime',
                               'return_kiosk', 'return_datetime'])

MockRider = namedtuple('rider', ['id', 'program', 'zip_code', 'membership_type', 'trips'])

DictContainer = namedtuple('container', 'to_dict')
ItemContainer = namedtuple('item_container', 'items')


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_404_not_found(self):
        rv = self.app.get('/this_route_doesnt_exists')
        json_rv = json.loads(rv.data.decode('UTF-8'))
        self.assertEqual(json_rv['status'], 404)
        self.assertEqual(json_rv['error'], 'not found')
        self.assertEqual(json_rv['message'], 'invalid resource URI')


class TripTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def _verify_trip(self, actual, expected):
        self.assertEqual(actual['id'], expected.id)
        self.assertEqual(actual['bike_id'], expected.bike_id)
        self.assertEqual(actual['duration'], expected.duration)
        self.assertEqual(actual['checkout_kiosk'], expected.checkout_kiosk)
        self.assertEqual(actual['checkout_datetime'], expected.checkout_datetime)
        self.assertEqual(actual['return_kiosk'], expected.return_kiosk)
        self.assertEqual(actual['return_datetime'], expected.return_datetime)

    @mock.patch('bcycle.v1.endpoints.Trip')
    def test_get_trips_endpoint(self, mock_trip):
        test_time = datetime.now().isoformat()
        trip = MockTrip(0, 1, 30, 'Main Street', test_time, '1st Ave', test_time)
        mock_trip.query.paginate.return_value = ItemContainer(
            [DictContainer(lambda: trip._asdict())]
        )
        mock_trip.query.count.return_value = 1

        rv = self.app.get('/v1/trip')
        response_data = json.loads(rv.data.decode('UTF-8'))
        self.assertEqual(len(response_data['trips']), 1)

        response_trip = response_data['trips'][0]
        self._verify_trip(response_trip, trip)

    @mock.patch('bcycle.v1.endpoints.Trip')
    def test_no_such_trip_endpoint(self, mock_trip):
        mock_trip.query.get.return_value = None

        rv = self.app.get('/v1/trip/0')
        response_data = json.loads(rv.data.decode('UTF-8'))

        self.assertEqual(response_data['error'], 'resource does not exist')

    @mock.patch('bcycle.v1.endpoints.Trip')
    def test_trip_endpoint(self, mock_trip):
        test_time = datetime.now().isoformat()
        trip = MockTrip(0, 1, 30, 'Main Street', test_time, '1st Ave', test_time)

        mock_trip.query.get.return_value = DictContainer(lambda: trip._asdict())
        rv = self.app.get('/v1/trip/0')
        response_trip = json.loads(rv.data.decode('UTF-8'))

        self._verify_trip(response_trip, trip)


class RiderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def _verify_rider(self, actual, expected):
        self.assertEqual(actual['id'], expected.id)
        self.assertEqual(actual['program'], expected.program)
        self.assertEqual(actual['zip_code'], expected.zip_code)
        self.assertEqual(actual['membership_type'], expected.membership_type)
        self.assertEqual(actual['trips'], expected.trips)

    @mock.patch('bcycle.v1.endpoints.Rider')
    def test_get_riders(self, mock_rider):
        rider = MockRider(0, 'Denver B Cycle', 80202, 'annual', [])
        mock_rider.query.paginate.return_value = ItemContainer(
            [DictContainer(lambda: rider._asdict())]
        )
        mock_rider.query.count.return_value = 1

        rv = self.app.get('/v1/rider')
        response_data = json.loads(rv.data.decode('UTF-8'))
        self.assertEqual(len(response_data['riders']), 1)

        response_rider = response_data['riders'][0]
        self._verify_rider(response_rider, rider)

    @mock.patch('bcycle.v1.endpoints.Rider')
    def test_no_such_trip_endpoint(self, mock_rider):
        mock_rider.query.get.return_value = None

        rv = self.app.get('/v1/rider/0')
        response_data = json.loads(rv.data.decode('UTF-8'))

        self.assertEqual(response_data['error'], 'resource does not exist')

    @mock.patch('bcycle.v1.endpoints.Rider')
    def test_trip_endpoint(self, mock_rider):
        rider = MockRider(0, 'Denver B Cycle', 80202, 'annual', [])
        mock_rider.query.get.return_value = DictContainer(lambda: rider._asdict())

        rv = self.app.get('/v1/rider/0')
        response_data = json.loads(rv.data.decode('UTF-8'))

        self._verify_rider(response_data, rider)
