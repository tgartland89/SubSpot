from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(200))

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.role}')"

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    school_name = db.Column(db.String(100), nullable=False)
    school_location = db.Column(db.String(100), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    user = db.relationship('User', backref=db.backref('teacher', uselist=False))

    def __repr__(self):
        return f"Teacher('{self.name}', '{self.school_name}', '{self.course_name}')"

class Substitute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    qualifications = db.Column(db.String(200))
    verification_id = db.Column(db.String(50))
    user = db.relationship('User', backref=db.backref('substitute', uselist=False))

    def __repr__(self):
        return f"Substitute('{self.name}', '{self.qualifications}')"

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    substitute_user_id = db.Column(db.Integer, db.ForeignKey('substitute.id'), nullable=False)
    teacher_user_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    course_being_covered = db.Column(db.String(100), nullable=False)
    confirmation = db.Column(db.Boolean)
    message_sub_sent_to = db.Column(db.String(120))
    teacher_if_declined = db.Column(db.Boolean)
    school_name = db.Column(db.String(100), nullable=False)
    teacher_school_location = db.Column(db.String(100), nullable=False)
    substitute = db.relationship('Substitute', backref='requests')
    teacher = db.relationship('Teacher', backref='requests')

    def __repr__(self):
        return f"Request('{self.course_being_covered}', '{self.school_name}', '{self.confirmation}')"
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    substitute_id = db.Column(db.Integer, db.ForeignKey('substitute.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Review('{self.rating}', '{self.comment}')"