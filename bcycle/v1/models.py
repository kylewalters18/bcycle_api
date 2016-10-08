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

    def to_dict(self):
        return dict(id=self.id,
                    bike_id=self.bike_id,
                    duration=self.duration,
                    checkout_kiosk_id=self.checkout_kiosk.id,
                    checkout_datetime=self._serialize_date(self.checkout_datetime),
                    return_kiosk_id=self.return_kiosk.id,
                    return_datetime=self._serialize_date(self.return_datetime))

    def _serialize_date(self, datetime):
        return datetime.isoformat()


class Route(db.Model):
    __tablename__ = 'route'

    id = db.Column(db.Integer, primary_key=True)
    checkout_kiosk_id = db.Column(db.Integer, db.ForeignKey('kiosk.id'))
    checkout_kiosk = db.relationship(Kiosk, foreign_keys=checkout_kiosk_id)
    return_kiosk_id = db.Column(db.Integer, db.ForeignKey('kiosk.id'))
    return_kiosk = db.relationship(Kiosk, foreign_keys=return_kiosk_id)
