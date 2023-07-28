from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users' 

    serialize_rules = ('-reviews', '-courses', '-password_hash')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    role = db.Column(Enum('Teacher', 'Substitute', 'SiteAdmin'), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255))  

    def __init__(self, name, email, location, phone, role, password, profile_picture=None):  
        self.name = name
        self.email = email
        self.location = location
        self.phone = phone
        self.role = role
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.profile_picture = profile_picture  

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    teacher = db.relationship('Teacher', back_populates='user', uselist=False, lazy='joined')
    substitute = db.relationship('Substitute', back_populates='user', uselist=False, lazy='joined')
    site_admin = db.relationship('SiteAdmin', back_populates='user', uselist=False, lazy='joined')


class Teacher(db.Model, SerializerMixin):
    __tablename__ = 'teachers'

    serialize_rules = ('-user.reviews', '-user.profile_picture', '-user.password_hash')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    school_name = db.Column(db.String(120), nullable=False)

    user = db.relationship('User', back_populates='teacher', uselist=False, lazy='joined')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.user.name,
            'email': self.user.email,
            'location': self.user.location,
            'phone': self.user.phone,
            'school_name': self.school_name,
            'profile_picture': self.user.profile_picture,
        }
    



class Substitute(db.Model, SerializerMixin):
    __tablename__ = 'substitutes'  

    serialize_rules = ('-user.reviews', '-user.profile_picture', '-user.password_hash')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    qualification = db.Column(db.String(120))
    verification_id = db.Column(db.String(120))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.user.name,
            'email': self.user.email,
            'location': self.user.location,
            'phone': self.user.phone,
            'qualification': self.qualification,
            'verification_id': self.verification_id,
            'profile_picture': self.user.profile_picture,
        }

    user = db.relationship('User', back_populates='substitute', uselist=False, lazy='joined')


class SiteAdmin(db.Model, SerializerMixin):
    __tablename__ = 'site_admins'  

    serialize_rules = ('-user.reviews', '-user.profile_picture', '-user.password_hash')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.user.name,
            'email': self.user.email,
            'location': self.user.location,
            'phone': self.user.phone,
            'profile_picture': self.user.profile_picture,
        }

    user = db.relationship('User', back_populates='site_admin', uselist=False, lazy='joined')


class Request(db.Model, SerializerMixin):
    __tablename__ = 'requests'

    Request_ID = db.Column(db.Integer, primary_key=True)
    Substitute_user_id = db.Column(db.Integer, db.ForeignKey('substitutes.id'))
    Teacher_name = db.Column(db.String(120))
    Teacher_school = db.Column(db.String(120))
    Teacher_school_location = db.Column(db.String(120))
    Course_Being_covered = db.Column(db.String(120))
    Confirmation = db.Column(Enum('Accept', 'Decline'))
    Message_sub_sent_to = db.Column(db.String(120))
    Teacher_if_declined = db.Column(db.String(120))

    substitute = db.relationship('Substitute', backref='requests', uselist=False)



class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'

    Course_ID = db.Column(db.Integer, primary_key=True)
    Course_name = db.Column(db.String(120))
    Correlating_teacher_ID = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    Correlating_substitute_ID = db.Column(db.Integer, db.ForeignKey('substitutes.id'))
    Course_status = db.Column(Enum('Available', 'Unavailable'))
    Course_school_name = db.Column(db.String(120))
    Course_location = db.Column(db.String(120))

    teacher = db.relationship('Teacher', backref='courses')
    substitute = db.relationship('Substitute', backref='courses')


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    Review_ID = db.Column(db.Integer, primary_key=True)
    Teacher_Id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    Rating = db.Column(db.Integer)
    Review = db.Column(db.String(255))
    Correlating_Substitute_ID = db.Column(db.Integer, db.ForeignKey('substitutes.id'))

    teacher = db.relationship('Teacher', backref='reviews')
    substitute = db.relationship('Substitute', backref='reviews')

