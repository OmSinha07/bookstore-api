from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app(testing=False):
    from .controllers import book_ns

    load_dotenv()

    app = Flask(__name__)  # Do NOT use template_folder here

  


     # UI route
    @app.route('/')
    def home():
        return render_template("index.html")

    # DB setup
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///books.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)



    # API setup
    api = Api(app, version='1.0', title='Book Store API',
              description='A simple Book Store API', doc='/docs')
    api.add_namespace(book_ns, path='/books')

   

    with app.app_context():
        db.create_all()

    return app
