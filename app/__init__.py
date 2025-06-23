from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app(testing=False):  # ← Added optional testing flag
    from .controllers import book_bp  

    load_dotenv()
    app = Flask(__name__)

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL")
        app.config['TESTING'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Avoid duplicate blueprint registration
    if "book" not in app.blueprints:
        app.register_blueprint(book_bp)

    with app.app_context():
        db.create_all()

    return app
