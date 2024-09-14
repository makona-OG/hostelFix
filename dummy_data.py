from models import db, Hostel, User
from app import app

with app.app_context():
    # Dummy users
    user_data = [
        {"name": "John Doe", "email": "joe@example.com", "contact": "0720397423", "password": "password123"},
        {"name": "Jane Doe", "email": "job@example.com", "contact": "0712961615", "password": "password123"},
    ]

    for user in user_data:
        new_user = User(name=user['name'], email=user['email'], contact=user['contact'])
        new_user.set_password(user['password'])  # Assuming set_password is a method in your User model
        db.session.add(new_user)

    # Dummy hostels
    hostel_data = [
        {
            "name": "Hostel A", "price_per_room": 1200, "available_rooms": 15,
            "distance_to_hostel": 500, "gate": "B", 
            "pictures": ["https://images.unsplash.com/photo-1", "https://images.unsplash.com/photo-2"],
            "amenities": {"WiFi": "https://images.unsplash.com/amenity-wifi", "Gym": "https://images.unsplash.com/amenity-gym"}
        },
        {
            "name": "Hostel B", "price_per_room": 1500, "available_rooms": 10,
            "distance_to_hostel": 300, "gate": "A",
            "pictures": ["https://images.unsplash.com/photo-3", "https://images.unsplash.com/photo-4"],
            "amenities": {"WiFi": "https://images.unsplash.com/amenity-wifi", "Pool": "https://images.unsplash.com/amenity-pool"}
        },
        {
            "name": "Hostel C", "price_per_room": 1000, "available_rooms": 20,
            "distance_to_hostel": 200, "gate": "C",
            "pictures": ["https://images.unsplash.com/photo-5", "https://images.unsplash.com/photo-6"],
            "amenities": {"Cafeteria": "https://images.unsplash.com/amenity-cafeteria", "Parking": "https://images.unsplash.com/amenity-parking"}
        },
        {
            "name": "Hostel D", "price_per_room": 1800, "available_rooms": 8,
            "distance_to_hostel": 450, "gate": "D",
            "pictures": ["https://images.unsplash.com/photo-7", "https://images.unsplash.com/photo-8"],
            "amenities": {"WiFi": "https://images.unsplash.com/amenity-wifi", "Study Room": "https://images.unsplash.com/amenity-study"}
        },
        {
            "name": "Hostel E", "price_per_room": 1300, "available_rooms": 12,
            "distance_to_hostel": 600, "gate": "B",
            "pictures": ["https://images.unsplash.com/photo-9", "https://images.unsplash.com/photo-10"],
            "amenities": {"Gym": "https://images.unsplash.com/amenity-gym", "Pool": "https://images.unsplash.com/amenity-pool"}
        },
        {
            "name": "Hostel F", "price_per_room": 1700, "available_rooms": 5,
            "distance_to_hostel": 350, "gate": "E",
            "pictures": ["https://images.unsplash.com/photo-11", "https://images.unsplash.com/photo-12"],
            "amenities": {"WiFi": "https://images.unsplash.com/amenity-wifi", "Lounge": "https://images.unsplash.com/amenity-lounge"}
        },
        {
            "name": "Hostel G", "price_per_room": 1600, "available_rooms": 6,
            "distance_to_hostel": 400, "gate": "C",
            "pictures": ["https://images.unsplash.com/photo-13", "https://images.unsplash.com/photo-14"],
            "amenities": {"Study Room": "https://images.unsplash.com/amenity-study", "WiFi": "https://images.unsplash.com/amenity-wifi"}
        },
        {
            "name": "Hostel H", "price_per_room": 1400, "available_rooms": 10,
            "distance_to_hostel": 550, "gate": "A",
            "pictures": ["https://images.unsplash.com/photo-15", "https://images.unsplash.com/photo-16"],
            "amenities": {"WiFi": "https://images.unsplash.com/amenity-wifi", "Laundry": "https://images.unsplash.com/amenity-laundry"}
        },
        {
            "name": "Hostel I", "price_per_room": 2000, "available_rooms": 4,
            "distance_to_hostel": 650, "gate": "D",
            "pictures": ["https://images.unsplash.com/photo-17", "https://images.unsplash.com/photo-18"],
            "amenities": {"Gym": "https://images.unsplash.com/amenity-gym", "Pool": "https://images.unsplash.com/amenity-pool"}
        },
        {
            "name": "Hostel J", "price_per_room": 1100, "available_rooms": 14,
            "distance_to_hostel": 700, "gate": "E",
            "pictures": ["https://images.unsplash.com/photo-19", "https://images.unsplash.com/photo-20"],
            "amenities": {"Parking": "https://images.unsplash.com/amenity-parking", "Lounge": "https://images.unsplash.com/amenity-lounge"}
        },
    ]

    for hostel in hostel_data:
        new_hostel = Hostel(
            name=hostel['name'], price_per_room=hostel['price_per_room'],
            available_rooms=hostel['available_rooms'], distance_to_hostel=hostel['distance_to_hostel'],
            gate=hostel['gate'], pictures=hostel['pictures'], amenities=hostel['amenities']
        )
        db.session.add(new_hostel)

    db.session.commit()
