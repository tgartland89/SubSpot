import os
from flask import Flask
from config import db, bcrypt
from models import User, Teacher, Substitute, SiteAdmin, Review, Request, Course
from resources import SignUp, LogIn, LogOut, UserResource, TeacherResource, SubstituteResource, SiteAdminResource, CourseResource, ReviewResource, RequestResource

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)


app.add_url_rule('/signup', view_func=SignUp.as_view('signup'))
app.add_url_rule('/login', view_func=LogIn.as_view('login'))
app.add_url_rule('/logout', view_func=LogOut.as_view('logout'))
app.add_url_rule('/users', view_func=UserResource.as_view('users'))
app.add_url_rule('/teachers', view_func=TeacherResource.as_view('teachers'))
app.add_url_rule('/substitutes', view_func=SubstituteResource.as_view('substitutes'))
app.add_url_rule('/site_admins', view_func=SiteAdminResource.as_view('site_admins'))
app.add_url_rule('/courses', view_func=CourseResource.as_view('courses'))
app.add_url_rule('/reviews', view_func=ReviewResource.as_view('reviews'))
app.add_url_rule('/requests', view_func=RequestResource.as_view('requests'))
app.add_url_rule('/requests/<int:request_id>', view_func=RequestResource.as_view('request'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555)