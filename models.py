from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    capital = db.Column(db.String, nullable=False)
    continent = db.Column(db.String, nullable=False)
