from flask import Flask, render_template, redirect, url_for, request, session, flash, send_file, current_app
from models import db, Hostel, User, Booking
from flask_bcrypt import Bcrypt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hostelfix.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if unauthorized

def create_admin_user():
    with app.app_context():
        
        admin = User.query.filter_by(email='admin@hostelfix.com').first()
        
        if not admin:
            # Admin credentials
            admin_email = 'admin@hostelfix.com'
            admin_password = generate_password_hash('adminpassword123') 
            is_admin = True
            admin_contact = "1234567890"
            # Create new admin user
            new_admin = User(name='admin', email=admin_email,contact=admin_contact, password_hash=admin_password, is_admin=is_admin)
            db.session.add(new_admin)
            db.session.commit()

            print("Admin user created!")
        else:
            print("Admin user already exists!")

# Load the logged-in user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Unauthorized access handler
@login_manager.unauthorized_handler
def unauthorized():
    flash("You need to log in to access this page.", "warning")
    return redirect(url_for('login'))

# Create tables
def create_all():
    db.create_all()

# Generate PDF receipt
def generate_pdf_receipt(hostel, room_number):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, f"Hostel Booking Receipt")
    c.drawString(100, height - 130, f"Hostel Name: {hostel.name}")
    c.drawString(100, height - 160, f"Room Number: {room_number}")
    c.drawString(100, height - 190, f"Booking Date: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(100, height - 220, f"Available Rooms Remaining: {hostel.available_rooms}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@app.route('/')
def home():
    return render_template("home.html")
@app.route("/hostels")
def hostels():
    # Assume you have a list of hostels from the database
    hostels = Hostel.query.all()

    # Prepare the hostels with their images from the static directory
    hostels_with_images = []
    for hostel in hostels:
        hostel_images_dir = os.path.join('static', 'images', hostel.name)
        if os.path.exists(hostel_images_dir):
            images = os.listdir(hostel_images_dir)  # List files in the directory
            images = [img for img in images if img.endswith(('png', 'jpg', 'jpeg', 'gif'))]  # Filter image files
        else:
            images = []  # No images found for the hostel

        hostels_with_images.append({
            'hostel': hostel,
            'images': images
        })

    return render_template('hostels.html', hostels=hostels ,hostels_with_images=hostels_with_images)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')  # Changed from 'name' to 'username'
        email = request.form.get('email')
        contact = request.form.get('contact')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user
        new_user = User(name=username, email=email, contact=contact, password_hash=hashed_password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Sign up successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')


# Hostel details route
@app.route('/hostel/<int:hostel_id>', methods=['GET'])
  # Ensures the user is logged in before accessing hostel details
def hostel_details(hostel_id):
    hostel = Hostel.query.get_or_404(hostel_id)
    hostel_images_dir = os.path.join('static', 'images', hostel.name)
    
    if os.path.exists(hostel_images_dir):
        images = os.listdir(hostel_images_dir)  # List files in the directory
        images = [img for img in images if img.endswith(('png', 'jpg', 'jpeg', 'gif'))]  # Filter image files
    else:
        images = []  # No images found for the hostel
    
    return render_template('hostel_detail.html', hostel=hostel, images=images)

# Book room route
@app.route('/book/<int:hostel_id>', methods=['POST'])
@login_required  # Ensure user is authenticated before booking
def book_room(hostel_id):
    # Fetch the hostel
    hostel = Hostel.query.get_or_404(hostel_id)

    # Check if the user has already booked a room in this hostel
    existing_booking = Booking.query.filter_by(user_id=current_user.id, hostel_id=hostel_id).first()
    if existing_booking:
        flash('You have already booked a room in this hostel.', 'warning')
        return redirect(url_for('hostel_details', hostel_id=hostel_id))

    # Fetch the room number from the hidden input
    room_number = request.form.get('room_number')

    # Validate room number
    if not room_number:
        flash('Room number is required!', 'danger')
        return redirect(url_for('hostel_details', hostel_id=hostel_id))

    # Check if there are available rooms in the hostel
    if hostel.available_rooms > 0:
        hostel.available_rooms -= 1  # Decrease available rooms count
        new_booking = Booking(user_id=current_user.id, hostel_id=hostel_id, room_number=room_number)
        db.session.add(new_booking)

        try:
            db.session.commit()
            flash('Room booked successfully!', 'success')

            # Generate PDF receipt (assuming generate_pdf_receipt is a utility function that returns a PDF buffer)
            pdf_buffer = generate_pdf_receipt(hostel, room_number)

            # Return the PDF as a response
            return send_file(pdf_buffer, as_attachment=True, download_name=f"receipt_{hostel_id}.pdf", mimetype='application/pdf')

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f'Error while booking the room: {str(e)}', 'danger')
            return redirect(url_for('hostel_details', hostel_id=hostel_id))

    else:
        flash('No rooms available!', 'error')

    return redirect(url_for('hostel_details', hostel_id=hostel_id))

@app.route('/search')
def search():
    query = request.args.get('query')
    search_results = Hostel.query.filter(Hostel.name.ilike(f'%{query}%')).all()

    # Prepare list of hostels with images
    hostels_with_images = []
    for hostel in search_results:
        hostel_images_dir = os.path.join('static', 'images', hostel.name)
        if os.path.exists(hostel_images_dir):
            images = os.listdir(hostel_images_dir)
            images = [img for img in images if img.endswith(('png', 'jpg', 'jpeg', 'gif'))]
        else:
            images = []  # No images found

        hostels_with_images.append({'hostel': hostel, 'images': images})

    return render_template('search_results.html', query=query, hostels_with_images=hostels_with_images)


# Admin dashboard route
@app.route('/admin', methods=['GET'])
@login_required  # Ensure the user is authenticated
def admin_dashboard():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('You need to log in to access the admin dashboard.', 'danger')
        return redirect(url_for('login'))
    users = User.query.all()
    hostels = Hostel.query.all()
    bookings = Booking.query.all()
    return render_template('dashboard.html',users=users, hostels=hostels,bookings=bookings)

@app.route('/logout')
def logout():
    # Clear the session
    session.pop('user_id', None)
    session.pop('is_admin', None)
    logout_user()
    # Redirect to the homepage or login page
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context(): 
        create_admin_user()
    app.run(debug=True)
