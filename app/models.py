from . import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)    # Increased from 100 to 255
    author = db.Column(db.String(255), nullable=False)   # Increased from 100 to 255
    price = db.Column(db.Float, nullable=False)
