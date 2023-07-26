from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users' 

    serialize_rules = ('-reviews', '-password_hash')

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255))  
    role = db.Column(db.Enum('Teacher', 'Substitute', 'Site Admin'), nullable=False)

    def __init__(self, email, password, role, profile_picture=None):  
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
        self.profile_picture = profile_picture  

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Teacher(db.Model, SerializerMixin):
    __tablename__ = 'teachers'

    serialize_rules = ('-user.reviews', '-user.profile_picture', '-user.password_hash')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    school = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    grade_or_course = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(255), default='default_image_url.png')
 
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'school': self.school,
            'location': self.location,
            'grade_or_course': self.grade_or_course,
            'image_url': self.image_url,
        }

class Substitute(db.Model, SerializerMixin):
    __tablename__ = 'substitutes'  

    serialize_rules = ('-user.reviews', '-user.profile_picture', '-user.password_hash')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    verification_id = db.Column(db.String(6), nullable=True)
    location = db.Column(db.String(120), nullable=False)
    grade_or_course = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    qualifications = db.Column(db.Text)
    image_url = db.Column(db.String(255), default='default_image_url.png')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'verification_id': self.verification_id,
            'location': self.location,
            'grade_or_course': self.grade_or_course,
            'phone': self.phone,
            'email': self.email,
            'qualifications': self.qualifications,
            'image_url': self.image_url,
        }

class SiteAdmin(db.Model, SerializerMixin):
    __tablename__ = 'site_admins'  

    serialize_rules = ('-user.reviews', '-user.profile_picture', '-user.password_hash')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(255), default='default_image_url.png')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_url': self.image_url,
        }

class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'  

    serialize_rules = ('-teacher.reviews', '-substitute.reviews')

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    substitute_id = db.Column(db.Integer, db.ForeignKey('substitutes.id'), nullable=False)
    class_subject = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'substitute_id': self.substitute_id,
            'class_subject': self.class_subject,
            'date': self.date.isoformat(), 
            'time': self.time,
            'status': self.status,
        }

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'  

    serialize_rules = ('-writer.reviews', '-writer.profile_picture', '-writer.password_hash', '-rental.reviews')

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    substitute_id = db.Column(db.Integer, db.ForeignKey('substitutes.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'substitute_id': self.substitute_id,
            'rating': self.rating,
            'comment': self.comment,
        }