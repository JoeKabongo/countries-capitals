import os
import sys
import requests
from passlib.hash import pbkdf2_sha256
from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/play/<continent>")
def play(continent):
    """
        Quiz the user on the  continent they selected
    """

    #selet 10 countries from the database whose continent equal the continent selected
    countries = Country.query.filter_by(continent=continent).limit(10).all()

    #select all the capitals of that same continent, will be used to generate random choice
    capitals = Country.query.filter_by(continent=continent).with_entities("capital")

    #convert data into list and send the data  to javascript
    listCountries = []
    listCapitals = []
    for n in countries:
        listCountries.append((n.name, n.capital))
    for n in capitals:
        listCapitals.append(n[0])
    return jsonify({"countries":listCountries, "capitals":listCapitals})


@app.route("/contact")
def contact():
    return render_template("contact.html")
