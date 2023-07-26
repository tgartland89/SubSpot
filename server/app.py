import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import app, db, api
from models import *
from resources import *
from routes import *

CORS(app, supports_credentials=True)
app.template_folder = "templates"
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')

api.add_resource(SignUp, '/signup')
api.add_resource(UserResource, '/users')
api.add_resource(TeacherResource, '/teachers')
api.add_resource(SubstituteResource, '/substitutes')
api.add_resource(SiteAdminResource, '/site_admins')
api.add_resource(CourseResource, '/courses')
api.add_resource(ReviewResource, '/reviews')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555)