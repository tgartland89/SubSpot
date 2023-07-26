import os
from flask import Flask, jsonify, request, make_response, render_template, session, redirect, url_for
from flask_restful import Resource, fields, marshal 
from models import User, Teacher, Substitute, SiteAdmin, Course, Review
from config import app, db, api
from flask_cors import CORS
from flask_bcrypt import Bcrypt

CORS(app, supports_credentials=True)
app.template_folder = "templates"
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
bcrypt = Bcrypt(app)

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

class SignUp(Resource):
    def post(self):
        try:
            data = request.get_json()
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            if password != confirm_password:
                return make_response({'errors': ['Password and Confirm Password do not match']}, 400)
            user = User(
                email=data['email'],
                password=password,  
                role='Teacher',
            )
            db.session.add(user)
            db.session.commit()

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
            db.session.commit()

            return make_response({'message': 'New teacher created successfully'}, 201)
        except Exception as e:
            print(e)
            return make_response({'errors': ['Validation errors']}, 400)
        
class SubstituteSignUp(Resource):
    def post(self):
        try:
            data = request.get_json()
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            if password != confirm_password:
                return make_response({'errors': ['Password and Confirm Password do not match']}, 400)

            user = User(
                email=data['email'],
                password=password,  
                role='Substitute',
            )
            db.session.add(user)
            db.session.commit()

            user_id = user.id

            substitute = Substitute(
                user_id=user_id,
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

            return make_response({'message': 'New substitute created successfully'}, 201)
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

class ReviewResource(Resource):
    def get(self):
        reviews = Review.query.all()
        serialized_reviews = [marshal(review, review_fields) for review in reviews]
        return jsonify(serialized_reviews)
    
api.add_resource(SignUp, '/signup')
api.add_resource(UserResource, '/users')
api.add_resource(TeacherResource, '/teachers')
api.add_resource(SubstituteResource, '/substitutes')
api.add_resource(SiteAdminResource, '/site_admins')
api.add_resource(CourseResource, '/courses')
api.add_resource(ReviewResource, '/reviews')
api.add_resource(SubstituteSignUp, '/substitute-signup')

@app.route('/teacher-form', methods=['GET', 'POST'])
def teacher_form():

    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.role == 'Teacher':
            if request.method == 'POST':

                return make_response({'message': 'Teacher added successfully'}, 201)
            return render_template('teacher_form.html')

    return make_response({'errors': ['Unauthorized']}, 401)

@app.route('/substitute-form', methods=['GET', 'POST'])
def substitute_form():

    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user and user.role == 'Substitute':
            if request.method == 'POST':
  
                return make_response({'message': 'Substitute added successfully'}, 201)
            return render_template('substitute_form.html')

    return make_response({'errors': ['Unauthorized']}, 401)

@app.route('/substitute-signup', methods=['POST'])
def substitute_signup():
    try:
        data = request.get_json()
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            return make_response({'errors': ['Password and Confirm Password do not match']}, 400)

        user = User(
            email=data['email'],
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
            role='Substitute',
        )
        db.session.add(user)
        db.session.commit()

        user_id = user.id

        substitute = Substitute(
            user_id=user_id,
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

        return make_response({'message': 'New substitute created successfully'}, 201)
    except Exception as e:
        print(e)
        return make_response({'errors': ['Validation errors']}, 400)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data['email']
        password = data['password']

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

    return render_template('login.html') 

@app.route('/logout', methods=['DELETE'])
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        return make_response({'message': 'Logged out successfully'}, 204)
    else:
        return make_response({'errors': ['User not logged in']}, 401)

if __name__ == '__main__':
    app.run(port=5555)