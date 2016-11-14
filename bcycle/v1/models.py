from flask import url_for
from sqlalchemy.dialects import postgresql

from bcycle import db


class Rider(db.Model):
    __tablename__ = 'rider'

    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String)
    zip_code = db.Column(db.Integer)
    membership_type = db.Column(db.String)
    trips = db.relationship("Trip", backref="rider")

    def to_dict(self):
        return dict(id=self.id,
                    program=self.program,
                    zip_code=self.zip_code,
                    membership_type=self.membership_type,
                    trip_ids=[trip.id for trip in self.trips])


class Kiosk(db.Model):
    __tablename__ = 'kiosk'
    id = db.Column(db.Integer, primary_key=True)
    kiosk_name = db.Column(db.String)
    lat = db.Column(db.Numeric(precision=9, scale=6))
    lng = db.Column(db.Numeric(precision=9, scale=6))

    def to_dict(self):
        originating_trips = Trip.query.filter_by(checkout_kiosk=self).all()
        destination_trips = Trip.query.filter_by(return_kiosk=self).all()

        return dict(name=self.kiosk_name,
                    lat=float(self.lat),
                    lon=float(self.lng),
                    id=self.id,
                    total_originating_trips=len(originating_trips),
                    total_destination_trips=len(destination_trips))


class Trip(db.Model):
    __tablename__ = 'trip'

    id = db.Column(db.Integer, primary_key=True)
    bike_id = db.Column(db.Integer)
    checkout_datetime = db.Column(db.DateTime)
    checkout_kiosk_id = db.Column(db.Integer, db.ForeignKey('kiosk.id'))
    checkout_kiosk = db.relationship(Kiosk, foreign_keys=checkout_kiosk_id)
    return_datetime = db.Column(db.DateTime)
    return_kiosk_id = db.Column(db.Integer, db.ForeignKey('kiosk.id'))
    return_kiosk = db.relationship(Kiosk, foreign_keys=return_kiosk_id)
    duration = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('rider.id'))
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))

    def to_dict(self):
        return dict(id=self.id,
                    bike_id=self.bike_id,
                    duration=self.duration,
                    route=url_for('v1.get_route', route_id=self.route_id, _external=True),
                    checkout_kiosk=dict(
                        kiosk_id=self.checkout_kiosk.id,
                        href=url_for('v1.get_kiosk', kiosk_id=self.checkout_kiosk.id, _external=True)
                    ),
                    checkout_datetime=self._serialize_date(self.checkout_datetime),
                    return_kiosk=dict(
                        kiosk_id=self.return_kiosk.id,
                        href=url_for('v1.get_kiosk', kiosk_id=self.return_kiosk.id, _external=True)
                    ),
                    return_datetime=self._serialize_date(self.return_datetime))

    def _serialize_date(self, datetime):
        return datetime.isoformat()


class Route(db.Model):
    __tablename__ = 'route'

    id = db.Column(db.Integer, primary_key=True)
    kiosk_one_id = db.Column(db.Integer, db.ForeignKey('kiosk.id'))
    kiosk_one = db.relationship(Kiosk, foreign_keys=kiosk_one_id)
    kiosk_two_id = db.Column(db.Integer, db.ForeignKey('kiosk.id'))
    kiosk_two = db.relationship(Kiosk, foreign_keys=kiosk_two_id)

    # Ideally capture relationship in coordinates table or even better, use PostGIS
    # Due to desire to stay under Heroku's 10,000 row cap for Hobby tier
    coordinates = db.Column(postgresql.JSON)

    def to_dict(self):
        return dict(
            id=self.id,
            route=[{'lat': lat, 'lon': lon} for lon, lat in self.coordinates],
            kiosk_one=dict(
                kiosk_id=self.kiosk_one_id,
                href=url_for('v1.get_kiosk', kiosk_id=self.kiosk_one.id, _external=True),
            ),
            kiosk_two=dict(
                kiosk_id=self.kiosk_two_id,
                href=url_for('v1.get_kiosk', kiosk_id=self.kiosk_two.id, _external=True),
            ),
        )
