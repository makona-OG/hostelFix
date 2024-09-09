from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hostel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    price_per_room = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db.String(255), nullable=False)
    reviews = db.relationship('Review', backref='hostel', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    hostel_id = db.Column(db.Integer, db.ForeignKey('hostel.id'), nullable=False)
