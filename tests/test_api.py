import unittest
import json

from collections import namedtuple
from datetime import datetime
from unittest import mock

from bcycle import app


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_404_not_found(self):
        rv = self.app.get('/this_route_doesnt_exists')
        self.assertIn(b'404 Not Found', rv.data)

    @mock.patch('bcycle.models.Trip.query')
    def test_trip_endpoint(self, mock_query):
        Trip = namedtuple('trip', ['bike_id',
                                   'duration',
                                   'checkout_kiosk',
                                   'checkout_datetime',
                                   'return_kiosk',
                                   'return_datetime'])

        trip = Trip(1, 30, "Main Street", datetime.now(), "1st Ave", datetime.now())
        mock_query.all.return_value = [trip]

        rv = self.app.get('/trip')
        response_data = json.loads(rv.data.decode('UTF-8'))
        self.assertEqual(len(response_data), 1)

        response_trip = response_data[0]
        self.assertEqual(response_trip['bike_id'], trip.bike_id)
        self.assertEqual(response_trip['duration'], trip.duration)
        self.assertEqual(response_trip['checkout_kiosk'], trip.checkout_kiosk)
        self.assertEqual(response_trip['checkout_datetime'], trip.checkout_datetime.isoformat())
        self.assertEqual(response_trip['return_kiosk'], trip.return_kiosk)
        self.assertEqual(response_trip['return_datetime'], trip.return_datetime.isoformat())

