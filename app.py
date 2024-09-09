from flask import Flask, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

@app.route("/")

def home():
    return render_template("index.html")

@app.route("/hostels")

def hostels():
    
    return render_template("hostels.html")

@app.route("/hostel_details")

def hostel_details():
    hostel = {
        'name':'Maisha Hostel',
        'distance':'0.5km',
        'price':5000,
        'gate':'C'
    }
    return render_template("hostel_detail.html",hostel=hostel)

@app.route("/login", methods = ["GET","POST"])

def login():
    
    return render_template("login.html")

@app.route("/register")

def register():
    return render_template("signup.html")

if __name__ == "__main__":
    
    app.run(debug=True)