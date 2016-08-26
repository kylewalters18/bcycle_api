from bcycle import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String)
    zip_code = db.Column(db.Integer)
    membership_type = db.Column(db.String)
    trips = db.relationship("Trip", backref="user")


class Trip(db.Model):
    __tablename__ = 'trip'

    id = db.Column(db.Integer, primary_key=True)
    bike_id = db.Column(db.Integer)
    checkout_datetime = db.Column(db.DateTime)
    checkout_kiosk = db.Column(db.String)
    return_datetime = db.Column(db.DateTime)
    return_kiosk = db.Column(db.String)
    duration = db.Column(db.Integer)