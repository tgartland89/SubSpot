from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.LargeBinary)
    role = db.Column(db.Enum('Teacher', 'Substitute', 'Site Admin'), nullable=False)

    def __init__(self, email, password, role):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Teacher(db.Model, SerializerMixin):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    contact_details = db.Column(db.Text)

class Substitute(db.Model, SerializerMixin):
    __tablename__ = 'substitutes'  
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    qualifications = db.Column(db.Text)

class SiteAdmin(db.Model, SerializerMixin):
    __tablename__ = 'site_admins'  
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'  
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    substitute_id = db.Column(db.Integer, db.ForeignKey('substitutes.id'), nullable=False)
    class_subject = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'  
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    substitute_id = db.Column(db.Integer, db.ForeignKey('substitutes.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
