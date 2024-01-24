from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User (db. Model) :
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_dt = db.Column(db.DateTime, default=datetime.utcnow)
