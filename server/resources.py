from flask import request, make_response, jsonify, session 
from flask_restful import Resource, reqparse, fields, marshal_with
from models import User, Teacher, Substitute, Request, Course, Review, SiteAdmin
from config import db, app, bcrypt  

user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'password_hash': fields.String,
    'profile_picture': fields.String,
    'role': fields.String,
}

teacher_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'school': fields.String,
    'location': fields.String,
    'grade_or_course': fields.String,
    'image_url': fields.String,
}

substitute_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'verification_id': fields.String,
    'location': fields.String,
    'grade_or_course': fields.String,
    'qualifications': fields.String,
    'image_url': fields.String,
}

site_admin_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'image_url': fields.String,
}

course_fields = {
    'id': fields.Integer,
    'teacher_id': fields.Integer,
    'substitute_id': fields.Integer,
    'class_subject': fields.String,
    'date': fields.String,
    'time': fields.String,
    'status': fields.String,
}
review_fields = {
    'id': fields.Integer,
    'teacher_id': fields.Integer,
    'substitute_id': fields.Integer,
    'rating': fields.Float,
    'comment': fields.String,
}

request_fields = {
    'Request_ID': fields.Integer,
    'Substitute_user_id': fields.Integer,
    'Teacher_name': fields.String,
    'Teacher_school': fields.String,
    'Teacher_school_location': fields.String,
    'Course_Being_covered': fields.String,
    'Confirmation': fields.String,
    'Message_sub_sent_to': fields.String,
    'Teacher_if_declined': fields.String,
}


class SignUp(Resource):
    def post(self):
        try:
            data = request.get_json()
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            if password != confirm_password:
                return make_response({'errors': ['Password and Confirm Password do not match']}, 400)
            
            role = data.get('role')  
            user = User(
                email=data['email'],
                password=password,
                role=role, 
            )
            db.session.add(user)
            db.session.commit()

            if role == 'Teacher':
                teacher = Teacher(
                    user_id=user.id,
                    name=data['name'],
                    email=data['email'],
                    phone=data['phone'],
                    school=data['school'],
                    location=data['location'],
                    grade_or_course=data['grade_or_course'],
                )
                db.session.add(teacher)

            elif role == 'Substitute':
                substitute = Substitute(
                    user_id=user.id,
                    name=data['name'],
                    email=data['email'],
                    phone=data['phone'],
                    location=data['location'],
                    grade_or_course=data['grade_or_course'],
                    verification_id=data['verification_id'],
                    qualifications=data['qualifications'],
                )
                db.session.add(substitute)

            db.session.commit()

            return make_response({'message': f'New {role} created successfully'}, 201)
        except Exception as e:
            print(e)
            return make_response({'errors': ['Validation errors']}, 400)

class LogIn(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            user = User.query.filter_by(email=email).first()
            if not user:
                return make_response({'errors': ['User not found']}, 404)

            if not bcrypt.check_password_hash(user.password_hash, password):
                return make_response({'errors': ['Invalid password']}, 401)

            session['user_id'] = user.id

            if user.role == 'Teacher':
                return redirect(url_for('teacher_form'))
            elif user.role == 'Substitute':
                return redirect(url_for('substitute_form'))
            else:
                return make_response({'errors': ['Invalid user role']}, 400)
        except Exception as e:
            print(e)
            return make_response({'errors': ['Validation errors']}, 400)
    
class LogOut(Resource):
    def delete(self):
        if 'user_id' in session:
            session.pop('user_id', None)
            return make_response({'message': 'Logged out successfully'}, 204)
        else:
            return make_response({'errors': ['User not logged in']}, 401)

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        serialized_users = [marshal(user, user_fields) for user in users]
        return jsonify(serialized_users)

class TeacherResource(Resource):
    def get(self):
        teachers = Teacher.query.all()
        serialized_teachers = [marshal(teacher, teacher_fields) for teacher in teachers]
        return jsonify(serialized_teachers)

class SubstituteResource(Resource):
    def get(self):
        substitutes = Substitute.query.all()
        serialized_substitutes = [marshal(substitute, substitute_fields) for substitute in substitutes]
        return jsonify(serialized_substitutes)

class SiteAdminResource(Resource):
    def get(self):
        site_admins = SiteAdmin.query.all()
        serialized_site_admins = [marshal(admin, site_admin_fields) for admin in site_admins]
        return jsonify(serialized_site_admins)

class CourseResource(Resource):
    def get(self):
        courses = Course.query.all()
        serialized_courses = [marshal(course, course_fields) for course in courses]
        return jsonify(serialized_courses)

class RequestResource(Resource):
    def get(self, request_id):
        # Implementation for GET request to retrieve a specific request by its ID...
        pass

    def post(self):
        # Implementation for POST request to create a new request...
        pass

    def delete(self, request_id):
        # Implementation for DELETE request to delete a specific request...
        pass

class ReviewResource(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user.role == 'Teacher':
           
                reviews = Review.query.filter_by(writer_id=user_id).all()
            elif user.role == 'Substitute':
          
                reviews = Review.query.filter_by(substitute_reviewed_id=user_id).all()
            else:
            
                reviews = Review.query.all()

            serialized_reviews = [marshal(review, review_fields) for review in reviews]
            return jsonify(serialized_reviews)
        else:
            return make_response({'errors': ['Unauthorized']}, 401)

    