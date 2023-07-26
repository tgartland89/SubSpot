from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users' 

    serialize_rules = ('-reviews', '-courses', '-password_hash')

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('Teacher', 'Substitute', 'Site Admin'), nullable=False)
    profile_picture = db.Column(db.String(255))  

    def __init__(self, email, password, role, profile_picture=None):  
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
        self.profile_picture = profile_picture  

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
 
    teacher = db.relationship('Teacher', back_populates="user", lazy='joined')
    substitute = db.relationship('Substitute', back_populates="user", lazy='joined')
    site_admin = db.relationship('SiteAdmin', back_populates="user", lazy='joined')

    
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
    
    user = db.relationship('User', back_populates='teacher', uselist=False, lazy='joined')

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

    user = db.relationship('User', back_populates='substitute', uselist=False, lazy='joined')


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

    user = db.relationship('User', back_populates='site_admin', uselist=False, lazy='joined')


User.teacher = relationship("Teacher", back_populates="user", uselist=False, lazy='joined')
User.substitute = relationship("Substitute", back_populates="user", uselist=False, lazy='joined')
User.site_admin = relationship("SiteAdmin", back_populates="user", uselist=False, lazy='joined')

class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'  

    serialize_rules = ('-teacher.reviews', '-substitute.reviews')

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    substitute_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_subject = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    teacher_reviewed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    substitute_reviewed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    writer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  
    teacher = db.relationship('User', foreign_keys=[teacher_id], backref='teacher_courses', lazy='joined')
    substitute = db.relationship('User', foreign_keys=[substitute_id], backref='substitute_courses', lazy='joined')

    def to_dict(self):
        return {
            'id': self.id,
            'writer_id': self.writer_id,  
            'teacher_id': self.teacher_id,
            'substitute_id': self.substitute_id,
            'class_subject': self.class_subject,
            'date': self.date.isoformat(),
            'time': self.time,
            'status': self.status,
        }
    
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    serialize_rules = ('-writer.reviews', '-writer.courses', '-writer.password_hash')

    id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
 
    teacher_reviewed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    substitute_reviewed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

   
    writer = db.relationship('User', foreign_keys=[writer_id], backref='reviews', lazy='joined')
    teacher_reviewed = db.relationship('User', foreign_keys=[teacher_reviewed_id], backref='teacher_reviews', lazy='joined')
    substitute_reviewed = db.relationship('User', foreign_keys=[substitute_reviewed_id], backref='substitute_reviews', lazy='joined')


    def to_dict(self):
        return {
            'id': self.id,
            'writer_id': self.writer_id,
            'course_id': self.course_id,
            'teacher_reviewed_id': self.teacher_reviewed_id,
            'substitute_reviewed_id': self.substitute_reviewed_id,
            'rating': self.rating,
            'comment': self.comment,
        }