import os
from flask import Flask
from config import db, bcrypt
from models import User, Teacher, Substitute, SiteAdmin, Review, Request, Course
from flask_migrate import Migrate

app = Flask(__name__)
migrate = Migrate(app, db) 
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subspot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

if __name__ == '__main__':
    app.run(port=5555)
