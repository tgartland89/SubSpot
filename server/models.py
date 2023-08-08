from sqlalchemy import Column, Integer, String, Enum, ForeignKey
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
    school_name = db.Column(db.String(120))  # Add teacher_school attribute here
    school_location = db.Column(db.String(120))  # Add school_location attribute here

    def __init__(self, name, email, location, phone, role, password, profile_picture=None, school_name=None, school_location=None):
        self.name = name
        self.email = email
        self.location = location
        self.phone = phone
        self.role = role
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.profile_picture = profile_picture
        self.school_name = school_name  # Set the teacher_school attribute
        self.school_location = school_location  # Set the school_location attribute

    # ... (rest of the class code remains the same)


    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    teacher = db.relationship('Teacher', back_populates='user', uselist=False, lazy='joined')
    substitute = db.relationship('Substitute', back_populates='user', uselist=False, lazy='joined')
    site_admin = db.relationship('SiteAdmin', back_populates='user', uselist=False, lazy='joined')


class Teacher(db.Model, SerializerMixin):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    location = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    course_name = db.Column(db.String(120))
    school_name = db.Column(db.String(120))  # Add teacher_school attribute here
    school_location = db.Column(db.String(120))  # Add school_location attribute here

    user = db.relationship('User', back_populates='teacher', uselist=False, lazy='joined')
    requests = db.relationship('Request', back_populates='teacher')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'location': self.location,
            'phone': self.phone,
            'course_name': self.course_name,
            'school_name': self.school_name,  # Include the teacher_school attribute in the dictionary
            'school_location': self.school_location,  # Include the school_location attribute in the dictionary
            'profile_picture': self.user.profile_picture,
        }



    # ... (rest of the class code remains the same)



class Substitute(db.Model, SerializerMixin):
    __tablename__ = 'substitutes' 

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    location = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    qualifications = db.Column(db.String(120))
    verification_id = db.Column(db.String(120))

    requests = db.relationship('Request', back_populates='substitute')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'location': self.location,
            'phone': self.phone,
            'qualifications': self.qualifications,
            'verification_id': self.verification_id,
            'profile_picture': self.user.profile_picture,
        }

    user = db.relationship('User', back_populates='substitute', uselist=False, lazy='joined')


class SiteAdmin(db.Model, SerializerMixin):
    __tablename__ = 'site_admins'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'profile_picture': self.user.profile_picture,
        }

    user = db.relationship('User', back_populates='site_admin', uselist=False, lazy='joined')


class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    Substitute_user_id = db.Column(db.Integer, db.ForeignKey('substitutes.id'), nullable=False)
    Teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    Course_Being_covered = db.Column(db.String(120))
    Confirmation = db.Column(db.String(10))  # 'Accept' or 'Decline'
    Message_sub_sent_to = db.Column(db.String(120))
    Teacher_if_declined = db.Column(db.String(120))
    # Add school_name and Teacher_school_location attributes
    school_name = db.Column(db.String(120))
    Teacher_school_location = db.Column(db.String(120))

    substitute = db.relationship('Substitute', back_populates='requests')
    teacher = db.relationship('Teacher', back_populates='requests')

    def __init__(self, Substitute_user_id, Teacher_id, school_name, Teacher_school_location, Course_Being_covered, Confirmation, Message_sub_sent_to, Teacher_if_declined):
        self.Substitute_user_id = Substitute_user_id
        self.Teacher_id = Teacher_id
        self.school_name = school_name
        self.Teacher_school_location = Teacher_school_location
        self.Course_Being_covered = Course_Being_covered
        self.Confirmation = Confirmation
        self.Message_sub_sent_to = Message_sub_sent_to
        self.Teacher_if_declined = Teacher_if_declined

    def to_dict(self):
        return {
            'id': self.id,
            'Substitute_user_id': self.Substitute_user_id,
            'Teacher_id': self.Teacher_id,
            'school_name': self.school_name,
            'Teacher_school_location': self.Teacher_school_location,
            'Course_Being_covered': self.Course_Being_covered,
            'Confirmation': self.Confirmation,
            'Message_sub_sent_to': self.Message_sub_sent_to,
            'Teacher_if_declined': self.Teacher_if_declined,
        }
   
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