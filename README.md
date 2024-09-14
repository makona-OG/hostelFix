HostelFix
Introduction
HostelFix is a web application designed to streamline the process of finding and booking hostels for students. Built using Flask as the backend, the application allows users to view available hostels, check room amenities, and make bookings in real-time. The platform also features user authentication, dynamic room availability updates, and admin dashboards for managing hostel bookings. This project was created with a focus on improving the hostel booking experience for students at Dedan Kimathi University of Technology.

Live Demo: [Link to Deployed Site] (https://hostelfixgu.onrender.com/)
Final Project Blog: [Link to Blog Article]
Author's LinkedIn: Pharel Makona LinkedIn

Installation
Clone the repository:

bash
Copy code
git clone https://github.com/makona-OG/HostelFix.git
cd HostelFix
Create a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the database:

Initialize the SQLite database:
bash
Copy code
flask db init
flask db migrate
flask db upgrade
Run the application:

bash
Copy code
flask run
Usage
User Authentication:

Sign up as a user to gain access to the hostel listing.
Log in using your credentials.
Booking a Hostel:

Browse available hostels, check details like distance and amenities.
Book a room directly from the hostel details page.
View booking confirmation and download a PDF receipt.
Admin Dashboard:

Access the admin panel to manage hostel bookings.
View booked rooms, user details, and update room availability.
Contributing
Contributions are welcome! Here's how you can help improve HostelFix:

Fork this repository
Create a feature branch: git checkout -b feature/new-feature
Commit your changes: git commit -m 'Add some new feature'
Push to the branch: git push origin feature/new-feature
Open a Pull Request
For major changes, please open an issue first to discuss what you would like to improve.

Related Projects
If you're interested in related projects, check out these:

Airbnb Clone with Flask
Room Booking System with Django
Student Accommodation Platform
Licensing
This project is licensed under the MIT License - see the LICENSE file for details.
