import os
import csv
from flask import  Flask, render_template, request
from models import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    #insert countries into my database
    with open("countries.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            country = Country(name=row[0], capital=row[1], continent=row[2] )
            db.session.add(country)
            print(f"{row} was added in the databases")
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
