from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Hostel(db.Model):
    __tablename__ = 'hostels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price_per_room = db.Column(db.Float, nullable=False)
    available_rooms = db.Column(db.Integer, nullable=False)
    distance_to_hostel = db.Column(db.Float, nullable=False)
    gate = db.Column(db.String(1), nullable=False)  # A, B, or C
    pictures = db.Column(db.PickleType, nullable=False)  # List of image URLs
    amenities = db.Column(db.PickleType, nullable=False)  # Dictionary of amenities with picture URLs

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
    @property
    def is_active(self):
        return True  

    @property
    def is_authenticated(self):
        return True  

    @property
    def is_anonymous(self):
        return False  

    def get_id(self):
        return str(self.id)  


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hostel_id = db.Column(db.Integer, db.ForeignKey('hostels.id'), nullable=False)
    room_number = db.Column(db.String(20), nullable=False)
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    hostel = db.relationship('Hostel', backref=db.backref('bookings', lazy=True))

    __table_args__ = (db.UniqueConstraint('user_id', 'hostel_id', name='unique_user_hostel_booking'),)
    